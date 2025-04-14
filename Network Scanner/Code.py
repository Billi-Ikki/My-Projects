import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from scapy.all import *
from ipaddress import IPv4Network
import sys
import io
import threading

class RedirectOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        
    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        
    def flush(self):
        pass

class NetworkScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Scanning toolkit")
        self.root.geometry("1000x700")
        self.setup_style()
        self.create_widgets()
        self.setup_output_redirect()
        
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2E3440')
        style.configure('TLabel', background='#2E3440', foreground='#D8DEE9')
        style.configure('TButton', background='#3B4252', foreground='#D8DEE9')
        style.configure('TRadiobutton', background='#2E3440', foreground='#D8DEE9')
        style.map('TButton', background=[('active', '#4C566A')])
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scan Selection
        scan_frame = ttk.LabelFrame(main_frame, text="Scan Configuration")
        scan_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        self.scan_var = tk.StringVar(value='icmp')
        scans = [
            ('ICMP Ping', 'icmp'),
            ('TCP ACK Ping', 'tcp_ack'),
            ('SCTP Init Ping', 'sctp_init'),
            ('ICMP Timestamp Ping', 'icmp_timestamp'),
            ('ICMP Address Mask Ping', 'icmp_address_mask'),
            ('ARP Ping', 'arp'),
            ('Find MAC Address', 'find_mac'),
            ('OS Detection', 'os'),
            ('Advanced Scan', 'advanced')
        ]
        
        for i, (text, val) in enumerate(scans):
            rb = ttk.Radiobutton(scan_frame, text=text, variable=self.scan_var, 
                                 value=val, command=self.update_input_fields)
            rb.grid(row=i//2, column=i%2, sticky='w', padx=5, pady=2)
        
        # Input Fields
        input_frame = ttk.LabelFrame(main_frame, text="Target Parameters")
        input_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        ttk.Label(input_frame, text="Target IP/Range:").grid(row=0, column=0, sticky='w')
        self.target_entry = ttk.Entry(input_frame, width=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Ports (comma-separated):").grid(row=1, column=0, sticky='w')
        self.ports_entry = ttk.Entry(input_frame, width=30)
        self.ports_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Protocols (comma-separated):").grid(row=2, column=0, sticky='w')
        self.protocols_entry = ttk.Entry(input_frame, width=30)
        self.protocols_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # Advanced Options
        self.adv_scan_var = tk.StringVar()
        self.adv_scan_combo = ttk.Combobox(input_frame, textvariable=self.adv_scan_var,
                                           values=['TCP Connect', 'UDP', 'TCP NULL', 'TCP FIN', 
                                                   'Xmas', 'TCP ACK', 'TCP Window', 
                                                   'TCP Maimon', 'IP Protocol'])
        self.adv_scan_combo.grid(row=3, column=1, padx=5, pady=2)
        
        # Control Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, sticky='ew', pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="Start Scan", command=self.start_scan)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Clear Results", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        
        # Results Output
        output_frame = ttk.LabelFrame(main_frame, text="Scan Results")
        output_frame.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
        
        self.output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                     bg='#2E3440', fg='#D8DEE9',
                                                     insertbackground='white')
        self.output_area.pack(fill=tk.BOTH, expand=True)
        
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        self.update_input_fields()
        
    def setup_output_redirect(self):
        redirect = RedirectOutput(self.output_area)
        sys.stdout = redirect
        sys.stderr = redirect
        
    def update_input_fields(self):
        # Clear all input fields when the scan type changes
        # self.target_entry.delete(0, tk.END)
        # self.ports_entry.delete(0, tk.END)
        # self.protocols_entry.delete(0, tk.END)
        
        # Update the state of input fields based on the selected scan type
        scan_type = self.scan_var.get()
        self.ports_entry.config(state='normal')
        self.protocols_entry.config(state='normal')
        self.adv_scan_combo.config(state='normal')
        
        if scan_type == 'advanced':
            adv_type = self.adv_scan_var.get()
            self.ports_entry.config(state='normal')
            self.protocols_entry.config(state='normal')
        else:
            self.protocols_entry.config(state='disabled')
            self.adv_scan_combo.config(state='disabled')
            self.ports_entry.config(state='disabled')


    def validate_inputs(self):
        scan_type = self.scan_var.get()
        target = self.target_entry.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target IP or range")
            return False
            
        # Validate ports for scans that require them
        if scan_type == 'advanced' and self.adv_scan_var.get() != 'IP Protocol':
            if not self.ports_entry.get().strip():
                messagebox.showerror("Error", "Please enter ports to scan")
                return False
        
        # Validate protocols for IP Protocol Scan
        if scan_type == 'advanced' and self.adv_scan_var.get() == 'IP Protocol':
            if not self.protocols_entry.get().strip():
                messagebox.showerror("Error", "Please enter protocols to scan")
                return False
        
        return True
        
    def start_scan(self):
        if not self.validate_inputs():
            return
            
        self.start_btn.config(state='disabled')
        scan_thread = threading.Thread(target=self.run_scan)
        scan_thread.start()
        
    def run_scan(self):
        try:
            scan_type = self.scan_var.get()
            target = self.target_entry.get().strip()
            ports = [int(p) for p in self.ports_entry.get().split(',')] if self.ports_entry.get() else []
            protocols = [int(p) for p in self.protocols_entry.get().split(',')] if self.protocols_entry.get() else []
            
            if scan_type == 'icmp':
                icmp_ping_scan(target)
            elif scan_type == 'tcp_ack':
                tcp_ack_ping(target)
            elif scan_type == 'sctp_init':
                sctp_init_ping(target)
            elif scan_type == 'icmp_timestamp':
                icmp_timestamp_ping(target)
            elif scan_type == 'icmp_address_mask':
                icmp_address_mask_ping(target)
            elif scan_type == 'arp':
                arp_ping(target)
            elif scan_type == 'find_mac':
                find_mac_address(target)
            elif scan_type == 'os':
                os_detection(target)
            elif scan_type == 'port':
                tcp_connect_scan(target, ports)
            elif scan_type == 'udp':
                udp_scan(target, ports)
            elif scan_type == 'advanced':
                adv_type = self.adv_scan_var.get()
                if adv_type == 'TCP Connect':
                    tcp_connect_scan(target, ports)
                elif adv_type == 'TCP NULL':
                    tcp_null_scan(target, ports)
                elif adv_type == 'TCP FIN':
                    tcp_fin_scan(target, ports)
                elif adv_type == 'Xmas':
                    xmas_scan(target, ports)
                elif adv_type == 'UDP':
                    udp_scan(target, ports)
                elif adv_type == 'TCP ACK':
                    tcp_ack_scan(target, ports)
                elif adv_type == 'TCP Window':
                    tcp_window_scan(target, ports)
                elif adv_type == 'TCP Maimon':
                    tcp_maimon_scan(target, ports)
                elif adv_type == 'IP Protocol':
                    ip_protocol_scan(target, protocols)
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            self.start_btn.config(state='normal')
        
    def clear_output(self):
        self.output_area.delete(1.0, tk.END)

# Scanning Functions
def icmp_ping_scan(ip_range):
    """Perform ICMP Echo Request scan."""
    print(f"\n=== Starting ICMP Ping Scan on {ip_range} ===")
    live_hosts = []
    for ip in IPv4Network(ip_range, strict=False).hosts():
        ip_str = str(ip)
        response = sr1(IP(dst=ip_str)/ICMP(), timeout=1, verbose=0)
        status = "Up" if response else "Down"
        print(f"{ip_str}: {status}")
        if response:
            live_hosts.append(ip_str)
    print(f"Scan complete. Found {len(live_hosts)} live hosts\n")
    return live_hosts

def tcp_ack_ping(ip_range):
    """Perform TCP ACK Ping scan."""
    print(f"\n=== Starting TCP ACK Ping Scan on {ip_range} ===")
    live_hosts = []
    for ip in IPv4Network(ip_range, strict=False).hosts():
        ip_str = str(ip)
        response = sr1(IP(dst=ip_str)/TCP(dport=80, flags="A"), timeout=1, verbose=0)
        status = "Up" if response else "Down"
        print(f"{ip_str}: {status}")
        if response:
            live_hosts.append(ip_str)
    print(f"Scan complete. Found {len(live_hosts)} live hosts\n")
    return live_hosts

def sctp_init_ping(ip_range):
    """Perform SCTP INIT Ping scan."""
    print(f"\n=== Starting SCTP INIT Ping Scan on {ip_range} ===")
    live_hosts = []
    for ip in IPv4Network(ip_range, strict=False).hosts():
        ip_str = str(ip)
        response = sr1(IP(dst=ip_str)/SCTP(dport=80), timeout=1, verbose=0)
        status = "Up" if response else "Down"
        print(f"{ip_str}: {status}")
        if response:
            live_hosts.append(ip_str)
    print(f"Scan complete. Found {len(live_hosts)} live hosts\n")
    return live_hosts

def icmp_timestamp_ping(ip_range):
    """Perform ICMP Timestamp Ping scan."""
    print(f"\n=== Starting ICMP Timestamp Ping Scan on {ip_range} ===")
    live_hosts = []
    for ip in IPv4Network(ip_range, strict=False).hosts():
        ip_str = str(ip)
        response = sr1(IP(dst=ip_str)/ICMP(type=13), timeout=1, verbose=0)
        status = "Up" if response else "Down"
        print(f"{ip_str}: {status}")
        if response:
            live_hosts.append(ip_str)
    print(f"Scan complete. Found {len(live_hosts)} live hosts\n")
    return live_hosts

def icmp_address_mask_ping(ip_range):
    """Perform ICMP Address Mask Ping scan."""
    print(f"\n=== Starting ICMP Address Mask Ping Scan on {ip_range} ===")
    live_hosts = []
    for ip in IPv4Network(ip_range, strict=False).hosts():
        ip_str = str(ip)
        response = sr1(IP(dst=ip_str)/ICMP(type=17), timeout=1, verbose=0)
        status = "Up" if response else "Down"
        print(f"{ip_str}: {status}")
        if response:
            live_hosts.append(ip_str)
    print(f"Scan complete. Found {len(live_hosts)} live hosts\n")
    return live_hosts

def arp_ping(ip_range):
    """Perform ARP Ping scan."""
    print(f"\n=== Starting ARP Ping Scan on {ip_range} ===")
    live_hosts = []
    for ip in IPv4Network(ip_range, strict=False).hosts():
        ip_str = str(ip)
        response = sr1(ARP(pdst=ip_str), timeout=1, verbose=0)
        if response:
            print(f"{ip_str} - MAC: {response.hwsrc}")
            live_hosts.append((ip_str, response.hwsrc))
    print(f"Scan complete. Found {len(live_hosts)} devices\n")
    return live_hosts

def find_mac_address(ip):
    """Find MAC address of a specific IP."""
    print(f"\n=== Finding MAC Address for {ip} ===")
    response = sr1(ARP(pdst=ip), timeout=1, verbose=0)
    if response:
        print(f"MAC Address: {response.hwsrc}")
    else:
        print("No response from target.")
    print()

def os_detection(ip):
    """Detect OS based on TTL value."""
    print(f"\n=== Starting OS Detection for {ip} ===")
    response = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=0)
    if response:
        ttl = response.ttl
        os_type = "Linux/Unix" if ttl <= 64 else "Windows" if ttl <= 128 else "Unknown"
        print(f"Detected OS: {os_type} (TTL={ttl})")
    else:
        print("No response from target.")
    print()

