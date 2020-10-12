from my_module import text_formatter
from my_module.path_manager import get_abs_path
import pandas as pd
from tweets_getter import TweetsGetter
from pathlib import Path


class TweetsCSVGenerator:
    '''
    Twitterスクレイピングで取得したデータをCSVへ出力します。
    '''

    def test(self):
        print('test')

    def __init__(self, mode: str = 'k'):
        # print('インスタンスが生成されました。')
        # 保存するデータ群
        self.list_created_at = []
        self.list_id = []
        self.list_full_text = []
        self.list_user_id = []
        self.list_user_screen_name = []
        self.list_formatted_text = []
        # self.list_user_mentions = []
        # self.list_urls = []
        self.tweets_path = self.tweets_text_path = self.params_path = None
        # self.path_by_user = self.path_by_keyword = {}
        self.keyword = self.screen_name = None
        self.mode = mode
        self.params = {}

        if self.mode == 'y':
            self.params_path = get_abs_path(
                __file__, 'csv/params/user/params.csv')
        elif self.mode == 'k':
            self.params_path = get_abs_path(
                __file__, 'csv/params/keyword/params.csv')

    def __del__(self):
        print('インスタンスが破棄されました。')

    def set_csv_path(self):
        '''
        CSVを出力するファイルパスをセットします。
        '''

        if self.mode == 'y':
            # self.tweets_path = get_abs_path(
            #     __file__, f'csv/users/{self.keyword}/tweets.csv')
            # self.tweets_text_path = get_abs_path(
            #     __file__, f'csv/users/{self.keyword}/tweets_text.csv')
            # self.params_path = get_abs_path(
            #     __file__, 'csv/params/user/params.csv')
            if self.screen_name is None:
                # ユーザーを指定して取得 （screen_name）
                self.tweets_path = get_abs_path(
                    __file__, f'csv/users/{self.keyword}/tweets.csv')
                self.tweets_text_path = get_abs_path(
                    __file__, f'csv/users/{self.keyword}/tweets_text.csv')
                self.params_path = get_abs_path(
                    __file__, 'csv/params/user/params.csv')
            else:
                self.tweets_path = get_abs_path(
                    __file__, f'csv/users/{self.screen_name}/tweets.csv')
                self.tweets_text_path = get_abs_path(
                    __file__, f'csv/users/{self.screen_name}/tweets_text.csv')
                self.params_path = get_abs_path(
                    __file__, 'csv/params/user/params.csv')
        elif self.mode == 'k':
            # キーワードで取得
            self.tweets_path = get_abs_path(
                __file__, f'csv/keywords/{self.keyword}/tweets.csv')
            self.tweets_text_path = get_abs_path(
                __file__, f'csv/keywords/{self.keyword}/tweets_text.csv')
            self.params_path = get_abs_path(
                __file__, 'csv/params/keyword/params.csv')

    def set_getter(self):
        '''
        getterをセットします。
        '''

        if self.mode == 'y':
            # ユーザーを指定して取得 （screen_name）
            return TweetsGetter.byUser(self.keyword, **self.params)
        elif self.mode == 'k':
            # キーワードで取得
            return TweetsGetter.bySearch(self.keyword, **self.params)

    def add_list(self, tweet: list):
        '''
        取得したTweetから各種ステータスをリストへ追加します。
        '''

        self.list_created_at.append(tweet['created_at'])
        self.list_id.append(tweet['id'])
        self.list_full_text.append(tweet['full_text'])
        self.list_user_id.append(tweet['user']['id'])
        self.list_user_screen_name.append(
            tweet['user']['screen_name'])
        self.list_formatted_text.append(
            text_formatter.rm_url_mention(tweet['full_text']))

        # region old
        # # メンションを空欄で連結した文字列として保存
        # user_mentions = ''
        # # URLを空欄で連結した文字列として保存
        # urls = ''
        # # 正規表現で使用するパターン文字列
        # pattern = ''

        # # tweet内に含まれるメンションを抽出
        # for user_mention in tweet['entities']['user_mentions']:
        #     user_mentions += '@' + user_mention['screen_name'] + ' '
        #     pattern += '@' + user_mention['screen_name'] + '|'

        # # 抽出したメンションをリストへ格納
        # list_user_mentions.append(user_mentions.rstrip(' '))

        # # tweet内に含まれるURLを抽出
        # for url in tweet['entities']['urls']:
        #     urls += url['url'] + ' '
        #     pattern += url['url'] + '|'

        # # 抽出したURLをリストへ格納
        # list_urls.append(urls.rstrip(' '))

        # # 正規表現で使用するパターンをコンパイル
        # repatter = re.compile(pattern.rstrip('|'))

        # self.list_formatted_text.append(
        #     re.sub(repatter, '', tweet['full_text']))
        # endregion

    def generate_params_by_user(self):
        '''
        スクレイピングに利用する各種パラメータをCSVに出力します。
        '''

        # region old
        # # 保存するパラメータ群

        # # since_idより大きい（つまり、より新しい）IDの結果を返す。
        # # IDの最大（新しい）値はリストの最初
        # since_id = [self.list_id[0]]

        # # max_idより小さい（つまり、より古い）IDの結果を返す。
        # # IDの最小（古い）値はリストの最後
        # # max_idはID以下の値を返す。つまり、max_id自体を含むため-1を減じて除外する。
        # max_id = [self.list_id[-1] - 1]

        # # user別検索のため（ただし、screen_nameは変更可能なため信頼性は低い）
        # screen_name = [self.list_user_screen_name[-1]]

        # # user別検索のため（user毎に一意の値のこちらを検索に用いる）
        # user_id = [self.list_user_id[-1]]

        # # 新規データフレームを作成
        # df_new_params = pd.DataFrame(
        #     columns=['since_id', 'max_id', 'user_id', 'screen_name'])

        # df_new_params = df_new_params.assign(
        #     since_id=since_id, max_id=max_id,
        #     user_id=user_id, screen_name=screen_name)
        # endregion

        # 新規データフレームを作成
        df_new_params = pd.DataFrame(
            [[
                self.list_id[0],
                self.list_id[-1] - 1,
                self.list_user_id[-1],
                self.list_user_screen_name[-1],
            ]],
            columns=['since_id', 'max_id', 'user_id', 'screen_name']
        )

        df_new_params = self.update_df_params(
            key=self.list_user_id[-1], df_new_params=df_new_params)

        # index=Falseを設定しない場合はCSVファイルを読み込み時にcolumnsが一致しない
        df_new_params.to_csv(self.params_path, index=False)

    def generate_params_by_keyword(self):
        '''
        スクレイピングに利用する各種パラメータをCSVに出力します。
        '''

        # 新規データフレームを作成
        df_new_params = pd.DataFrame(
            [[
                self.list_id[0],
                self.list_id[-1] - 1,
                self.keyword
            ]],
            columns=['since_id', 'max_id', 'keyword']
        )

        df_new_params = self.update_df_params(
            key=self.keyword, df_new_params=df_new_params)

        # index=Falseを設定しない場合はCSVファイルを読み込み時にcolumnsが一致しない
        df_new_params.to_csv(self.params_path, index=False)

    def update_df_params(self, key: str, df_new_params):
        '''
        各種パラメータに追記します。
        '''

        # CSVが存在する場合はパラメータの要素を更新
        if Path(self.params_path).exists() is False:
            return df_new_params

        # パラメータCSVを読み込み
        df_params = pd.read_csv(self.params_path)

        # パラメータの疑似インデックスを取得するためにenumerateを使用
        for params in enumerate(self.read_params()):

            # # パラメータID/Keywordと一致するまでcontinue
            # if self.mode == 'y':
            #     if type(self.keyword) == int:
            #         if params[1][2] != self.keyword:
            #             continue
            #     # 初回検索時のみスクリーンネームを使用する
            #     elif type(self.keyword) == str:
            #         if params[1][3] != self.keyword:
            #             continue
            # elif self.mode == 'k':
            #     if params[1][2] != self.keyword:
            #         continue

            if params[1][2] != self.keyword:
                continue

            # # ユーザー検索時はスクリーンネームを更新
            # if self.mode == 'y':
            #     # ユーザーIDが負の値の時、取得したユーザーIDを代入する
            #     if params[1][2] < 0:
            #         df_params.iat[params[0], 2] = self.list_user_id[-1]
            #     # スクリーンネームが更新されている場合、ユーザーネームを代入する
            #     if params[1][3] != self.list_user_screen_name[-1]:
            #         df_params.iat[params[0],
            #                       3] = self.list_user_screen_name[-1]

            # パラメータsince_idが負の値の時、取得したツイートのIDを代入する
            if params[1][0] < 0:
                df_params.iat[params[0], 0] = self.list_id[0]
            # パラメータsince_idより取得したツイートのIDが大きいとき
            # if params[1][0] < self.list_id[0]:
            elif params[1][0] < self.list_id[0]:
                # パラメータsince_idを更新
                df_params.iat[params[0], 0] = self.list_id[0]

            # パラメータmax_idが負の値の時、取得したツイートのIDを代入する
            if params[1][1] < 0:
                df_params.iat[params[0], 1] = self.list_id[-1] - 1
            # パラメータmax_idより取得したツイートのIDが小さいとき
            # if params[1][1] > self.list_id[-1] - 1:
            elif params[1][1] > self.list_id[-1] - 1:
                # パラメータmax_idを更新
                df_params.iat[params[0], 1] = self.list_id[-1] - 1

            return df_params
        else:
            # パラメータID/Keywordと一致しない場合に新規パラメータを追加
            df_new_params = df_params.append(df_new_params)
            return df_new_params

    def generate_tweets(self):
        '''
        取得したTweetをCSVに出力します。
        '''

        # region old
        # 新規データフレームを作成
        # df_new = pd.DataFrame(
        #     columns=[
        #         'created_at', 'id', 'full_text',
        #         'user_mentions', 'urls' 'user_id', 'screen_name'])
        # df_new = df_new.assign(
        #     created_at=list_created_at, id=list_id,
        #     full_text=list_full_text, user_mentions=list_user_mentions,
        #     urls=list_urls, user_id=list_user_id,
        #     screen_name=list_user_screen_name)
        # endregion

        # 新規データフレームを作成
        df_new_tweets = pd.DataFrame(
            columns=[
                'created_at', 'id', 'full_text', 'user_id', 'screen_name'])
        df_new_tweets = df_new_tweets.assign(
            created_at=self.list_created_at, id=self.list_id,
            full_text=self.list_full_text, user_id=self.list_user_id,
            screen_name=self.list_user_screen_name)

        # 新規データフレームを作成
        df_new_tweets_text = pd.DataFrame(columns=['formatted_text'])
        df_new_tweets_text = df_new_tweets_text.assign(
            formatted_text=self.list_formatted_text)

        # ファイルが存在する場合は追記
        if Path(self.tweets_path).exists():

            df_tweets = pd.read_csv(self.tweets_path)
            df_tweets_text = pd.read_csv(self.tweets_text_path)

            # 取得したツイートの最初（新しい）IDとデータフレームの最初（新しい）のツイートのIDを比較
            # if self.list_id[0] > df_tweets.head(1).values.tolist()[0][1]:
            # if self.list_id[0] > df_tweets.iloc[0]['id']:
            if self.list_id[0] > df_tweets.iat[0, 1]:
                df_new_tweets = df_new_tweets.append(df_tweets)
                df_new_tweets_text = df_new_tweets_text.append(df_tweets_text)

            # 取得したツイートの最後（古い）IDとデータフレームの最後（古い）のツイートのIDを比較
            # if self.list_id[-1] < df_tweets.tail(1).values.tolist()[0][1]:
            # if self.list_id[-1] < df_tweets.iloc[-1]['id']:
            if self.list_id[-1] < df_tweets.iat[-1, 1]:
                df_new_tweets = df_tweets.append(df_new_tweets)
                df_new_tweets_text = df_tweets_text.append(df_new_tweets_text)

        # CSV形式にデータを出力
        df_new_tweets.to_csv(self.tweets_path, index=False)
        # CSV形式にデータを出力
        df_new_tweets_text.to_csv(self.tweets_text_path, index=False)

    def read_params(self):
        '''
        各種パラメータを読み込みます。
        '''
        if Path(self.params_path).exists() is False:
            return
        df_params = pd.read_csv(self.params_path, chunksize=1)
        for row in df_params:
            yield row.values[0].tolist()

    def show_params(self):
        '''
        各種パラメータを表示します。
        '''
        if Path(self.params_path).exists() is False:
            return
        df_params = pd.read_csv(self.params_path, chunksize=10)
        for row in df_params:
            yield row

    def set_keyword(self, index: int, mode: str):

        index = int(index) + 1

        params_generator = self.read_params()
        params_list = None
        for i in range(index):
            params_list = next(params_generator)

        # if isnan(params_list[2]):
        #     # スクリーンネームのセット
        #     self.keyword = params_list[3]
        #     if mode == 'r':
        #         if isnan(params_list[0]) is False:
        #             self.params_list = {'since_id': params_list[0]}
        #     elif mode == 'p':
        #         if isnan(params_list[1]) is False:
        #             self.params_list = {'max_id': params_list[1]}
        # else:
        #     # キーワード/IDのセット
        #     self.keyword = params_list[2]
        #     if mode == 'r':
        #         if isnan(params_list[0]) is False:
        #             self.params = {'since_id': params_list[0]}
        #     elif mode == 'p':
        #         if isnan(params_list[1]) is False:
        #             self.params = {'max_id': params_list[1]}

        # キーワード/IDのセット
        self.keyword = params_list[2]

        if self.mode == 'y':
            self.screen_name = '@' + params_list[3]

        if mode == 'r':
            self.params['since_id'] = params_list[0]
        elif mode == 'p':
            self.params['max_id'] = params_list[1]
            print()

    def set_tmp_keyword(self, keyword: str):
        self.keyword = keyword

    def show_tmp_df_tweet(self):

        # 新規データフレームを作成
        df_new_tweets = pd.DataFrame(
            columns=[
                'created_at', 'id', 'full_text', 'user_id', 'screen_name'])
        df_new_tweets = df_new_tweets.assign(
            created_at=self.list_created_at, id=self.list_id,
            full_text=self.list_full_text, user_id=self.list_user_id,
            screen_name=self.list_user_screen_name)

        print('=' * 50)
        print(df_new_tweets[['full_text', 'user_id', 'screen_name']])
        print('=' * 50)

    def has_duplicate_keyword(self, params: dict):
        '''
        キーワード検索パラメータ内のキーワードの重複をチェックします。
        '''
        for keyword in self.read_params():
            # キーワードの重複がある場合
            if params['keywrod'] == keyword[2]:
                return True

        # キーワードの重複がない場合最後までループする
        return False

    def update_params_by_keyword(self, params: dict):
        '''
        キーワード検索パラメータにキーワードをセットします。
        '''

        if self.params_path is None:
            # キーワードで取得
            self.params_path = get_abs_path(
                __file__, 'csv/params/keyword/params.csv')

        # キーワード重複時アーリーリターン
        if self.has_duplicate_keyword(params):
            return

        # 新規データフレームを作成
        df_new_params = pd.DataFrame(
            # DataFrame結合時にdtypeがint型からfloat型への変換を防ぐためnanを-1で置換する
            [[-1, -1, params['keyword']]],
            columns=['since_id', 'max_id', 'keyword'])

        # パラメータを読み込みます。
        if Path(self.params_path).exists():
            df_params = pd.read_csv(self.params_path)
            df_new_params = df_params.append(df_new_params)

        # CSVを出力します。
        df_new_params.to_csv(self.params_path, index=False)

    def has_duplicate_screen_name(self, params: dict):
        '''
        ユーザー検索パラメータ内のキーワードの重複をチェックします。
        '''
        for screen_name in self.read_params():
            # キーワードの重複がある場合
            if params['keyword'] == screen_name[3]:
                return True

        # キーワードの重複がない場合最後までループする
        return False

    def update_params_by_user(self, params: dict):
        '''
        ユーザー検索パラメータにキーワードをセットします。
        '''

        if self.params_path is None:
            # ユーザーを指定して取得 （screen_name）
            self.params_path = get_abs_path(
                __file__, 'csv/params/user/params.csv')

        # キーワード重複時アーリーリターン
        if self.has_duplicate_screen_name(params):
            return

        # 新規データフレームを作成
        df_new_params = pd.DataFrame(
            # DataFrame結合時にdtypeがint型からfloat型への変換を防ぐためnanを-1で置換する
            [[-1, -1, -1, params['keyword']]],
            columns=['since_id', 'max_id', 'user_id', 'screen_name'])

        # パラメータを読み込みます。
        if Path(self.params_path).exists():
            df_params = pd.read_csv(self.params_path)
            df_new_params = df_params.append(df_new_params)

        # CSVを出力します。
        df_new_params.to_csv(self.params_path, index=False)


if __name__ == "__main__":
    pass
