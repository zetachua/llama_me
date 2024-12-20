from flask import Flask, request, jsonify
from flask_cors import CORS
from groq_chatbot import Chatbot,load_personality_data,client

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

# Create a Chatbot instance
file_path = './data/document.txt'
persona_sentences = load_personality_data(file_path)
chatbot = Chatbot(persona_sentences, client)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    if user_input:
        response = chatbot.respond(user_input)  # Get response from the chatbot
        return jsonify({'response': response})
    return jsonify({'error': 'No input received'}), 400

if __name__ == '__main__':
    app.run(debug=True)
