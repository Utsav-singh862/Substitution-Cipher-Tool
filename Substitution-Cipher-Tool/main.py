import random
import string
import os

KEYS_DIR = "keys"         # Folder to store all keys
MESSAGES_DIR = "messages" # Folder to store encrypted messages
os.makedirs(KEYS_DIR, exist_ok=True)
os.makedirs(MESSAGES_DIR, exist_ok=True)

# Character set used for substitution cipher
chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)

def generate_key(key_name):
    """
    Generate a new shuffled key and save it to a file.
    """
    key = chars.copy()
    random.shuffle(key)
    with open(os.path.join(KEYS_DIR, f"{key_name}.txt"), "w") as f:
        f.write("".join(key))
    print(f"Key '{key_name}' generated and saved.")
    return key

def load_key(key_name):
    """
    Load a key from a file. Return None if not found.
    """
    path = os.path.join(KEYS_DIR, f"{key_name}.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            key = list(f.read())
        print(f"Key '{key_name}' loaded.")
        return key
    else:
        print(f"No key found with name '{key_name}'.")
        return None

def list_keys():
    """
    List all saved keys.
    """
    keys = [f.split(".txt")[0] for f in os.listdir(KEYS_DIR) if f.endswith(".txt")]
    if keys:
        print("Available keys:", ", ".join(keys))
    else:
        print("No keys available.")

def delete_key():
    """
    Delete a key file by name.
    """
    list_keys()
    key_name = input("Enter the key name to delete: ").strip()
    path = os.path.join(KEYS_DIR, f"{key_name}.txt")
    if os.path.exists(path):
        os.remove(path)
        print(f"Key '{key_name}' deleted successfully.")
    else:
        print(f"No key found with name '{key_name}'.")

def encrypt_message():
    """
    Encrypt a message using a selected or new key.
    """
    list_keys()
    key_name = input("Enter key name to use (or type new name to create a new key): ").strip()
    key = load_key(key_name)
    if key is None:
        key = generate_key(key_name)
    plain_text = input("Enter message to encrypt: ")
    
    cipher_text = ""
    for c in plain_text:
        if c in chars:
            cipher_text += key[chars.index(c)]
        else:
            cipher_text += c  # preserve unknown chars
    
    print(f"Original message: {plain_text}")
    print(f"Encrypted message: {cipher_text}")
    
    save_option = input("Do you want to save the encrypted message to a file? (Y/N): ").strip().upper()
    if save_option == 'Y':
        while True:
            file_name = input("Enter filename for the encrypted message: ").strip()
            if not file_name:
                print("Filename cannot be empty. Please try again.")
                continue
            if any(c in file_name for c in r'\/:*?"<>|'):
                print("Filename contains invalid characters (\\ / : * ? \" < > |). Please try again.")
                continue
            file_path = os.path.join(MESSAGES_DIR, f"{file_name}.txt")
            if os.path.exists(file_path):
                overwrite = input(f"File '{file_name}.txt' already exists. Overwrite? (Y/N): ").strip().upper()
                if overwrite != 'Y':
                    continue
            with open(file_path, "w") as f:
                f.write(cipher_text)
            print(f"Encrypted message saved to '{file_name}.txt'")
            break

def decrypt_message():
    """
    Decrypt a message using a selected key.
    """
    list_keys()
    key_name = input("Enter key name to use for decryption: ").strip()
    key = load_key(key_name)
    if key is None:
        return
    
    cipher_text_input = input("Enter message to decrypt (or type filename to load): ").strip()
    
    # Check if input matches a saved file
    file_path = os.path.join(MESSAGES_DIR, f"{cipher_text_input}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            cipher_text_input = f.read()
        print(f"Loaded encrypted message from '{cipher_text_input}.txt'")
    
    plain_text_decrypted = ""
    for c in cipher_text_input:
        if c in key:
            plain_text_decrypted += chars[key.index(c)]
        else:
            plain_text_decrypted += c  # preserve unknown chars
    
    print(f"Encrypted message: {cipher_text_input}")
    print(f"Decrypted message: {plain_text_decrypted}")

# Main menu loop
def main():
    print("Welcome to the Substitution Cipher Tool!")
    while True:
        choice = input("\nChoose an option: (E)ncrypt, (D)ecrypt, (L)ist keys, (Del)ete key, (Q)uit: ").strip().upper()
        
        if choice == 'E':
            encrypt_message()
        elif choice == 'D':
            decrypt_message()
        elif choice == 'L':
            list_keys()
        elif choice == 'DEL':
            delete_key()
        elif choice == 'Q':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select E, D, L, Del, or Q.")

if __name__ == "__main__":
    main()
