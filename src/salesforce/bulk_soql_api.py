'''
llmが作成したsoqlを使用して、bulkapiを叩く
'''

import requests
import time
import csv
import io
import os
import zipfile
from config.settings import settings
from datetime import datetime
import json


def generate_embed_file(soql: str, output_dir: str) -> str:
    """
    SOQLを埋め込んだ再利用可能なBulk API実行ファイルを生成する
    """
    template_path = os.path.join(os.path.dirname(__file__), "embed_template.py")
    with open(template_path, "r", encoding="utf-8") as f:
        user_code = f.read()

    escaped_soql = soql.replace('"""', '\\"\\"\\"')
    content = f'SOQL_QUERY = """{escaped_soql}"""\n\n{user_code}'

    file_path = f"{output_dir}/embed.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def generate_proxy_embed_file(soql: str, output_dir: str) -> str:
    """
    SOQLを埋め込んだproxy_embed.pyを生成する
    """
    template_path = os.path.join(os.path.dirname(__file__), "proxy_embed_template.py")
    with open(template_path, "r", encoding="utf-8") as f:
        user_code = f.read()

    escaped_soql = soql.replace('"""', '\\"\\"\\"')
    content = f'SOQL_QUERY = """{escaped_soql}"""\n\n{user_code}'

    file_path = f"{output_dir}/proxy_embed.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def _build_column_label_map(report_meta: dict, base_object: str = None) -> dict:
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
        # 例: "OptionObject__c.Name" → "Name" (ベースオブジェクトの場合)
        # 例: "OptionObject__c.denki_contract_id__c.Name" → "denki_contract_id__r.Name"
        # 例: "Contractor_Information__c.Payment_agency_name__c" → "contractor_information__r.Payment_agency_name__c" (親オブジェクトの場合)
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


def _convert_headers_to_labels(headers_row: list, label_map: dict) -> list:
    """
    CSVヘッダー行をAPI名から日本語ラベルに変換する

    Args:
        headers_row: CSVのヘッダー行（API名のリスト）
        label_map: API名（小文字）→ラベルのマッピング

    Returns:
        日本語ラベルに変換されたヘッダー行
    """
    return [label_map.get(h.lower(), h) for h in headers_row]


def _extract_base_object_from_soql(soql: str) -> str:
    """
    SOQLからFROM句のベースオブジェクト名を抽出する

    Args:
        soql: SOQLクエリ文字列

    Returns:
        ベースオブジェクト名（例: "OptionObject__c"）
    """
    import re
    match = re.search(r'\bFROM\s+(\w+)', soql, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def run_bulk_query(instance_url: str, headers: dict, soql: str, report_meta: dict = None) -> str:
    api_version = settings.SALESFORCE_API_VERSION
    base_url = f"{instance_url}/services/data/v{api_version}/jobs/query"

    # 1️⃣ ジョブ作成
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
            error_text = job_res.text
            print(error_text)
        job_res.raise_for_status()

    job_id = job_res.json()["id"]
    print(f"[INFO] Job created: {job_id}")

    # 2️⃣ ジョブ完了待ち
    while True:
        status_res = requests.get(f"{base_url}/{job_id}", headers=headers)
        status_res.raise_for_status()
        state = status_res.json()["state"]
        if state in ("JobComplete", "Failed", "Aborted"):
            break
        time.sleep(5)

    if state != "JobComplete":
        print(f"[ERROR] Job ended with state: {state}")
        print(status_res.text)
        raise Exception("Bulk query job failed.")

    # 3️⃣ 結果CSVダウンロード (Bulk API 2.0)
    result_res = requests.get(f"{base_url}/{job_id}/results", headers=headers)
    result_res.raise_for_status()
    decoded = result_res.content.decode("utf-8")
    all_rows = list(csv.reader(io.StringIO(decoded)))

    # 4️⃣ ヘッダーを日本語ラベルに変換
    if report_meta and len(all_rows) > 0:
        base_object = _extract_base_object_from_soql(soql)
        print(f"[DEBUG] Base object: {base_object}")
        label_map = _build_column_label_map(report_meta, base_object)
        print(f"[DEBUG] CSV headers: {all_rows[0]}")
        print(f"[DEBUG] Label map: {label_map}")
        # マッチしなかったヘッダーを表示
        for h in all_rows[0]:
            if h.lower() not in label_map:
                print(f"[DEBUG] No match for: {h}")
        all_rows[0] = _convert_headers_to_labels(all_rows[0], label_map)

    # 5️⃣ 保存ディレクトリ作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{settings.OUTPUT_DIR}/{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # 6️⃣ SOQLをtxtファイルに保存
    soql_path = f"{output_dir}/query.txt"
    with open(soql_path, "w", encoding="utf-8") as f:
        f.write(soql)

    # 7️⃣ CSVファイルを保存
    csv_path = f"{output_dir}/result.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)
    print(f"[INFO] Saved CSV to {csv_path}")

    # 8️⃣ 再利用可能なembed.pyを生成
    embed_path = generate_embed_file(soql, output_dir)
    print(f"[INFO] Generated embed file: {embed_path}")

    # 9️⃣ proxy_embed.pyを生成
    proxy_embed_path = generate_proxy_embed_file(soql, output_dir)
    print(f"[INFO] Generated proxy embed file: {proxy_embed_path}")

    return output_dir
