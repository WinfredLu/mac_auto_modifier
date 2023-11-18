import winreg as reg
import random
import ctypes
import sys
import os


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def generate_mac_address():
    mac = [0x00, 0x05, 0x69, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    mac_str = ''.join(f'{x:02X}' for x in mac)
    return mac_str


def set_network_address(network_key_path, new_mac):
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, network_key_path, 0, reg.KEY_WRITE) as key:
            reg.SetValueEx(key, "NetworkAddress", 0, reg.REG_SZ, new_mac)
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False


if is_admin():
    network_key_path = r"SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002bE10318}\0002"
    new_mac = generate_mac_address()

    if set_network_address(network_key_path, new_mac):
        print(f"MAC address changed to {new_mac}")
    else:
        print("Failed to change MAC address")
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
