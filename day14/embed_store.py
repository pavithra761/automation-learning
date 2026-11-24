import os

import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

from chunking import load_chunks

load_dotenv()

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks")

    model = SentenceTransformer(MODEL_NAME, device="cpu")
    dimension = model.get_embedding_dimension()
    vectors = model.encode([c["text"] for c in chunks], normalize_embeddings=True)
    print(f"Embedded each chunk as {dimension} numbers")

    with psycopg.connect(os.environ["DATABASE_URL"], autocommit=True) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(conn)
        conn.execute("DROP TABLE IF EXISTS chunks")
        conn.execute(
            f"CREATE TABLE chunks (id serial PRIMARY KEY, source text, number int, "
            f"content text, embedding vector({dimension}))"
        )
        for chunk, vector in zip(chunks, vectors):
            conn.execute(
                "INSERT INTO chunks (source, number, content, embedding) VALUES (%s, %s, %s, %s)",
                (chunk["source"], chunk["number"], chunk["text"], vector),
            )
        count = conn.execute("SELECT count(*) FROM chunks").fetchone()[0]
    print(f"Stored {count} rows")


if __name__ == "__main__":
    main()