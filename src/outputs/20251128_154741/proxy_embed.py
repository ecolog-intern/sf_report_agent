SOQL_QUERY = """SELECT
    Contractor_Information__r.Name,
    Contractor_Information__r.smart_customer_id__c,
    Name,
    plan_code__r.Name,
    Contractor_Information__r.parent_agency__c,
    Contractor_Information__r.account__c,
    Contractor_Information__r.sales_channel__c,
    Contractor_Information__r.customer_type__c,
    Contractor_Information__r.contractor_name__c,
    Contractor_Information__r.contractor_name_kana__c,
    Comp_Before_Switch__r.Name,
    current_gas_plam__c,
    supply_point_identification_no__c,
    customer_no__c,
    latest_billing_year_month__c,
    bill__c,
    usage_fee__c,
    billing_amount__c,
    discount_rate__c,
    Contractor_Information__r.payment_type__c,
    place_name__c,
    Contractor_Information__r.zip__c,
    Contractor_Information__r.contractor_address__c,
    Contractor_Information__r.request_date__c,
    Contractor_Information__r.atokaku_call_status__c,
    contract_confirmation_call_ok_date__c,
    Contractor_Information__r.latest_billing_month__c,
    Contractor_Information__r.Latest_payment_meyhod__c,
    cancel_date__c,
    cancel_confirmed_date__c,
    cancellation_date__c,
    cancel_reason__c,
    use_place_zip__c,
    use_place_address_connect__c,
    use_place_name__c,
    use_place_name_kana__c,
    matching_result__c,
    switching_request_ok_date__c,
    scheduled_switching_date__c,
    Contractor_Information__r.email__c,
    Contractor_Information__r.business_sector__c,
    Contractor_Information__r.business_sector_detail__c,
    Contractor_Information__r.fact_clct_date__c,
    Contractor_Information__r.representative_age__c,
    Contractor_Information__r.representative_brth__c,
    Contractor_Information__r.representative_country__c,
    Contractor_Information__r.representative_name__c,
    Contractor_Information__r.representative_name_kana__c,
    Contractor_Information__r.pic_name__c,
    Contractor_Information__r.pic_name_kana__c,
    Contractor_Information__r.pic_tel__c,
    Contractor_Information__r.shop_name__c,
    distinguish_place_tel__c,
    Contractor_Information__r.tel1_connect__c,
    use_place_tel_connect__c,
    Contractor_Information__r.tel2_connect__c,
    Contractor_Information__r.document_destination_name__c,
    Contractor_Information__r.document_destination_address_connect__c,
    remarks1__c,
    remarks2__c,
    remarks3__c,
    Contractor_Information__r.atokaku_comment__c,
    Contractor_Information__r.claim_linking_no__c,
    Contractor_Information__r.application_information__r.Name
FROM Gas_Contract__c
WHERE
    cancel_date__c = null
    AND cancel_confirmed_date__c = null
    AND cancel_cooperation_date__c = null
    AND cancel_reason__c = null
    AND forced_termination_date__c = null
    AND cancellation_date__c = null
    AND Compulsory_cancellation_date__c = null
    AND cancellation_confirmed_date__c = null
    AND Contractor_Information__r.parent_agency__c != '株式会社アイステーション（管理）'
    AND Contractor_Information__r.parent_agency__c != '株式会社アクセル（商品企画）'
    AND Contractor_Information__r.parent_agency__c != '株式会社ネクシィーズ'
    AND Contractor_Information__r.account__c != '株式会社ネクシィーズ'
    AND Contractor_Information__r.account__c != 'NUWORKS株式会社（テンポス）'
    AND Contractor_Information__r.account__c != 'NUWORKS株式会社(t)'
    AND Contractor_Information__r.account__c != '株式会社come up'
    AND Contractor_Information__r.Latest_payment_meyhod__c != 'コンビニ'
    AND Contractor_Information__r.Call_FLG__c = null
    AND Contractor_Information__r.parent_agency__c != '株式会社エコログ（SP）'
    AND Contractor_Information__r.parent_agency__c != 'EPARK（管理）'
    AND scheduled_switching_date__c >= 2025-09-01
    AND scheduled_switching_date__c < 2025-10-01
ORDER BY Contractor_Information__r.contractor_name__c ASC"""

import requests
import time
import csv
import io
import json
from datetime import datetime
import os
import pandas as pd
import winreg

