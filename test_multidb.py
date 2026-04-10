from db import customers, orders, order_items, payments, products

print("Customers:", customers.count_documents({}))
print("Orders:", orders.count_documents({}))
print("Order Items:", order_items.count_documents({}))
print("Payments:", payments.count_documents({}))
print("Products:", products.count_documents({}))

# Sample join-like check
sample_order = orders.find_one()

print("\nSample Order:")
print(sample_order)