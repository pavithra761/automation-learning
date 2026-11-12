from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

question = "Explain what an API is."

# Without a system prompt
r1 = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=300,
    messages=[{"role": "user", "content": question}],
)
print("--- No system prompt ---")
print(r1.content[0].text)

# With a system prompt
r2 = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=300,
    system="You are a concise support agent. Answer in two sentences, no jargon.",
    messages=[{"role": "user", "content": "what is a cattepilar"}],
)
print("\n--- With system prompt ---")
print(r2.content[0].text)