import socket
from my_cryptography_module import decrypt_message  # Assurez-vous que ce module contient vos fonctions de cryptographie
import os
from dotenv import load_dotenv
import base64

def start_server(port, key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"Server listening on port {port}...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                encrypted_data = conn.recv(1024)
                if not encrypted_data:
                    break

                data = decrypt_message(encrypted_data, key)
                print(f"Received: {data}")
def is_valid_fernet_key(key):
    try:
        # La clé doit être décodable en base64 et avoir une longueur de 32 octets
        return len(base64.urlsafe_b64decode(key)) == 32
    except Exception:
        return False

if __name__ == "__main__":
    load_dotenv()
    PORT = os.getenv("PORT")
    KEY = os.getenv("KEY")
    print(PORT, KEY)
    # KEY= crypto.generate_key()
    if is_valid_fernet_key(KEY):
        key = KEY.encode()  # Convertit la clé en bytes
        # Utiliser la clé pour le chiffrement/déchiffrement
        start_server(int(PORT), KEY)
    else:
        print("La clé Fernet n'est pas valide.")
        print(KEY)
    
