'''
環境変数読み込み・設定
'''

import os
from dotenv import load_dotenv

# .envを読み込む
load_dotenv()

class Settings:
    """アプリ全体で使う環境変数を集中管理するクラス"""

    # agent関係
    LLM_PROVIDER = os.getenv("LLM_PROVIDER")  
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL_NAME = os.getenv("ANTHROPIC_MODEL_NAME")
    MAX_RETRY_COUNT = os.getenv("MAX_RETRY_COUNT")
    
    # Salesforce接続設定
    SALESFORCE_CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
    SALESFORCE_CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")
    SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")
    SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD")
    SALESFORCE_ACCESSTOKEN_URL = os.getenv("SALESFORCE_ACCESSTOKEN_URL")
    SALESFORCE_REPORT_ID = os.getenv("SALESFORCE_REPORT_ID")
    SALESFORCE_API_VERSION = os.getenv("SALESFORCE_API_VERSION")


    # 出力パス
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")

settings = Settings()
