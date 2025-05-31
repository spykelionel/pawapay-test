import requests
import uuid
import os
from dotenv import load_dotenv
from order_manager import OrderManager, OrderStatus

# Load environment variables from .env file
load_dotenv()

# Get API token and URL from environment variables
url = os.getenv('PAWAPAY_API_URL', "https://api.sandbox.pawapay.io/deposits")
token = os.getenv('PAWAPAY_API_TOKEN')

# Initialize order manager
order_manager = OrderManager()

def create_payment_request(order):
    """Create a payment request for an order"""
    # Generate a UUID for the deposit
    deposit_uuid = str(uuid.uuid4())
    
    # Update order with deposit ID
    order.deposit_id = deposit_uuid
    
    payload = {
        "depositId": deposit_uuid,
        "amount": str(order.total_amount),
        "currency": order.currency,
        "country": "CMR",
        "correspondent": "MTN_MOMO_CMR",
        "payer": {
            "type": "MSISDN",
            "address": {"value": "237677777777"}
        },
        "customerTimestamp": order.created_at.isoformat(),
        "statementDescription": f"Order {order.order_id.replace('-', ' ')}",
        "preAuthorisationCode": "1234567890",
        "metadata": [
            {
                "fieldName": "orderId",
                "fieldValue": order.order_id
            },
            {
                "fieldName": "customerId",
                "fieldValue": order.customer_id,
                "isPII": True
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Update order status
    order_manager.update_order_status(order.order_id, OrderStatus.PAYMENT_INITIATED)
    
    # Make the API request
    response = requests.request("POST", url, json=payload, headers=headers)
    
    return response.json()

# Example usage
if __name__ == "__main__":
    # Example product items
    items = [
        {"product_id": "PROD-001", "name": "Product 1", "quantity": 2, "price": 25},
        {"product_id": "PROD-002", "name": "Product 2", "quantity": 1, "price": 50}
    ]
    
    # Create an order
    order = order_manager.create_order(
        customer_id="CUST-001",
        items=items,
        total_amount=100,
        currency="XAF"
    )
    
    print("Created Order:", order.to_dict())
    
    # Create payment request
    payment_response = create_payment_request(order)
    print("Payment Response:", payment_response)