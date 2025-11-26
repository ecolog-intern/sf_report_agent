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


# 埋め込まれたSOQLクエリ
SOQL_QUERY = """SELECT 
    Contractor_Information__r.Payment_agency_name__c,
    Contractor_Information__r.parent_agency__c,
    Contractor_Information__r.account__c,
    Contractor_Information__r.Name,
    Name,
    option_plan_code__r.Name,
    denki_contract_id__r.Name,
    denki_contract_id__r.contract_confirmation_call_ok_date__c,
    denki_contract_id__r.cancel_date__c,
    denki_contract_id__r.cancellation_date__c,
    gas_contract_id__r.Name,
    gas_contract_id__r.contract_confirmation_call_ok_date__c,
    gas_contract_id__r.cancel_date__c,
    gas_contract_id__r.cancellation_date__c,
    cancel_day__c,
    cancellation_day__c,
    use_start_date__c,
    billing_start_date__c
FROM OptionObject__c
WHERE (
    (gas_contract_id__r.contract_confirmation_call_ok_date__c >= 2025-11-01 
     AND gas_contract_id__r.contract_confirmation_call_ok_date__c <= 2025-11-30)
    OR 
    (denki_contract_id__r.contract_confirmation_call_ok_date__c >= 2025-11-01 
     AND denki_contract_id__r.contract_confirmation_call_ok_date__c <= 2025-11-30)
)
AND option_plan_code__r.Name IN (
    '【新】設備メンテナンス',
    '店舗サポートパック（3ヶ月無料）',
    'オフィスサポートパック（3ヶ月無料）',
    '設備メンテナンスサービス（3ヶ月無料）'
)
ORDER BY gas_contract_id__r.contract_confirmation_call_ok_date__c ASC"""


def authenticate_salesforce(client_id: str, client_secret: str, username: str, password: str,
                             access_token_url: str = "https://login.salesforce.com/services/oauth2/token") -> tuple:
    """
    Salesforce OAuth2認証を行う

    Returns:
        (access_token, instance_url)
    """
    payload = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password
    }

    response = requests.post(access_token_url, data=payload)
    if response.status_code != 200:
        print("[ERROR] Salesforce authentication failed:")
        print(response.text)
        raise Exception(f"Salesforce authentication failed ({response.status_code})")

    data = response.json()
    return data["access_token"], data["instance_url"]


def run_bulk_query(instance_url: str, access_token: str, soql: str = None,
                   api_version: str = "62.0", output_csv_path: str = None) -> list:
    """
    Bulk API 2.0でSOQLクエリを実行し、結果をリストで返す

    Args:
        instance_url: SalesforceインスタンスURL
        access_token: アクセストークン
        soql: SOQLクエリ（省略時は埋め込みクエリを使用）
        api_version: APIバージョン
        output_csv_path: CSV出力パス（省略時はタイムスタンプ付きで保存）

    Returns:
        CSVデータを2次元リストとして返す
    """
    if soql is None:
        soql = SOQL_QUERY

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    base_url = f"{instance_url}/services/data/v{api_version}/jobs/query"

    # 1. ジョブ作成
    payload = {
        "operation": "query",
        "query": soql,
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
    if output_csv_path:
        save_to_csv(all_rows, output_csv_path)

    return all_rows


def save_to_csv(data: list, output_path: str = "output.csv"):
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
    # 認証情報を設定
    CLIENT_ID = "your_client_id"
    CLIENT_SECRET = "your_client_secret"
    USERNAME = "your_username@example.com"
    PASSWORD = "your_password"
    ACCESS_TOKEN_URL = "https://login.salesforce.com/services/oauth2/token"
    output_path = "output.csv"  # 任意のパスを指定

    # 認証
    access_token, instance_url = authenticate_salesforce(
        CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, ACCESS_TOKEN_URL
    )
    print(f"[INFO] Connected to {instance_url}")

    # クエリ実行（CSV出力パスを指定可能）
    results = run_bulk_query(instance_url, access_token, output_csv_path=output_path)
