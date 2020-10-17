import re
import datetime as dt


def remove_url(text):
    '''
    正規表現で取得したテキストのURLを''に置換します。
    '''
    # 正規表現で使用するパターンをコンパイル
    pattern = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    repatter = re.compile(pattern)
    return re.sub(repatter, '', text)


def extract_date_ymd(text: str) -> list:
    '''
    文字列から「YYYY年MM月DD日」を抽出します。
    '''
    pattern = r'\d{1,4}年\d{1,2}月\d{1,2}日'
    repatter = re.compile(pattern)
    return re.search(repatter, text).group()


def disassemble_date_ymd(date: str) -> list:
    '''
    「YYYY年MM月DD日」文字列から年月日を抽出します。
    '''
    pattern = r'\d{1,4}年|\d{1,2}月|\d{1,2}日'
    repatter = re.compile(pattern)
    date = re.findall(repatter, date)
    date = [d[:-1] for d in date]
    date = list(map(int, date))
    return date


def convert_datetime_date(date: str):
    '''
    DateTimeオブジェクトに変換します。
    '''
    date = extract_date_ymd(date)
    date = disassemble_date_ymd(date)
    return dt.date(*date)


if __name__ == "__main__":
    pass
