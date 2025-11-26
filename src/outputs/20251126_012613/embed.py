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
    Contractor_Information__r.Name,
    Contractor_Information__r.smart_customer_id__c,
    Name,
    plan_code__r.Name,
    Contractor_Information__r.parent_agency__c,
    Contractor_Information__r.account__c,
    Contractor_Information__r.sales_channel__c,
    Contractor_Information__r.customer_type__c,
    Contractor_Information__r.contractor_name__c,
    Contractor_Information__r.contractor_name_kana__c,
    Comp_Before_Switch__r.Name,
    current_gas_plam__c,
    supply_point_identification_no__c,
    customer_no__c,
    latest_billing_year_month__c,
    bill__c,
    usage_fee__c,
    billing_amount__c,
    discount_rate__c,
    Contractor_Information__r.payment_type__c,
    place_name__c,
    Contractor_Information__r.zip__c,
    Contractor_Information__r.contractor_address__c,
    Contractor_Information__r.request_date__c,
    Contractor_Information__r.atokaku_call_status__c,
    contract_confirmation_call_ok_date__c,
    Contractor_Information__r.latest_billing_month__c,
    Contractor_Information__r.Latest_payment_meyhod__c,
    cancel_date__c,
    cancel_confirmed_date__c,
    cancellation_date__c,
    cancel_reason__c,
    use_place_zip__c,
    use_place_address_connect__c,
    use_place_name__c,
    use_place_name_kana__c,
    matching_result__c,
    switching_request_ok_date__c,
    scheduled_switching_date__c,
    Contractor_Information__r.email__c,
    Contractor_Information__r.business_sector__c,
    Contractor_Information__r.business_sector_detail__c,
    Contractor_Information__r.fact_clct_date__c,
    Contractor_Information__r.representative_age__c,
    Contractor_Information__r.representative_brth__c,
    Contractor_Information__r.representative_country__c,
    Contractor_Information__r.representative_name__c,
    Contractor_Information__r.representative_name_kana__c,
    Contractor_Information__r.pic_name__c,
    Contractor_Information__r.pic_name_kana__c,
    Contractor_Information__r.pic_tel__c,
    Contractor_Information__r.shop_name__c,
    distinguish_place_tel__c,
    Contractor_Information__r.tel1_connect__c,
    use_place_tel_connect__c,
    Contractor_Information__r.tel2_connect__c,
    Contractor_Information__r.document_destination_name__c,
    Contractor_Information__r.document_destination_address_connect__c,
    remarks1__c,
    remarks2__c,
    remarks3__c,
    Contractor_Information__r.atokaku_comment__c,
    Contractor_Information__r.claim_linking_no__c,
    Contractor_Information__r.application_information__r.Name
FROM Gas_Contract__c
WHERE 
    cancel_date__c = null
    AND cancel_confirmed_date__c = null
    AND cancel_cooperation_date__c = null
    AND cancel_reason__c = null
    AND forced_termination_date__c = null
    AND cancellation_date__c = null
    AND Compulsory_cancellation_date__c = null
    AND cancellation_confirmed_date__c = null
    AND Contractor_Information__r.parent_agency__c != '株式会社アイステーション（管理）'
    AND Contractor_Information__r.parent_agency__c != '株式会社アクセル（商品企画）'
    AND Contractor_Information__r.parent_agency__c != '株式会社ネクシィーズ'
    AND Contractor_Information__r.account__c != '株式会社ネクシィーズ'
    AND Contractor_Information__r.account__c != 'NUWORKS株式会社（テンポス）'
    AND Contractor_Information__r.account__c != 'NUWORKS株式会社(t)'
    AND Contractor_Information__r.account__c != '株式会社come up'
    AND Contractor_Information__r.Latest_payment_meyhod__c != 'コンビニ'
    AND Contractor_Information__r.Call_FLG__c = null
    AND Contractor_Information__r.parent_agency__c != '株式会社エコログ（SP）'
    AND Contractor_Information__r.parent_agency__c != 'EPARK（管理）'
    AND scheduled_switching_date__c >= 2025-09-01
    AND scheduled_switching_date__c < 2025-10-01
ORDER BY Contractor_Information__r.contractor_name__c ASC"""


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
