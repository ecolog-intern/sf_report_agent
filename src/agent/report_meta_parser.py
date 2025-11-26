'''
構造化データを自然言語化
'''

def report_meta_to_text(report_meta: dict) -> str:
    """Salesforce report_metaを自然言語テキスト化する（RAG入力用）"""
    lines = []
    if "name" in report_meta:
        lines.append(f"レポート名: {report_meta['name']}")
    if "reportType" in report_meta:
        rt = report_meta["reportType"]
        lines.append(f"レポートタイプラベル: {rt.get('label', '')}")
        # レポートタイプIDは使用禁止であることを明示
        lines.append(f"レポートタイプID: {rt.get('type', '')} ※これはFROM句に使用禁止")

    # 表示項目から実際のsObject名を抽出
    if "detailColumns" in report_meta:
        cols = ", ".join(report_meta["detailColumns"])
        lines.append(f"表示項目: {cols}")

        # オブジェクト名を抽出
        object_names = set()
        for col in report_meta["detailColumns"]:
            parts = col.split(".")
            if len(parts) >= 2 and parts[0].endswith("__c"):
                object_names.add(parts[0])

        if object_names:
            lines.append(f"FROM句に使用可能なオブジェクト: {', '.join(sorted(object_names))}")

    if "reportFilters" in report_meta:
        lines.append("フィルタ条件:")
        for i, f in enumerate(report_meta["reportFilters"], 1):
            lines.append(f"  {i}. {f['column']} {f['operator']} {f['value']}")
    if "reportBooleanFilter" in report_meta:
        lines.append(f"フィルタ論理式: {report_meta['reportBooleanFilter']}")
    if "sortBy" in report_meta:
        lines.append(f"ソート条件: {report_meta['sortBy']}")
    return "\n".join(lines)
