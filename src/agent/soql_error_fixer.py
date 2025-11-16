"""
SOQLエラー修正エージェント
Bulk APIのエラーを解析し、LLMでSOQLを修正する
"""

from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import PyPDFLoader
from config.settings import settings
from agent.soql_checker import extract_soql


def fix_soql_with_error(soql: str, error_message: str) -> str:
    """
    エラーメッセージを基にSOQLを修正する

    Args:
        soql: 元のSOQLクエリ
        error_message: Bulk APIから返されたエラーメッセージ

    Returns:
        修正されたSOQLクエリ
    """

    # PDF全文を読み込む（リファレンス用）
    pdf_path = "agent/docs/salesforce_soql_document.pdf"
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    full_text = "\n\n".join([d.page_content for d in docs])

    # Claudeモデル設定
    llm = ChatAnthropic(
        model=settings.ANTHROPIC_MODEL_NAME,
        temperature=0,
        api_key=settings.ANTHROPIC_API_KEY
    )

    # エラー修正用プロンプト
    prompt = f"""
あなたはSalesforceのSOQL専門家です。
以下のSOQLクエリはBulk APIで実行時にエラーが発生しました。
エラーメッセージを分析し、修正したSOQLを生成してください。

【元のSOQL】
{soql}

【エラーメッセージ】
{error_message}

【SOQLリファレンス全文】
{full_text}

【修正のポイント】
1. エラーメッセージの内容を注意深く分析してください
2. 特に以下の点に注意:
   - カスタムリレーションシップは '__r' を使用（例: Account__r.Name）
   - 親オブジェクトへの参照は正しいリレーション名を使用
   - フィールドパスが正しいか確認
3. Bulk APIで実行可能な構文を使用してください

修正したSOQLクエリのみを以下の形式で返してください：
```sql
修正されたSOQL
```
"""

    response = llm.invoke(prompt)
    fixed_soql = extract_soql(response.content.strip())

    return fixed_soql
