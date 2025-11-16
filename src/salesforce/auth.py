'''
oauthトークン取得
'''

import requests
from config.settings import settings

class SalesforceAuth:
    def __init__(self):
        self.client_id = settings.SALESFORCE_CLIENT_ID
        self.client_secret = settings.SALESFORCE_CLIENT_SECRET
        self.username = settings.SALESFORCE_USERNAME
        self.password = settings.SALESFORCE_PASSWORD
        self.access_token_url = settings.SALESFORCE_ACCESSTOKEN_URL

    def authenticate(self):
        #アクセストークンを取得
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password
        }
        
        response = requests.post(self.access_token_url, data=data)
        if response.status_code != 200:
            print("[ERROR] Salesforce authentication failed:")
            print(response.text)
            raise Exception(f"Salesforce authentication failed ({response.status_code})")

        auth_data = response.json()
        access_token = auth_data["access_token"]
        instance_url = auth_data["instance_url"]

        print("[INFO] Salesforce authentication successful.")
        return access_token, instance_url