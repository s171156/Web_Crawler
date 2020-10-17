from pathlib import Path


def get_abs_path(file_path: str, *args, num: int = 0):
    '''
    絶対パスを取得

    Args
    ----
    path    :   str
        指定のパス
    num     :   int
        階層数の指定

    Returns
    -------
    親ディレクトリの絶対パス

    Notes
    -----
    path未指定時は実行ファイルのディレクトリの絶対パスを取得
    '''

    # データを保存するディレクトリを作成
    if args:
        # パスの最後がファイルの場合は親ディレクトリまでのディレクトリを作成
        if Path(args[-1]).suffix != '':
            Path(file_path).resolve().parents[num].joinpath(
                *args).parent.mkdir(parents=True, exist_ok=True)
        else:
            Path(file_path).resolve().parents[num].joinpath(
                *args).mkdir(parents=True, exist_ok=True)

        return Path(file_path).resolve().parents[num].joinpath(*args)
    else:
        return Path(file_path).resolve().parents[num]


if __name__ == "__main__":
    pass