'''
sfからオプションの数値を引っ張る
'''
class OptionIndex:
    def __init__(self, config):
        #sf関係
        self.sf_username = config.sf_username
        self.sf_password = config.sf_password
        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.sf_access_token_URL = config.sf_access_token_URL
        self.sf_report_unique = config.sf_report_unique
        self.api_version = config.api_version
        
        #オプション名
        self.option_sf_names = config.option_sf_names
        
        #代理店名
        self.agency_names = config.agency_names
        
        #proxy関係
        self.proxies = config.proxies
        self.MAX_RETRIES = config.MAX_RETRIES
        
        #soql取得
        soql_path = config.soql_path
        with open(soql_path, "r", encoding="utf-8") as f:
            self.soql = f.read()
            
        # output の csv のパス
        now = datetime.now()
        year = now.strftime("%Y年")          # 例: 2025
        month = now.strftime("%m月")         # 例: 01
        file_name = now.strftime("%m月%d日.csv")  # 例: 01月12日.csv

        base_dir = config.sf_folder_base_path
        year_dir = os.path.join(base_dir, year)
        month_dir = os.path.join(year_dir, month)

        # フォルダを自動作成
        os.makedirs(month_dir, exist_ok=True)

        # 完全パス
        self.output_csv_path = os.path.join(month_dir, file_name)
        
    def make_option_matrix(self, df_raw):
        """
        SF の生データ → 代理店 × OP の集計テーブルへ変換する。
        戻り値：
            index : 代理店名
            columns : 各OP数 + ALL付帯数 + ALL付帯率 + 各OP率
        """

        df = df_raw.copy()

        # 列抽出
        df = df[[
            "contractor_information__r.Payment_agency_name__c",
            "option_plan_code__r.Name"
        ]].rename(columns={
            "contractor_information__r.Payment_agency_name__c": "代理店名",
            "option_plan_code__r.Name": "オプション名"
        })

        # 代理店 × OP の件数集計
        pivot_df = (
            df.groupby(["代理店名", "オプション名"])
            .size()
            .unstack(fill_value=0)
        )

        # ALL付帯数
        pivot_df = pivot_df.reindex(self.agency_names, fill_value=0)
        pivot_df["ALL付帯数"] = pivot_df.sum(axis=1)

        # ALL付帯率（1.0になるか確認）
        pivot_df["ALL付帯率"] = (
            pivot_df["ALL付帯数"] / pivot_df["ALL付帯数"]
        ).replace([float('inf'), float('nan')], 0)

        # 整合性チェック：1.0 以外なら警告
        abnormal_rows = pivot_df[pivot_df["ALL付帯率"] != 1.0]
        if not abnormal_rows.empty:
            print(f"⚠【警告】ALL付帯率 ≠ 100% の代理店が{len(abnormal_rows)}件分あります")

        # OPの割合を計算
        for col in pivot_df.columns:
            if col in ["ALL付帯数", "ALL付帯率"]:
                continue
            pivot_df[f"{col}_率"] = (
                pivot_df[col] / pivot_df["ALL付帯数"]
            ).replace([float('inf'), float('nan')], 0)

        count_cols = [col for col in pivot_df.columns if not col.endswith("率")]
        rate_cols = [col for col in pivot_df.columns if col.endswith("率")]
        pivot_df = pivot_df[count_cols + rate_cols]

        return pivot_df

    def option_extract(self):
        '''
        実際の抽出処理
        sfのアクセストークンを取得して、sfのレポートを取得
        そのあと、dataframeを加工
        返り値はpandasのdataframeで縦軸が代理店名、横軸がALL付帯数、各オプション数、ALL付帯率、各オプション割合
        '''
        for attempt in range(1, self.MAX_RETRIES+1):
            try:
                # proxyエラー対策
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    for i in range(2):
                        # OFF
                        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
                        time.sleep(2)
                        # ON
                        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                        time.sleep(2)
                
                # 認証
                access_token, instance_url = self.authenticate_salesforce()
                print(f"[INFO] Connected to {instance_url}")

                # クエリ実行
                self.run_bulk_query(instance_url, access_token)
                self.df = pd.read_csv(self.output_csv_path)
                print(self.df)
                
            except Exception as e:
                print(f"❌ エラー発生（{attempt}回目）: {e}")

                if attempt < self.MAX_RETRIES:
                    print("🔁 再実行します...\n")
                else:
                    print("🚨 最大試行回数に達しました。プログラムを終了します。")
                    raise   # ここでエラーを投げて終了
                
            else:
                # try が一度も例外を出さずに完走したらここに来る
                print("✅ 処理成功！")
                return self.make_option_matrix(self.df)

    def authenticate_salesforce(self):
        """
        Salesforce OAuth2認証を行う

        Returns:
            (access_token, instance_url)
        """
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.sf_username,
            "password": self.sf_password
        }

        response = requests.post(self.sf_access_token_URL, data=payload, proxies=self.proxies)
        if response.status_code != 200:
            print("[ERROR] Salesforce authentication failed:")
            print(response.text)
            raise Exception(f"Salesforce authentication failed ({response.status_code})")

        data = response.json()
        return data["access_token"], data["instance_url"]


    def run_bulk_query(self, instance_url, access_token) -> list:
        """
        Bulk API 2.0でSOQLクエリを実行し、結果をリストで返す

        Args:
            instance_url: SalesforceインスタンスURL
            access_token: アクセストークン
            soql: SOQLクエリ（省略時は埋め込みクエリを使用）
            api_version: APIバージョン
            output_csv_path: CSV出力パス（省略時はタイムスタンプ付きで保存）

        Returns:
            CSVデータを2次元リストとして返す
        """
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        base_url = f"{instance_url}/services/data/v{self.api_version}/jobs/query"

        # 1. ジョブ作成
        payload = {
            "operation": "query",
            "query": self.soql,
            "contentType": "CSV"
        }

        job_res = requests.post(base_url, headers=headers, json=payload)

        if not job_res.ok:
            print("[ERROR] Job creation failed")
            print("Status:", job_res.status_code)
            try:
                error_text = json.dumps(job_res.json(), indent=2, ensure_ascii=False)
                print(error_text)
            except Exception:
                print(job_res.text)
            job_res.raise_for_status()

        job_id = job_res.json()["id"]
        print(f"[INFO] Job created: {job_id}")

        # 2. ジョブ完了待ち
        while True:
            status_res = requests.get(f"{base_url}/{job_id}", headers=headers)
            status_res.raise_for_status()
            state = status_res.json()["state"]
            print(f"[INFO] Job state: {state}")
            if state in ("JobComplete", "Failed", "Aborted"):
                break
            time.sleep(5)

        if state != "JobComplete":
            print(f"[ERROR] Job ended with state: {state}")
            print(status_res.text)
            raise Exception("Bulk query job failed.")

        # 3. 結果CSVダウンロード
        result_res = requests.get(f"{base_url}/{job_id}/results", headers=headers)
        result_res.raise_for_status()
        decoded = result_res.content.decode("utf-8")
        all_rows = list(csv.reader(io.StringIO(decoded)))

        print(f"[INFO] Retrieved {len(all_rows)} rows (including header)")

        # 4. CSV保存（パスが指定されている場合）
        self.save_to_csv(all_rows, self.output_csv_path)

    def save_to_csv(self, data, output_path):
        """
        データをCSVファイルに保存する

        Args:
            data: 2次元リストのデータ
            output_path: 出力ファイルパス
        """
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"[INFO] Saved to {output_path}")


