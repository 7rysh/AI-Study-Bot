from services.embedding_service import create_embeddings

result = create_embeddings(["hello world", "this is a test"])
print(len(result))
print(len(result[0]))