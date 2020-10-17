from bs4 import BeautifulSoup
import re
from pathlib import Path
from my_module.path_manager import get_abs_path
import pandas as pd
import datetime as dt
from abc import ABCMeta, abstractmethod
from my_module import text_formatter as tf
import os
import urllib


class URLValidator:

    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def validate(url: str) -> bool:
        '''
        URLの妥当性を検証します。
        '''
        pattern = r'http(s)*://(www.)*amazon.(co.)*jp/'
        repatter = re.compile(pattern)
        return bool(re.search(repatter, url))

    @staticmethod
    def shorten(url: str) -> str:
        '''
        商品ページのURLを最適化します。
        '''
        pattern = r'dp/\w+/'
        repatter = re.compile(pattern)
        dp = re.search(repatter, url).group()
        url = 'https://www.amazon.co.jp/' + dp
        return url

    @staticmethod
    def shorten_next(url: str) -> str:
        '''
        商品レビューページの「次へ」URLを最適化します。
        '''
        pattern = r'product-reviews/.+'
        repatter = re.compile(pattern)
        pr = re.search(repatter, url).group()
        url = 'https://www.amazon.co.jp/' + pr
        return url

    @staticmethod
    def generate_review(url: str) -> str:
        '''
        商品レビューページのURLに置換します。
        -----
        '''
        # ASINコードは10桁
        # url = self.shorten_url(url)
        url = url.replace('dp', 'product-reviews')
        return url

    @staticmethod
    def get_ASIN_by_dp(url: str) -> str:
        '''
        商品ページのURLからASINコードを取得します。
        '''
        pattern = r'dp/\w+/'
        repatter = re.compile(pattern)
        ASIN = re.search(repatter, url).group()
        return ASIN[3:-1]

    @staticmethod
    def get_ASIN_by_pr(url: str) -> str:
        '''
        カスタマーレビューページのURLからASINコードを取得します。
        '''
        pattern = r'product-reviews/\w+/'
        repatter = re.compile(pattern)
        ASIN = re.search(repatter, url).group()
        return ASIN[16:-1]

    @staticmethod
    def get_product_name(url):
        # url = r'https://www.amazon.co.jp/%E7%99%BD%E5%B7%9E-%E3%82%B5%E3%83%B3%E3%83%88%E3%83%AA%E3%83%BC-%E3%82%B7%E3%83%B3%E3%82%B0%E3%83%AB%E3%83%A2%E3%83%AB%E3%83%88-700ml/dp/B00840PFXU/'
        pattern = r'/[\w%-]+/dp/'
        repatter = re.compile(pattern)
        product_name = re.search(repatter, url).group()
        return urllib.parse.unquote(product_name[1:-4])


class BaseCSVGenerator(metaclass=ABCMeta):
    '''
    CSVを生成する基底クラスです。
    '''

    @abstractmethod
    def generate_csv_from_dict(self):
        pass


class ReviewCSVGenerator(BaseCSVGenerator):

    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def generate_csv_from_dict(review: dict, file_path: str, is_latest: bool = False):
        '''
        辞書からCSVを生成します。
        '''

        # 辞書からデータフレームを生成
        df_new = pd.DataFrame.from_dict(review)

        # 指定したパスにファイルが存在するか
        if Path(file_path).exists():

            if is_latest:  # 新しい場合
                # 一時ファイルのパスを生成
                tmp_path = get_abs_path(file_path, 'tmp.csv')
                # 既存CSVを一時ファイルにリネーム
                os.rename(file_path, tmp_path)
                # 最新データの新規CSVを生成
                df_new.to_csv(file_path, index=False)
                # 既存のCSVを分割読込
                df_chunks = pd.read_csv(tmp_path, chunksize=50)
                # 分割読込した既存CSVを新規に生成したCSVに追記
                for chunk in df_chunks:
                    chunk.to_csv(file_path, mode='a',
                                 header=False, index=False)
                # 一時ファイルを削除する
                os.remove(tmp_path)
            else:  # 古い場合
                # 既存CSVの末尾に追記
                df_new.to_csv(file_path, mode='a', header=False, index=False)
        else:  # 存在しない場合
            df_new.to_csv(file_path, index=False)

    @staticmethod
    def read_newest_date(file_path: str) -> str:
        '''
        CSVから最新の日付を取得します。
        '''
        if Path(file_path).exists():
            df = pd.read_csv(file_path, chunksize=1)
            date = next(df).iloc[0]['dates']
            return date
        else:
            return None

    @staticmethod
    def generate_log_csv(dict_log: dict, file_path: str):
        '''
        ログファイルを出力します。
        '''
        df = pd.DataFrame.from_dict([dict_log])
        if Path(file_path).exists():
            # ファイルが存在する場合は追記する。
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            # ファイルが存在しない場合はCSVを出力する。
            df.to_csv(file_path, index=False)


class BaseParser:
    '''
    パーサーの基底クラスです。
    '''
    pass


class ProductParser:
    '''
    商品ページのHTMLパーサーです。
    '''

    def __init__(self):
        pass

    def get_pagination(self, soup):
        '''
        商品ページのパンくずリストを取得します。
        '''
        s_pagination = '#wayfinding-breadcrumbs_feature_div > ul > li > span > a'
        paginations = soup.select(s_pagination)
        list_paginations = []
        for pagination in paginations:
            list_paginations.append(pagination.text.strip())
        return list_paginations


