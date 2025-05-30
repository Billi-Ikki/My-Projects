# USB Write Blocker

## Overview
A Python tool to enable or disable write protection for USB devices on Windows via registry modifications, featuring a Tkinter GUI for forensic and secure operations.

## Features
- Toggles USB write protection using registry key `SYSTEM\CurrentControlSet\Control\StorageDevicePolicies`.
- Simple Tkinter GUI with "Enable" and "Disable" buttons.
- Checks for administrative privileges.
- Creates registry key if missing.

## How It Works
- Checks for admin rights using `ctypes`.
- Modifies `WriteProtect` registry value: `1` to block writes, `0` to allow.
- Displays success/error messages via GUI.

## Requirements
- Python 3.6+
- Tkinter (included with Python)
- Windows 10/11 (admin privileges required)

Verify Tkinter:
```bash
python -c "import tkinter"
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Billi-Ikki/Projects.git
   ```
2. Navigate to project directory (adjust if needed):
   ```bash
   cd Projects/USB_Write_Blocker
   ```

## Usage
1. Run as administrator:
   ```bash
   python Code.py
   ```
2. Click "Enable Write Protection" to block USB writes.
3. Click "Disable Write Protection" to allow USB writes.
4. View success/error messages in pop-ups.

## Notes
- Requires admin rights to modify registry.
- For forensic use to prevent USB data alteration.
- Compatible with Windows 10/11 only.
