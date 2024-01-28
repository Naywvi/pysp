import socket
import my_cryptography_module as crypto
import os
from dotenv import load_dotenv
import base64

def send_message(host, port, key, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((host, port))
        encrypted_data = crypto.encrypt_message(message, key)
        client_sock.sendall(encrypted_data)
        response = client_sock.recv(1024)
        print(f"Received: {response}")

def is_valid_fernet_key(key):
    try:
        # La clé doit être décodable en base64 et avoir une longueur de 32 octets
        return len(base64.urlsafe_b64decode(key)) == 32
    except Exception:
        return False

if __name__ == "__main__":
    HOST, PORT = 'localhost', 3000  # Modifier le port selon les besoins
    load_dotenv()
    KEY = os.getenv("KEY")

    if is_valid_fernet_key(KEY):
        key = KEY.encode()  # Convertit la clé en bytes

        # Envoyer un message au serveur
        message = "Salut serveur !"
        send_message(HOST, PORT, key, message)
        message = "Salut a !"
        send_message(HOST, PORT, key, message)
        message = "Salut r !"
        send_message(HOST, PORT, key, message)
        message = "Salut e !"
        send_message(HOST, PORT, key, message)
        message = "QUIT"
        send_message(HOST, PORT, key, message)

    else:
        print("La clé Fernet n'est pas valide.")
        print(KEY)
