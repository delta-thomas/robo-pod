import tkinter as tk
from .settings_window import show_settings
from .generation_window import show_generation
from .phonetics_window import show_phonetics





class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Delta Stock Market Buffet generator")

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(padx=10, pady=10)

        self.show_navigation()

    def show_navigation(self):
        self.clear_frame()

        tk.Label(self.frame, text="Welcome to the Delta Stock Market Buffet generator!").pack(pady=10)
        tk.Button(self.frame, text="Settings", command=lambda: show_settings(self, self.show_navigation)).pack(pady=10)
        tk.Button(self.frame, text="Generate MP3", command=lambda: show_generation(self, self.show_navigation)).pack(pady=10)
        tk.Button(self.frame, text="Phonetics", command=lambda: show_phonetics(self)).pack(pady=10)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
