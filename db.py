from pymongo import MongoClient

# Connect
client = MongoClient("mongodb://localhost:27017/")

db = client["order_details"]

# Collections
customers = db["df_customers"]
orders = db["df_orders"]
order_items = db["df_orderitems"]
payments = db["df_payments"]
products = db["df_products"]