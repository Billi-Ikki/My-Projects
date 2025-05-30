# Network Scanning Toolkit

## Overview
A Python-based network scanning tool using Scapy and Tkinter GUI, designed for ethical hacking. Supports host discovery, port scanning, and OS detection with scans like ICMP, TCP, ARP, and advanced methods.

## Features
- Tkinter GUI with dark theme (`#2E3440` background, `#D8DEE9` text).
- Host discovery: ICMP, TCP ACK, SCTP Init, ARP, and more.
- Port scanning: TCP Connect, UDP, NULL, FIN, Xmas, ACK, Window, Maimon.
- OS detection via TTL analysis.
- IP Protocol scanning for service discovery.

## How It Works
- Select scan type (e.g., ICMP, TCP Connect) in GUI.
- Enter target IP/range, ports, or protocols as needed.
- Click "Start Scan" to run; results display in real-time.
- Clear results with "Clear Results" button.

## Requirements
- Python 3.6+
- Scapy, Tkinter (included with Python)
- Install Scapy:
  ```bash
  pip install scapy
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Billi-Ikki/Projects.git
   ```
2. Navigate to Packet_Sniff directory:
   ```bash
   cd Projects/Packet_Sniff
   ```
3. Verify dependencies:
   ```bash
   python -c "import scapy, tkinter"
   ```

## Usage
1. Run the tool:
   ```bash
   python Code.py
   ```
2. Select scan type in GUI.
3. Enter target IP/range (e.g., `192.168.1.0/24`), ports (e.g., `80,443`), or protocols (e.g., `6,17`).
4. Click "Start Scan" to view results (e.g., live hosts, open ports).
5. Use "Clear Results" to reset output.

## Notes
- Requires root/admin privileges for raw packet operations.
- For ethical hacking and authorized use only.
- GUI uses threading to prevent freezing during scans.
