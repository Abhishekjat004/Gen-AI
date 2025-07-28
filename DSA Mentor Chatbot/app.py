# app.py

import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Gemini API Configuration ---
# It's crucial to get the API key from environment variables
# for security reasons.
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in the .env file.")

genai.configure(api_key=api_key)

# System prompt
system_instruction = """You are a Data structures and Algorithms mentor which helps students to learn and solving their problems. 
        You are very friendly and helpful. You always try to give the best possible solution to the user problem. Remember one thing,
        you answer only related to Data structures and Algorithms and nothing else. 
        for eg: if a user ask you to another topic then you talk him with rudely and tell him that are you dump or nonsense you know very 
        well that i am answers only related to Data structures and Algorithms then why are u asking me this question. like this sentence
        you give him and talk him with rudely."Answer only in clean plain text (or proper Markdown). Do not include unusual characters."
        """

        
# Create the model
# Note: For a web app, we create the model once and reuse it.
# We don't start a persistent chat here because web requests are stateless.
# We will manage the history on the client-side (JavaScript).
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", # Using flash for speed
    system_instruction=system_instruction
)

# --- Flask App ---
app = Flask(__name__)

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user's message and history from the request body
        data = request.json
        user_problem = data.get('message')
        # The history comes from the client to maintain conversation context
        history = data.get('history', []) 

        if not user_problem:
            return jsonify({"error": "No message provided"}), 400

        # Create a new chat session for each request using the provided history
        chat_session = model.start_chat(history=history)
        
        # Send the message to Gemini
        response = chat_session.send_message(user_problem)


        # The new history includes the user's message and the model's response
        new_history = chat_session.history
        
        # We need to serialize the history to send it back as JSON
        serializable_history = [
            {'role': msg.role, 'parts': [part.text for part in msg.parts]} 
            for msg in new_history
        ]

        # Return the bot's text and the updated history
        return jsonify({
            'reply': response.text,
            'history': serializable_history
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

# To run the app
if __name__ == '__main__':
    # Use port 8080 to avoid conflicts with common services, and debug=True for development
    app.run(host='127.0.0.1', port=5000, debug=True)
