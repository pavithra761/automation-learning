import time
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

# Put a ~300-word article in a file called article.txt (same folder)
with open("article.txt") as f:
    article = f.read()

prompt = f"Summarize this article in 3 bullet points:\n\n{article}"

# Prices in USD per 1,000,000 tokens: (input, output)
# FILL THESE IN from the Anthropic pricing page
PRICES = {
    "claude-opus-5-5": (4, 20),
    "claude-haiku-5-5": (0.10, 0.50),
}

results = []

for model, (price_in, price_out) in PRICES.items():
    start = time.perf_counter()
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    seconds = time.perf_counter() - start

    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    cost = (input_tokens / 1_000_000 * price_in) + (output_tokens / 1_000_000 * price_out)

    print(f"\n===== {model} =====")
    for block in response.content:
        if block.type == "text":
            print(block.text)
    print(f"seconds: {seconds:.2f} | input: {input_tokens} | output: {output_tokens} | cost: ${cost:.6f}")

    results.append((model, seconds, input_tokens + output_tokens, cost))

print("\n| model | latency (s) | tokens | cost ($) | quality (1-5) |")
print("|---|---|---|---|---|")
for model, seconds, tokens, cost in results:
    print(f"| {model} | {seconds:.2f} | {tokens} | {cost:.6f} | ? |")