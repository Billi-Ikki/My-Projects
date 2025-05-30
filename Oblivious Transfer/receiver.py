import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import hashlib
import threading
import time
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


class Receiver(ObliviousTransfer):
    """Receiver role in the OT protocol."""
    
    def __init__(self, key_size=32):
        super().__init__(key_size)
        self.choice = None
        self.k = None  # Private key
        self.PK = None  # Public key to send
        self.decryption_key = None
        
    def choose_message_index(self, index, sender_public):
        """Choose which message to receive (0 or 1)."""
        self.choice = index
        assert index in [0, 1], "Index must be 0 or 1"
        
        # Update parameters from sender
        self.p = sender_public['p']
        self.g = sender_public['g']
        self.C0 = sender_public['C0']
        self.C1 = sender_public['C1']
        
        self.log(f"Receiver choosing message index: {index}")
        self.log(f"Received public values from sender:")
        self.log(f"Prime p: {self.p}")
        self.log(f"Generator g: {self.g}")
        self.log(f"C0: {self.C0}")
        self.log(f"C1: {self.C1}")
        
        # Generate private key
        self.k = random.randint(1, self.p-1)
        self.log(f"Generated private key k: {self.k}")
        
        # Generate public key based on choice
        if index == 0:
            # PK = g^k mod p
            self.PK = pow(self.g, self.k, self.p)
            self.log(f"Generated PK = g^k mod p = {self.PK}")
        else:
            # PK = C1 * g^k mod p
            temp = pow(self.g, self.k, self.p)
            self.PK = (self.C1 * temp) % self.p
            self.log(f"Generated PK = C1 * g^k mod p = {self.PK}")
            
        return self.PK
    
    def decrypt_message(self, encrypted_messages):
        """Decrypt the chosen message."""
        assert self.choice is not None, "Must choose message index first"
        assert len(encrypted_messages) == 2, "Must provide both encrypted messages"
        
        self.log(f"Receiver decrypting message {self.choice}")
        
        # Calculate shared secret based on choice
        if self.choice == 0:
            # For message 0: Key = C0^k mod p
            self.decryption_key = pow(self.C0, self.k, self.p)
            self.log(f"Calculating key = C0^k mod p = {self.decryption_key}")
        else:
            # For message 1: When PK = C1 * g^k, the common key is g^(k*x1)
            # Since we don't know x1 on receiver's side, we use C1 (which is g^x1)
            # Shared secret for message 1 is g^(k*x1) which equals (g^x1)^k = C1^k
            self.decryption_key = pow(self.C1, self.k, self.p)
            self.log(f"Calculating key = C1^k mod p = {self.decryption_key}")
        
        key = self._derive_key(self.decryption_key)
        encrypted = encrypted_messages[self.choice]
        decrypted = self._decrypt(key, encrypted)
        
        try:
            return decrypted.decode('utf-8')
        except UnicodeDecodeError:
            return decrypted.decode('latin-1')
    
    def get_calculation_details(self):
        """Get calculation details for visualization purposes."""
        return {
            'choice': self.choice,
            'k': self.k,
            'PK': self.PK,
            'decryption_key': self.decryption_key
        }


class ReceiverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Oblivious Transfer - Receiver")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        
        # Set style
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        # Initialize receiver
        self.receiver = None
        self.client_socket = None
        self.is_connected = False
        self.decrypted_message = None
        
        # Create UI components
        self.create_header_frame()
        self.create_network_frame()
        self.create_choice_frame()
        self.create_log_frame()
        self.create_result_frame()
        
        # Initialize protocol
        self.initialize_protocol()
    
    def create_header_frame(self):
        """Create the header frame with title."""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="Oblivious Transfer Protocol - Receiver",
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
        
        # Connect button
        button_frame = ttk.Frame(network_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        self.connect_button = ttk.Button(button_frame, text="Connect to Sender", command=self.connect_to_sender)
        self.connect_button.pack(side='left', padx=5)
        
        self.disconnect_button = ttk.Button(button_frame, text="Disconnect", command=self.disconnect, state='disabled')
        self.disconnect_button.pack(side='left', padx=5)
    
    def create_choice_frame(self):
        """Create message choice frame."""
        choice_frame = ttk.LabelFrame(self.root, text="Message Selection")
        choice_frame.pack(fill='x', padx=20, pady=5)
        
        # Choice selection
        choice_inner_frame = ttk.Frame(choice_frame)
        choice_inner_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(choice_inner_frame, text="Choose message to receive:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.choice_var = tk.IntVar(value=0)
        ttk.Radiobutton(choice_inner_frame, text="Message 0", variable=self.choice_var, value=0).grid(row=0, column=1, sticky='w', padx=5, pady=5)
        ttk.Radiobutton(choice_inner_frame, text="Message 1", variable=self.choice_var, value=1).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        
        # Run protocol button
        button_frame = ttk.Frame(choice_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        self.run_button = ttk.Button(button_frame, text="Run Protocol", command=self.run_protocol, state='disabled')
        self.run_button.pack(side='left', padx=5)
    
    def create_log_frame(self):
        """Create the log frame for protocol details."""
        log_frame = ttk.LabelFrame(self.root, text="Protocol Log")
        log_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_result_frame(self):
        """Create frame for showing the results."""
        result_frame = ttk.LabelFrame(self.root, text="Protocol Results")
        result_frame.pack(fill='x', padx=20, pady=5)
        
        # Result text
        self.result_text = scrolledtext.ScrolledText(result_frame, height=5, wrap=tk.WORD)
        self.result_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.result_text.insert(tk.END, "Connect to sender and run the protocol to see results...")
        self.result_text.config(state='disabled')
        
        # Reset button at the bottom
        reset_frame = ttk.Frame(self.root)
        reset_frame.pack(fill='x', padx=20, pady=10)
        
        self.status_var = tk.StringVar(value="Not connected")
        status_label = ttk.Label(reset_frame, textvariable=self.status_var)
        status_label.pack(side='left', padx=5)
        
        self.reset_button = ttk.Button(reset_frame, text="Reset Protocol", command=self.initialize_protocol)
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
        
        # Clear results
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Connect to sender and run the protocol to see results...")
        self.result_text.config(state='disabled')
        
        # Initialize receiver
        self.receiver = Receiver(key_size=32)  # Using smaller key size for demo
        self.receiver.set_log_callback(self.log)
        
        # Reset connection state
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        
        self.is_connected = False
        self.decrypted_message = None
        
        # Reset buttons
        self.connect_button.config(state='normal')
        self.disconnect_button.config(state='disabled')
        self.run_button.config(state='disabled')
        
        self.log("Protocol initialized. Ready to connect to sender.")
        self.status_var.set("Ready")
    
    def connect_to_sender(self):
        """Connect to the sender server."""
        host = self.host_var.get()
        port = self.port_var.get()
        
        try:
            # Create socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            
            self.is_connected = True
            self.connect_button.config(state='disabled')
            self.disconnect_button.config(state='normal')
            self.run_button.config(state='normal')
            
            self.log(f"Connected to sender at {host}:{port}")
            self.status_var.set(f"Connected to {host}:{port}")
            
        except Exception as e:
            self.log(f"Connection error: {e}")
            messagebox.showerror("Connection Error", f"Failed to connect to {host}:{port}: {e}")
            self.status_var.set("Connection failed")
    
    def disconnect(self):
        """Disconnect from the sender."""
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        
        self.is_connected = False
        self.connect_button.config(state='normal')
        self.disconnect_button.config(state='disabled')
        self.run_button.config(state='disabled')
        
        self.log("Disconnected from sender")
        self.status_var.set("Disconnected")
    
    def run_protocol(self):
        """Run the oblivious transfer protocol."""
        if not self.is_connected or not self.client_socket:
            messagebox.showerror("Connection Error", "Not connected to sender")
            return
        
        # Disable UI during protocol execution
        self.run_button.config(state='disabled')
        self.disconnect_button.config(state='disabled')
        
        # Start the protocol in a separate thread
        protocol_thread = threading.Thread(target=self.protocol_thread)
        protocol_thread.daemon = True
        protocol_thread.start()
    
    def protocol_thread(self):
        """Run the protocol in a separate thread."""
        try:
            # Step 1: Receive public values from sender
            self.log("Waiting for sender's public values...")
            data = self.client_socket.recv(4096)
            if not data:
                self.root.after(0, self.log, "Connection closed by sender")
                self.root.after(0, self.disconnect)
                return
            
            sender_public = json.loads(data.decode())
            self.log("Received sender's public values")
            
            # Step 2: Choose message index and generate PK
            choice = self.choice_var.get()
            self.log(f"Choosing message {choice}")
            receiver_pk = self.receiver.choose_message_index(choice, sender_public)
            
            # Step 3: Send PK to sender
            self.log("Sending public key to sender")
            self.client_socket.sendall(str(receiver_pk).encode())
            
            # Step 4: Receive encrypted messages
            self.log("Waiting for encrypted messages...")
            data = self.client_socket.recv(4096)
            if not data:
                self.root.after(0, self.log, "Connection closed by sender")
                self.root.after(0, self.disconnect)
                return
            
            encrypted_messages = pickle.loads(data)
            self.log("Received encrypted messages")
            
            # Step 5: Decrypt chosen message
            self.decrypted_message = self.receiver.decrypt_message(encrypted_messages)
            self.log(f"Decrypted message {choice}: {self.decrypted_message}")
            
            # Step 6: Send acknowledgment to sender
            self.client_socket.sendall(b"Decryption complete")
            
            # Update results
            self.root.after(0, self.update_results)
            
        except Exception as e:
            self.root.after(0, self.log, f"Protocol error: {e}")
            self.root.after(0, messagebox.showerror, "Protocol Error", f"Error during protocol: {e}")
        finally:
            # Re-enable UI
            self.root.after(0, self.run_button.config, {'state': 'normal'})
            self.root.after(0, self.disconnect_button.config, {'state': 'normal'})
    
    def update_results(self):
        """Update the results display."""
        if self.decrypted_message is None:
            return
        
        # Get calculation details
        receiver_details = self.receiver.get_calculation_details()
        
        # Format results
        results = f"Protocol Completed Successfully!\n\n"
        results += f"Receiver chose message {receiver_details['choice']}\n"
        results += f"Decrypted message: {self.decrypted_message}\n\n"
        
        results += "Key Protocol Values:\n"
        results += f"Receiver's private key k: {receiver_details['k']}\n"
        results += f"Receiver's public key PK: {str(receiver_details['PK'])[:10]}...\n"
        results += f"Shared secret key: {str(receiver_details['decryption_key'])[:10]}...\n"
        
        # Update results text
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, results)
        self.result_text.config(state='disabled')
        
        # Show message box with result
        messagebox.showinfo("Protocol Complete", 
                           f"Successfully received message {receiver_details['choice']}:\n\n{self.decrypted_message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiverGUI(root)
    root.mainloop()