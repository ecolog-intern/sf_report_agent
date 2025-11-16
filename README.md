# Salesforce Bulk Agent

SalesforceレポートからSOQLを自動生成し、Bulk API 2.0でデータを取得するツール

## ローカル環境構築
1. .envファイルをルート直下に配置
2. dockerで起動
```bash
# .envファイルを設定後
docker-compose up --build
```

## Output

実行後、`src/outputs/{datetime}/` に以下が生成されます：

- **query.txt** - 実行されたSOQLクエリ
- **result.csv** - クエリ結果データ
- **embed.py** - 再利用可能なBulk API実行ファイル

embed.pyには実際のsqlを織り込んだpythonファイルが出力されるので、それをそのまま自分のプログラムに貼り付ける

関数の使い方はembed.pyの最後を参照に

## 技術詳細

1. **レポート定義取得** - Salesforce REST APIでレポートメタデータを取得
2. **SOQL自動生成** - Claude APIでレポート定義からSOQLを生成
3. **エラー自動修正** - Bulk APIエラー時にLLMが最大3回までSOQLを修正
4. **データ取得** - Bulk API 2.0で大量データを効率的に取得
5. **成果物生成** - 結果CSV、クエリ、再利用可能なPythonファイルを出力
