---
name: sf-report
description: SalesforceレポートIDと手動エクスポートCSVのパスを受け取り、Bulk API経由でデータ取得・検証を自動実行するスキル
---

# Salesforce Bulk Report スキル (sf-report)

このスキルは、ユーザーから `SALESFORCE_REPORT_ID` と手動エクスポートCSVのファイルパスを受け取り、READMEの手順に従ってBulk API実行 → 結果検証を自動で行います。


---

## ステップ1: 情報の受領

以下をユーザーから受け取ってください：

- **SALESFORCE_REPORT_ID**（例: `00OQ9000006ST3dMAG`）
- **手動エクスポートCSVの絶対パス**（例: `/Users/shimizukanon/Downloads/kanon.csv`）
  - Salesforceレポートから「詳細のみ・カンマ区切り・UTF-8」でエクスポートしたCSVファイルの絶対パスを指定してもらう
  - ファイル名だけでなく `/Users/...` から始まるフルパスで指定すること

両方揃ったら次のステップへ進んでください。

---

## ステップ2: .env の SALESFORCE_REPORT_ID を更新する

`sf_report_agent/.env` の `SALESFORCE_REPORT_ID=` の行を、受け取ったIDに書き換えてください。

Edit ツールを使って該当行のみを変更してください。

---

## ステップ3: checker/inputs/ を準備する

ユーザーが指定したCSVファイルパスから `checker/inputs/` にコピーしてください。

```bash
cp "<ユーザー指定のCSVパス>" /sf_report_agent/checker/inputs/manual_export.csv
```

---

## ステップ4: Docker を起動する

Docker Desktop が起動していない場合は起動してください。

```bash
open -a Docker
```

Docker デーモンが Ready になるまで待機してください。

```bash
until docker info > /dev/null 2>&1; do sleep 1; done
echo "Docker is ready"
```

---

## ステップ5: Bulk Agent を実行する

以下のコマンドをプロジェクトルートで実行します：

```bash
cd sf_report_agent && docker-compose up --abort-on-container-exit --exit-code-from bulk-agent
```

実行完了後、`src/outputs/` 配下に最新のタイムスタンプディレクトリが作成されます。

---

## ステップ6: result.csv を checker/inputs/ にコピーする

`src/outputs/` 内の `result.csv` を `checker/inputs/` にコピーしてください。

```bash
LATEST=$(ls -td /sf_report_agent/src/outputs/*/ | grep -v '__pycache__' | head -1)
cp "${LATEST}result.csv"  sf_report_agent/checker/inputs/result.csv
```

---

## ステップ7: Checker を実行する

```bash
cd /sf_report_agent && docker compose -f docker-compose.checker.yml up --build
```

---

## ステップ8: 結果を報告する

Checker のログから以下の行を確認し、ユーザーに報告してください：

```
checker-1  | Columns match: ⭕️ または ❌
checker-1  | Shape match: ⭕️ または ❌
```

- 両方 ⭕️ → 検証成功。`src/outputs/{datetime}/` に生成されたファイル一覧（query.txt, result.csv, embed.py, proxy_embed.py, report_meta.json）をユーザーに伝えてください。
- ❌ が含まれる → 差分の詳細をログから読み取ってユーザーに報告してください。

---

## ステップ9: 後片付け

`checker/inputs/` 内の CSV ファイルをすべて削除してください（`__init__.py` は残す）。

`src/outputs/`内のファイルを全て削除してください。
（`__init__.py` は残す）。

```bash
rm -f /sf_report_agent/checker/inputs/*.csv
```

---

## 注意事項

- ステップ5のdocker-compose実行前に、必ずステップ2の `.env` 更新とステップ4のDocker起動が完了していることを確認すること
- `checker/inputs/` には CSV が2つ存在する状態にすること（手動エクスポート + result.csv）
- エラーが発生した場合はログを読み取り、原因をユーザーに報告してから次の対応を相談すること
