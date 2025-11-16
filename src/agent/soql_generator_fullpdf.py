import json
from langchain_anthropic import ChatAnthropic
from config.settings import settings
from langchain_community.document_loaders import PyPDFLoader
from agent.report_meta_parser import report_meta_to_text

def generate_soql_with_full_pdf(report_meta: dict) -> str:
    """ClaudeにPDF全文を渡してSOQLを生成する"""

    # ① report_metaを自然言語化
    query_text = report_meta_to_text(report_meta)

    # ② PDF全文を読み込む
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

    # プロンプト定義
    prompt = f"""
あなたはSalesforceのSOQL専門家です。
次のSalesforceレポート定義を、Salesforce Bulk APIで実行可能なSOQLクエリに変換してください。

構文や演算子、日付リテラルなどは、下記の「SOQLリファレンス全文」を参考にしてください。
出力はSOQLクエリ本文のみを返してください。

回答の中でsqlは
```sql

```

で囲んでください
【レポート定義】
{query_text}

【SOQLリファレンス全文】
{full_text}
"""

    response = llm.invoke(prompt)
    return response.content.strip()
