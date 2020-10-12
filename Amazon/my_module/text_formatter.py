from datetime import datetime as dt
from datetime import timedelta
import re


def rm_url(text):
    '''
    正規表現で取得したテキストのURLを''に置換します。
    '''
    # 正規表現で使用するパターンをコンパイル
    pattern = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    repatter = re.compile(pattern)
    return re.sub(repatter, '', text)


if __name__ == "__main__":
    pass
