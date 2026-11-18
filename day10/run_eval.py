import csv

import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-haiku-5-5"

with open("classify.md") as f:
    prompt_template = f.read()

with open("hard_cases.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

correct = 0
wrong_cases = []

for number, row in enumerate(rows, start=1):
    prompt = prompt_template.replace("{{input}}", row["input"])

    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = ""
    for block in response.content:
        if block.type == "text":
            text = block.text

    got = text.strip().lower()
    expected = row["expected"].strip().lower()

    if got == expected:
        correct += 1
        print(f"{number:2}. OK     expected={expected} got={got}")
    else:
        print(f"{number:2}. WRONG  expected={expected} got={got}")
        print(f"      message: {row['input']}")
        wrong_cases.append((number, expected, got, row["input"]))

total = len(rows)
percent = correct / total * 100
print()
print(f"{correct} / {total} correct ({percent:.0f}%)")

if wrong_cases:
    print()
    print("Wrong cases:")
    for number, expected, got, message in wrong_cases:
        print(f"  {number}. expected {expected}, got {got}: {message}")