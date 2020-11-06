# Web_Crawler

### AmazonとTwitterのWebクローラー
__Amazonのスクレイピングは[利用規約](https://www.amazon.co.jp/gp/help/customer/display.html?nodeId=GLSBYFE9MGKKQXXM)により明示的に禁止されています。__  
>この利用許可には、アマゾンサービスまたはそのコンテンツの転売および商業目的での利用、製品リスト、解説、価格などの収集と利用、アマゾンサービスまたはそのコンテンツの二次的利用、第三者のために行うアカウント情報のダウンロードとコピーやその他の利用、データマイニング、ロボットなどのデータ収集・抽出ツールの使用は、一切含まれません。  

__あくまで、スクレイピングのコードの参考としてください。__

# DEMO

"hoge"の魅力が直感的に伝えわるデモ動画や図解を載せる

# Features

"hoge"のセールスポイントや差別化などを説明する

# Requirement

"hoge"を動かすのに必要なライブラリなどを列挙する

requirements.txtを参照してください。

# Installation

Requirementで列挙したライブラリなどのインストール方法を説明する

```
# 仮想環境を利用する場合
$ cd [project dir]
$ python3 -m venv [newenvname]

$ pip install -r requirements.txt
```

# Usage

DEMOの実行方法など、"hoge"の基本的な使い方を説明する  
### Amazon
```
$ cd [any directory]
$ git clone https://github.com/s171156/Web_Crawler.git
$ cd ~/Crawler

# Windows
$ .\[envname]\Scripts\activate
# Linux,Mac
$ . [newenvname]/bin/activate

$ python ./selen_crawler.py
$ https://www.Amazon.co.jp/dp/ASIN
```

### Twitter

```
$ git clone https://github.com/s171156/Web_Crawler.git
$ cd ~/Crawler
```

# Note

__Twitterのアクセストークンは含まれていません。__  
Twitterのスクレイピングをご利用になる場合は以下の手順に従ってください。  
#### \[手順]
1. TwitterのAPIキーの入手
1. 環境変数ファイル(Web_Crawler/Twitter/env/.env.template)の編集  
1. 環境変数ファイルのリネーム  
```
# TwitterのAPI_Key
API_Key = "XXXXXXXXXX"
API_Secret_Key = "XXXXXXXXXXXXXXXXXXXX"
# TwitterのAccess_Token
Access_Token = "XXXXXXXXXX"
Access_Token_Secret = "XXXXXXXXXXXXXXXXXXXX"
```
> Web_Crawler/Twitter/env/.env.template
>> Web_Crawler/Twitter/env/.env

# Author

* 作成者
* 所属
* E-mail

# License



## Disclaimer
当スクリプトの利用によるいかなる損害に対して一切の責任を負いません。自己責任の上でご利用ください。
