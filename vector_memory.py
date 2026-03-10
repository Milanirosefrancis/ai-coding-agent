import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="agent_memory"
)


def store_memory(text):

    collection.add(
        documents=[text],
        ids=[str(hash(text))]
    )


def search_memory(query):

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    return results["documents"]