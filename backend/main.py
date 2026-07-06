from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
from services.pdf_service import chunk_text
from services.rag_service import add_chunks_to_collection, retrieve_relevant_chunks
from services.rag_service import collection
import os

load_dotenv()

app = FastAPI()

os.makedirs("uploads", exist_ok=True)


# Configure Gemini API
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.get("/")
def home():
    return {"message": "Running AI Assistant"}


# Debugging rout
@app.get("/debug-collection")
def debug_collection():

    results = collection.get()

    return {
        "num_documents": len(results["documents"]),
        "sample": results["documents"][:3]
    }

#Test if the AI is working with a sample prompt
@app.get("/test-ai")
def test_ai():

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": "Explain embeddings in simple terms."
                }
            ]
        )

        return {
            "response": response.choices[0].message.content
        }
    
    except Exception as e:

        return {
            "error": str(e)
        }
    


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    global stored_pdf_text
    try:

        file_path = f"uploads/{file.filename}"

        with open(file_path, "wb") as pdf_file:

            content = await file.read()

            pdf_file.write(content)

        #
        print("STEP 1: File saved")

        reader = PdfReader(file_path)

        extracted_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                extracted_text += text

        #
        print("STEP 2: Text extracted, length:", len(extracted_text))

        chunks = chunk_text(extracted_text)

        #
        print("STEP 3: Chunked into", len(chunks), "chunks")

        add_chunks_to_collection(chunks)

        #
        print("STEP 4: Chunks added to collection")

        return {
            "filename": file.filename,
            "num_chunks": len(chunks),
            "text": extracted_text[:500]
        }
    
    except Exception as e:

        return {
            "error": str(e)
        }
    

@app.get("/ask-pdf") # Creates endpoint
def ask_pdf(question: str, n_results: int = 4):

    
    try:
        
        relevant_chunks = retrieve_relevant_chunks(question, n_results=n_results)

        context = "\n".join(relevant_chunks)

        # This is the prompt    f""" ... """ is a multi line string"
        prompt = f""" 
        Answer the question using ONLY the provided context.

        If the answer is not explicitly stated in the context, say:
        "I could not find that information in the document."

        Be concise and quote specific information when available.

        Context:
        {context}

        USER QUESTION:
        {question}
        """


        #Sending to Groq
        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return{
            "question": question,
            "retrieved_chunks": relevant_chunks, #temp
            "answer": response.choices[0].message.content
        }
    
    except Exception as e:

        return{
            "error": str(e)
        }

@app.get("/search-text")
def search_text(term: str):

    results = collection.get()

    matches = []

    for doc in results["documents"]:

        if term.lower() in doc.lower():

            matches.append(doc)

    return {
        "matches": matches
    }