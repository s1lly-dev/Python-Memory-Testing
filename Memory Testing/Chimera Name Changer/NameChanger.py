import pymem
import random
import string
import time
import keyboard  
from pymem.exception import MemoryReadError, MemoryWriteError

PROCESS_NAME = "RainbowSix.exe"
NAME_ADDR = 0x22795913CC0 # needs to be changed after every restart 
MAX_LEN = 15

def get_current_name(pm):
    try:
        raw_bytes = pm.read_bytes(NAME_ADDR, MAX_LEN)
    except MemoryReadError:
        return None
    return raw_bytes.split(b"\x00", 1)[0].decode("utf-8", errors="ignore")

def set_new_name(pm, new_name):
    if len(new_name) > MAX_LEN:
        return
    data = new_name.encode("utf-8") + b"\x00"
    try:
        pm.write_bytes(NAME_ADDR, data, len(data))
    except MemoryWriteError:
        return False
    return True

def random_name(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

if __name__ == "__main__":
    pm = pymem.Pymem(PROCESS_NAME)

    current_name = get_current_name(pm)
    if current_name is None or current_name == "":
        print("[!] Failed to read name — address may be invalid.")
    else:
        print(f"[+] Found current name: {current_name}")

    choice = input("1 = Set name | 2 = Randomize quickly (Press F6 to stop): ").strip()
    
    if choice == "1":
        if current_name is None:
            print("Error: Cannot set name, address invalid.")
        else:
            new_name = input(f"Enter new name (max {MAX_LEN}): ").strip()
            if set_new_name(pm, new_name):
                print(f"Changed to: {new_name}")
            else:
                print("Failed to set name.")
    elif choice == "2":
        print("[*] Randomizing names... Press F6 to stop.")
        try:
            while True:
                if keyboard.is_pressed("F6"):
                    print("[*] F6 pressed — stopping randomizer.")
                    break

                current = get_current_name(pm)
                if current is None or current == "":
                    print("[!] Address invalid or name reset — stopping randomizer.")
                    break
                
                name = random_name(random.randint(5, MAX_LEN))
                if not set_new_name(pm, name):
                    print("[!] Failed to write to memory — stopping.")
                    break

                print(f"[+] Changed to: {name}")
                time.sleep(0.2)  
        except KeyboardInterrupt:
            print("Stopped randomizing.")
