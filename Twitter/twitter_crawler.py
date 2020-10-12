from tqdm import tqdm
from my_module.questionnaire import TwitterQuestionnaire
from tweets_csv import TweetsCSVGenerator
import sys

if __name__ == "__main__":

    number = 10
    questionnaire = TwitterQuestionnaire()

    print('ようこそ！\nこのプログラムは指定したキーワードを含むツイートやユーザーのタイムラインを収集します。')
    print()
    print('===============操作方法===============')
    print("y        : YES")
    print("n        : NO")
    print("q        :プログラムの終了")
    print("CTRL+C   :プログラムの強制終了")
    print('======================================')
    print()

    print('プログラムをご利用になりますか？ y/n')
    if questionnaire.ask_y_or_n() is False:
        print('プログラムを終了します。')
        sys.exit()

    # キーワード検索用インスタンス
    csv_gen_k = TweetsCSVGenerator(mode='k')
    # ユーザー検索用インスタンス
    csv_gen_y = TweetsCSVGenerator(mode='y')

    while True:

        print('新規パラメータを登録しますか？       :   y/n')
        if questionnaire.ask_y_or_n() is False:
            break

        print('登録済みパラメータを参照しますか？       :   y/n')
        if questionnaire.ask_y_or_n():
            print('キーワード検索パラメータを参照しますか？     :   y/n')
            if questionnaire.ask_y_or_n():
                for params in csv_gen_k.show_params():
                    print(params)
            print('ユーザー検索パラメータを参照しますか？       :   y/n')
            if questionnaire.ask_y_or_n():
                for params in csv_gen_y.show_params():
                    print(params)

        # キーワードをセット
        answer = questionnaire.ask_keyword()

        if answer['by_keyword'] and answer['by_user'] is False:
            csv_gen_k.update_params_by_keyword(answer)
        elif answer['by_user'] and answer['by_keyword'] is False:

            print('最新のツイート１件を表示します')
            csv_gen_y.set_tmp_keyword(answer['keyword'])
            csv_gen_y.set_csv_path()
            getter = csv_gen_y.set_getter()
            pbar_tweets = tqdm(getter.collect(total=1), total=1)
            # total件数だけツイートを収集する
            for tweet in pbar_tweets:
                pbar_tweets.set_description('Progress')
                csv_gen_y.add_list(tweet)

            csv_gen_y.show_tmp_df_tweet()
            print('こちらのツイートで間違いありませんか？')
            if questionnaire.ask_y_or_n() is False:
                continue

            csv_gen_y.generate_tweets()
            csv_gen_y.generate_params_by_user()

            del csv_gen_y
            csv_gen_y = TweetsCSVGenerator(mode='y')

            if answer['by_keyword']:
                csv_gen_k.update_params_by_keyword(answer)

            # csv_gen_y.update_params_by_user(answer)
        elif answer['by_user'] == answer['by_keyword'] is False:
            print('スキップされました。')
            break

    while True:

        print('登録キーワード/ユーザーのツイートを収集しますか？   y/n')
        if questionnaire.ask_y_or_n() is False:
            break

        print('登録キーワードのツイートを収集しますか？     y/n')
        if questionnaire.ask_y_or_n():
            print('登録済みパラメータを参照します')
            for params in csv_gen_k.show_params():
                print(params)
            print('キーワードのインデックスを入力してください')
            index = questionnaire.ask_number()
            print('最新のツイートを収集しますか？')
            if questionnaire.ask_y_or_n():
                csv_gen_k.set_keyword(index=index, mode='r')
            else:
                print('過去のツイートを収集しますか？')
                if questionnaire.ask_y_or_n():
                    csv_gen_k.set_keyword(index=index, mode='p')
                else:
                    print('最近と過去どちらかをお選びください')
                    continue
            print(f'何件のデータを収集しますか？ デフォルトでは{number}件に設定されています。')
            number = questionnaire.ask_number()
            if number <= 0:
                print('1以上のアラビア数字を入力してください')
                continue
            print(f'{number}件でよろしいですか？')
            if questionnaire.ask_y_or_n() is False:
                continue
            csv_gen_k.set_csv_path()
            getter = csv_gen_k.set_getter()
            pbar_tweets = tqdm(getter.collect(total=number), total=number)
            # total件数だけツイートを収集する
            for tweet in pbar_tweets:
                # for tweet in getter.collect(total=3000):
                pbar_tweets.set_description('Progress')
                csv_gen_k.add_list(tweet)

            csv_gen_k.generate_tweets()
            csv_gen_k.generate_params_by_keyword()

            del csv_gen_k
            csv_gen_k = TweetsCSVGenerator(mode='k')

        print('登録ユーザーのタイムラインを収集しますか？   y/n')
        if questionnaire.ask_y_or_n():
            print('登録済みパラメータを参照します')
            for params in csv_gen_y.show_params():
                print(params)
            print('キーワードのインデックスを入力してください')
            index = questionnaire.ask_number()
            print('最新のツイートを収集しますか？')
            if questionnaire.ask_y_or_n():
                csv_gen_y.set_keyword(index=index, mode='r')
            else:
                print('過去のツイートを収集しますか？')
                if questionnaire.ask_y_or_n():
                    csv_gen_y.set_keyword(index=index, mode='p')
                else:
                    print('最近と過去どちらかをお選びください')
                    continue
            print(f'何件のデータを収集しますか？ デフォルトでは{number}件に設定されています。')
            number = questionnaire.ask_number()
            if number <= 0:
                print('1以上のアラビア数字を入力してください')
                continue
            print(f'{number}件でよろしいですか？')
            if questionnaire.ask_y_or_n() is False:
                continue
            csv_gen_y.set_csv_path()
            getter = csv_gen_y.set_getter()
            pbar_tweets = tqdm(getter.collect(total=2), total=2)
            # total件数だけツイートを収集する
            for tweet in pbar_tweets:
                # for tweet in getter.collect(total=3000):
                pbar_tweets.set_description('Progress')
                csv_gen_y.add_list(tweet)

            csv_gen_y.generate_tweets()
            csv_gen_y.generate_params_by_user()

            del csv_gen_y
            csv_gen_y = TweetsCSVGenerator(mode='y')

    print('全ての登録キーワードのツイートを収集しますか？   y/n')
    if questionnaire.ask_y_or_n():
        print('未実装')
        pass

    print('プログラムを終了します。')
