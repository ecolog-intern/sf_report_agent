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
        return match.group(1).strip()

    # SELECT～の行を検出
    match = re.search(r"(SELECT[\s\S]*)", text, flags=re.I)
    if match:
        return match.group(1).strip()

    # fallback
    return text.strip()
