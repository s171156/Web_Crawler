import sys
import csv
from pathlib import Path
import pandas as pd
import re
import datetime as dt
from abc import ABCMeta, abstractmethod
import os
import urllib


def slice_str():
    ASIN = 'dp/B00840PFXU/'
    print(ASIN[3:-1])


def unpack_list():
    test = [1,  2, 3]
    print(test)
    print(*test)


def inner_yield(txt):
    yield txt
    yield txt*2
    yield txt*3


def test_size():
    with open('./Amazon/test.txt', mode='a', encoding='utf-8') as f:
        print(sys.getsizeof(f))
    with open('./Amazon/test.txt', mode='ab') as f:
        print(sys.getsizeof(f))
    with open('./Amazon/test.txt', mode='rb') as f:
        print(sys.getsizeof(f.read()))
    with open('./Amazon/test.txt', mode='r', encoding='utf-8') as f:
        print(sys.getsizeof(f.read()))


class test_closure:

    def __init__(self):
        self.hoge = 'instance argument'

    def outer(self):

        dic = {'hoge': [], 'fuga': []}
        print('running outer')
        print()

        def inner(string: str = None, output: bool = None):

            if output:
                return dic

            if string:
                print('入力がありません。')
                pass

            dic['hoge'].append(string)
            dic['fuga'].append(string)
            print(dic)
            print('running inner')
            print()

        return inner


'''
Pythonの引数は全て参照渡し。
関数にミュータブルなオブジェクトを引数に渡して変更を加えた場合、元のオブジェクトにもその変更は適用される。
対して、引数にイミュータブルなオブジェクトを渡して変更を加えても、元のオブジェクトに変更は適用されない。
ただし、これまでの参照先から新たに生成されたオブジェクトを参照するようになる。
'''


def test_ref_id(ref):

    print(id(ref))
    if type(ref) == int:
        ref += 1
        print(id(ref))


def test_ref_dict():
    dic = dic2 = {'hoge': 'hoge', 'fuga': 'fuaga'}
    print(id(dic) == id(dic2))
    dic2['hogefuga'] = 'hogefuga'
    print(id(dic) == id(dic2))
    print(dic)
    print(dic2)


def test_ref_str():
    a = b = 123
    print(a, b)
    print(id(a) == id(b))  # True
    a += 4
    print(a, b)
    print(id(a) == id(b))  # False


def test_ref_df(df):
    print('ref:', id(df))
    print()

    df_new = pd.DataFrame([[1, 2, 3]], columns=['hoge', 'fuga', 'hogefuga'])
    print('new_df', id(df_new))
    print()

    df_new = df.append(df_new)
    print('appending...')
    print(id(df.append(df_new)))
    print()
    print('appended:', id(df))
    print(df_new)
    # df_new.append(df)
    # print('appended', id(df_new))
    print()


def append_df_from_csv():
    # df_new = pd.read_csv('./test.csv')
    _dict = {'hoga': [2], 'fuge': [2], 'hogafuge': [2]}
    df_new = pd.DataFrame.from_dict(_dict)
    print(df_new.iloc[0]['hoga'])
    # df_new.to_csv('./test.csv', mode='a', header=False, index=False)


def read_df_from_csv():
    df_new = pd.read_csv('./test.csv', chunksize=1)
    row = next(df_new)
    # print(row.to_dict(orient='dict'))
    # print(row.to_dict(orient='list'))
    # print(row.to_dict(orient='series'))
    # print(row.to_dict(orient='split'))
    # print(row.to_dict(orient='records')[0]['hoge'])
    # print(type(row.to_dict(orient='records')[0]['hoge']))
    print(row.iloc[0]['hoge'])


def test_rename():
    path = Path('./test.csv')
    test = './tmp.csv'
    os.rename(path, test)


def re_test():
    text = '2020年2月2日または2020-2-3に日本でレビュー済み'
    pattern = r'\d{1,4}年\d{1,2}月\d{1,2}日|\d{1,4}-\d{1,2}-\d{1,2}'
    repatter = re.compile(pattern)
    date = re.findall(repatter, text)
    if re.match(repatter, date[1]):
        print(True)


