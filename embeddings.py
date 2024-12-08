import faiss
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from PyPDF2 import PdfReader
from config import model_path

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_path)

def extract_text_from_pdf(file_path):
    """Extract text from the provided PDF."""
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() for page in reader.pages)

def create_embeddings(text_chunks):
    """Create embeddings for a list of text chunks using the model."""
    embeddings = []
    for chunk in text_chunks:
        # Tokenizing the text chunk
        inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # Ensure you're using the model for embedding generation
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Mean pooling of the last hidden state to create the embedding
        embeddings.append(outputs.last_hidden_state.mean(dim=1).cpu().numpy())
    
    return np.vstack(embeddings)

def build_faiss_index(pdf_path, index_path):
    """Build a FAISS index from a PDF document."""
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Split the text into manageable chunks (this can be sentence-level or paragraph-level)
    text_chunks = pdf_text.split("\n")  # You may want to split by sentences or paragraphs
    
    # Create embeddings for the text chunks
    embeddings = create_embeddings(text_chunks)
    
    # Normalize embeddings for FAISS
    faiss.normalize_L2(embeddings)
    
    # Build and populate the FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])  # Use L2 distance
    index.add(embeddings)
    
    # Save the index to a file
    faiss.write_index(index, index_path)

if __name__ == "__main__":
    # Example PDF and FAISS index path
    build_faiss_index("data/personal_statement_zeta.pdf", "data/pdf_faiss.index")
