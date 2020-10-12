from datetime import datetime as dt
from datetime import timedelta
import re


def c_at2f_dtime():
    '''
    statuses[created_at]をDateTime(YYYY-mm-dd HH:MM:SS)形式へフォーマット

    Returns
    -------
    f_dtime :   str
        YYYY-mm-dd HH:MM:SS
    '''
    # dtime = tweet['created_at']
    dtime = 'Fri Oct 09 10:01:41 +0000 2015'
    f_dtime = dt.strftime(dt.strptime(
        dtime, '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')

    # フォーマットされた日付を返す
    return f_dtime


def dtime2q_dtime(dtime):
    '''
    クエリ用に日付(UTC)をフォーマット

    Returns
    -------
    q_dtime :   str
        YYYY-mm-dd_HH:MM:SS_UTC
    '''
    if type(dtime) is str:
        q_dtime = dt.strftime(dt.strptime(
            dtime, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d_%H:%M:%S_UTC')
    elif type(dtime) is dt:
        q_dtime = dt.strftime(
            dtime, '%Y-%m-%d_%H:%M:%S_UTC')
    else:
        pass

    # クエリ用にフォーマットされた日付を返す
    return q_dtime


def get_q_period(kwd: str):
    '''
    更新Tweet取得のクエリを生成

    Args
    ----
    kwd     :   str
        検索対象のキーワード
    '''
    # sinceDate = self.dtime2q_dtime(self.c_at2f_dtime())  # 日付以降のTweetを取得
    # untilDate = self.dtime2q_dtime(dt.utcnow())  # 日付以前のTweetを取得
    sinceDate = dtime2q_dtime(
        dt.utcnow() - timedelta(hours=1))  # 今から1時間前
    untilDate = dtime2q_dtime(dt.utcnow())  # 今
    query = f"{kwd} since:{sinceDate} until:{untilDate}"  # queryを生成
    return query


def rm_url_mention(tweet_text):
    '''
    正規表現で取得したテキストのURLとMentionを''に置換します。
    '''
    # 正規表現で使用するパターンをコンパイル
    pattern = r"(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(@\w+)"
    repatter = re.compile(pattern)
    return re.sub(repatter, '', tweet_text)


def rm_url(text):
    '''
    正規表現で取得したテキストのURLを''に置換します。
    '''
    # 正規表現で使用するパターンをコンパイル
    pattern = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    repatter = re.compile(pattern)
    return re.sub(repatter, '', text)


def rm_mention(text):
    '''
    正規表現で取得したテキストのMentionを''に置換します。
    '''
    # 正規表現で使用するパターンをコンパイル
    pattern = r"@\w+"
    repatter = re.compile(pattern)
    return re.sub(repatter, '', text)


if __name__ == "__main__":
    pass
