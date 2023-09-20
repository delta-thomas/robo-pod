import requests
import tkinter as tk
from tkinter import simpledialog, messagebox, Text, Button, filedialog
from datetime import datetime
from pydub import AudioSegment
import configparser
import os

# Load configuration from config.ini
config = configparser.ConfigParser()

# Check if config.ini exists
if os.path.exists('config.ini'):
    config.read('config.ini')
    print("=== Configuration ===")
    print("Configuration loaded successfully!")
else:
    print("config.ini not found!")
    exit()  # Exit the script if config.ini is not found

# Check configuration sections
if 'OpenAI' in config and 'ElevenLabs' in config and 'Texts' in config:
    print("All expected sections are present in the config!")
else:
    print("Some sections are missing in the config!")
    exit()  # Exit the script if some sections are missing

# Print configuration values for verification
print("\n=== OpenAI Configuration ===")
print("API Key:", config.get('OpenAI', 'API_KEY'))
print("Model:", config.get('OpenAI', 'MODEL'))

print("\n=== ElevenLabs Configuration ===")
print("API Key:", config.get('ElevenLabs', 'API_KEY'))
print("Voice ID:", config.get('ElevenLabs', 'VOICE_ID'))

print("\n=== Text Configuration ===")
print("PromptTweak:", config.get('Texts', 'PromptTweak'))
print("Welcome:", config.get('Texts', 'Welcome'))

# OpenAI API details
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = config.get('OpenAI', 'API_KEY')
MODEL = config.get('OpenAI', 'MODEL')
MAX_TOKENS = config.getint('OpenAI', 'MAX_TOKENS')
TEMPERATURE = config.getfloat('OpenAI', 'TEMPERATURE')

# Eleven Labs API details
ELEVEN_LABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
ELEVEN_LABS_API_KEY = config.get('ElevenLabs', 'API_KEY')
VOICE_ID = config.get('ElevenLabs', 'VOICE_ID')

# Texts
PROMPT_TWEAK = config.get('Texts', 'PromptTweak')
WELCOME_TEXT = config.get('Texts', 'Welcome')

def get_response_from_chatgpt(prompt, temperature=TEMPERATURE):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "temperature": temperature
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} from OpenAI API.")
        print(response.text)
        return ""

    return response.json()["choices"][0]["message"]["content"].strip()

def get_spoken_file_from_eleven_labs(text, voice_id=VOICE_ID):
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text
    }
    response = requests.post(ELEVEN_LABS_API_URL.format(voice_id=voice_id), headers=headers, json=data)
    return response.content

def combine_mp3s(intro_path, generated_path, output_path):
    intro = AudioSegment.from_mp3(intro_path)
    generated = AudioSegment.from_mp3(generated_path)

    combined = intro + generated
    combined.export(output_path, format="mp3")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatGPT to MP3")
        self.intro_music_path = "IntroMusic.mp3"
        self.user_input = simpledialog.askstring("Input", "Which 3 companies?")
        if not self.user_input:
            exit()  # Exit the app if no input is provided

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="Generate spoken content from ChatGPT")
        self.label.pack(pady=10)

        self.select_music_button = tk.Button(self.frame, text="Select Intro Music", command=self.select_intro_music)
        self.select_music_button.pack(pady=10)

        self.selected_music_label = tk.Label(self.frame, text="", font=("Arial", 10, "italic"), fg="blue")
        self.selected_music_label.pack(pady=5)

        self.generate_button = Button(self.frame, text="Generate MP3", command=self.generate_response)
        self.generate_button.pack()

    def select_intro_music(self):
        self.intro_music_path = filedialog.askopenfilename(title="Select Intro Music", filetypes=[("MP3 Files", "*.mp3")])
        if not self.intro_music_path:
            self.intro_music_path = "IntroMusic.mp3"
        file_name = self.intro_music_path.split("/")[-1]
        self.selected_music_label.config(text=f"Selected: {file_name}")

    def preview_content(self, chatgpt_response):
        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("Content Preview")

        self.text_widget = Text(self.preview_window, wrap=tk.WORD, height=10, width=50)
        self.text_widget.insert(tk.END, chatgpt_response)
        self.text_widget.pack(padx=10, pady=10)

        button_frame = tk.Frame(self.preview_window)
        button_frame.pack(pady=20)

        Button(button_frame, text="Confirm", command=self.confirm_content).pack(side=tk.LEFT, padx=5)
        Button(button_frame, text="Regenerate", command=self.regenerate_content).pack(side=tk.LEFT, padx=5)
        Button(button_frame, text="Edit", command=self.edit_content).pack(side=tk.LEFT, padx=5)
        Button(button_frame, text="Start Again", command=self.start_again).pack(side=tk.LEFT, padx=5)

    def confirm_content(self):
        chatgpt_response = self.text_widget.get("1.0", tk.END).strip()
        mp3_content = get_spoken_file_from_eleven_labs(WELCOME_TEXT + chatgpt_response)

        current_date = datetime.now().strftime('%Y-%m-%d')
        default_filename = f"{current_date}_{self.user_input.replace(' ', '_')}.mp3"
        save_path = filedialog.asksaveasfilename(title="Save MP3 As", initialfile=default_filename, filetypes=[("MP3 Files", "*.mp3")])

        if not save_path:
            return

        with open(save_path, "wb") as f:
            f.write(mp3_content)

        combine_mp3s(self.intro_music_path, save_path, save_path)

        messagebox.showinfo("Info", f"Saved the combined spoken file as {save_path}")
        self.preview_window.destroy()

    def regenerate_content(self):
        self.preview_window.destroy()
        self.generate_response()

    def edit_content(self):
        self.text_widget.config(state=tk.NORMAL)

    def start_again(self):
        self.preview_window.destroy()

    def generate_response(self):
        hardcoded_prompt = PROMPT_TWEAK + self.user_input
        chatgpt_response = get_response_from_chatgpt(hardcoded_prompt)
        self.preview_content(chatgpt_response)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
