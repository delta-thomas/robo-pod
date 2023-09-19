import requests
import tkinter as tk
from tkinter import simpledialog, messagebox, Text, Button, filedialog
from datetime import datetime
from pydub import AudioSegment

# OpenAI API details
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = "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"
ELEVEN_LABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
ELEVEN_LABS_API_KEY = "a842ce16fb9d66486e6412294dbac613"

def get_response_from_chatgpt(prompt, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "temperature": temperature
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} from OpenAI API.")
        print(response.text)
        return ""
    
    return response.json()["choices"][0]["message"]["content"].strip()

def get_spoken_file_from_eleven_labs(text, voice_id):
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

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="Generate spoken content from ChatGPT")
        self.label.pack(pady=10)

        self.select_music_button = tk.Button(self.frame, text="Select Intro Music", command=self.select_intro_music)
        self.select_music_button.pack(pady=10)

        self.generate_button = Button(self.frame, text="Generate MP3", command=self.generate_response)
        self.generate_button.pack()

    def select_intro_music(self):
        self.intro_music_path = filedialog.askopenfilename(title="Select Intro Music", filetypes=[("MP3 Files", "*.mp3")])
        if not self.intro_music_path:
            self.intro_music_path = "IntroMusic.mp3"

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
        voice_id = "21m00Tcm4TlvDq8ikWAM"
        mp3_content = get_spoken_file_from_eleven_labs(chatgpt_response, voice_id)
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        default_filename = f"{current_date}_{self.user_input.replace(' ', '_')}.mp3"
        filename = simpledialog.askstring("Filename", "Enter filename for the mp3:", initialvalue=default_filename)
        
        with open(filename, "wb") as f:
            f.write(mp3_content)
        
        combine_mp3s(self.intro_music_path, filename, "CombinedOutput.mp3")
        
        messagebox.showinfo("Info", f"Saved the combined spoken file as CombinedOutput.mp3")
        self.preview_window.destroy()

    def regenerate_content(self):
        self.preview_window.destroy()
        self.generate_response()

    def edit_content(self):
        self.text_widget.config(state=tk.NORMAL)

    def start_again(self):
        self.preview_window.destroy()

    def generate_response(self):
        hardcoded_prompt = "Write me 1 cool fact about each of these companies: "
        self.user_input = simpledialog.askstring("Input", "Which 3 companies?")
        
        if not self.user_input:
            return
        
        full_prompt = hardcoded_prompt + self.user_input
        temperature = 0.7
        chatgpt_response = get_response_from_chatgpt(full_prompt, temperature)
        
        self.preview_content(chatgpt_response)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
