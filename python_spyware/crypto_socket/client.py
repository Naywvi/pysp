import socket
# Assurez-vous que ce module contient vos fonctions de cryptographie
import my_cryptography_module as crypto
import os
from dotenv import load_dotenv
import base64

def start_client(host, port, key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        message = "Hello, encrypted world!"
        encrypted_data = crypto.encrypt_message(message, key)
        sock.sendall(encrypted_data)
        response = sock.recv(1024)
        print(f"Received: {response}")
        
def is_valid_fernet_key(key):
    try:
        # La clé doit être décodable en base64 et avoir une longueur de 32 octets
        return len(base64.urlsafe_b64decode(key)) == 32
    except Exception:
        return False
    
if __name__ == "__main__":
    HOST, PORT = 'localhost', 9000
    load_dotenv()
    KEY = os.getenv("KEY")
    # KEY= crypto.generate_key()
    if is_valid_fernet_key(KEY):
        key = KEY.encode()  # Convertit la clé en bytes
        # Utiliser la clé pour le chiffrement/déchiffrement
        start_client(HOST, PORT, KEY)
    else:
        print("La clé Fernet n'est pas valide.")
        print(KEY)
