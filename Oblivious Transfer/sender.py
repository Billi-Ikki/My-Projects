import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import hashlib
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import socket
import pickle
import json

class ObliviousTransfer:
    """
    Implementation of 1-out-of-2 Oblivious Transfer using the Naor-Pinkas protocol.
    """
    
    def __init__(self, key_size=512):
        """Initialize with parameters for the specified key size."""
        # For demo purposes, we'll use smaller values
        # In production, use larger primes and secure parameters
        self.key_size = key_size
        
        # For small demo, use predefined primes
        if key_size <= 64:
            # Small prime for visualization
            self.p = 2**31 - 1  # A 31-bit Mersenne prime
            self.g = 7  # Generator
        else:
            # For larger keys, we'd use secure parameter generation
            # This is simplified for demonstration
            self.p = self._generate_prime(key_size)
            self.g = 2  # Common generator choice
        
        self.log_callback = None
    
    def set_log_callback(self, callback):
        """Set callback for logging protocol steps."""
        self.log_callback = callback
    
    def log(self, message):
        """Log protocol steps if callback is set."""
        if self.log_callback:
            self.log_callback(message)
    
    def _generate_prime(self, bits):
        """Generate a prime number of the specified bit length."""
        # For demonstration, using a simplified method
        # In production, use proper crypto libraries
        while True:
            # Generate a random odd integer of the specified bit length
            p = random.getrandbits(bits) | 1
            # Check if it's prime (probabilistic test)
            if self._is_probable_prime(p):
                return p
    
    def _is_probable_prime(self, n, k=5):
        """Probabilistic primality test."""
        # Simple implementation of Miller-Rabin
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False
        
        # Write n as 2^r * d + 1
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Witness loop
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    def _derive_key(self, shared_secret, salt=None):
        """Derive encryption key from shared secret."""
        shared_secret_bytes = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, byteorder='big')
        
        if salt is None:
            salt = b'oblivious_transfer_salt'
            
        # Use SHA-256 to derive a key from the shared secret
        key = hashlib.sha256(shared_secret_bytes + salt).digest()
        return key
    
    def _encrypt(self, key, message):
        """Encrypt a message with a key using simple XOR."""
        if isinstance(message, str):
            message = message.encode('utf-8')
            
        # Hash the key to get the right size
        key_hash = hashlib.sha256(key).digest()
        
        # Simple XOR encryption
        encrypted = bytearray()
        for i in range(len(message)):
            encrypted.append(message[i] ^ key_hash[i % len(key_hash)])
            
        return bytes(encrypted)
    
    def _decrypt(self, key, ciphertext):
        """Decrypt a message - XOR is symmetric so use the same method."""
        return self._encrypt(key, ciphertext)