def tcp_connect_scan(ip, ports):
    """Perform TCP Connect Scan."""
    print(f"\n=== Starting TCP Connect Scan on {ip}:{ports} ===")
    open_ports = []
    for port in ports:
        response = sr1(IP(dst=ip)/TCP(dport=port, flags="S"), timeout=1, verbose=0)
        if response and response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:  # SYN-ACK
            print(f"Port {port}: Open")
            open_ports.append(port)
            sr1(IP(dst=ip)/TCP(dport=port, flags="R"), timeout=1, verbose=0)  # Send RST
        else:
            print(f"Port {port}: Closed")
    print(f"Scan complete. Found {len(open_ports)} open ports\n")
    return open_ports

def udp_scan(ip, ports):
    """Perform UDP Scan."""
    print(f"\n=== Starting UDP Scan on {ip}:{ports} ===")
    open_ports = []
    for port in ports:
        response = sr1(IP(dst=ip)/UDP(dport=port), timeout=1, verbose=0)
        if response is None:
            print(f"Port {port}: Open|Filtered")
            open_ports.append(port)
        elif response.haslayer(ICMP):
            print(f"Port {port}: Closed")
    print(f"Scan complete. Found {len(open_ports)} open|filtered ports\n")
    return open_ports

def tcp_null_scan(ip, ports):
    """Perform TCP Null Scan."""
    print(f"\n=== Starting TCP Null Scan on {ip}:{ports} ===")
    open_filtered_ports = []
    for port in ports:
        response = sr1(IP(dst=ip)/TCP(dport=port, flags=""), timeout=1, verbose=0)
        if response is None:
            print(f"Port {port}: Open|Filtered")
            open_filtered_ports.append(port)
        elif response.haslayer(TCP) and response.getlayer(TCP).flags == 0x14:  # RST
            print(f"Port {port}: Closed")
    print(f"Scan complete. Found {len(open_filtered_ports)} open|filtered ports\n")
    return open_filtered_ports

