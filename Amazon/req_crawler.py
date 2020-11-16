from bs4 import BeautifulSoup
import requests
import re
# import webbrowser
from pathlib import Path
from my_module import questionnaire
from my_module.path_manager import get_abs_path
import pandas as pd
from time import sleep


class AmazonCrawler:
    '''
    Amazonのクローラーです。
    '''

    def __init__(self):
        self.dict_reviews = None

    def __del__(self):
        pass

    def validate_url(self, url: str) -> bool:
        '''
        URLの妥当性を検証します。
        '''
        pattern = r'http(s)*://(www.)*amazon.(co.)*jp/'
        repatter = re.compile(pattern)
        return bool(re.search(repatter, url))

    def shorten_url(self, url: str) -> str:
        '''
        商品ページのURLを短縮します。
        '''
        pattern = r'dp/\w+[/?]'
        repatter = re.compile(pattern)
        dp = re.search(repatter, url).group()
        url = 'https://www.amazon.co.jp/' + dp[:-1]
        return url

    def shorten_next_url(self, url: str):
        pattern = r'product-reviews/.+'
        repatter = re.compile(pattern)
        pr = re.search(repatter, url).group()
        url = 'https://www.amazon.co.jp/' + pr
        return url

    def generate_review_url(self, url: str) -> str:
        '''
        商品レビューページのURLに置換します。
        -----
        '''
        # ASINコードは10桁
        url = self.shorten_url(url)
        url = url.replace('dp', 'product-reviews')
        return url

    def detect_error(self, response):
        '''
        例外を検知します。
        '''
        try:
            response.raise_for_status()
        except Exception as exc:
            print(f'問題が発生しました。\nstatus_code：{exc}')

    def get_base_soup(self, url: str):
        '''
        Webページを取得します。
        '''
        response = requests.get(url, timeout=3)
        self.detect_error(response)
        return BeautifulSoup(response.text, features='lxml')

    def get_reviews(self, soup):
        '''
        商品レビューページのレビューをすべて取得します
        '''
        s_review = 'div[id^=customer_review-]'
        return soup.select(s_review)

    def get_product_info(self, soup):
        '''
        商品ページのURLから商品名を取得します。
        '''
        s_info = '#cm_cr-brdcmb > ul.a-unordered-list > li:nth-of-type(1) > span > a'
        return soup.select_one(s_info).text

    def get_brand_name(self, soup):
        '''
        商品レビューページからブランド名を取得します。
        '''
        s_brand = '#cr-arp-byline > a'
        return soup.select_one(s_brand).text

    def get_next_link(self, soup):
        '''
        商品レビューページから次のリンクを取得します。
        '''
        s_next = '#cm_cr-pagination_bar > ul.a-pagination > li.a-last > a'

        for i in range(2):
            try:
                return soup.select_one(s_next).get('href')
            except AttributeError as e:
                print(f'解析に失敗しました。\n{e}')
                sleep(1)
                return soup.select_one(s_next).get('href')
            else:
                break
        else:
            print('CSSセレクタが間違っています。')

    def get_common_selectors(self, response, s_common: str):
        '''
        共通
        '''
        bs = BeautifulSoup(response.text, features='lxml')
        return bs.select(s_common)

    def get_common_selector(self, response, s_common: str):
        '''
        共通
        '''
        bs = BeautifulSoup(response.text, features='lxml')
        return bs.select_one(s_common)

    def get_links_by_rating(self, soup):
        '''
        商品レビューページから評価レートごとのURLを取得します。
        Note
        -----
        未実装
        '''
        # dict_urls = {
        #     '1star': None, '2star': None,
        #     '3star': None, '4star': None, '5star': None,
        # }

        # dict_s_urls = {}
        # for i in range(1, 5):
        # dict_s_urls[f's_{i}star'] = f'#histogramTable > tbody > tr:nth-of-type({6-i}) > td.aok-nowrap > span.a-size-base > a.{i}star'
        # dict_urls[f'{i}star'] = bs.select_one(
        #     f'#histogramTable > tbody > tr:nth-of-type({6-i}) > td.aok-nowrap > span.a-size-base > a[class="{i}star"]').get('href')
        pass

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
        self.dict_reviews = {
            'users': [], 'rates': [], 'titles': [], 'dates': [],
            'kinds': [], 'shops': [], 'comments': [], 'votes': []}

        for review in reviews:
            self.dict_reviews['users'].append(
                review.select_one(s_user).text.strip())
            self.dict_reviews['rates'].append(
                review.select_one(s_rate).text.strip())
            self.dict_reviews['titles'].append(
                review.select_one(s_title).text.strip())
            self.dict_reviews['dates'].append(
                review.select_one(s_date).text.strip())
            self.dict_reviews['kinds'].append(
                review.select_one(s_kind).text.strip())
            self.dict_reviews['shops'].append(
                review.select_one(s_shop).text.strip())
            self.dict_reviews['comments'].append(
                review.select_one(s_comment).text.strip())
            self.dict_reviews['votes'].append(
                review.select_one(s_vote).text.strip())

        # デバッグ
        # print(users[0])
        # print(rates[0])
        # print(titles[0])
        # print(dates[0])
        # print(kinds[0])
        # print(shops[0])
        # print(comments[0])
        # print(votes[0])

    # def get_reviews_re(self, response):
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

        # デバッグ
        # print(rate_list[0])
        # print(user_list[0])
        # print(date_and_region_list[0])
        # print(title_list[0])
        # print(kind_and_shop_list[0])
        # print(comment_list[0])
        # print(vote_list[0])

    def generate_csv_from_dict(self, file_path: str):
        '''
        辞書からCSVを生成します。
        '''
        df_new = pd.DataFrame.from_dict(self.dict_reviews)
        df_new.to_csv(file_path)


if __name__ == "__main__":

    crawler = AmazonCrawler()
    questionnaire = questionnaire.Questionnaire()
    print('URLを入力してください。')
    url = questionnaire.ask_url()
    print('商品名を入力してください。')
    file_name = questionnaire.ask_keyword()
    url = r'https://amazon.co.jp/dp/B00840PFXU/'
    # url = r'http://amazon.jp/product-reviews/B00840PFXU/'
    if crawler.validate_url(url):
        url = crawler.generate_review_url(url)
    base_soup = crawler.get_base_soup(url=url)
    next_url = crawler.shorten_next_url(crawler.get_next_link(base_soup))
    print(next_url)
    # while True:
    #     base_soup = crawler.get_base_soup(url=url)
    #     crawler.get_reviews_bs4(base_soup)
    #     next_url = crawler.get_next_link(base_soup)
    #     if next_url:
    #         url = 'https://www.amazon.co.jp' + next_url
    #         sleep(1)
    #     else:
    #         break
    # brand_name = crawler.get_brand_name(base_soup)
    # file_path = get_abs_path(__file__, f'/csv/{brand_name}/{file_name}.csv')
    # crawler.generate_csv_from_dict(file_path)
