'''
restapiでレポートの定義を取得する
'''

import requests
from config.settings import settings


def get_object_relationships(instance_url, headers, object_names: list) -> dict:
    """
    指定オブジェクトのdescribe APIを叩き、ルックアップ/参照フィールドの
    リレーション情報を返す。

    Returns:
        {
            "Billing_And_Payment_Detail__c": [
                {
                    "fieldName": "Billing_And_Payment_Master__c",
                    "relationshipName": "Billing_And_Payment_Master__r",
                    "referenceTo": ["Billing_And_Payment_Master__c"]
                },
                ...
            ],
            ...
        }
    """
    result = {}
    for obj_name in object_names:
        url = f"{instance_url}/services/data/v59.0/sobjects/{obj_name}/describe/"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"[WARN] Failed to describe {obj_name}: {resp.status_code}")
            result[obj_name] = []
            continue

        data = resp.json()
        relationships = []
        for field in data.get("fields", []):
            if field.get("type") == "reference" and field.get("relationshipName"):
                relationships.append({
                    "fieldName": field["name"],
                    "relationshipName": field["relationshipName"],
                    "referenceTo": field.get("referenceTo", [])
                })
        result[obj_name] = relationships
        print(f"[DEBUG] {obj_name}: {len(relationships)} 個の参照フィールドを取得")

    return result


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

    # 項目ラベル情報を追加（detailColumnInfo）
    report_extended_meta = report_json.get("reportExtendedMetadata", {})
    detail_column_info = report_extended_meta.get("detailColumnInfo", {})
    report_meta["detailColumnInfo"] = detail_column_info

    print(f"[DEBUG] detailColumnInfo keys: {list(detail_column_info.keys())}")

    return report_meta
