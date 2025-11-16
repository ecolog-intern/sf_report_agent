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
        lines.append(f"レポートタイプ: {rt.get('label', '')}（オブジェクト: {rt.get('type', '')}）")
    if "detailColumns" in report_meta:
        cols = ", ".join(report_meta["detailColumns"])
        lines.append(f"表示項目: {cols}")
    if "reportFilters" in report_meta:
        lines.append("フィルタ条件:")
        for i, f in enumerate(report_meta["reportFilters"], 1):
            lines.append(f"  {i}. {f['column']} {f['operator']} {f['value']}")
    if "reportBooleanFilter" in report_meta:
        lines.append(f"フィルタ論理式: {report_meta['reportBooleanFilter']}")
    if "sortBy" in report_meta:
        lines.append(f"ソート条件: {report_meta['sortBy']}")
    return "\n".join(lines)