def tcp_fin_scan(ip, ports):
    """Perform TCP FIN Scan."""
    print(f"\n=== Starting TCP FIN Scan on {ip}:{ports} ===")
    open_filtered_ports = []
    for port in ports:
        response = sr1(IP(dst=ip)/TCP(dport=port, flags="F"), timeout=1, verbose=0)
        if response is None:
            print(f"Port {port}: Open|Filtered")
            open_filtered_ports.append(port)
        elif response.haslayer(TCP) and response.getlayer(TCP).flags == 0x14:  # RST
            print(f"Port {port}: Closed")
    print(f"Scan complete. Found {len(open_filtered_ports)} open|filtered ports\n")
    return open_filtered_ports

def xmas_scan(ip, ports):
    """Perform Xmas Scan."""
    print(f"\n=== Starting Xmas Scan on {ip}:{ports} ===")
    open_filtered_ports = []
    for port in ports:
        response = sr1(IP(dst=ip)/TCP(dport=port, flags="FPU"), timeout=1, verbose=0)
        if response is None:
            print(f"Port {port}: Open|Filtered")
            open_filtered_ports.append(port)
        elif response.haslayer(TCP) and response.getlayer(TCP).flags == 0x14:  # RST
            print(f"Port {port}: Closed")
    print(f"Scan complete. Found {len(open_filtered_ports)} open|filtered ports\n")
    return open_filtered_ports

