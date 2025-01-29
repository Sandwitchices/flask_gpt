from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Ensure your environment variable is set correctly
openai.api_key = os.getenv('OPENAI_API_KEY')

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
        logging.debug(f"OpenAI response: {response}")
        return jsonify({'response': response.choices[0].message['content']})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch response from OpenAI'}), 500

@app.route('/', methods=['GET'])
def home():
    return "Server is running!", 200

if __name__ == '__main__':
    app.run(debug=True)
