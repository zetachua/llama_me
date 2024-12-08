import faiss
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import model_path

# Load tokenizer, model, and FAISS index
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
index = faiss.read_index("data/pdf_faiss.index")

def query_faiss(query, top_k=3):
    inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    query_embedding = outputs.last_hidden_state.mean(dim=1).numpy()
    _, indices = index.search(query_embedding, top_k)
    return indices

def generate_response(user_input):
    related_chunks = query_faiss(user_input)
    prompt = " ".join(related_chunks) + f"\nUser: {user_input}\nAssistant:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=1024)
    outputs = model.generate(**inputs, max_length=2048, num_beams=3)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