def tcp_ack_scan(ip, ports):
    """Perform TCP ACK Scan."""
    print(f"\n=== Starting TCP ACK Scan on {ip}:{ports} ===")
    filtered_ports = []
    for port in ports:
        response = sr1(IP(dst=ip)/TCP(dport=port, flags="A"), timeout=1, verbose=0)
        if response and response.haslayer(ICMP):
            print(f"Port {port}: Filtered")
            filtered_ports.append(port)
        else:
            print(f"Port {port}: Unfiltered")
    print(f"Scan complete. Found {len(filtered_ports)} filtered ports\n")
    return filtered_ports

def tcp_window_scan(ip, ports):
    """Perform TCP Window Scan."""
    print(f"\n=== Starting TCP Window Scan on {ip}:{ports} ===")
    open_ports = []
    for port in ports:
        response = sr1(IP(dst=ip)/TCP(dport=port, flags="A"), timeout=1, verbose=0)
        if response and response.haslayer(TCP):
            window_size = response.getlayer(TCP).window
            if window_size == 0:
                print(f"Port {port}: Closed")
            else:
                print(f"Port {port}: Open")
                open_ports.append(port)
    print(f"Scan complete. Found {len(open_ports)} open ports\n")
    return open_ports

def tcp_maimon_scan(ip, ports):
    """Perform TCP Maimon Scan."""
    print(f"\n=== Starting TCP Maimon Scan on {ip}:{ports} ===")
    open_filtered_ports = []
    for port in ports:
        response = sr1(IP(dst=ip)/TCP(dport=port, flags="FA"), timeout=1, verbose=0)
        if response is None:
            print(f"Port {port}: Open|Filtered")
            open_filtered_ports.append(port)
        elif response.haslayer(TCP) and response.getlayer(TCP).flags == 0x14:  # RST
            print(f"Port {port}: Closed")
    print(f"Scan complete. Found {len(open_filtered_ports)} open|filtered ports\n")
    return open_filtered_ports

def ip_protocol_scan(ip, protocols):
    """Perform IP Protocol Scan."""
    print(f"\n=== Starting IP Protocol Scan on {ip} ===")
    open_protocols = []
    for proto in protocols:
        response = sr1(IP(dst=ip, proto=proto), timeout=1, verbose=0)
        if response:
            print(f"Protocol {proto}: Open")
            open_protocols.append(proto)
        else:
            print(f"Protocol {proto}: Closed")
    print(f"Scan complete. Found {len(open_protocols)} open protocols\n")
    return open_protocols

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkScannerGUI(root)
    root.mainloop()