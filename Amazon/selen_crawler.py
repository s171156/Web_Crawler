# Selenium Module
# import chromedriver_binary
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
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
from random import randint
import traceback


class ReviewCrawler:
    '''
    Amazonのクローラーです。
    '''

    def __init__(self):
        # ドライバのセットアップ
        self.option = webdriver.ChromeOptions()
        # Ubuntuの場合
        self.option.binary_location = '/usr/bin/google-chrome'
        # ヘッドレスモードでクロール
        self.option.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.implicitly_wait(30)

        # インスタンスの生成
        self.r_parser = ReviewParser()

        # レビュー情報を格納する辞書
        self.dict_review = None
        # CSVを出力するパスを格納する辞書
        self.file_path = {}
        # BS4で解析するためにHTMLを一時的に格納
        self.soup = None
        # 現在何ページ処理したか
        self.counter = 0

    def __del__(self):
        print('インスタンスが破棄されました。')
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
        '''
        既存CSVから最新のレビューの日付を取得します。
        '''
        # e_date = existing_date:既存CSVの最新レビューの日付
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
            return True

        except (ElementClickInterceptedException, StaleElementReferenceException, TimeoutException) as e:
            print(e)
            lim = 3
            for i in range(lim):
                print(f'リトライ処理：{i+1}回目     残りの試行回数{lim-i-1}回')
                time.sleep(2)
                print('ページの再読み込みを実施します。')
                self.driver.refresh()
                print('ページの再読み込みを実施しました。')
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.ID, 'cm_cr-pagination_bar')))
                    self.driver.find_element_by_xpath(
                        '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()
                    # target = self.driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a')
                    # self.driver.execute_script("arguments[0].click();", target)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                else:
                    return True
            else:
                print('次のページの読込みに失敗しました。')
                print('CSVを生成します。')
                ReviewCSVGenerator.generate_csv_from_dict(
                    self.dict_review, self.file_path['review'])
                print('CSVの生成が完了しました。')
                return False

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
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "a-autoid-4-announce")))
        self.driver.find_element_by_xpath(
            '//*[@id="a-autoid-4-announce"]').click()
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "sort-order-dropdown_1")))
        self.driver.find_element_by_xpath(
            '//*[@id="sort-order-dropdown_1"]').click()

    def generate_log_csv(self, url: str, status: str):
        '''
        ログファイルを生成します。
        '''
        print('ログファイルを出力します。')
        dict_log = {}
        # 日付をセット
        dict_log['date'] = dt.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-4]
        # スクレイピングの成否をセット
        dict_log['status'] = status
        # ASINコードをセット
        dict_log['ASIN'] = URLValidator.get_ASIN_by_pr(url)
        # 製造メーカーあるいはブランドをセット
        dict_log['brand'] = self.r_parser.get_brand_name(self.soup)
        # 製品名をセット
        dict_log['product'] = self.r_parser.get_product_name(self.soup)
        # ログを生成します。
        ReviewCSVGenerator.generate_log_csv(dict_log, self.file_path['log'])
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
        '''
        カスタマーレビューを収集します。
        '''
        # URLの妥当性を検証します。
        if URLValidator.validate(url) is False:
            print('不正なURLです\nプログラムを終了します。')
            sys.exit()
        # URLを短縮します。
        url = URLValidator.shorten(url)
        # 商品ページのURLを商品レビューページのURLに置換します。
        url = URLValidator.generate_review(url)
        # 各種CSVのパスをセットします。
        self.set_csv_path(url)
        # 各種CSVが既存であるか確認します。
        is_existing = Path(self.file_path['review']).exists()
        # セレニウムで検索します。
        self.driver.get(url)
        # カスタマーレビューを日付順にソートします。
        self.sort_by_date()
        while True:
            try:
                # 1秒スリープします。
                time.sleep(randint(1, 3))
                # HTMLを取得してBS4でパースします。
                self.get_html_soup()
                # カスタマーレビューを収集します。
                if self.get_reviews_bs4(is_existing) is False:
                    break
                # 次のページへ遷移します。
                if self.transition_next_page() is False:
                    break
            except Exception as e:
                print(e)
                traceback.print_exc()
                # セレニウムを終了します。
                self.driver.quit()
                # ログを生成します。
                self.generate_log_csv(url, status='FAILED')
                return
            else:
                pass
        # セレニウムを終了します。
        self.driver.quit()
        # ログを生成します。
        self.generate_log_csv(url, status='SUCCEED')


if __name__ == "__main__":

    print('ようこそ！')
    print('本プログラムはAmzonのカスタマーレビューを収集するものです。')
    print('商品ページのURLを入力してください。')
    # インスタンスの生成
    questionnaire = questionnaire.Questionnaire()
    # URLを標準入力から取得します。
    url = questionnaire.ask_url()

    # インスタンスの生成
    crawler = ReviewCrawler()
    crawler.collect(url)
    print('プログラムを終了します。')
