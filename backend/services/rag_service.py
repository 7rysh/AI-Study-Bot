import chromadb #RAG 
import uuid #Allows for unique ID generation
from services.embedding_service import create_embeddings

# Initialize the Chroma client with a persistent database for no loss on restart
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Collection stores embeddings is and like a folder in the vector DB
collection = chroma_client.get_or_create_collection( name="study_materials" ) #Get or create checks for existing study_materials collection


# Function: Adds text chunks to the Chroma collection
# --------------------------------------------------- #
def add_chunks_to_collection(chunks: list[str]) -> None:
    
    embeddings = create_embeddings(chunks)

    for index, chunk in enumerate(chunks): #Enumerate gives position number and chunk value

        collection.add( #Add chunks to collection
            documents=[chunk],
            embeddings=[embeddings[index]],
            ids=[str(uuid.uuid4())]
        )


# Function:
# --------------------------------------------------- #
def retrieve_relevant_chunks(question: str, n_results=8)-> list[str]:

    question_embedding = create_embeddings(question)
    results = collection.query( #Search database for semantically similar chunks to the question
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    return results["documents"][0]