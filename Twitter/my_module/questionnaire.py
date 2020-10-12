from . import text_validator
import sys


class Questionnaire(object):

    def ask_y_or_n(self, limit: int = 3):
        counter: int = 0
        while True:
            answer = input().strip()
            if answer == 'y':
                return True
            elif answer == 'n':
                return False
            elif answer == 'q':
                print("'q'の入力を検出したためプログラムを終了します。")
                sys.exit()
            else:
                counter += 1
                if counter == limit:
                    print(f'{counter}回入力エラーを検出したためプログラムを終了します。')
                    sys.exit()
                print(f"'y'または'n'を入力してください。        残り試行回数{limit - counter}")

    def ask_keyword(self, limit: int = 3):
        counter = 0
        while True:
            keyword = input().strip()
            if keyword == 'q':
                print("'q'の入力を検出したためプログラムを終了します。")
                sys.exit()
            elif not keyword:
                print('キーワードを入力してください')
            elif keyword:
                print(f"入力は'{keyword}'で間違いありませんか？     :   y/n")

                if self.ask_y_or_n():
                    return keyword
                else:
                    counter += 1
                    if counter == limit:
                        print(f'{counter}回入力エラーを検出したためプログラムを終了します。')
                        sys.exit()
                    print(f"キーワードを入力してください。      残り試行回数{limit - counter}")

    def ask_number(self, limit: int = 3):
        counter = 0
        while True:
            keyword = input().strip()
            if keyword == 'q':
                print("'q'の入力を検出したためプログラムを終了します。")
                sys.exit()
            elif not keyword:
                print('キーワードを入力してください')

            if keyword.isdecimal() is False:
                print('全角または半角アラビア数字を入力してください')
                continue
            print(f"入力は'{keyword}'で間違いありませんか？     :   y/n")
            if self.ask_y_or_n():
                return int(keyword)
            else:
                counter += 1
                if counter == limit:
                    print(f'{counter}回入力エラーを検出したためプログラムを終了します。')
                    sys.exit()
                print(f"キーワードを入力してください。      残り試行回数{limit - counter}")

    def show_dict(self, _dict: dict):
        '''
        辞書の内容を確認します。
        '''
        while True:
            print()
            print('=' * 50)
            print('Parameters'.center(50))
            for key, value in _dict.items():
                print(f'{key}'.ljust(25), end='')
                print(':', end='')
                print(f'{value}'.rjust(24))
            print('=' * 50)
            print()

            print('上記の内容でよろしいでしょうか？       :   y/n')
            return self.ask_y_or_n()


class TwitterQuestionnaire(Questionnaire):
    """
    docstring
    """

    def ask_keyword(self):
        '''
        検索に使用するキーワードの登録を受け取ります。
        '''
        answers = {'keyword': '', 'by_user': False, 'by_keyword': False}
        while True:
            print('キーワードを入力してください')
            keyword = input().strip()

            if keyword == 'q':
                print("'q'の入力を検出したためプログラムを終了します。")
                sys.exit()
            elif keyword == 's':
                return answers
            elif not keyword:
                print('入力がありません。もう一度入力をお願いします。')
                continue

            print(f"入力は'{keyword}'で間違いありませんか？     :   y/n")
            if super().ask_y_or_n() is False:
                continue

            if not keyword[0] == '@':
                answers['keyword'] = keyword
                print('キーワード検索のキーワードとして登録しますか？       :   y/n')
                answers['by_keyword'] = super().ask_y_or_n()
                if answers['by_keyword'] == answers['by_user'] is False:
                    continue
                if super().show_dict(answers) is False:
                    continue
                return answers

            if text_validator.validate_username(keyword):
                answers['keyword'] = keyword
                print('タイムライン検索のキーワードとして登録しますか？     :   y/n')
                answers['by_user'] = super().ask_y_or_n()
                print('キーワード検索のキーワードとして登録しますか？       :   y/n')
                answers['by_keyword'] = super().ask_y_or_n()
                if answers['by_keyword'] == answers['by_user'] is False:
                    continue
                if super().show_dict(answers) is False:
                    continue
                return answers
            else:
                print('ユーザー名は半角英数字かつ15文字以下の文字列で構成されます。')
                print('入力はスクリーンネームですか？       :   y/n')
                if super().ask_y_or_n():
                    if text_validator.validate_screen_name(keyword) is False:
                        print('スクリーンネームは50文字以下の文字列で構成されます。')
                        continue
                    print('タイムライン検索のキーワードとして登録しますか？     :   y/n')
                    answers['by_user'] = super().ask_y_or_n()

                print('キーワード検索のキーワードとして登録しますか？       :  y/n')
                answers['by_keyword'] = super().ask_y_or_n()
                if answers['by_keyword'] == answers['by_user'] is False:
                    continue
                if super().show_dict(answers) is False:
                    continue
                return answers


if __name__ == "__main__":
    pass
