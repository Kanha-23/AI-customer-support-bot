from agent import run_agent

print("🤖 AI Customer Support Bot")
print("Type 'exit' to quit\n")

while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    response = run_agent(query)

    print("\nBot:")
    print(response)
    print("-" * 40)