import requests

ELEVEN_LABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

def get_spoken_file_from_eleven_labs(text, API_KEY, VOICE_ID):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.75,
            "style": 0.25,
            "use_speaker_boost": True
        }
    }
    response = requests.post(ELEVEN_LABS_API_URL.format(voice_id=VOICE_ID), headers=headers, json=data)
    return response.content
