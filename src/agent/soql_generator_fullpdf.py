import json
from datetime import date
from dateutil.relativedelta import relativedelta
from langchain_anthropic import ChatAnthropic
from config.settings import settings
from langchain_community.document_loaders import PyPDFLoader
from agent.report_meta_parser import report_meta_to_text


def _get_date_info() -> str:
    """現在日付と相対日付の計算情報を生成"""
    today = date.today()

    # 各相対日付の計算
    date_info = f"""
【現在日付情報】
今日: {today.strftime('%Y-%m-%d')}
今月初日: {today.replace(day=1).strftime('%Y-%m-%d')}
今月末日: {(today.replace(day=1) + relativedelta(months=1) - relativedelta(days=1)).strftime('%Y-%m-%d')}

先月初日: {(today.replace(day=1) - relativedelta(months=1)).strftime('%Y-%m-%d')}
先月末日: {(today.replace(day=1) - relativedelta(days=1)).strftime('%Y-%m-%d')}

2ヶ月前初日: {(today.replace(day=1) - relativedelta(months=2)).strftime('%Y-%m-%d')}
2ヶ月前末日: {(today.replace(day=1) - relativedelta(months=1) - relativedelta(days=1)).strftime('%Y-%m-%d')}

3ヶ月前初日: {(today.replace(day=1) - relativedelta(months=3)).strftime('%Y-%m-%d')}
3ヶ月前末日: {(today.replace(day=1) - relativedelta(months=2) - relativedelta(days=1)).strftime('%Y-%m-%d')}
"""
    return date_info


def generate_soql_with_full_pdf(report_meta: dict) -> str:
    """ClaudeにPDF全文を渡してSOQLを生成する"""

    # report_metaを自然言語化
    query_text = report_meta_to_text(report_meta)
    print(query_text)

    # 現在日付情報を取得
    date_info = _get_date_info()

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

【最重要：必ず従うべきSOQL構文ルール】

1. FROM句のオブジェクト選択:
   - レポートタイプID（TC_OP__c, TC_TDC__c, TC_TGC__c等）は絶対に使用禁止
   - 表示項目の「ObjectName__c.FieldName__c」から実際のsObject名を特定する
   - 複数オブジェクトがある場合、子オブジェクト（詳細データを持つ側）をFROM句に使用する

2. SELECT句のフィールド参照（FROM句のオブジェクトを基準に）:
   - FROM句のオブジェクト自身のフィールド → プレフィックスなしで記述
   - 親オブジェクトのフィールド → ObjectName__c を ObjectName__r に変更
   - ルックアップフィールド経由の参照 → field__c を field__r に変更

   【超重要：カスタムルックアップフィールド経由の参照】
   親オブジェクトへの参照は、オブジェクト名ではなく、ルックアップフィールド名を使用する。

   例: OptionObject__c から Electrical_Contract__c への参照
   - レポート定義: OptionObject__c.denki_contract_id__c (これがルックアップフィールド)
   - 正しい: denki_contract_id__r.Name ✓
   - 間違い: Electrical_Contract__r.Name ❌（このリレーション名は存在しない）

   例: OptionObject__c から Contractor_Information__c への参照
   - ルックアップフィールドが denki_contract_id__c の場合
   - 正しい: denki_contract_id__r.Contractor_Information__r.Name ✓
   - 間違い: Electrical_Contract__r.Contractor_Information__r.Name ❌

3. WHERE句・ORDER BY句:
   - FROM句のオブジェクトを基準に、上記と同じルールでフィールドを参照

4. 【超重要：OR と AND の優先順位】
   SOQLでは AND が OR より優先されます。複数の OR 条件がある場合は必ず括弧で囲んでください。

   正しい書き方:
   - (field LIKE '%A%' OR field LIKE '%B%') AND other_field = null ✓

   間違い（意図しない結果になる）:
   - field LIKE '%A%' OR field LIKE '%B%' AND other_field = null ❌
     → これは field LIKE '%A%' OR (field LIKE '%B%' AND other_field = null) と解釈される

5. 【超重要：NULL比較の構文（Bulk API）】
   Bulk APIでは「IS NULL」「IS NOT NULL」は使用できません。
   必ず「= null」「!= null」を使用してください。

   正しい書き方:
   - cancel_date__c = null ✓
   - cancel_date__c != null ✓
   - cancel_date__c IS NULL ❌（Bulk APIで認識されない）
   - cancel_date__c IS NOT NULL ❌（Bulk APIで認識されない）

   例: 「cancel_date__c equals 」（空値）は
   → cancel_date__c = null

6. 【超重要：相対日付フィルタの変換ルール】
   Bulk APIでは相対日付リテラル（LAST_N_MONTHS:N等）が認識されない場合があります。
   そのため、必ず実日付に展開してクエリを作成してください。

   相対日付表現の変換方法:
   - 「Nか月前」または「N月前」→ Nヶ月前の月の初日から末日までの範囲
     例: 「2か月前」で今日が11/17の場合 → 9/1〜9/30
     → field >= 2025-09-01 AND field < 2025-10-01

   - 「先月」→ 先月の初日から末日まで
   - 「今月」→ 今月の初日から末日まで

   正しい書き方（Bulk API対応）:
   - scheduled_switching_date__c >= 2025-09-01 AND scheduled_switching_date__c < 2025-10-01 ✓
   - scheduled_switching_date__c = LAST_N_MONTHS:2 ❌（Bulk APIで認識されない可能性）

   例: 「scheduled_switching_date__c equals 2か月前」は
   → scheduled_switching_date__c >= 2025-09-01 AND scheduled_switching_date__c < 2025-10-01

7. 【超重要：日付リテラルの書式（Bulk API）】
   Bulk APIでは日付リテラルをクォートで囲んではいけません。

   正しい書き方:
   - field >= 2025-11-01 ✓
   - field < 2025-12-01 ✓

   間違い:
   - field >= '2025-11-01' ❌（クォートで囲むとエラー）
   - field < '2025-12-01' ❌

{date_info}

回答の中でsqlは
```sql

```

で囲んでください

【レポート定義】
{query_text}
"""

    response = llm.invoke(prompt)
    return response.content.strip()
