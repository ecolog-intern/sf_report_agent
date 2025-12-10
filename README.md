# Salesforce Bulk Agent

SalesforceレポートからSOQLを自動生成し、Bulk API 2.0でデータを取得するツール

## 使用方法
1. `.env`をルート直下に配置

    内容は基本的に使い回しで、`SALESFORCE_REPORT_ID`のみ取得したいレポートのIDに変える


2. dockerで起動
```bash
# .envファイルを設定後
docker-compose up --abort-on-container-exit --exit-code-from bulk-agent
```

3. 実行後、`src/outputs/{datetime}/` に以下が生成されます：

- **query.txt** - 実行されたSOQLクエリ
- **result.csv** - クエリ結果データ
- **embed.py** - 再利用可能なBulk API実行ファイル
- **proxy_embed.py** - proxy環境で実行するためのBulk API実行ファイル
- **report_meta.json** - レポートのメタ情報をまとめたjson

4. 生成されたcsvの検証

    実際のcsvをsalesforceで作成したレポートを比較して、レコード数に差がないかを確認する

    差があった場合は、`query.txt`のクエリに修正をかける

5. 自分のプログラムに組み込む
- 光ネットワーク下で使用する場合は`proxy_embed.py`を流用する
- それ以外は`embed.py`を流用する
- プログラムでの使い方は各ファイルの最後に記載した使用例をもとにアレンジ加えて

関数の使い方はembed.pyの最後を参照に
