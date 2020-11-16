# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 環境変数のAPI_KEY/ACCESS_TOKENを代入
AK = os.environ.get("API_KEY")
ASK = os.environ.get("API_SECRET_KEY")
AT = os.environ.get("ACCESS_TOKEN")
ATS = os.environ.get("ACCESS_TOKEN_SECRET")
