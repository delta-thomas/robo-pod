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

    company_label = tk.Label(frame, text="Paste up to 3 WIIM snippets")
    company_label.pack(pady=5)

    # Three company entry boxes
    company_entry1 = tk.Entry(frame, width=50)
    company_entry1.pack(pady=5)
    company_entry2 = tk.Entry(frame, width=50)
    company_entry2.pack(pady=5)
    company_entry3 = tk.Entry(frame, width=50)
    company_entry3.pack(pady=5)

    generate_button = tk.Button(frame, text="Generate Script", command=lambda: generate_response(main_window, company_entry1.get(), company_entry2.get(), company_entry3.get()))
    generate_button.pack(pady=10)

    tk.Button(frame, text="Back Home", command=back_callback).pack(pady=10)

def generate_response(main_window, company_name1, company_name2, company_name3):
    # Concatenate the company names with square brackets
    combined_company_name = "[" + company_name1 + "], [" + company_name2 + "], [" + company_name3 + "]"

    openai_config = get_openai_config()
    elevenlabs_config = get_elevenlabs_config()
    texts_config = get_texts_config()

    hardcoded_prompt = texts_config["prompttweak"] + combined_company_name
    chatgpt_response = get_response_from_chatgpt(hardcoded_prompt, **openai_config)
    show_preview(main_window, chatgpt_response, combined_company_name, elevenlabs_config, texts_config)

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
    tk.Button(button_frame, text="Return to the beginning", command=lambda: show_generation(main_window, main_window.show_navigation)).pack(side=tk.LEFT, padx=5)

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