class Sender(ObliviousTransfer):
    """Sender role in the OT protocol."""
    
    def __init__(self, key_size=32):
        super().__init__(key_size)
        # Private values for the sender
        self.x0 = random.randint(1, self.p-1)
        self.x1 = random.randint(1, self.p-1)
        
        # Public values 
        self.C0 = pow(self.g, self.x0, self.p)
        self.C1 = pow(self.g, self.x1, self.p)
        
        self.messages = None
        self.encrypted_messages = None
        self.transfer_keys = None
        
        self.log(f"Sender initialized with parameters:")
        self.log(f"Prime p: {self.p}")
        self.log(f"Generator g: {self.g}")
        self.log(f"Private x0: {self.x0}")
        self.log(f"Private x1: {self.x1}")
        self.log(f"Public C0 = g^x0 mod p: {self.C0}")
        self.log(f"Public C1 = g^x1 mod p: {self.C1}")
    
    def get_public_values(self):
        """Return public values to be sent to the receiver."""
        self.log("Sender sending public values to receiver")
        return {
            'p': self.p,
            'g': self.g,
            'C0': self.C0,
            'C1': self.C1
        }

    def encrypt_messages(self, messages, PK):
        """Encrypt the two messages using the receiver's PK."""
        assert len(messages) == 2, "Must provide exactly 2 messages"
        self.messages = messages
        
        self.log(f"Sender received two messages to encrypt:")
        self.log(f"Message 0: {messages[0]}")
        self.log(f"Message 1: {messages[1]}")
        
        self.encrypted_messages = []
        self.transfer_keys = []
        
        # For message 0
        k0 = pow(PK, self.x0, self.p)
        key0 = self._derive_key(k0)
        self.transfer_keys.append(key0)
        self.encrypted_messages.append(self._encrypt(key0, messages[0]))
        self.log(f"Message 0 encrypted with shared secret: {k0}")
        
        # For message 1
        # If PK = C1 * g^k, then PK/C1 = g^k
        # So (PK/C1)^x1 = g^(k*x1)
        if PK % self.C1 == 0:  # Check if C1 divides PK evenly
            PK_div_C1 = PK // self.C1
        else:
            PK_div_C1 = (PK * pow(self.C1, -1, self.p)) % self.p
        
        k1 = pow(PK_div_C1, self.x1, self.p)
        key1 = self._derive_key(k1)
        self.transfer_keys.append(key1)
        self.encrypted_messages.append(self._encrypt(key1, messages[1]))
        self.log(f"Message 1 encrypted with shared secret: {k1}")
            
        return self.encrypted_messages
    
    def get_calculation_details(self):
        """Get calculation details for visualization purposes."""
        return {
            'x0': self.x0,
            'x1': self.x1,
            'C0': self.C0,
            'C1': self.C1,
            'keys': [k.hex()[:16] + '...' for k in self.transfer_keys] if self.transfer_keys else None,
            'messages': self.messages,
            'encrypted': [e.hex()[:16] + '...' for e in self.encrypted_messages] if self.encrypted_messages else None
        }


class SenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Oblivious Transfer - Sender")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        
        # Set style
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        # Initialize sender
        self.sender = None
        
        # Create network settings
        self.create_header_frame()
        self.create_network_frame()
        self.create_message_frame()
        self.create_log_frame()
        self.create_status_frame()
        
        # Initialize protocol
        self.initialize_protocol()
        
        # Start listening in a separate thread
        self.server_thread = None
        self.is_running = False
    
    def create_header_frame(self):
        """Create the header frame with title."""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="Oblivious Transfer Protocol - Sender",
            style='Header.TLabel'
        )
        title_label.pack(anchor='center', pady=5)
    
    def create_network_frame(self):
        """Create network configuration frame."""
        network_frame = ttk.LabelFrame(self.root, text="Network Configuration")
        network_frame.pack(fill='x', padx=20, pady=5)
        
        # Host and port configuration
        host_port_frame = ttk.Frame(network_frame)
        host_port_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(host_port_frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.host_var = tk.StringVar(value="localhost")
        ttk.Entry(host_port_frame, textvariable=self.host_var, width=15).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(host_port_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.port_var = tk.IntVar(value=12345)
        ttk.Entry(host_port_frame, textvariable=self.port_var, width=6).grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        # Network control buttons
        button_frame = ttk.Frame(network_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        self.start_button = ttk.Button(button_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop Server", command=self.stop_server, state='disabled')
        self.stop_button.pack(side='left', padx=5)
    
    def create_message_frame(self):
        """Create message input frame."""
        message_frame = ttk.LabelFrame(self.root, text="Messages")
        message_frame.pack(fill='x', padx=20, pady=5)
        
        # Message inputs
        ttk.Label(message_frame, text="Message 0:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.message0_var = tk.StringVar(value="Secret document access code")
        ttk.Entry(message_frame, textvariable=self.message0_var, width=40).grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(message_frame, text="Message 1:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.message1_var = tk.StringVar(value="Financial transaction details")
        ttk.Entry(message_frame, textvariable=self.message1_var, width=40).grid(row=1, column=1, sticky='ew', padx=5, pady=5)
    
    def create_log_frame(self):
        """Create the log frame for protocol details."""
        log_frame = ttk.LabelFrame(self.root, text="Protocol Log")
        log_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, wrap=tk.WORD)
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_status_frame(self):
        """Create status frame at the bottom."""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill='x', padx=20, pady=10)
        
        # Status indicator
        self.status_var = tk.StringVar(value="Not connected")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side='left', padx=5)
        
        # Reset button
        self.reset_button = ttk.Button(status_frame, text="Reset Protocol", command=self.initialize_protocol)
        self.reset_button.pack(side='right', padx=5)
    
    def log(self, message):
        """Add message to the log with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
    
    def initialize_protocol(self):
        """Initialize or reset the protocol."""
        # Clear the log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Initialize sender
        self.sender = Sender(key_size=32)  # Using smaller key size for demo
        self.sender.set_log_callback(self.log)
        
        self.log("Protocol initialized. Ready to start server.")
        self.status_var.set("Ready")
    
    def start_server(self):
        """Start the server to listen for receiver connections."""
        if self.is_running:
            return
        
        host = self.host_var.get()
        port = self.port_var.get()
        
        # Start server in a separate thread
        self.server_thread = threading.Thread(target=self.run_server, args=(host, port))
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_var.set(f"Server running on {host}:{port}")
        self.log(f"Server started on {host}:{port}")
    
    def stop_server(self):
        """Stop the server."""
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Server stopped")
        self.log("Server stopped")
    
    def run_server(self, host, port):
        """Run the server to handle receiver connections."""
        try:
            # Create socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.settimeout(1.0)  # 1 second timeout for checking is_running
            server_socket.listen(1)
            
            self.root.after(0, self.log, f"Listening for connections on {host}:{port}")
            
            while self.is_running:
                try:
                    # Accept connection
                    client_socket, addr = server_socket.accept()
                    self.root.after(0, self.log, f"Connection from {addr}")
                    self.root.after(0, self.status_var.set, f"Connected to {addr}")
                    
                    # Handle the connection in a separate thread
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.timeout:
                    # Just a timeout for checking is_running
                    continue
                except Exception as e:
                    self.root.after(0, self.log, f"Error accepting connection: {e}")
            
            server_socket.close()
            
        except Exception as e:
            self.root.after(0, self.log, f"Server error: {e}")
            self.root.after(0, self.status_var.set, "Error")
            self.root.after(0, self.start_button.config, {'state': 'normal'})
            self.root.after(0, self.stop_button.config, {'state': 'disabled'})
            self.is_running = False
    
    def handle_client(self, client_socket):
        """Handle a client connection for the OT protocol."""
        try:
            # Step 1: Send public values to receiver
            public_values = self.sender.get_public_values()
            self.root.after(0, self.log, "Sending public values to receiver")
            client_socket.sendall(json.dumps(public_values).encode())
            
            # Step 2: Receive receiver's public key
            data = client_socket.recv(4096)
            if not data:
                self.root.after(0, self.log, "Connection closed by receiver")
                client_socket.close()
                return
                
            receiver_pk = int(data.decode())
            self.root.after(0, self.log, f"Received receiver's public key: {receiver_pk}")
            
            # Step 3: Encrypt messages
            message0 = self.message0_var.get()
            message1 = self.message1_var.get()
            
            encrypted_messages = self.sender.encrypt_messages([message0, message1], receiver_pk)
            self.root.after(0, self.log, "Messages encrypted")
            
            # Step 4: Send encrypted messages
            self.root.after(0, self.log, "Sending encrypted messages to receiver")
            client_socket.sendall(pickle.dumps(encrypted_messages))
            
            # Step 5: Wait for acknowledgment
            data = client_socket.recv(1024)
            if data:
                self.root.after(0, self.log, f"Received from receiver: {data.decode()}")
            
            self.root.after(0, self.log, "Transfer complete")
            
        except Exception as e:
            self.root.after(0, self.log, f"Error handling client: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = SenderGUI(root)
    root.mainloop()