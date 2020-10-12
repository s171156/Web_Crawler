import re


def validate_username(text):
    '''
    正規表現でTwitterのユーザー名としての妥当性を検証します。
    '''

    if text[0] == '@':
        # ユーザー名は15文字以下
        if len(text) > 16:
            return False
    else:
        # ユーザー名は15文字以下
        if len(text) > 15:
            return False

    pattern = r"@\w+"
    repatter = re.compile(pattern)
    return re.match(repatter, text)


def validate_screen_name(text):
    # スクリーンネームは50文字以下
    return len(text) <= 50


if __name__ == "__main__":
    pass
