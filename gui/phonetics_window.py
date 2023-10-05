import tkinter as tk
import json
import os

def show_phonetics(main_window, text_widget=None):
    try:
        with open("phonetics.json", "r") as f:
            saved_phonetics_dict = json.load(f)
    except Exception as e:
        print(f"Error loading phonetics: {e}")
        saved_phonetics_dict = {}
        for i, (ticker, phonetic) in enumerate(saved_phonetics_dict.items()):
            if i < 10:  # Assuming a maximum of 10 entries for simplicity
                ticker_entries[i].insert(0, ticker)
                phonetic_entries[i].insert(0, phonetic)

    phonetics_window = tk.Toplevel(main_window.root)
    phonetics_window.title("Phonetics Library")

    ticker_label = tk.Label(phonetics_window, text="Ticker Symbol")
    ticker_label.grid(row=0, column=0)
    phonetic_label = tk.Label(phonetics_window, text="Phonetical Writing")
    phonetic_label.grid(row=0, column=1)
    check_label = tk.Label(phonetics_window, text="Select")
    check_label.grid(row=0, column=2)

    ticker_entries = []
    phonetic_entries = []
    check_vars = []

    for i in range(1, 11):  # Assuming a maximum of 10 entries for simplicity
        ticker_entry = tk.Entry(phonetics_window)
        ticker_entry.grid(row=i, column=0)
        ticker_entries.append(ticker_entry)

        phonetic_entry = tk.Entry(phonetics_window)
        phonetic_entry.grid(row=i, column=1)
        phonetic_entries.append(phonetic_entry)

        check_var = tk.BooleanVar()
        check_button = tk.Checkbutton(phonetics_window, variable=check_var)
        check_button.grid(row=i, column=2)
        check_vars.append(check_var)

    def apply_phonetics():
        selected_tickers = {}
        for ticker, phonetic, check_var in zip(ticker_entries, phonetic_entries, check_vars):
            if ticker.get() and phonetic.get() and check_var.get():
                selected_tickers[ticker.get()] = phonetic.get()

        if text_widget:  # Only replace tickers if text_widget is provided
            replace_tickers(text_widget, selected_tickers)
        phonetics_window.destroy()
        
    def save_and_close():
        phonetics_dict = {}
        for ticker, phonetic in zip(ticker_entries, phonetic_entries):
            if ticker.get() and phonetic.get():
                phonetics_dict[ticker.get()] = phonetic.get()

        with open("phonetics.json", "w") as f:
            json.dump(phonetics_dict, f)
   
        phonetics_window.destroy()

    save_button = tk.Button(phonetics_window, text="Save", command=save_and_close)
    save_button.grid(row=13, column=0, pady=10)

    cancel_button = tk.Button(phonetics_window, text="Cancel", command=phonetics_window.destroy)
    cancel_button.grid(row=13, column=1, pady=10)

    def replace_tickers(text_widget, selected_tickers):

        with open("phonetics.json", "r") as f:
            phonetics_dict = json.load(f)

        text = text_widget.get("1.0", tk.END)
        for ticker, phonetic in selected_tickers.items():
            text = text.replace(ticker, phonetic)

        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, text)


