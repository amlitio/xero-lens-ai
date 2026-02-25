import requests
from typing import Dict, Any, Optional

XERO_API_BASE = "https://api.xero.com/api.xro/2.0"

class XeroClient:
    """
    Production-safe wrapper for Xero Accounting API calls.
    Requires:
      - valid access_token
      - tenant_id (xero-tenant-id header)
    """

    def __init__(self, access_token: str, tenant_id: str):
        self.access_token = access_token
        self.tenant_id = tenant_id

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "xero-tenant-id": self.tenant_id,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_invoice_by_number(self, invoice_number: str) -> Dict[str, Any]:
        # Uses InvoiceNumbers query param (preferred) or where filter in some cases
        url = f"{XERO_API_BASE}/Invoices"
        params = {"InvoiceNumbers": invoice_number}
        r = requests.get(url, headers=self._headers(), params=params, timeout=30)
        r.raise_for_status()
        return r.json()

    def create_draft_invoice_accrec_tax_exempt(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        payload should already include:
          Type=ACCREC
          Status=DRAFT
          InvoiceNumber=FieldTicketNumber
          LineItems with TaxType=NONE
        """
        url = f"{XERO_API_BASE}/Invoices"
        body = {"Invoices": [payload]}
        r = requests.post(url, headers=self._headers(), json=body, timeout=30)
        r.raise_for_status()
        return r.json()

    def attach_pdf_to_invoice(self, invoice_id: str, filename: str, pdf_bytes: bytes) -> None:
        url = f"{XERO_API_BASE}/Invoices/{invoice_id}/Attachments/{filename}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "xero-tenant-id": self.tenant_id,
            "Content-Type": "application/pdf",
        }
        r = requests.post(url, headers=headers, data=pdf_bytes, timeout=60)
        r.raise_for_status()
