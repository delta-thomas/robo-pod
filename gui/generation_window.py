import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from api.openai_api import get_response_from_chatgpt
from api.elevenlabs_api import get_spoken_file_from_eleven_labs
from config.settings import get_openai_config, get_elevenlabs_config, get_texts_config
from utils.audio_utils import combine_mp3s

def show_generation(main_window, back_callback):
    main_window.clear_frame()

    frame = main_window.frame

    company_label = tk.Label(frame, text="Which company to focus on")
    company_label.pack(pady=5)
    company_entry = tk.Entry(frame, width=50)
    company_entry.pack(pady=5)

    generate_button = tk.Button(frame, text="Generate MP3", command=lambda: generate_response(main_window, company_entry.get()))
    generate_button.pack(pady=10)

    tk.Button(frame, text="Back to Navigation", command=back_callback).pack(pady=10)

def generate_response(main_window, company_name):
    openai_config = get_openai_config()
    elevenlabs_config = get_elevenlabs_config()
    texts_config = get_texts_config()

    hardcoded_prompt = texts_config["prompttweak"] + company_name  # Corrected the key here
    chatgpt_response = get_response_from_chatgpt(hardcoded_prompt, **openai_config)
    show_preview(main_window, chatgpt_response, company_name, elevenlabs_config, texts_config)

def show_preview(main_window, chatgpt_response, company_name, elevenlabs_config, texts_config):
    main_window.clear_frame()
    frame = main_window.frame

    text_widget = tk.Text(frame, wrap=tk.WORD, height=10, width=50)
    text_widget.insert(tk.END, chatgpt_response)
    text_widget.pack(padx=10, pady=10)

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Confirm", command=lambda: confirm_content(text_widget.get("1.0", tk.END).strip(), company_name, elevenlabs_config, texts_config)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Regenerate", command=lambda: generate_response(main_window, company_name)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Start Again", command=lambda: show_generation(main_window, main_window.show_navigation)).pack(side=tk.LEFT, padx=5)

def confirm_content(chatgpt_response, company_name, elevenlabs_config, texts_config):
    mp3_content = get_spoken_file_from_eleven_labs(texts_config["welcome"] + chatgpt_response, **elevenlabs_config)

    current_date = datetime.now().strftime('%Y-%m-%d')
    default_filename = f"{current_date}_{company_name.replace(' ', '_')}.mp3"
    save_path = filedialog.asksaveasfilename(title="Save MP3 As", initialfile=default_filename, filetypes=[("MP3 Files", "*.mp3")])

    if not save_path:
        return

    with open(save_path, "wb") as f:
        f.write(mp3_content)

    combine_mp3s("IntroMusic.mp3", save_path, save_path)

    messagebox.showinfo("Info", f"Saved the combined spoken file as {save_path}")
