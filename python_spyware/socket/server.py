import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Cette méthode sera appelée pour chaque requête reçue
        self.data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} a écrit :")
        print(self.data)
        # Réponse au client
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Création du serveur, en passant le gestionnaire de requêtes
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activation du serveur; il fonctionnera jusqu'à une interruption manuelle
        server.serve_forever()
