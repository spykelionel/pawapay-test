import requests
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API token and URL from environment variables
url = os.getenv('PAWAPAY_API_URL', "https://api.sandbox.pawapay.io/deposits")
token = os.getenv('PAWAPAY_API_TOKEN')

# Generate a UUID for the deposit
deposit_uuid = str(uuid.uuid4())

payload = {
    "depositId": deposit_uuid,
    "amount": "50",
    "currency": "XAF",
    "country": "CMR",
    "correspondent": "MTN_MOMO_CMR",
    "payer": {
        "type": "MSISDN",
        "address": {"value": "237651321911"}
    },
    "customerTimestamp": "2020-02-21T17:32:28Z",
    "statementDescription": "Note of 4 to 22 chars",
    "preAuthorisationCode": "1234567890",
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