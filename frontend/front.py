import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📚 Study Bot")

st.sidebar.header("Settings")

n_results = st.sidebar.slider(
    "Number of chunks to retrieve",
    min_value=1,
    max_value=15,
    value=4
)

# Upload a file #
#---------------#
st.header("Upload a PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if st.button("Upload and Process"):
        files = {"file": uploaded_file}
        with st.spinner("Uploading and processing PDF..."):
            response = requests.post(f"{API_URL}/upload-pdf", files=files)
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                st.error(f"Error: {data['error']}")
            else:
                st.success(f"Uploaded {data['filename']} - {data['num_chunks']} chunks created!")
        else:
            st.error(f"Request failed with status code {response.status_code}")

# Ask a question #
#----------------#
st.header("Ask a Question")

question = st.text_input("What do you want to know from the PDF?")

if st.button("Get Answer"):
    if question.strip() == "":
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):
            response = requests.get(
                f"{API_URL}/ask-pdf",
                params={"question": question, "n_results": n_results}
            )

        if response.status_code == 200:
            data = response.json()

            if "error" in data:
                st.error(f"Error: {data['error']}")
            else:
                st.subheader("Answer")
                st.write(data["answer"])

                with st.expander("show retrieved chunks"):
                    for i, chunk in enumerate(data["retrieved_chunks"]):
                        st.markdown(f"**Chunk {i+1}:**")
                        st.write(chunk)
        else:
            st.error(f"Request failed with status code {response.status_code}")
        

