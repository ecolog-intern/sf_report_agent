"""
SOQLエラー修正エージェント
Bulk APIのエラーを解析し、LLMでSOQLを修正する
RAGを使用して関連ドキュメントのみを取得
"""

from langchain_anthropic import ChatAnthropic
from config.settings import settings
from agent.soql_checker import extract_soql
from agent.soql_vectorstore import search_relevant_docs


def fix_soql_with_error(soql: str, error_message: str) -> str:
    """
    エラーメッセージを基にSOQLを修正する（RAG使用）

    Args:
        soql: 元のSOQLクエリ
        error_message: Bulk APIから返されたエラーメッセージ

    Returns:
        修正されたSOQLクエリ
    """

    # Claudeモデル設定
    llm = ChatAnthropic(
        model=settings.ANTHROPIC_MODEL_NAME,
        temperature=0,
        api_key=settings.ANTHROPIC_API_KEY
    )

    # エラーメッセージを自然言語化して検索クエリを生成
    search_query = _generate_search_query(llm, error_message)
    print(f"検索クエリ: {search_query}")

    # 自然言語化したクエリで関連ドキュメントを検索（RAG）
    print(f"関連ドキュメントを検索中...")
    relevant_docs = search_relevant_docs(search_query, k=1)
    context = "\n\n---\n\n".join(relevant_docs)
    print(f"取得したドキュメント数: {len(relevant_docs)}")
    print(f"コンテキストサイズ: {len(context)} 文字")

    # 検索結果を全て表示
    print("\n===== 検索されたドキュメント =====")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"\n--- ドキュメント {i} ---")
        print(doc)
    print("\n===== 検索結果終了 =====\n")

    # エラー修正用プロンプト
    prompt = f"""
あなたはSalesforceのSOQL専門家です。
以下のSOQLクエリはBulk APIで実行時にエラーが発生しました。
エラーメッセージを分析し、修正したSOQLを生成してください。

【元のSOQL】
{soql}

【エラーメッセージ】
{error_message}

【関連SOQLドキュメント（エラーに関連する情報）】
{context}

【修正のポイント】
1. エラーメッセージの内容を注意深く分析してください
2. 特に以下の点に注意:
   - カスタムリレーションシップは '__r' を使用（例: Account__r.Name）
   - 親オブジェクトへの参照は正しいリレーション名を使用
   - フィールドパスが正しいか確認
3. Bulk APIで実行可能な構文を使用してください

【超重要：Bulk API固有の構文ルール】
Bulk APIでは通常のSOQLと異なる構文が必要です：

1. NULL比較:
   - IS NULL → = null に変更
   - IS NOT NULL → != null に変更
   例: cancel_date__c IS NULL → cancel_date__c = null

2. 相対日付リテラル:
   - LAST_N_MONTHS:N, LAST_N_DAYS:N などは使用不可
   - 実日付に展開して使用
   例: = LAST_N_MONTHS:2 → >= 2025-09-01 AND < 2025-10-01

3. 日付リテラルの書式:
   - 日付リテラルはクォートで囲まない
   - 正しい: field >= 2025-11-01 ✓
   - 間違い: field >= '2025-11-01' ❌（クォートで囲むとエラー）

修正したSOQLクエリのみを以下の形式で返してください：
```sql
修正されたSOQL
```
"""

    response = llm.invoke(prompt)
    fixed_soql = extract_soql(response.content.strip())

    return fixed_soql


def _generate_search_query(llm, error_message: str) -> str:
    """
    LLMを使ってエラーメッセージを検索クエリに変換する
    """
    prompt = f"""
以下のSOQLエラーメッセージを分析し、エラーの核心を表す重要なキーワードを3つだけ抽出してください。

【エラーメッセージ】
{error_message}

【出力形式】
最も重要なキーワードを3つだけ、スペース区切りで出力してください。

キーワード3つのみを出力してください（説明は不要）:
"""

    response = llm.invoke(prompt)
    return response.content.strip()
