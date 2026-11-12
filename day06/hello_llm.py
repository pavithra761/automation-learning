from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4000,
    messages=[
        {"role": "user", "content": "Explain what an API is in two sentences."}
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)

print(response.usage)

