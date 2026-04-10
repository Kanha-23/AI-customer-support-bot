import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    get_order_info,
    get_order_items,
    get_product_info,
    get_payment_info,
    cancel_order,
    get_orders_by_customer
)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an AI customer support assistant. 
The user is logged in. You have access to their customer_id and must use it to fetch information.

GUARDRAILS:
- If a user asks about movies, celebrities, general knowledge, coding, or anything NOT related to their orders or our products, politely refuse.
- Example Refusal: "I'm sorry, I am an automated assistant designed only to help with your orders and shopping experience. I cannot provide information on [topic]."
- NEVER break character.

Rules:
1. If you don't know the order_id, call get_orders_by_customer first.
2. If the customer has multiple orders, list them and ask the user to specify which one they are referring to.
3. If they have only one order, proceed with that order_id.
4. Tool usage:
   - Status/Dates -> get_order_info
   - Payments -> get_payment_info
   - Cancel -> cancel_order
   - Items/Products -> get_order_items (Note: get_product_info is used automatically in the background).
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_orders_by_customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"}
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_info",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_payment_info",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_items",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    }
]


def run_agent(user_input, session_data, customer_id):
    if not customer_id or customer_id == "0":
        return "Invalid session. Please login again."

    if "messages" not in session_data:
        session_data["messages"] = []

    # 1. Add User Message to History
    session_data["messages"].append({"role": "user", "content": user_input})

    # Prepare message list for API (System + History)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + session_data["messages"]

    # Limit loops to prevent infinite calls
    for _ in range(3):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools # Use the tools list defined in your code
        )

        msg = response.choices[0].message
        
        # If the model wants to talk to the user (Final Answer)
        if not msg.tool_calls:
            session_data["messages"].append({"role": "assistant", "content": msg.content})
            return msg.content

        # 2. Handle Tool Calls
        messages.append(msg) # Append the tool call request
        
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            # Inject customer_id automatically if tool requires it
            if name == "get_orders_by_customer":
                args["customer_id"] = customer_id
            
            # Inject last_order_id if the model forgot it but we have it in session
            if "order_id" not in args and session_data.get("last_order_id"):
                if name in ["get_order_info", "get_payment_info", "cancel_order", "get_order_items"]:
                    args["order_id"] = session_data["last_order_id"]

            # Execute the actual tool
            result = execute_tool(name, args, session_data)
            
            # Append result to history
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # After tool execution, the loop continues to let the LLM see the results and reply

def execute_tool(name, args, session_data):
    """Helper to route tool calls to actual functions"""
    if name == "get_orders_by_customer":
        res = get_orders_by_customer(**args)
        # If exactly one order found, cache it for convenience
        if isinstance(res, list) and len(res) == 1:
            session_data["last_order_id"] = res[0]["order_id"]
        return res
    
    elif name == "get_order_info":
        return get_order_info(**args)
    
    elif name == "get_payment_info":
        return get_payment_info(**args)
    
    elif name == "cancel_order":
        return cancel_order(**args)
    
    elif name == "get_order_items":
        items = get_order_items(**args)
        # Background enrichment of product names/categories
        if isinstance(items, list):
            for item in items:
                p_info = get_product_info(item["product_id"])
                item.update(p_info) # Adds category, weight, etc.
        return items
    
    return {"error": "Tool not found"}