# 使用例
if __name__ == "__main__":
    # 設定クラス（Config）を作成する
    class Config:
        def __init__(self):
            # Salesforce接続情報
            self.sf_username = "your_username@example.com"
            self.sf_password = "your_password"
            self.client_id = "your_client_id"
            self.client_secret = "your_client_secret"
            self.sf_access_token_URL = "https://login.salesforce.com/services/oauth2/token"
            self.sf_report_unique = "report_id"
            self.api_version = "62.0"
            
            # オプション名（Salesforce上のオプション名リスト）
            self.option_sf_names = ["オプションA", "オプションB", "オプションC"]
            
            # 代理店名リスト
            self.agency_names = ["代理店A", "代理店B", "代理店C"]
            
            # プロキシ設定
            self.proxies = {
                "http": "http://proxy.example.com:8080",
                "https": "http://proxy.example.com:8080"
            }
            self.MAX_RETRIES = 3
            
            # SOQL取得用のパス（このファイルではSOQL_QUERYを使用）
            # 注意: self.soql = SOQL_QUERY に書き換えることを推奨
            self.soql_path = "query.txt"  # または直接 SOQL_QUERY を使用
            
            # CSV出力先のベースパス
            self.sf_folder_base_path = "./output"
    
    # Configインスタンスを作成
    config = Config()
    
    # OptionIndexを実行
    option_index = OptionIndex(config)
    
    # オプションマトリックスを取得
    result_df = option_index.option_extract()
    print(result_df)
