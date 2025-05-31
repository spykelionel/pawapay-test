from datetime import datetime
import uuid
from enum import Enum
import json
import os

class OrderStatus(Enum):
    PENDING = "PENDING"
    PAYMENT_INITIATED = "PAYMENT_INITIATED"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Order:
    def __init__(self, customer_id, items, total_amount, currency="XAF"):
        self.order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        self.customer_id = customer_id
        self.items = items  # List of product items
        self.total_amount = total_amount
        self.currency = currency
        self.status = OrderStatus.PENDING
        self.deposit_id = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.payment_details = None

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items": self.items,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "status": self.status.value,
            "deposit_id": self.deposit_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "payment_details": self.payment_details
        }

    @classmethod
    def from_dict(cls, data):
        order = cls(
            customer_id=data['customer_id'],
            items=data['items'],
            total_amount=data['total_amount'],
            currency=data['currency']
        )
        order.order_id = data['order_id']
        order.status = OrderStatus(data['status'])
        order.deposit_id = data['deposit_id']
        order.created_at = datetime.fromisoformat(data['created_at'])
        order.updated_at = datetime.fromisoformat(data['updated_at'])
        order.payment_details = data['payment_details']
        return order

class OrderManager:
    def __init__(self, storage_file='orders.json'):
        self.storage_file = storage_file
        self.orders = self._load_orders()

    def _load_orders(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    return {order_id: Order.from_dict(order_data) 
                           for order_id, order_data in data.items()}
            except Exception as e:
                print(f"Error loading orders: {e}")
                return {}
        return {}

    def _save_orders(self):
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(
                    {order_id: order.to_dict() 
                     for order_id, order in self.orders.items()},
                    f,
                    indent=2
                )
        except Exception as e:
            print(f"Error saving orders: {e}")

    def create_order(self, customer_id, items, total_amount, currency="XAF"):
        order = Order(customer_id, items, total_amount, currency)
        self.orders[order.order_id] = order
        self._save_orders()
        return order

    def get_order(self, order_id):
        return self.orders.get(order_id)

    def update_order_status(self, order_id, status, payment_details=None):
        if order_id in self.orders:
            order = self.orders[order_id]
            order.status = status
            order.updated_at = datetime.now()
            if payment_details:
                order.payment_details = payment_details
            self._save_orders()
            return True
        return False

    def get_orders_by_customer(self, customer_id):
        return [order for order in self.orders.values() if order.customer_id == customer_id]

    def get_orders_by_status(self, status):
        return [order for order in self.orders.values() if order.status == status]

# Example usage:
if __name__ == "__main__":
    # Create order manager
    order_manager = OrderManager()

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