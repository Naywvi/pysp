import socket

def main():
    host, port = 'localhost', 9999

    # Création d'un socket client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connexion au serveur
        sock.connect((host, port))

        # Envoi de données
        message = "Hello, World!"
        sock.sendall(bytes(message, 'utf-8'))

        # Réception de la réponse
        response = sock.recv(1024)
        print(f"Reçu : {response.decode('utf-8')}")

if __name__ == "__main__":
    main()
