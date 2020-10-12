from requests_oauthlib import OAuth1Session
import json
from datetime import datetime as dt
import time
import sys
from abc import ABCMeta, abstractmethod
import env.dotenv_reader as dr


KEYS = {

    # Twitter_API_KEY
    "API_KEY": dr.AK,
    "API_SECRET_KEY": dr.ASK,

    # Twitter_ACCESS_TOKEN
    "ACCESS_TOKEN": dr.AT,
    "ACCESS_TOKEN_SECRET": dr.ATS,

}


class TweetsGetter(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.session = OAuth1Session(
            KEYS["API_KEY"],
            KEYS["API_SECRET_KEY"],
            KEYS["ACCESS_TOKEN"],
            KEYS["ACCESS_TOKEN_SECRET"])

    @abstractmethod
    def specifyUrlAndParams(self, keyword):
        '''
        呼出し先 URL、パラメータを返す
        '''

    @abstractmethod
    def pickupTweet(self, res_text, includeRetweet):
        '''
        res_text からツイートを取り出し、配列にセットして返却
        '''

    @abstractmethod
    def getLimitContext(self, res_text):
        '''
        回数制限の情報を取得 （起動時）
        '''

    def collect(self, total=-1, onlyText=False, includeRetweet=False):
        '''
        ツイート取得を開始する
        '''

        # ----------------
        # 回数制限を確認
        # ----------------
        self.checkLimit()

        # ----------------
        # URL、パラメータ
        # ----------------
        url, params = self.specifyUrlAndParams()
        params['include_rts'] = str(includeRetweet).lower()
        # include_rts は statuses/user_timeline のパラメータ。search/tweets には無効

        # ----------------
        # ツイート取得
        # ----------------
        cnt = 0
        unavailableCnt = 0
        while True:
            res = self.session.get(url, params=params)
            if res.status_code == 503:
                # 503 : Service Unavailable
                if unavailableCnt > 10:
                    raise Exception(f'Twitter API error {res.status_code}')

                unavailableCnt += 1
                print('Service Unavailable 503')
                self.waitUntilReset(time.mktime(
                    dt.now().timetuple()) + 30)
                continue

            unavailableCnt = 0

            if res.status_code != 200:
                raise Exception(f'Twitter API error {res.status_code}')

            tweets = self.pickupTweet(json.loads(res.text))
            if len(tweets) == 0:
                # len(tweets) != params['count'] としたいが
                # count は最大値らしいので判定に使えない。
                # ⇒  "== 0" にする
                # https://dev.twitter.com/discussions/7513
                break

            for tweet in tweets:
                if (('retweeted_status' in tweet) and (includeRetweet is False)):
                    pass
                else:
                    if onlyText is True:
                        yield tweet['text']
                    else:
                        yield tweet

                    cnt += 1

                    # tqdm使用のためコメントアウト
                    # if cnt % 100 == 0:
                    #     print(f'{cnt}件')

                    if total > 0 and cnt >= total:
                        return

            params['max_id'] = tweet['id'] - 1
            print(params)

            # if 'since_id' in params:
            #     params['since_id'] = tweet['id']

            # ヘッダ確認 （回数制限）
            # X-Rate-Limit-Remaining が入ってないことが稀にあるのでチェック
            if ('X-Rate-Limit-Remaining' in res.headers and
                    'X-Rate-Limit-Reset' in res.headers):
                if (int(res.headers['X-Rate-Limit-Remaining']) == 0):
                    self.waitUntilReset(int(res.headers['X-Rate-Limit-Reset']))
                    self.checkLimit()
            else:
                print('not found  -  X-Rate-Limit-Remaining or X-Rate-Limit-Reset')
                self.checkLimit()

    def checkLimit(self):
        '''
        回数制限を問合せ、アクセス可能になるまで wait する
        '''
        unavailableCnt = 0
        while True:
            url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
            res = self.session.get(url)

            if res.status_code == 503:
                # 503 : Service Unavailable
                if unavailableCnt > 10:
                    raise Exception(f'Twitter API error {res.status_code}')

                unavailableCnt += 1
                print('Service Unavailable 503')
                self.waitUntilReset(time.mktime(
                    dt.now().timetuple()) + 30)
                continue

            unavailableCnt = 0

            if res.status_code != 200:
                raise Exception(f'Twitter API error {res.status_code}')

            remaining, reset = self.getLimitContext(json.loads(res.text))
            if (remaining == 0):
                self.waitUntilReset(reset)
            else:
                break

    def waitUntilReset(self, reset):
        '''
        reset 時刻まで sleep
        '''
        seconds = reset - time.mktime(dt.now().timetuple())
        seconds = max(seconds, 0)
        print('\n     =====================')
        print('     == waiting %d sec ==' % seconds)
        print('     =====================')
        sys.stdout.flush()
        time.sleep(seconds + 10)  # 念のため + 10 秒

    @staticmethod
    def bySearch(keyword: str, **kwargs):
        return TweetsGetterBySearch(keyword, kwargs)

    @staticmethod
    def byUser(screen_name: str, **kwargs):
        return TweetsGetterByUser(screen_name, kwargs)


class TweetsGetterBySearch(TweetsGetter):
    '''
    キーワードでツイートを検索
    '''

    def __init__(self, keyword: str, params: dict):
        super(TweetsGetterBySearch, self).__init__()
        self.keyword = keyword
        self.params = params

    def specifyUrlAndParams(self):
        '''
        呼出し先 URL、パラメータを返す
        '''
        url = "https://api.twitter.com/1.1/search/tweets.json"

        # retult_type   :   'recent'    応答で最新の結果のみを返します
        #               :   'polular'   レスポンスで最も人気のある結果のみを返します。
        #               :   'mixed'     人気のある結果とリアルタイムの結果の両方を応答に含めます。(default)

        # 公式のドキュメントにはないパラメータ
        # tweet_mode    :   'extended'  textをfullで取得できる

        self.keyword += ' -filter:links'
        params = {'q': self.keyword, 'count': 100, 'lang': 'ja', 'tweet_mode': 'extended'}
        params.update(self.params)

        return url, params

    def pickupTweet(self, res_text):
        '''
        res_text からツイートを取り出し、配列にセットして返却
        '''
        results = []
        for tweet in res_text['statuses']:
            results.append(tweet)

        return results

    def getLimitContext(self, res_text):
        '''
        回数制限の情報を取得 （起動時）
        '''
        remaining = res_text['resources']['search']['/search/tweets']['remaining']
        reset = res_text['resources']['search']['/search/tweets']['reset']

        return int(remaining), int(reset)


class TweetsGetterByUser(TweetsGetter):
    '''
    ユーザーを指定してツイートを取得
    '''

    # def __init__(self, screen_name: strt):
    def __init__(self, screen_name: str, params: dict):
        super(TweetsGetterByUser, self).__init__()
        self.screen_name = screen_name
        self.params = params

    def specifyUrlAndParams(self):
        '''
        呼出し先 URL、パラメータを返す
        '''
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

        # 公式のドキュメントにはないパラメータ
        # tweet_mode    :   'extended'  textをfullで取得できる

        if type(self.screen_name) == int:
            params = {'user_id': self.screen_name,
                      'count': 200, 'lang': 'ja', 'tweet_mode': 'extended'}
        else:
            params = {'screen_name': self.screen_name,
                      'count': 200, 'lang': 'ja', 'tweet_mode': 'extended'}

        params.update(self.params)

        return url, params

    def pickupTweet(self, res_text):
        '''
        res_text からツイートを取り出し、配列にセットして返却
        '''
        results = []
        for tweet in res_text:
            results.append(tweet)

        return results

    def getLimitContext(self, res_text):
        '''
        回数制限の情報を取得 （起動時）
        '''
        remaining = res_text['resources']['statuses']['/statuses/user_timeline']['remaining']
        reset = res_text['resources']['statuses']['/statuses/user_timeline']['reset']

        return int(remaining), int(reset)


if __name__ == '__main__':
    pass
