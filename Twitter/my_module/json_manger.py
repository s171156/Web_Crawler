from pathlib import Path
import json


def generate_json(file_path: str, dict_json: dict):
    '''
    辞書のリスト型jsonファイルを生成

    Args
    ----
    file_path   :   str
        出力先のパス
    dict_json   :   dict
        記述したい辞書型データ

    Notes
    -----
    同名の既存jsonファイルには末尾にデータを挿入する。
    '''

    # jsonデータを生成する
    with Path(file_path).open(mode='ab+') as f:
        f.seek(0, 2)                                    # ファイル末尾に移動
        if f.tell() == 0:                               # ファイルが空かチェック
            f.write('[\n'.encode())
            f.write(json.dumps(dict_json, indent=4,
                               ensure_ascii=False
                               ).encode())
            f.write('\n]'.encode())
        else:
            f.seek(-1, 2)                               # ファイル末尾から-1文字移動
            f.truncate()                                # 最後の文字(])を削除し、jsonの配列を開く
            f.seek(-1, 2)
            f.truncate()
            f.write(',\n'.encode())                     # 最後のセパレーターを書き込む

            f.write(json.dumps(dict_json, indent=4,
                               ensure_ascii=False
                               ).encode())              # 辞書をjson形式でダンプ書き込み
            f.write('\n]'.encode())                     # jsonの配列を閉じる
