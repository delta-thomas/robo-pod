import tkinter as tk
from tkinter import messagebox, filedialog
from config.settings import save_config, get_openai_config, get_elevenlabs_config, get_texts_config

def show_settings(main_window, back_callback):
    main_window.clear_frame()

    frame = main_window.frame

    tk.Label(frame, text="Settings").pack(pady=10)

    settings_entries = {}
    config_sections = {
        "OpenAI": get_openai_config(),
        "ElevenLabs": get_elevenlabs_config(),
        "Texts": get_texts_config()
    }

    for section, values in config_sections.items():
        for key, value in values.items():
            tk.Label(frame, text=f"{section} - {key}").pack(pady=5)
            entry = tk.Entry(frame, width=50)
            entry.insert(0, value)
            entry.pack(pady=5)
            settings_entries[(section, key)] = entry

    tk.Button(frame, text="Save", command=lambda: save_and_notify(settings_entries)).pack(pady=10)
    tk.Button(frame, text="Back to Navigation", command=back_callback).pack(pady=10)

def save_and_notify(settings_entries):
    for (section, key), entry in settings_entries.items():
        save_config(section, key, entry.get())
    messagebox.showinfo("Info", "Settings saved successfully!")
