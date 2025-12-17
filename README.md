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

    llmが作成したqueryによって作成したcsvはコンソールから作成したcsvと異なることがあるので、一致不一致を確かめる

    1. salesforceのレポートを手動でエクスポートする
        - 詳細のみ
        - 形式 カンマ区切り形式(.csv)
        - 文字コード Unicode(UTF-8)

    2. checker/inputs/にcsvを2つコピーする(名前変更はしなくてもいい)
        - 先ほどエクスポートしたcsvをそのままコピー
        - src/outputs/{時間}/result.csvをコピー

    3. ルート直下でdocker composeを実行
    ```bash
    docker compose -f docker-compose.checker.yml up --build
    ```

    4. 実行結果のログを確認

    カラムの一致とdataframeのshapeの一致度を確かめている
    ```bash
    checker-1  | Columns match: ⭕️
    checker-1  | Shape match: ⭕️
    ```
    ログの最後がこうなったら検証成功
    
    バツが表示された場合は差分を確認する



5. 自分のプログラムに組み込む
    - 光ネットワーク下で使用する場合は`proxy_embed.py`を流用する
    - それ以外は`embed.py`を流用する
    - プログラムでの使い方は各ファイルの最後に記載した使用例をもとにアレンジ加えて

    関数の使い方はembed.pyの最後を参照に
