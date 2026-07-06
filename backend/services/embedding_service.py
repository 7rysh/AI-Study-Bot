from sentence_transformers import SentenceTransformer #Import

# Choose and load model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Takes in text and returns vector embedding
def create_embeddings(texts):
    
    embeddings = embedding_model.encode(texts) #Converts

    return embeddings.tolist() #ToList converts NumPy arrat into normal Python list