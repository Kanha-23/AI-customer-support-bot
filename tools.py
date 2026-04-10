from db import customers, orders, order_items, payments, products


# TOOL 1: Get order info
def get_order_info(order_id):
    order = orders.find_one({"order_id": order_id})

    if not order:
        return {"error": "Order not found"}

    return {
        "order_id": order["order_id"],
        "status": order["order_status"],
        "customer_id": order["customer_id"],
        "purchase_time": str(order["order_purchase_timestamp"])
    }


# TOOL 2: Get customer info
def get_customer_info(customer_id):
    customer = customers.find_one({"customer_id": customer_id})

    if not customer:
        return {"error": "Customer not found"}

    return {
        "customer_id": customer["customer_id"],
        "city": customer["customer_city"],
        "state": customer["customer_state"]
    }


# TOOL 3: Get order items
def get_order_items(order_id):
    items = list(order_items.find({"order_id": order_id}))

    if not items:
        return {"error": "No items found"}

    return [
        {
            "product_id": item["product_id"],
            "price": item["price"],
            "shipping_charges": item["shipping_charges"]
        }
        for item in items
    ]


# TOOL 4: Get product info
def get_product_info(product_id):
    product = products.find_one({"product_id": product_id})

    if not product:
        return {"error": "Product not found"}

    return {
        "product_id": product["product_id"],
        "category": product["product_category_name"],
        "weight": product["product_weight_g"]
    }


# TOOL 5: Get payment info
def get_payment_info(order_id):
    payment = payments.find_one({"order_id": order_id})

    if not payment:
        return {"error": "Payment not found"}

    return {
        "order_id": order_id,
        "payment_type": payment["payment_type"],
        "installments": payment["payment_installments"],
        "amount": payment["payment_value"]
    }


# TOOL 6: Cancel order
def cancel_order(order_id):
    order = orders.find_one({"order_id": order_id})

    if not order:
        return {"error": "Order not found"}

    if order["order_status"] == "delivered":
        return {"error": "Cannot cancel delivered order"}

    orders.update_one(
        {"order_id": order_id},
        {"$set": {"order_status": "cancelled"}}
    )

    return {"status": "Order cancelled successfully"}

# TOOL 7: Get all orders for a customer
def get_orders_by_customer(customer_id):
    user_orders = list(orders.find({"customer_id": customer_id}))

    if not user_orders:
        return {"error": "No orders found"}

    return [
        {
            "order_id": o["order_id"],
            "status": o["order_status"]
        }
        for o in user_orders
    ]