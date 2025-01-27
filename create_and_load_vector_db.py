import chromadb
import json

# chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(
    "kevin_db",
)

collection = chroma_client.create_collection(
    name="visit_lisboa"
)

with open("data/visit_lisboa.json") as f:
    data = json.load(f)

collection.upsert(
    documents=[row["description"] for row in data],
    metadatas=[
        {
            "title": row["title"],
            "date": row["date"],
        }
        for row in data
    ],
    ids=[str(i) for i in range(len(data))],
)

# collection.delete_all()

