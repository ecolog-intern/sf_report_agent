import re

def extract_soql(text: str) -> str:
    """
    Claude の出力から SOQL クエリ本文だけを抽出する。
    ```sql ... ``` で囲まれていればその中身、
    なければ先頭行から SELECT を探して末尾までを返す。
    """
    # ```sql``` ブロック検出
    match = re.search(r"```sql(.*?)```", text, flags=re.S)
    if match:
        soql = match.group(1).strip()
    elif re.search(r"(SELECT[\s\S]*)", text, flags=re.I):
        # SELECT～の行を検出
        match = re.search(r"(SELECT[\s\S]*)", text, flags=re.I)
        soql = match.group(1).strip()
    else:
        # fallback
        soql = text.strip()

    # Bulk API用の構文変換
    soql = _convert_to_bulk_api_syntax(soql)

    return soql


def _convert_to_bulk_api_syntax(soql: str) -> str:
    """
    Bulk APIで認識されない構文を変換する
    """
    # IS NULL → = null
    soql = re.sub(r'\bIS\s+NULL\b', '= null', soql, flags=re.IGNORECASE)

    # IS NOT NULL → != null
    soql = re.sub(r'\bIS\s+NOT\s+NULL\b', '!= null', soql, flags=re.IGNORECASE)

    return soql
