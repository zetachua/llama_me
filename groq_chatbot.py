from groq import Groq
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from config import groq_api

# Initialize Groq client with your API key
api_key = groq_api
client = Groq(api_key=api_key)

# Pre-process the text (tokenization and lemmatization)
def pre_process_text(text):
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    text = word_tokenize(text)  # Tokenize the words
    lemmatizer = WordNetLemmatizer()  # Initialize lemmatizer
    text = [lemmatizer.lemmatize(word) for word in text]  # Lemmatize each word
    return ' '.join(text)  # Return as a single string

# Load personality data
def load_personality_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            sentences = nltk.sent_tokenize(data)  # Tokenize the document into sentences
            return sentences
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    
def get_groq_response(persona_description, user_input):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",  
         messages = [
            {"role": "system", "content": "You are an AI twin chatbot of a persona described below. Answer questions as if you were that persona."},
            {"role": "assistant", "content": persona_description},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,  
        max_tokens=200,  
        top_p=1,
        stream=False
    )
    response_content = completion.choices[0].message.content
    return response_content
   

# Chatbot Class
class Chatbot:
    def __init__(self, persona_sentences, groq_client):
        self.persona_sentences = persona_sentences
        self.persona_description = " ".join(persona_sentences)  # Combine persona sentences into one string
        self.groq_client = groq_client

    def respond(self, user_input):
        # Step 1: Get Groq response
        try:
            groq_response = get_groq_response(self.persona_description, user_input)
            print(f"Groq response: {groq_response}")  # Debugging the response
            return groq_response
        except Exception as e:
            print(f"Groq API failed: {e}")
            return "I'm sorry, I couldn't understand your question."

# Example usage
if __name__ == "__main__":
    # Load persona from document.txt
    file_path = './data/document.txt'
    persona_sentences = load_personality_data(file_path)
    
    if persona_sentences:
        chatbot = Chatbot(persona_sentences, client)

        print("Chatbot: Hello! I am your AI twin. How can I assist you today?")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Chatbot: Goodbye!")
                break
            response = chatbot.respond(user_input)
            print(f"Chatbot: {response}")
    else:
        print("No valid persona data found in the document.")
