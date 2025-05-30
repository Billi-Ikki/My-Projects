# Oblivious Transfer

## Overview
A Python-based 1-out-of-2 Oblivious Transfer tool using the Naor-Pinkas protocol. Enables a sender to share two messages, allowing a receiver to retrieve one without revealing their choice, using SHA256-derived keys and Tkinter GUI.

## Features
- Implements Naor-Pinkas OT with 31-bit Mersenne prime for demo.
- Sender GUI for inputting two messages; receiver GUI for selecting one.
- XOR encryption with SHA256-derived keys.
- Real-time protocol logs and network status.

## How It Works
- **Sender**: Generates public values (`C0`, `C1`) and encrypts two messages based on receiver’s public key.
- **Receiver**: Chooses message (0 or 1), sends public key, and decrypts selected message.
- **Protocol**: Ensures sender learns nothing about receiver’s choice; receiver gets only one message.

## Requirements
- Python 3.6+
- Tkinter, matplotlib (included with Python)
Verify Tkinter:
```bash
python -c "import tkinter"
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Billi-Ikki/Projects.git
   ```
2. Navigate to project directory:
   ```bash
   cd Projects/Oblivious_Transfer
   ```

## Usage
1. Start sender:
   ```bash
   python sender.py
   ```
   - Set host/port (default: `localhost:12345`).
   - Enter two messages, click "Start Server".
2. Start receiver:
   ```bash
   python receiver.py
   ```
   - Set same host/port.
   - Select message (0 or 1), click "Connect to Sender", then "Run Protocol".
3. View decrypted message and logs in receiver GUI.

## Notes
- Run sender before receiver.
- Uses small key size (31-bit) for demo; not secure for production.
- For cryptographic education only.
