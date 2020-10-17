# Selenium Module
import chromedriver_binary
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Common Module
from bs4 import BeautifulSoup
import sys
from pathlib import Path
# My Module
from my_module import questionnaire
from my_module import text_formatter as tf
from my_module.path_manager import get_abs_path
from base_crawler import ReviewParser, URLValidator, ReviewCSVGenerator
import time
from datetime import datetime as dt


class ReviewCrawler:
    '''
    Amazonのクローラーです。
    '''

    def __init__(self):
        # ドライバのセットアップ
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.implicitly_wait(10)

        self.dict_review = {}
        self.file_path = {}
        # self.dict_logs = {}
        self.soup = None
        self.counter = 0

        self.r_parser = ReviewParser()

    def __del__(self):
        pass

    def get_html_soup(self):
        '''
        アクセスしたページからHTMLを取得します。
        '''
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located)
        except TimeoutException as e:
            print(e)
            sys.exit()
        else:
            html = self.driver.page_source.encode('utf-8')
            self.soup = BeautifulSoup(html, features='lxml')

    def get_reviews_bs4(self, is_existing: bool = False):
        '''
        カスタマーレビューページからレビューを収集します。
        '''

        if self.dict_review is None:
            self.dict_review = self.r_parser.get_reviews_bs4(self.soup)
        else:
            for key, value in self.r_parser.get_reviews_bs4(self.soup).items():
                self.dict_review[key].extend(value)
        if is_existing:
            if self.collect_newer_review():
                print('更新差分レビューの取得が完了しました。')
                return False
        return True

    def collect_newer_review(self):
        # 既存CSVから最新のレビューの日付を取得
        e_date = ReviewCSVGenerator.read_newest_date(self.file_path['review'])
        e_date = tf.convert_datetime_date(e_date)
        can_generate = False

        for index, date in enumerate(self.dict_review['dates']):
            n_date = tf.convert_datetime_date(date)
            if n_date <= e_date:
                for key in self.dict_review.keys():
                    self.dict_review[key].pop(index)
                can_generate = True

        if can_generate:
            ReviewCSVGenerator.generate_csv_from_dict(
                self.dict_review, self.file_path['review'], is_latest=True)
            return True

        return False

    def transition_next_page(self):
        '''
        カスタマーレビューページを次ページへ遷移させます。
        '''
        self.counter += 1
        try:
            print(f'{self.counter}ページ目のデータの取得に成功しました')
            print(f'{self.counter+1}ページ目に遷移します。')
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, 'cm_cr-pagination_bar')))
            self.driver.find_element_by_xpath(
                '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()
            # self.get_html_soup()
            return True
        except NoSuchElementException:
            print('最後のページに到達しました。\nCSVを生成します。')
            ReviewCSVGenerator.generate_csv_from_dict(
                self.dict_review, self.file_path['review'])
            print('CSVの生成が完了しました。')
            return False

    def set_csv_path(self, url):
        '''
        CSVファイルを生成する絶対パスを生成します。
        '''
        ASIN = URLValidator.get_ASIN_by_pr(url)
        path = f'csv/reviews/{ASIN}/{ASIN}.csv'
        self.file_path['review'] = get_abs_path(__file__, path)
        path = 'csv/log/reviews/log.csv'
        self.file_path['log'] = get_abs_path(__file__, path)

    def sort_by_date(self):
        '''
        カスタマーレビューを「新しい順」にソートします。
        '''
        self.driver.find_element_by_xpath(
            '//*[@id="a-autoid-4-announce"]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="sort-order-dropdown_1"]').click()

    def generate_log_csv(self, url: str, status: str):
        print('ログファイルを出力します。')
        dict_log = {}
        dict_log['date'] = dt.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-4]
        dict_log['status'] = status
        dict_log['ASIN'] = URLValidator.get_ASIN_by_pr(url)
        dict_log['brand'] = self.r_parser.get_brand_name(self.soup)
        dict_log['product'] = self.r_parser.get_product_name(self.soup)
        ReviewCSVGenerator.generate_log_csv(dict_log, self.file_path['log'])
        print(dict_log)
        print('ログファイルの出力が完了しました。')

    # def retry(self):
        # WebDriverWait(self.driver, 15).until(
        #     EC.presence_of_all_elements_located)
        # WebDriverWait(self.driver, 15).until(
        #     EC.presence_of_element_located(By.ID, 'ID名'))
        # WebDriverWait(self.driver, 15).until(
        #     EC.presence_of_element_located(By.CLASS_NAME, 'CLASS名'))
        # try:
        #     WebDriverWait(self.driver, 15).until(
        #         EC.presence_of_all_elements_located)
        # except TimeoutException:
        #     sys.exit()

    def collect(self, url: str):
        try:
            if URLValidator.validate(url) is False:
                print('不正なURLです\nプログラムを終了します。')
                sys.exit()
            url = URLValidator.shorten(url)
            url = URLValidator.generate_review(url)
            self.set_csv_path(url)
            is_existing = Path(self.file_path['review']).exists()
            self.driver.get(url)
            time.sleep(1)
            self.sort_by_date()
            while True:
                time.sleep(1)
                self.get_html_soup()
                time.sleep(1)
                if self.get_reviews_bs4(is_existing) is False:
                    break
                time.sleep(1)
                if self.transition_next_page() is False:
                    break
            print('プログラムを終了します。')
            self.generate_log_csv(url, status='SUCCEED')
        except Exception:
            self.generate_log_csv(url, status='FAILED')
        finally:
            self.driver.quit()


if __name__ == "__main__":

    crawler = ReviewCrawler()
    # questionnaire = questionnaire.Questionnaire()

    # print('URLを入力してください。')
    # url = questionnaire.ask_url()
    url = r'https://www.amazon.co.jp/dp/B00840PFXU/'
    # url = r'http://www.amazon.jp/product-reviews/B00840PFXU/'
    crawler.collect(url)