import chromadb
client = chromadb.PersistentClient(
    path="database/chroma_database_v2"
)

collection = client.get_or_create_collection(
        name = "us_visa_rag"
    )