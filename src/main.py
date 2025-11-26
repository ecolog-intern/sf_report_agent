import os
import json
from config.settings import settings
from salesforce.auth import SalesforceAuth
from salesforce.rest_report_api import get_report_definition
from agent.soql_generator_fullpdf import generate_soql_with_full_pdf
from agent.soql_checker import extract_soql
from agent.soql_error_fixer import fix_soql_with_error
from salesforce.bulk_soql_api import run_bulk_query
from agent.soql_vectorstore import init_vectorstore
from requests.exceptions import HTTPError

def main():
    # 0️⃣ ベクトルストアを初期化（DBが空なら構築、存在すればスキップ）
    print("[INFO] Initializing vector store...")
    init_vectorstore()

    # 1️⃣ Salesforce 認証
    sf_auth = SalesforceAuth()
    access_token, instance_url = sf_auth.authenticate()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    print("[INFO] Salesforce connection established.")
    print(f"{access_token, instance_url}")

    # 2️⃣ レポート定義をREST APIで取得
    report_meta = get_report_definition(instance_url, headers)
    print("[INFO] Report definition retrieved successfully.")

    # 3️⃣ Claude/GeminiでSOQLを自動生成
    soql_raw = generate_soql_with_full_pdf(report_meta)
    soql = extract_soql(soql_raw)
    print("\n[RESULT] ===== Generated SOQL =====")
    print(soql)

    # 4️⃣ Bulk APIで実行し、結果をCSVとして保存（リトライ付き）
    retry_count = 0
    last_error = None
    MAX_RETRY_COUNT = int(settings.MAX_RETRY_COUNT)

    while retry_count < MAX_RETRY_COUNT:
        try:
            csv_path = run_bulk_query(instance_url, headers, soql)
            print(f"[INFO] 結果を {csv_path} に保存しました。")
            break
        except HTTPError as e:
            retry_count += 1
            last_error = e

            if retry_count >= MAX_RETRY_COUNT:
                print(f"[ERROR] {MAX_RETRY_COUNT}回のリトライ後も失敗しました。")
                raise

            # エラーメッセージを抽出
            try:
                error_message = json.dumps(e.response.json(), indent=2, ensure_ascii=False)
            except Exception:
                error_message = e.response.text

            print(f"\n[RETRY {retry_count}/{MAX_RETRY_COUNT}] SOQLエラーを検出。LLMで修正を試みます...")
            print(f"[INFO] エラー内容:\n{error_message}")

            # LLMでSOQLを修正
            soql = fix_soql_with_error(soql, error_message)
            print(f"\n[RESULT] ===== 修正されたSOQL (試行 {retry_count + 1}) =====")
            print(soql)

    print("[SUCCESS] Report extraction pipeline finished successfully")


if __name__ == "__main__":
    main()
