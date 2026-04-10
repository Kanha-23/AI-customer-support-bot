from tools import (
    get_order_info,
    get_customer_info,
    get_order_items,
    get_product_info,
    get_payment_info,
    cancel_order
)


def main():
    print("🛠️ TOOL TESTER")
    print("Type 'exit' anytime to quit\n")

    while True:
        print("\nChoose Tool:")
        print("1. Get Order Info")
        print("2. Get Customer Info")
        print("3. Get Order Items")
        print("4. Get Product Info")
        print("5. Get Payment Info")
        print("6. Cancel Order")

        choice = input("\nEnter choice (1-6): ")

        if choice.lower() == "exit":
            break

        try:
            if choice == "1":
                order_id = input("Enter order_id: ")
                result = get_order_info(order_id)

            elif choice == "2":
                customer_id = input("Enter customer_id: ")
                result = get_customer_info(customer_id)

            elif choice == "3":
                order_id = input("Enter order_id: ")
                result = get_order_items(order_id)

            elif choice == "4":
                product_id = input("Enter product_id: ")
                result = get_product_info(product_id)

            elif choice == "5":
                order_id = input("Enter order_id: ")
                result = get_payment_info(order_id)

            elif choice == "6":
                order_id = input("Enter order_id: ")
                result = cancel_order(order_id)

            else:
                print("❌ Invalid choice")
                continue

            print("\n✅ RESULT:")
            print(result)

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()