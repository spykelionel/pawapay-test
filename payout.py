import requests
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

url = os.getenv('PAWAPAY_PAYOUT_URL', "https://api.sandbox.pawapay.io/payouts")
token = os.getenv('PAWAPAY_API_TOKEN')

# Generate a UUID for the payout
payout_uuid = str(uuid.uuid4())

payload = {
    "payoutId": payout_uuid,
    "amount": "15",
    "currency": "XAF",  # Cameroon currency
    "country": "CMR",   # Cameroon country code
    "correspondent": "MTN_MOMO_CMR",  # Cameroon correspondent
    "recipient": {
        "type": "MSISDN",
        "address": {"value": "237677777777"}  # Cameroon phone number
    },
    "customerTimestamp": "2025-05-31T17:32:28Z",
    "statementDescription": "Order Payout 12345",
    "metadata": [
        {
            "fieldName": "orderId",
            "fieldValue": "ORD-123456789"
        },
        {
            "fieldName": "customerId",
            "fieldValue": "customer@email.com",
            "isPII": True
        }
    ]
}
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text) 