class ReviewParser:
    '''
    商品レビューページのHTMLパーサーです。
    '''

    def __init__(self):
        pass

    def __del__(self):
        pass

    def get_reviews(self, soup):
        '''
        商品レビューページのレビューをすべて取得します
        '''
        s_review = 'div[id^=customer_review-]'
        return soup.select(s_review)

    def get_brand_name(self, soup):
        '''
        商品レビューページからブランド名を取得します。
        '''
        s_brand = '#cr-arp-byline > a'
        return soup.select_one(s_brand).text

    def get_product_name(self, soup):
        s_product = '#cm_cr-brdcmb > ul > li:nth-of-type(1) > span > a'
        return soup.select_one(s_product).text.strip()

    def get_next_link(self, soup):
        '''
        商品レビューページから次のリンクを取得します。
        '''
        s_next = '#cm_cr-pagination_bar > ul.a-pagination > li.a-last > a'
        return soup.select_one(s_next).get('href')

    def get_reviews_bs4(self, soup):
        '''
        取得したレビューから必要なデータを抽出します。
        '''
        reviews = self.get_reviews(soup)

        s_user = 'div:nth-of-type(1) > a.a-profile > div.a-profile-content > span.a-profile-name'
        s_rate = 'div:nth-of-type(2) > a[href^="/gp/customer-reviews/"] > i.review-rating'
        s_title = 'div:nth-of-type(2) > a[href^="/gp/customer-reviews/"].review-title-content > span'
        s_date = 'span.review-date'
        s_kind = 'div.review-data.review-format-strip > a'
        s_shop = 'div.review-data.review-format-strip > span'
        s_comment = 'div.review-data > span.review-text-content'
        s_vote = 'div.review-comments > div > span.cr-vote > div > span.cr-vote-text'

        # 保存するデータ群
        dict_reviews = {
            'users': [], 'rates': [], 'titles': [], 'dates': [],
            'kinds': [], 'shops': [], 'comments': [], 'votes': []}

        for review in reviews:
            # print(11)
            dict_reviews['users'].append(
                review.select_one(s_user).text.strip())
            # print(12)
            dict_reviews['rates'].append(
                review.select_one(s_rate).text.strip())
            # print(13)
            dict_reviews['titles'].append(
                review.select_one(s_title).text.strip())
            # print(14)
            dict_reviews['dates'].append(
                review.select_one(s_date).text.strip())
            # print(15)
            dict_reviews['kinds'].append(
                review.select_one(s_kind).text.strip())
            # print(16)
            try:
                dict_reviews['shops'].append(
                    review.select_one(s_shop).text.strip())
            except AttributeError:
                dict_reviews['shops'].append(None)
            # print(17)
            dict_reviews['comments'].append(
                review.select_one(s_comment).text.strip())
            # print(18)
            try:
                dict_reviews['votes'].append(
                    review.select_one(s_vote).text.strip())
            except AttributeError:
                dict_reviews['votes'].append(None)
            # print(19)

        # region Debug
        # デバッグ
        # print(users[0])
        # print(rates[0])
        # print(titles[0])
        # print(dates[0])
        # print(kinds[0])
        # print(shops[0])
        # print(comments[0])
        # print(votes[0])
        # endregion

        return dict_reviews

    def get_reviews_re(self, soup):
        '''
        取得したレビューから必要なデータを抽出します。
        '''

        reviews = self.get_reviews(soup)

        # Amazonレビュー専用正規表現
        # 「レート（評価）、ユーザー名、日付と地域、タイトル、種類と販売者、コメント、投票」パターン
        pattern = r'.+\dつ星のうち\d\.\d\s*.+\s*.+\s*.+\s*.+'
        repatter_review = re.compile(pattern)

        # Errorパターン
        pattern = r'コメントの読み込み中に問題が発生しました。後でもう一度試してください。'
        repatter_error = re.compile(pattern)

        review_list = []

        # レビューより「レート（評価）、ユーザー名、日付と地域、タイトル、種類と販売者、コメント、投票」を抽出。
        # 文章の構造はtest.txtを参照のこと
        for review in reviews:
            review_list.append(re.sub(repatter_error, '', re.search(
                repatter_review, review.text).group()).split())

        # 保存するパラメータ群
        rate_list = []
        user_list = []
        date_and_region_list = []
        title_list = []
        kind_and_shop_list = []
        comment_list = []
        vote_list = []

        # レート（評価）パターン
        pattern = r'\dつ星のうち\d\.\d'
        repatter_rate = re.compile(pattern)
        # 日付と地域パターン
        pattern = r'.+レビュー済み'
        repatter_date_and_region = re.compile(pattern)

        # レビューより「レート（評価）、ユーザー名、日付と地域、タイトル、種類と販売者、コメント、投票」を抽出。
        for review in review_list:
            rate_list.append(re.search(repatter_rate, review[0]).group())
            user_list.append(re.sub(repatter_rate, '', review[0]))
            title_list.append(review[1])
            date_and_region_list.append(
                re.search(repatter_date_and_region, review[2]).group())
            tmp = re.sub(repatter_date_and_region, '', review[2])
            tmp += review[3]
            kind_and_shop_list.append(tmp)
            comment_list.append(review[4])
            vote_list.append(review[5])

        # region Debug
        # デバッグ
        # print(rate_list[0])
        # print(user_list[0])
        # print(date_and_region_list[0])
        # print(title_list[0])
        # print(kind_and_shop_list[0])
        # print(comment_list[0])
        # print(vote_list[0])
        # endregion
