import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-haiku-5-5"
MAX_STEPS = 8
DRAFTS_DIR = Path("drafts")

SYSTEM = (
    "You are a support assistant for an online shop. "
    "Use the tools to look up orders and to save draft replies. "
    "Never guess an order's details. "
    "When asked to draft a reply, save the draft with the wording the user asked for. "
    "If the wording seems to conflict with the order data, add a short note after "
    "the draft text saying so, but still save it. "
    "A draft reply is only saved for a human to review. It is never sent, "
    "so never tell the customer that anything was sent. "
    "Don't state a currency unless the tool result includes one."
)


ORDERS = {
    "A100": {"status": "shipped", "total": 49.90, "eta": "2 days"},
    "A101": {"status": "processing", "total": 120.00, "eta": "5 days"},
    "A102": {"status": "delivered", "total": 15.50, "eta": "already delivered"},
    "A103": {"status": "shipped", "total": 75.00, "eta": "1 day"},
}

VALID_STATUSES = ["processing", "shipped", "delivered"]


def lookup_order(order_id):
    order = ORDERS.get(order_id.upper())
    if order is None:
        return f"Error: order {order_id} not found. Ask the customer to check the ID."
    return str(order)


def list_orders(status):
    if status not in VALID_STATUSES:
        return f"Error: status must be one of {VALID_STATUSES}."
    matches = [oid for oid, order in ORDERS.items() if order["status"] == status]
    if not matches:
        return f"No orders have the status {status}."
    return ", ".join(matches)


def create_draft_reply(order_id, message):
    order_id = order_id.upper()
    if order_id not in ORDERS:
        return f"Error: order {order_id} not found. Look the order up first."

    message = message.strip()
    if not message:
        return "Error: the draft message is empty. Write the reply text and try again."
    if len(message) > 1000:
        return "Error: the draft is too long (limit 1000 characters). Shorten it."

    DRAFTS_DIR.mkdir(exist_ok=True)
    path = DRAFTS_DIR / f"{order_id}.txt"

    if path.exists():
        if path.read_text() == message:
            return f"A draft for {order_id} with this exact text already exists. Nothing changed."
        return (
            f"Error: a different draft for {order_id} already exists. "
            "Do not overwrite it. Tell the user a draft already exists."
        )

    path.write_text(message)
    return f"Draft saved for {order_id}. It has NOT been sent to the customer."


tools = [
    {
        "name": "lookup_order",
        "description": (
            "Get the details of ONE order by its ID, such as A100: status, total and "
            "delivery estimate. Use it when the customer names a specific order. "
            "To find orders by status, use list_orders instead."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID, for example A100"}
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "list_orders",
        "description": (
            "List the IDs of all orders with a given status. Use it for questions like "
            "'which orders have shipped?'. It returns IDs only. Use lookup_order for details."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": VALID_STATUSES,
                    "description": "The order status to filter by",
                }
            },
            "required": ["status"],
        },
    },
    {
        "name": "create_draft_reply",
        "description": (
            "Save a draft reply about an order for a human to review. It does NOT send "
            "anything. Use it only when the user asks you to prepare or draft a reply. "
            "Look up the order first so the draft is accurate."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID the reply is about"},
                "message": {"type": "string", "description": "The full text of the draft reply"},
            },
            "required": ["order_id", "message"],
        },
    },
]


def run_tool(name, tool_input):
    if name == "lookup_order":
        return lookup_order(tool_input["order_id"])
    if name == "list_orders":
        return list_orders(tool_input["status"])
    if name == "create_draft_reply":
        return create_draft_reply(tool_input["order_id"], tool_input["message"])
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
    question = sys.argv[1] if len(sys.argv) > 1 else "Which orders have shipped?"
    print("Question:", question)
    print()
    print("Answer:", run_agent(question))