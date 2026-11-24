RAG(reterival augumented generation)
Gives answers from the documents that you share along with its souces.


documents -> split into chunks -> embed each chunk -> store in Postgres (pgvector)
question -> embed -> find the 4 nearest chunks -> send chunks + question to Claude -> answer with citations
