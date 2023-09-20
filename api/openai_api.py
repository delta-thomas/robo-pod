import requests

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def get_response_from_chatgpt(prompt, MODEL, MAX_TOKENS, TEMPERATURE, API_KEY):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} from OpenAI API.")
        print(response.text)
        return ""

    return response.json()["choices"][0]["message"]["content"].strip()
