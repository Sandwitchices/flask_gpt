from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import logging

app = Flask(__name__)

# Enable CORS (modify for production)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Get OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    logging.warning("⚠️ OpenAI API Key is not set! Please check your environment variables.")
else:
    openai.api_key = openai_api_key  # Set API key only if available

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    logging.debug(f"Received data: {data}")

    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        chat_response = response['choices'][0]['message']['content']
        logging.debug(f"OpenAI response: {chat_response}")

        return jsonify({'response': chat_response})

    except openai.error.OpenAIError as oe:
        logging.error(f"OpenAI API Error: {oe}")
        return jsonify({'error': 'OpenAI API error occurred'}), 500
    except Exception as e:
        logging.error(f"Server Error: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500

@app.route('/', methods=['GET'])
def home():
    return "Server is running!", 200

if __name__ == '__main__':
    app.run(debug=True)
