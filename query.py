import numpy as np
import faiss
import subprocess
import torch
from transformers import AutoTokenizer, AutoModel
import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def get_document_embedding(text):
    try:
        tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
        model = AutoModel.from_pretrained('distilbert-base-uncased')

        
        # Move model to CPU to avoid MPS issues
        model = model.to('cpu')
        
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        
        print("am i safe")
        embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        print(f"Embedding shape: {embedding.shape}")
        return embedding
    except Exception as e:
        print(f"Error during embedding extraction: {e}")
        raise


def create_faiss_index(embeddings):
    try:
        embeddings = np.array(embeddings).astype("float32")  # Ensure embeddings are float32
        print(f"Embedding shape before adding to FAISS: {embeddings.shape}")
        index = faiss.IndexFlatL2(embeddings.shape[1])  # Dimensionality of the embeddings
        index.add(embeddings)  # Add embeddings to the FAISS index
        return index
    except Exception as e:
        print(f"Error during FAISS indexing: {e}")
        raise

def query_ollama(query):
    try:
        print(f"Querying Ollama with input: {query}")
        command = f"ollama run llama3.2 --input 'Context: {query}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        response = result.stdout.strip()  # Get the output from Ollama
        if result.returncode != 0:
            print(f"Error querying Ollama: {result.stderr}")
            return None
        return response
    except Exception as e:
        print(f"Error during Ollama query: {e}")
        return None

def perform_rag(query, faiss_index, document_embeddings):
    query_embedding = get_document_embedding(query)
    # Ensure the shape of the query_embedding is (1, embedding_dim)
    query_embedding = query_embedding.astype('float32')
    _, indices = faiss_index.search(query_embedding, k=1)  # Get the top 1 closest document
    retrieved_document = document_embeddings[indices[0][0]]
    ollama_response = query_ollama(retrieved_document)
    return ollama_response

def main(pdf_path, query):
    try:
        document_text = extract_text_from_pdf(pdf_path)
        print(f"Extracted text from PDF:\n{document_text[:500]}...")  # Display the first 500 chars

        document_embedding = get_document_embedding(document_text)
        faiss_index = create_faiss_index([document_embedding])

        answer = perform_rag(query, faiss_index, [document_text])
        if answer:
            print(f"Generated Answer: {answer}")
        else:
            print("Error: No answer generated")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("MPS is available and will be used for the model.")
    else:
        device = torch.device("cpu")
        print("MPS is not available, using CPU instead.")

    pdf_path = "./data/personal_statement_zeta.pdf"
    query = "What inspired you to pursue computer science?"
    main(pdf_path, query)