def disassemble_date(date: str):
    pattern = r'\d{1,4}年|\d{1,2}月|\d{1,2}日'
    repatter = re.compile(pattern)
    date = re.findall(repatter, date)
    date = [d[:-1] for d in date]
    date = list(map(int, date))
    return date


def extract_keys():
    _dict1 = {'f_name': 'hoge', 'l_name': 'hoge'}
    _dict2 = {'f_name': 'fuga', 'l_name': 'fuga'}
    keys1 = _dict1.keys()
    keys2 = _dict2.keys()
    print(keys1 == keys2)


def test_datetime_date():
    date = [2020, 1, 1]
    date = dt.date(*date)
    print(date)


def test_list_slice():
    li = (1, 2, 3, 4, 5)
    print(len(li))
    print(li[len(li)-1])
    print(li[-1])


class TestAbstractClass(metaclass=ABCMeta):
    @ abstractmethod
    def test_method(self):
        pass


class TestClass(TestAbstractClass):
    def test2_method(self, hoge: int):
        print(hoge)


class DictsKeyError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'A dictionary does not contain specified keys.'


def test_raise():
    hoge = 1
    if hoge == 0:
        print(hoge)
    else:
        pass


def join_dict():
    _dict1 = [{'hoge': [1], 'fuga': [1], 'hogefuga': [1]}]
    print(_dict1)
    _dict2 = {'hoge': [2, 3, 4, 5], 'fuga': [
        2, 3, 4, 5], 'hogefuga': [2, 3, 4, 5]}
    for key, value in _dict2.items():
        _dict1[key].extend(value)
    print(_dict1)
    df = pd.DataFrame.from_dict(_dict1)
    print(df)


def generate_log_csv():
    '''
    ログファイルを出力します。
    '''
    dict_log = {'date': '2020/10/17 18:52:20.35', 'status': 'SUCCEED',
                'ASIN': 'B00840PFXU', 'brand': '白州', 'product': 'サントリー シングルモルト ウイスキー 白州 [日本 700ml ]'}
    df = pd.DataFrame.from_dict([dict_log])
    file_path = './test.csv'
    if Path(file_path).exists():
        df.to_csv(file_path)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)


def say_hello():
    print('Hello')


def test_none():
    none = None
    for key, value in none:
        print(key, value)


def test_path():
    path = Path('.').resolve()
    print(path)
    path = Path(__file__).resolve()
    print(path)
    path = Path(__file__).resolve().parents[0]
    print(path)


def test_datetime():
    date = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-4]
    print(date)


def get_product_name():
    url = r'https://www.amazon.co.jp/%E7%99%BD%E5%B7%9E-%E3%82%B5%E3%83%B3%E3%83%88%E3%83%AA%E3%83%BC-%E3%82%B7%E3%83%B3%E3%82%B0%E3%83%AB%E3%83%A2%E3%83%AB%E3%83%88-700ml/dp/B00840PFXU/'
    pattern = r'/[\w%-]+/dp/'
    repatter = re.compile(pattern)
    product_name = re.search(repatter, url).group()
    return urllib.parse.unquote(product_name[1:-4])


def get_ASIN_by_pr():
    '''
    カスタマーレビューページのURLからASINコードを取得します。
    '''
    url = r'https://www.amazon.co.jp/%E7%99%BD%E5%B7%9E-%E3%82%B5%E3%83%B3%E3%83%88%E3%83%AA%E3%83%BC-%E3%82%B7%E3%83%B3%E3%82%B0%E3%83%AB%E3%83%A2%E3%83%AB%E3%83%88-700ml/product-reviews/B00840PFXU/ref=cm_cr_getr_d_paging_btm_prev_5?ie=UTF8&reviewerType=all_reviews&pageNumber=5'
    pattern = r'product-reviews/\w+/'
    repatter = re.compile(pattern)
    ASIN = re.search(repatter, url).group()
    print(ASIN[16:-1])


if __name__ == "__main__":
    # read_df()
    # test_datetime()
    # get_product_name()
    # test_dict()
    # get_ASIN_by_pr()
    # join_dict()
    generate_log_csv()
    pass
