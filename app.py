# [app.py]
from flask import Flask, render_template, request, jsonify
from api.openai_api import get_response_from_chatgpt
from api.elevenlabs_api import get_spoken_file_from_eleven_labs
from config.settings import get_openai_config, get_elevenlabs_config, get_texts_config
from utils.audio_utils import combine_mp3s
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    company_names = data.get('companyNames', [])
    combined_company_name = ', '.join(f'[{name}]' for name in company_names)

    openai_config = get_openai_config()
    elevenlabs_config = get_elevenlabs_config()
    texts_config = get_texts_config()

    hardcoded_prompt = texts_config["prompttweak"] + combined_company_name
    chatgpt_response = get_response_from_chatgpt(hardcoded_prompt, **openai_config)

    # ... (rest of your logic)

    return jsonify(result="success", data={})

if __name__ == '__main__':
    app.run(debug=True)
