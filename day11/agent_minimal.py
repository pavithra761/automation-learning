#code for only lookup tool
# import sys

# import ast 
# import operator
# import anthropic
# from dotenv import load_dotenv

# load_dotenv()
# client = anthropic.Anthropic()

# MODEL = "claude-haiku-5-5"

# ORDERS = {
#     "A100": {"status": "shipped", "total": 49.90, "eta": "2 days"},
#     "A101": {"status": "processing", "total": 120.00, "eta": "5 days"},
#     "A102": {"status": "delivered", "total": 15.50, "eta": "already delivered"},
# }


# def lookup_order(order_id):
#     order = ORDERS.get(order_id.upper())
#     if order is None:
#         return f"Error: order {order_id} not found. Ask the customer to check the ID."
#     return str(order)


# tools = [
#     {
#         "name": "lookup_order",
#         "description": "Look up an order by its ID, such as A100. Returns its status, total and delivery estimate. Use it whenever the customer asks about an order.",
#         "input_schema": {
#             "type": "object",
#             "properties": {
#                 "order_id": {"type": "string", "description": "The order ID, for example A100"}
#             },
#             "required": ["order_id"],
#         },
#     }
# ]

# # question = "Where is order A100?"

# # response = client.messages.create(
# #     model=MODEL,
# #     max_tokens=2000,
# #     tools=tools,
# #     messages=[{"role": "user", "content": question}],
# # )

# # print("stop_reason:", response.stop_reason)
# # for block in response.content:
# #     print(block.type, "->", block)

# SYSTEM = (
#     "You are a support assistant for an online shop. "
#     "Use the tools to look up orders. Never guess an order's details."
#     "Dont state a currency unless the tool result includes one."
#     "Keep the order ID exactly as the customer wrote it, including capitals."

# )
# MAX_STEPS = 8


# def run_tool(name, tool_input):
#     if name == "lookup_order":
#         return lookup_order(tool_input["order_id"])
#     return f"Error: unknown tool {name}"


# def run_agent(question):
#     messages = [{"role": "user", "content": question}]

#     for step in range(1, MAX_STEPS + 1):
#         response = client.messages.create(
#             model=MODEL,
#             max_tokens=2000,
#             system=SYSTEM,
#             tools=tools,
#             messages=messages,
#         )

#         if response.stop_reason != "tool_use":
#             return "".join(b.text for b in response.content if b.type == "text")

#         messages.append({"role": "assistant", "content": response.content})

#         results = []
#         for block in response.content:
#             if block.type == "tool_use":
#                 print(f"[step {step}] tool: {block.name}  input: {block.input}")
#                 output = run_tool(block.name, block.input)
#                 print(f"           result: {output}")
#                 results.append(
#                     {"type": "tool_result", "tool_use_id": block.id, "content": output}
#                 )

#         messages.append({"role": "user", "content": results})

#     return "Stopped: too many steps."


# if __name__ == "__main__":
#     question = sys.argv[1] if len(sys.argv) > 1 else "Where is order A100?"
#     print("Question:", question)
#     print()
#     print("Answer:", run_agent(question))


#code with lookup and calculatoe tool.

import ast
import operator
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-haiku-5-5"
MAX_STEPS = 8

SYSTEM = (
    "You are a support assistant for an online shop. "
    "Use the tools to look up orders. Never guess an order's details. "
    "Use the calculate tool for any arithmetic, and never do maths in your head. "
    "Don't state a currency unless the tool result includes one. "
    "Keep the order ID exactly as the customer wrote it, including capitals."
)

ORDERS = {
    "A100": {"status": "shipped", "total": 49.90, "eta": "2 days"},
    "A101": {"status": "processing", "total": 120.00, "eta": "5 days"},
    "A102": {"status": "delivered", "total": 15.50, "eta": "already delivered"},
}


def lookup_order(order_id):
    order = ORDERS.get(order_id.upper())
    if order is None:
        return f"Error: order {order_id} not found. Ask the customer to check the ID."
    return str(order)


OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    raise ValueError("only numbers and + - * / are allowed")


def calculate(expression):
    try:
        tree = ast.parse(expression, mode="eval")
        return str(safe_eval(tree.body))
    except Exception as error:
        return f"Error: {error}"


tools = [
    {
        "name": "lookup_order",
        "description": "Look up an order by its ID, such as A100. Returns its status, total and delivery estimate. Use it whenever the customer asks about an order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID, for example A100"}
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "calculate",
        "description": "Do arithmetic with + - * /. Use it for any calculation, such as adding totals or finding a difference, instead of working it out yourself.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "For example 120.0 - 49.9"}
            },
            "required": ["expression"],
        },
    },
]


def run_tool(name, tool_input):
    if name == "lookup_order":
        return lookup_order(tool_input["order_id"])
    if name == "calculate":
        return calculate(tool_input["expression"])
    return f"Error: unknown tool {name}"


def run_agent(question):
    messages = [{"role": "user", "content": question}]

    for step in range(1, MAX_STEPS + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=SYSTEM,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        messages.append({"role": "assistant", "content": response.content})

        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[step {step}] tool: {block.name}  input: {block.input}")
                output = run_tool(block.name, block.input)
                print(f"           result: {output}")
                results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": output}
                )

        messages.append({"role": "user", "content": results})

    return "Stopped: too many steps."


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "Where is order A100?"
    print("Question:", question)
    print()
    print("Answer:", run_agent(question))