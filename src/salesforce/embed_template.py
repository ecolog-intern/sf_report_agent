"""
Salesforce Bulk API 2.0 を使用してレポートデータを取得する
自動生成されたファイル
"""

import requests
import time
import csv
import io
import json
from datetime import datetime
import os


class SalesforceBulkQuery:
    def __init__(self, config):
        # Salesforce関係
        self.sf_username = config.sf_username
        self.sf_password = config.sf_password
        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.sf_access_token_URL = config.sf_access_token_URL
        self.api_version = config.api_version
        
        # SOQL取得
        self.soql = config.soql
            
        # output の csv のパス
        now = datetime.now()
        year = now.strftime("%Y年")          # 例: 2025
        month = now.strftime("%m月")         # 例: 01
        file_name = now.strftime("%m月%d日.csv")  # 例: 01月12日.csv

        base_dir = config.sf_folder_base_path
        year_dir = os.path.join(base_dir, year)
        month_dir = os.path.join(year_dir, month)

        # フォルダを自動作成
        os.makedirs(month_dir, exist_ok=True)

        # 完全パス
        self.output_csv_path = os.path.join(month_dir, file_name)

    def execute(self):
        """
        実際の抽出処理
        Salesforceのアクセストークンを取得して、Salesforceのレポートを取得
        """
        # 認証
        access_token, instance_url = self.authenticate_salesforce()
        print(f"[INFO] Connected to {instance_url}")

        # クエリ実行
        results = self.run_bulk_query(instance_url, access_token)
        print(f"[INFO] 結果を {self.output_csv_path} に保存しました。")
        
        return results

    def authenticate_salesforce(self):
        """
        Salesforce OAuth2認証を行う

        Returns:
            (access_token, instance_url)
        """
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.sf_username,
            "password": self.sf_password
        }

        response = requests.post(self.sf_access_token_URL, data=payload)
        if response.status_code != 200:
            print("[ERROR] Salesforce authentication failed:")
            print(response.text)
            raise Exception(f"Salesforce authentication failed ({response.status_code})")

        data = response.json()
        return data["access_token"], data["instance_url"]

    def run_bulk_query(self, instance_url, access_token) -> list:
        """
        Bulk API 2.0でSOQLクエリを実行し、結果をリストで返す

        Args:
            instance_url: SalesforceインスタンスURL
            access_token: アクセストークン

        Returns:
            CSVデータを2次元リストとして返す
        """
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        base_url = f"{instance_url}/services/data/v{self.api_version}/jobs/query"

        # 1. ジョブ作成
        payload = {
            "operation": "query",
            "query": self.soql,
            "contentType": "CSV"
        }

        job_res = requests.post(base_url, headers=headers, json=payload)

        if not job_res.ok:
            print("[ERROR] Job creation failed")
            print("Status:", job_res.status_code)
            try:
                error_text = json.dumps(job_res.json(), indent=2, ensure_ascii=False)
                print(error_text)
            except Exception:
                print(job_res.text)
            job_res.raise_for_status()

        job_id = job_res.json()["id"]
        print(f"[INFO] Job created: {job_id}")

        # 2. ジョブ完了待ち
        while True:
            status_res = requests.get(f"{base_url}/{job_id}", headers=headers)
            status_res.raise_for_status()
            state = status_res.json()["state"]
            print(f"[INFO] Job state: {state}")
            if state in ("JobComplete", "Failed", "Aborted"):
                break
            time.sleep(5)

        if state != "JobComplete":
            print(f"[ERROR] Job ended with state: {state}")
            print(status_res.text)
            raise Exception("Bulk query job failed.")

        # 3. 結果CSVダウンロード
        result_res = requests.get(f"{base_url}/{job_id}/results", headers=headers)
        result_res.raise_for_status()
        decoded = result_res.content.decode("utf-8")
        all_rows = list(csv.reader(io.StringIO(decoded)))

        print(f"[INFO] Retrieved {len(all_rows)} rows (including header)")

        # 4. CSV保存（パスが指定されている場合）
        self.save_to_csv(all_rows, self.output_csv_path)
        
        return all_rows

    def save_to_csv(self, data, output_path):
        """
        データをCSVファイルに保存する

        Args:
            data: 2次元リストのデータ
            output_path: 出力ファイルパス
        """
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"[INFO] Saved to {output_path}")


# 使用例
if __name__ == "__main__":
    # 設定クラス（Config）を作成する
    class Config:
        def __init__(self):
            # Salesforce接続情報
            self.sf_username = "your_username@example.com"
            self.sf_password = "your_password"
            self.client_id = "your_client_id"
            self.client_secret = "your_client_secret"
            self.sf_access_token_URL = "https://login.salesforce.com/services/oauth2/token"
            self.api_version = "62.0"
            
            # SOQL（このファイルではSOQL_QUERYを使用）
            self.soql = SOQL_QUERY
            
            # CSV出力先のベースパス
            self.sf_folder_base_path = "./output"
    
    # Configインスタンスを作成
    config = Config()
    
    # SalesforceBulkQueryを実行
    sf_query = SalesforceBulkQuery(config)
    
    # クエリ実行
    results = sf_query.execute()
    print(f"[SUCCESS] 取得完了: {len(results)}行")
