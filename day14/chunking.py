from pathlib import Path


def split_into_chunks(text, min_words=25):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    buffer = ""
    for paragraph in paragraphs:
        buffer = f"{buffer}\n\n{paragraph}".strip()
        if len(buffer.split()) >= min_words:
            chunks.append(buffer)
            buffer = ""
    if buffer:
        chunks.append(buffer)
    return chunks


def load_chunks(folder="docs"):
    all_chunks = []
    for path in sorted(Path(folder).glob("*.txt")):
        text = path.read_text()
        for number, chunk in enumerate(split_into_chunks(text)):
            all_chunks.append({"source": path.name, "number": number, "text": chunk})
    return all_chunks


if __name__ == "__main__":
    chunks = load_chunks()
    print(f"{len(chunks)} chunks")
    for chunk in chunks[:3]:
        print("-" * 40)
        print(chunk["source"], chunk["number"], f"({len(chunk['text'].split())} words)")
        print(chunk["text"][:200])