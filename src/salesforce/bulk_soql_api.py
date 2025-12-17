'''
llmが作成したsoqlを使用して、bulkapiを叩く
'''

import requests
import time
import csv
import io
import os
import re
import zipfile
from config.settings import settings
from datetime import datetime
import json


def generate_embed_file(soql: str, output_dir: str, report_meta: dict = None) -> str:
    """
    SOQLとreport_metaを埋め込んだ再利用可能なBulk API実行ファイルを生成する
    """
    template_path = os.path.join(os.path.dirname(__file__), "embed_template.py")
    with open(template_path, "r", encoding="utf-8") as f:
        user_code = f.read()

    escaped_soql = soql.replace('"""', '\\"\\"\\"')

    # report_metaをJSON文字列として埋め込む
    if report_meta:
        meta_json = json.dumps(report_meta, ensure_ascii=False, indent=2)
        content = f'SOQL_QUERY = """{escaped_soql}"""\n\nREPORT_META = {meta_json}\n\n{user_code}'
    else:
        content = f'SOQL_QUERY = """{escaped_soql}"""\n\nREPORT_META = None\n\n{user_code}'

    file_path = f"{output_dir}/embed.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def generate_proxy_embed_file(soql: str, output_dir: str, report_meta: dict = None) -> str:
    """
    SOQLとreport_metaを埋め込んだproxy_embed.pyを生成する
    """
    template_path = os.path.join(os.path.dirname(__file__), "proxy_embed_template.py")
    with open(template_path, "r", encoding="utf-8") as f:
        user_code = f.read()

    escaped_soql = soql.replace('"""', '\\"\\"\\"')

    # report_metaをJSON文字列として埋め込む
    if report_meta:
        meta_json = json.dumps(report_meta, ensure_ascii=False, indent=2)
        content = f'SOQL_QUERY = """{escaped_soql}"""\n\nREPORT_META = {meta_json}\n\n{user_code}'
    else:
        content = f'SOQL_QUERY = """{escaped_soql}"""\n\nREPORT_META = None\n\n{user_code}'

    file_path = f"{output_dir}/proxy_embed.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def _build_soql_to_label_map(report_meta: dict, soql: str) -> dict:
    """
    SOQLのSELECTフィールドとdetailColumnsを順番にマッピングして、
    SOQLフィールド名→日本語ラベルの辞書を構築する

    Bulk APIはSELECT句の順序を保持しないが、フィールド名は保持されるため、
    SOQLフィールド名をキーにしてラベルを取得する

    Args:
        report_meta: レポートメタデータ（detailColumns, detailColumnInfoを含む）
        soql: 実行されたSOQLクエリ

    Returns:
        SOQLフィールド名（小文字）をキー、日本語ラベルを値とする辞書
    """
    label_map = {}
    detail_column_info = report_meta.get("detailColumnInfo", {})
    detail_columns = report_meta.get("detailColumns", [])

    # SOQLからSELECT句のフィールドを抽出
    select_match = re.search(r'SELECT\s+([\s\S]+?)\s+FROM', soql, re.IGNORECASE)
    soql_fields = []
    if select_match:
        fields_str = select_match.group(1)
        soql_fields = [f.strip() for f in fields_str.split(',')]

    # SOQLフィールドとdetailColumnsを順番にマッピング
    if len(soql_fields) == len(detail_columns):
        for soql_field, detail_col in zip(soql_fields, detail_columns):
            if detail_col in detail_column_info:
                label = detail_column_info[detail_col].get("label", detail_col)
                label_map[soql_field.lower()] = label

    return label_map


def _convert_headers_by_soql_mapping(headers_row: list, label_map: dict) -> list:
    """
    CSVヘッダー行をSOQLフィールド名に基づいて日本語ラベルに変換する

    Args:
        headers_row: CSVのヘッダー行（API名のリスト）
        label_map: SOQLフィールド名（小文字）→ラベルのマッピング

    Returns:
        日本語ラベルに変換されたヘッダー行
    """
    result = []
    for h in headers_row:
        h_lower = h.lower()
        if h_lower in label_map:
            result.append(label_map[h_lower])
        else:
            # フォールバック: 元のヘッダー名を使用
            result.append(h)
    return result


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
        print(f"[DEBUG] CSV headers: {all_rows[0]}")
        label_map = _build_soql_to_label_map(report_meta, soql)
        print(f"[DEBUG] Label map keys: {list(label_map.keys())}")
        all_rows[0] = _convert_headers_by_soql_mapping(all_rows[0], label_map)

    # 5️⃣ 保存ディレクトリ作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{settings.OUTPUT_DIR}/{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # 6️⃣ SOQLをtxtファイルに保存
    soql_path = f"{output_dir}/query.txt"
    with open(soql_path, "w", encoding="utf-8") as f:
        f.write(soql)

    # 6.5️⃣ report_metaをJSONファイルに保存
    if report_meta:
        meta_path = f"{output_dir}/report_meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(report_meta, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Saved report meta to {meta_path}")

    # 7️⃣ CSVファイルを保存
    csv_path = f"{output_dir}/result.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)
    print(f"[INFO] Saved CSV to {csv_path}")

    # 8️⃣ 再利用可能なembed.pyを生成（report_metaも埋め込み）
    embed_path = generate_embed_file(soql, output_dir, report_meta)
    print(f"[INFO] Generated embed file: {embed_path}")

    # 9️⃣ proxy_embed.pyを生成（report_metaも埋め込み）
    proxy_embed_path = generate_proxy_embed_file(soql, output_dir, report_meta)
    print(f"[INFO] Generated proxy embed file: {proxy_embed_path}")

    return output_dir
