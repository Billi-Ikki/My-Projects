import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import socket
import os
import json
import time

class SecureMessageClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Message Client")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        
        # Client status variables
        self.client_running = False
        self.client_thread = None
        
        # Default settings
        self.host = "localhost"
        self.port = 5000
        self.choice = 0
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 11))
        self.style.configure("TButton", font=("Arial", 11))
        self.style.configure("TEntry", font=("Arial", 11))
        self.style.configure("TRadiobutton", font=("Arial", 11))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        
        # Create the GUI elements
        self.create_gui()
    
    def create_gui(self):
        # Title
        ttk.Label(self.main_frame, text="Secure Message Client", 
                  style="Header.TLabel").grid(row=0, column=0, columnspan=3, pady=10)
        
        # Server connection frame
        connection_frame = ttk.LabelFrame(self.main_frame, text="Server Connection", padding=10)
        connection_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(connection_frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.host_entry = ttk.Entry(connection_frame, width=20)
        self.host_entry.insert(0, self.host)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(connection_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.insert(0, str(self.port))
        self.port_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Choice frame
        choice_frame = ttk.LabelFrame(self.main_frame, text="Message Choice", padding=10)
        choice_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        
        self.choice_var = tk.IntVar(value=self.choice)
        
        self.choice0_radio = ttk.Radiobutton(choice_frame, text="Choice 0", variable=self.choice_var, value=0)
        self.choice0_radio.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        self.choice1_radio = ttk.Radiobutton(choice_frame, text="Choice 1", variable=self.choice_var, value=1)
        self.choice1_radio.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        
        ttk.Label(choice_frame, text="Select which message you want to receive from the server").grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Control buttons
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        
        self.connect_button = ttk.Button(controls_frame, text="Connect & Retrieve Message", command=self.start_client)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(controls_frame, text="Clear Log", command=self.clear_log)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Message display area
        message_frame = ttk.LabelFrame(self.main_frame, text="Received Message", padding=10)
        message_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        
        self.message_display = scrolledtext.ScrolledText(message_frame, wrap=tk.WORD, width=80, height=3, font=("Arial", 11))
        self.message_display.pack(fill=tk.BOTH, expand=True)
        self.message_display.config(state=tk.DISABLED)
        
        # Log area
        log_frame = ttk.LabelFrame(self.main_frame, text="Client Log", padding=10)
        log_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=80, height=12)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.config(state=tk.DISABLED)
        
        # Configure grid weights to make the UI responsive
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(5, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
    
    def clear_log(self):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)
        
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete(1.0, tk.END)
        self.message_display.config(state=tk.DISABLED)
    
    def display_message(self, message):
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete(1.0, tk.END)
        self.message_display.insert(tk.END, message)
        self.message_display.config(state=tk.DISABLED)
    
    def start_client(self):
        if self.client_running:
            return
        
        try:
            self.host = self.host_entry.get()
            self.port = int(self.port_entry.get())
            self.choice = self.choice_var.get()
            
            self.client_thread = threading.Thread(target=self.run_client)
            self.client_thread.daemon = True
            self.client_thread.start()
            
            self.client_running = True
            self.connect_button.config(state=tk.DISABLED)
            self.host_entry.config(state=tk.DISABLED)
            self.port_entry.config(state=tk.DISABLED)
            self.choice0_radio.config(state=tk.DISABLED)
            self.choice1_radio.config(state=tk.DISABLED)
            
            self.status_var.set(f"Status: Connecting to {self.host}:{self.port}...")
            
        except ValueError:
            messagebox.showerror("Error", "Port must be a valid number!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start client: {str(e)}")
    
    def pad_message(self, message, block_size=16):
        pad_len = block_size - (len(message) % block_size)
        return message + bytes([pad_len] * pad_len)

    def unpad_message(self, padded_message):
        pad_len = padded_message[-1]
        return padded_message[:-pad_len]

    def decrypt_aes(self, key, ciphertext):
        iv = ciphertext[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_msg = cipher.decrypt(ciphertext[16:])
        return self.unpad_message(padded_msg)

    def hash_to_key(self, value, n):
        h = SHA256.new(long_to_bytes(value % n)).digest()[:16]
        return h
    
    def run_client(self):
        try:
            self.log(f"Connecting to server at {self.host}:{self.port}")
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)  # Set timeout to prevent hanging
                s.connect((self.host, self.port))
                self.log(f"Connected to server at {self.host}:{self.port}")
                self.status_var.set(f"Status: Connected to {self.host}:{self.port}")
                
                # Receive public key from server
                data = s.recv(1024)
                public_key = json.loads(data.decode())
                n, e = public_key['n'], public_key['e']
                self.log(f"Received public key: (n, e) = ({n}, {e})")
                
                # Prepare choice-dependent value
                x = bytes_to_long(os.urandom(64)) % n
                k = n - 1  # Same non-residue as server
                
                self.log(f"Using choice: {self.choice}")
                if self.choice == 0:
                    c = pow(x, e, n)
                    self.log("Calculating c = x^e mod n")
                else:
                    c = (k * pow(x, e, n)) % n
                    self.log("Calculating c = k * x^e mod n")
                    
                # Send 'c' to server
                s.sendall(json.dumps({'c': c}).encode())
                self.log(f"Sent c to server: {c}")
                
                # Receive encrypted messages
                self.log("Waiting for encrypted messages from server...")
                data = s.recv(4096)
                messages = json.loads(data.decode())
                e0 = bytes.fromhex(messages['e0'])
                e1 = bytes.fromhex(messages['e1'])
                self.log("Received encrypted messages from server")
                
                # Decrypt chosen message
                aes_key = self.hash_to_key(x, n)
                self.log(f"Generated AES key from seed x")
                
                if self.choice == 0:
                    result = self.decrypt_aes(aes_key, e0)
                    self.log("Decrypting message 0")
                else:
                    result = self.decrypt_aes(aes_key, e1)
                    self.log("Decrypting message 1")
                    
                decoded_message = result.decode()
                self.log(f"Successfully decrypted message: {decoded_message}")
                
                # Update UI with the message
                self.root.after(0, lambda: self.display_message(decoded_message))
                self.root.after(0, lambda: self.status_var.set("Status: Message received successfully"))
                
        except socket.timeout:
            self.log("Connection timed out")
            self.root.after(0, lambda: self.status_var.set("Status: Connection timed out"))
            self.root.after(0, lambda: messagebox.showerror("Error", "Connection to server timed out"))
        except ConnectionRefusedError:
            self.log("Connection refused - server may not be running")
            self.root.after(0, lambda: self.status_var.set("Status: Connection refused"))
            self.root.after(0, lambda: messagebox.showerror("Error", "Connection refused - server may not be running"))
        except Exception as e:
            self.log(f"Error: {str(e)}")
            self.root.after(0, lambda: self.status_var.set(f"Status: Error - {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.client_running = False
            self.root.after(0, lambda: self.connect_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.host_entry.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.port_entry.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.choice0_radio.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.choice1_radio.config(state=tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureMessageClientApp(root)
    root.mainloop()