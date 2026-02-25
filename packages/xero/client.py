import requests
import os

XERO_API = "https://api.xero.com/api.xro/2.0"

class XeroClient:

    def __init__(self, token, tenant_id):
        self.token = token
        self.tenant_id = tenant_id

    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Xero-tenant-id": self.tenant_id,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_invoices(self):
        r = requests.get(
            f"{XERO_API}/Invoices",
            headers=self.headers()
        )
        return r.json()
