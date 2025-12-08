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
import re


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

        # レポートメタデータ
        self.report_meta = config.report_meta

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
        REPORT_METAが定義されていれば、カラム名を日本語に変換する

        Args:
            data: 2次元リストのデータ
            output_path: 出力ファイルパス
        """
        # report_metaを使用してカラム名を日本語に変換
        if len(data) > 0 and self.report_meta is not None:
            try:
                base_object = self._extract_base_object_from_soql(self.soql)
                label_map = self._build_column_label_map(self.report_meta, base_object)
                data[0] = self._convert_headers_to_labels(data[0], label_map)
                print(f"[INFO] カラム名を日本語に変換しました")
            except Exception as e:
                print(f"[WARN] カラム名変換に失敗しました: {e}")

        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"[INFO] Saved to {output_path}")

    def _build_column_label_map(self, report_meta: dict, base_object: str = None) -> dict:
        """
        レポート定義からAPI名→日本語ラベルのマッピングを構築する
        キーは小文字に正規化される（Bulk APIが小文字で返すため）

        Args:
            report_meta: レポートメタデータ（detailColumnInfoを含む）
            base_object: FROM句のベースオブジェクト名（例: "OptionObject__c"）

        Returns:
            API名（小文字）をキー、日本語ラベルを値とする辞書
        """
        label_map = {}
        detail_column_info = report_meta.get("detailColumnInfo", {})

        for api_name, info in detail_column_info.items():
            label = info.get("label", api_name)
            # API名からBulk APIのカラム名形式に変換
            parts = api_name.split(".")
            if len(parts) >= 2:
                first_object = parts[0]  # 最初のオブジェクト名
                field_parts = parts[1:]

                # ベースオブジェクト以外のオブジェクトからのフィールドは親参照として扱う
                if base_object and first_object != base_object:
                    # 親オブジェクトへの参照: ObjectName__c → objectname__r
                    parent_ref = first_object.replace("__c", "__r").lower()
                    # __c を __r に変換（最後の項目以外）
                    converted_parts = []
                    for i, part in enumerate(field_parts):
                        if i < len(field_parts) - 1 and part.endswith("__c"):
                            converted_parts.append(part.replace("__c", "__r"))
                        else:
                            converted_parts.append(part)
                    bulk_column_name = parent_ref + "." + ".".join(converted_parts)
                else:
                    # ベースオブジェクトのフィールド: 最初のオブジェクト名を除去
                    converted_parts = []
                    for i, part in enumerate(field_parts):
                        if i < len(field_parts) - 1 and part.endswith("__c"):
                            converted_parts.append(part.replace("__c", "__r"))
                        else:
                            converted_parts.append(part)
                    bulk_column_name = ".".join(converted_parts)

                # 小文字に正規化してマッピング
                label_map[bulk_column_name.lower()] = label
            else:
                label_map[api_name.lower()] = label

        return label_map

    def _convert_headers_to_labels(self, headers_row: list, label_map: dict) -> list:
        """
        CSVヘッダー行をAPI名から日本語ラベルに変換する

        Args:
            headers_row: CSVのヘッダー行（API名のリスト）
            label_map: API名（小文字）→ラベルのマッピング

        Returns:
            日本語ラベルに変換されたヘッダー行
        """
        return [label_map.get(h.lower(), h) for h in headers_row]

    def _extract_base_object_from_soql(self, soql: str) -> str:
        """
        SOQLからFROM句のベースオブジェクト名を抽出する

        Args:
            soql: SOQLクエリ文字列

        Returns:
            ベースオブジェクト名（例: "OptionObject__c"）
        """
        match = re.search(r'\bFROM\s+(\w+)', soql, re.IGNORECASE)
        if match:
            return match.group(1)
        return None


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

            # レポートメタデータ（このファイルではREPORT_METAを使用）
            self.report_meta = REPORT_META

            # CSV出力先のベースパス
            self.sf_folder_base_path = "./output"

    # Configインスタンスを作成
    config = Config()

    # SalesforceBulkQueryを実行
    sf_query = SalesforceBulkQuery(config)

    # クエリ実行
    results = sf_query.execute()
    print(f"[SUCCESS] 取得完了: {len(results)}行")
