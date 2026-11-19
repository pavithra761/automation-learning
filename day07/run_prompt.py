import sys
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-haiku-5-5"

prompt_file = sys.argv[1]
sample_file = sys.argv[2]

with open(prompt_file) as f:
    prompt = f.read()
with open(sample_file) as f:
    sample = f.read()

full_prompt = prompt.replace("{{input}}", sample)

response = client.messages.create(
    model=MODEL,
    max_tokens=1000,
    messages=[{"role": "user", "content": full_prompt}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)

