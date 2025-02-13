import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ttkbootstrap as tb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

class EncryptionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Encryption Tool")
        self.style = tb.Style("darkly")  # Modern dark theme
        
        # Create Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Tabs
        self.create_encryption_tab()
        self.create_statistics_tab()
        self.create_settings_tab()

    def create_encryption_tab(self):
        self.enc_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.enc_tab, text="Encryption")
        
        # Input Frame
        input_frame = ttk.LabelFrame(self.enc_tab, text="Input")
        input_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(input_frame, text="Enter Text:").pack(anchor="w", padx=5, pady=2)
        self.input_text = scrolledtext.ScrolledText(input_frame, height=5)
        self.input_text.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(input_frame, text="Key (Number/Char/Word):").pack(anchor="w", padx=5, pady=2)
        self.key_entry = ttk.Entry(input_frame)
        self.key_entry.pack(fill="x", padx=5, pady=5)
        
        # Method Selection
        ttk.Label(input_frame, text="Encryption Method:").pack(anchor="w", padx=5, pady=2)
        self.method_var = tk.StringVar(value="Caesar Cipher")
        self.method_menu = ttk.Combobox(input_frame, textvariable=self.method_var, 
                                        values=["Caesar Cipher", "XOR Encryption", "Vigenère Cipher", "Atbash Cipher", "Base64"],
                                        state="readonly")
        self.method_menu.pack(fill="x", padx=5, pady=5)
        
        # Output
        output_frame = ttk.LabelFrame(self.enc_tab, text="Output")
        output_frame.pack(padx=10, pady=10, fill="x")
        self.output_text = scrolledtext.ScrolledText(output_frame, height=5, state="disabled")
        self.output_text.pack(fill="x", padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.enc_tab)
        button_frame.pack(pady=10)
        encrypt_button = ttk.Button(button_frame, text="Encrypt", command=lambda: self.process_text(True))
        encrypt_button.grid(row=0, column=0, padx=5)
        decrypt_button = ttk.Button(button_frame, text="Decrypt", command=lambda: self.process_text(False))
        decrypt_button.grid(row=0, column=1, padx=5)

    def create_statistics_tab(self):
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Statistics")
        
        self.stats_label = ttk.Label(self.stats_tab, text="Character Count: 0", font=("Arial", 12))
        self.stats_label.pack(pady=10)
        
        update_button = ttk.Button(self.stats_tab, text="Update Statistics", command=self.update_statistics)
        update_button.pack(pady=5)

    def update_statistics(self):
        text = self.input_text.get("1.0", tk.END).strip()
        char_count = len(text)
        self.stats_label.config(text=f"Character Count: {char_count}")

    
    def create_settings_tab(self):
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        
        theme_label = ttk.Label(self.settings_tab, text="Select Theme:")
        theme_label.pack(pady=5)
        
        theme_var = tk.StringVar(value="darkly")
        theme_menu = ttk.Combobox(self.settings_tab, textvariable=theme_var, values=self.style.theme_names(), state="readonly")
        theme_menu.pack(pady=5)
        
        apply_button = ttk.Button(self.settings_tab, text="Apply Theme", command=lambda: self.style.theme_use(theme_var.get()))
        apply_button.pack(pady=5)
    
    def process_text(self, is_encrypt):
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get()
        method = self.method_var.get()
        result = ""

        if method == "Caesar Cipher":
            shift = int(key) if key.isdigit() else 3  # Default shift if no key provided
            shift = shift if is_encrypt else -shift
            result = self.caesar_cipher(text, shift)

        elif method == "XOR Encryption":
            key_char = key[0] if key else 'K'  # Default key
            result = self.xor_cipher(text, key_char)

        elif method == "Vigenère Cipher":
            key = key if key else "KEY"  # Default key
            result = self.vigenere_cipher(text, key, is_encrypt)

        elif method == "Atbash Cipher":
            result = self.atbash_cipher(text)

        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)
        self.output_text.config(state="disabled")
    
    def caesar_cipher(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char
        return result
    
    def xor_cipher(self, text, key):
        return ''.join(chr(ord(c) ^ ord(key)) for c in text)
    
    def vigenere_cipher(self, text, key, is_encrypt):
        result = []
        key = key.upper()
        key_index = 0
        for char in text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                shift = shift if is_encrypt else -shift
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base + shift) % 26 + base))
                key_index += 1
            else:
                result.append(char)
        return ''.join(result)
    
    def atbash_cipher(self, text):
        return ''.join(chr(25 - (ord(c) - ord('a')) + ord('a')) if c.islower() else 
                       chr(25 - (ord(c) - ord('A')) + ord('A')) if c.isupper() else c for c in text)

if __name__ == "__main__":
    root = tb.Window(themename="darkly")  # Use ttkbootstrap for modern UI
    app = EncryptionTool(root)
    root.mainloop()
