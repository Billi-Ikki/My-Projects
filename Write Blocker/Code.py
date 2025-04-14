import tkinter as tk
from tkinter import messagebox
import winreg as reg
import ctypes

def set_write_protection(enable):
    try:
        # Open the registry key for modification
        key = reg.OpenKey(
            reg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\StorageDevicePolicies",
            0,
            reg.KEY_SET_VALUE
        )
        
        # Set the WriteProtect value
        reg.SetValueEx(key, "WriteProtect", 0, reg.REG_DWORD, 1 if enable else 0)
        reg.CloseKey(key)
        
        # Inform the user of the result
        status = "enabled" if enable else "disabled"
        messagebox.showinfo("Success", f"Write protection {status} successfully.")
        
    except PermissionError:
        # Handle permission errors
        messagebox.showerror("Permission Denied", "Please run this program as Administrator.")
    except FileNotFoundError:
        # Handle cases where the key doesn't exist and create it
        create_storage_device_policies_key()
        set_write_protection(enable)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_storage_device_policies_key():
    try:
        # Create the registry key if it does not exist
        reg.CreateKey(
            reg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\StorageDevicePolicies"
        )
        messagebox.showinfo("Information", "Registry key created successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while creating the registry key: {e}")

def check_admin():
    try:
        # Check if the user has admin privileges
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def enable_protection():
    set_write_protection(True)

def disable_protection():
    set_write_protection(False)

# Main GUI Application
def main():
    if not check_admin():
        messagebox.showerror("Permission Denied", "Please run this program as Administrator.")
        return

    # Create the main window
    root = tk.Tk()
    root.title("USB Write Blocker")
    root.geometry("300x200")

    # Create buttons to enable or disable write protection
    enable_button = tk.Button(root, text="Enable Write Protection", command=enable_protection)
    enable_button.pack(pady=20)

    disable_button = tk.Button(root, text="Disable Write Protection", command=disable_protection)
    disable_button.pack(pady=20)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
