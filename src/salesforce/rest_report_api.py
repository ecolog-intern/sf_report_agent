'''
restapiでレポートの定義を取得する
'''

import requests
from config.settings import settings

def get_report_definition(instance_url, headers):
    report_id = settings.SALESFORCE_REPORT_ID
    endpoint = f"{instance_url}/services/data/v59.0/analytics/reports/{report_id}/describe"
    response = requests.get(endpoint, headers=headers)

    if response.status_code != 200:
        print("[ERROR] Failed to fetch report definition")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        raise Exception(f"Report definition fetch failed ({response.status_code})")

    report_json = response.json()

    # ログ出力（レポート名など）
    report_meta = report_json.get("reportMetadata", {})

    return report_meta
