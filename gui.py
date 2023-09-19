import requests
import tkinter as tk
from tkinter import simpledialog, messagebox, Text, Scrollbar
from datetime import datetime

# OpenAI API details
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = "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"  # Replace with your OpenAI API key

# Eleven Labs API details
ELEVEN_LABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"  # Replace {voice_id} with desired voice ID
ELEVEN_LABS_API_KEY = "a842ce16fb9d66486e6412294dbac613"  # Replace with your Eleven Labs API key

def get_response_from_chatgpt(prompt, temperature=0.7):
    # ... [rest of the function remains unchanged]

def get_spoken_file_from_eleven_labs(text, voice_id):
    # ... [rest of the function remains unchanged]

def content_preview_window(chatgpt_response, user_input):
    preview_window = tk.Toplevel(root)
    preview_window.title("Content Preview")

    label = tk.Label(preview_window, text="Generated Content:")
    label.pack(pady=10)

    text_area = Text(preview_window, wrap=tk.WORD, height=10, width=50)
    text_area.insert(tk.END, chatgpt_response)
    text_area.pack(pady=10)

    scrollbar = Scrollbar(preview_window, command=text_area.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.config(yscrollcommand=scrollbar.set)

    def confirm():
        nonlocal chatgpt_response
        chatgpt_response = text_area.get("1.0", tk.END).strip()
        preview_window.destroy()

        voice_id = "21m00Tcm4TlvDq8ikWAM"
        mp3_content = get_spoken_file_from_eleven_labs(chatgpt_response, voice_id)

        # Set default filename
        current_date = datetime.now().strftime('%Y-%m-%d')
        default_filename = f"{current_date}_{user_input.replace(' ', '_')}.mp3"
        filename = simpledialog.askstring("Filename", "Enter filename for the mp3:", initialvalue=default_filename)

        with open(filename, "wb") as f:
            f.write(mp3_content)

        messagebox.showinfo("Info", f"Saved the spoken file as {filename}")

        # Option to start again
        start_again = messagebox.askyesno("Start Again?", "Would you like to generate another mp3?")
        if start_again:
            generate_response()

    def regenerate():
        preview_window.destroy()
        regenerate_response = get_response_from_chatgpt(full_prompt, temperature)
        content_preview_window(regenerate_response, user_input)

    def start_over():
        preview_window.destroy()

    confirm_button = tk.Button(preview_window, text="Confirm", command=confirm)
    confirm_button.pack(side=tk.LEFT, padx=10)

    regenerate_button = tk.Button(preview_window, text="Regenerate", command=regenerate)
    regenerate_button.pack(side=tk.LEFT, padx=10)

    edit_button = tk.Button(preview_window, text="Edit", command=lambda: text_area.focus_set())
    edit_button.pack(side=tk.LEFT, padx=10)

    start_over_button = tk.Button(preview_window, text="Start Over", command=start_over)
    start_over_button.pack(side=tk.LEFT, padx=10)

def generate_response():
    hardcoded_prompt = "Write me 1 cool fact about each of these companies: "
    user_input = simpledialog.askstring("Input", "Which 3 companies?")

    if not user_input:
        return

    full_prompt = hardcoded_prompt + user_input
    temperature = 0.7  # You can adjust this or ask the user for input
    chatgpt_response
