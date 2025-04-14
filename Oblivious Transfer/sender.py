import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import socket
import os
import json

class SecureMessageExchangeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Message Exchange")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        
        # Server status variables
        self.server_running = False
        self.server_thread = None
        
        # Default settings
        self.host = "localhost"
        self.port = 5000
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 11))
        self.style.configure("TButton", font=("Arial", 11))
        self.style.configure("TEntry", font=("Arial", 11))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        
        # Create the GUI elements
        self.create_gui()
    
    def create_gui(self):
        # Title
        ttk.Label(self.main_frame, text="Secure Message Exchange Server", 
                  style="Header.TLabel").grid(row=0, column=0, columnspan=3, pady=10)
        
        # Server settings frame
        settings_frame = ttk.LabelFrame(self.main_frame, text="Server Settings", padding=10)
        settings_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(settings_frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.host_entry = ttk.Entry(settings_frame, width=20)
        self.host_entry.insert(0, self.host)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(settings_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.port_entry = ttk.Entry(settings_frame, width=10)
        self.port_entry.insert(0, str(self.port))
        self.port_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Messages frame
        messages_frame = ttk.LabelFrame(self.main_frame, text="Messages", padding=10)
        messages_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        
        ttk.Label(messages_frame, text="Message for Choice 0:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.message0_entry = ttk.Entry(messages_frame, width=40)
        self.message0_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(messages_frame, text="Message for Choice 1:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.message1_entry = ttk.Entry(messages_frame, width=40)
        self.message1_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Control buttons
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        
        self.start_button = ttk.Button(controls_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(controls_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(controls_frame, text="Clear Log", command=self.clear_log)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Log area
        log_frame = ttk.LabelFrame(self.main_frame, text="Server Log", padding=10)
        log_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=80, height=15)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.config(state=tk.DISABLED)
        
        # Configure grid weights to make the UI responsive
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(4, weight=1)
        messages_frame.columnconfigure(1, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Server Status: Not running")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
    
    def clear_log(self):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)
    
    def start_server(self):
        if self.server_running:
            return
        
        try:
            self.host = self.host_entry.get()
            self.port = int(self.port_entry.get())
            
            if not self.message0_entry.get() or not self.message1_entry.get():
                messagebox.showerror("Error", "Both messages must be provided!")
                return
                
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.server_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.host_entry.config(state=tk.DISABLED)
            self.port_entry.config(state=tk.DISABLED)
            self.message0_entry.config(state=tk.DISABLED)
            self.message1_entry.config(state=tk.DISABLED)
            
            self.status_var.set(f"Server Status: Running on {self.host}:{self.port}")
            self.log(f"Server started on {self.host}:{self.port}")
            
        except ValueError:
            messagebox.showerror("Error", "Port must be a valid number!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
    
    def stop_server(self):
        if not self.server_running:
            return
            
        self.server_running = False
        
        try:
            # Connect to our own server to trigger socket.accept() to return
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.close()
        except:
            pass
            
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.host_entry.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.NORMAL)
        self.message0_entry.config(state=tk.NORMAL)
        self.message1_entry.config(state=tk.NORMAL)
        
        self.status_var.set("Server Status: Stopped")
        self.log("Server stopped")
    
    def generate_rsa_keys(self, bits=1024):
        self.log("Generating RSA keys...")
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        n = p * q
        phi = (p-1)*(q-1)
        e = 65537
        d = pow(e, -1, phi)
        self.log("RSA keys generated successfully")
        return (n, e), (n, d)
    
    def pad_message(self, message, block_size=16):
        pad_len = block_size - (len(message) % block_size)
        return message + bytes([pad_len] * pad_len)
    
    def unpad_message(self, padded_message):
        pad_len = padded_message[-1]
        return padded_message[:-pad_len]
    
    def encrypt_aes(self, key, message):
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_msg = self.pad_message(message)
        ciphertext = cipher.encrypt(padded_msg)
        return iv + ciphertext
    
    def hash_to_key(self, value, n):
        h = SHA256.new(long_to_bytes(value % n)).digest()[:16]
        return h
    
    def run_server(self):
        try:
            # Get messages from the GUI
            m0 = self.message0_entry.get().encode()
            m1 = self.message1_entry.get().encode()
            
            # Generate RSA keys
            self.log("Generating RSA keys...")
            public_key, private_key = self.generate_rsa_keys()
            n, e = public_key
            self.log(f"Public key (n, e): ({n}, {e})")
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((self.host, self.port))
                s.listen()
                self.log(f"Server listening on {self.host}:{self.port}")
                
                s.settimeout(1.0)  # Add timeout to allow for server stopping
                
                while self.server_running:
                    try:
                        conn, addr = s.accept()
                        self.log(f"Connected by {addr}")
                        
                        with conn:
                            # Send public key to client
                            public_key_json = json.dumps({'n': n, 'e': e})
                            conn.sendall(public_key_json.encode())
                            self.log(f"Sent public key: {public_key_json}")
                            
                            # Receive 'c' from client
                            data = conn.recv(1024)
                            client_data = json.loads(data.decode())
                            c = int(client_data['c'])
                            self.log(f"Received c: {c}")
                            
                            # Process both possibilities
                            k = n - 1  # Simplified non-residue
                            k0 = pow(c, private_key[1], n)
                            k1 = pow((c * pow(k, -1, n)) % n, private_key[1], n)
                            
                            aes_key0 = self.hash_to_key(k0, n)
                            aes_key1 = self.hash_to_key(k1, n)
                            
                            e0 = self.encrypt_aes(aes_key0, m0)
                            e1 = self.encrypt_aes(aes_key1, m1)
                            
                            # Send both encrypted messages
                            response = {
                                'e0': e0.hex(),
                                'e1': e1.hex()
                            }
                            conn.sendall(json.dumps(response).encode())
                            
                            self.log("Sent both encrypted messages")
                            self.log(f"Message 0 encrypted: {e0.hex()[:30]}...")
                            self.log(f"Message 1 encrypted: {e1.hex()[:30]}...")
                            self.log("Transaction completed\n")
                        
                    except socket.timeout:
                        continue
                    except ConnectionResetError:
                        self.log("Connection reset by client")
                    except Exception as e:
                        self.log(f"Error in connection: {str(e)}")
                        
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Server Error", str(e)))
            self.log(f"Server error: {str(e)}")
        finally:
            self.root.after(0, lambda: self.stop_server())

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureMessageExchangeApp(root)
    root.mainloop()