import socket
from app.module_crypto import encrypt_message as encrypt
import  asyncio

class Client:
    
    async def ainit(self,config = None):
        try:
            #creating a suitable configuration & check if config is not empty
            self.config = config
            KEY = str(self.config['key']).encode(); 
            PORT = int(self.config['port'])
            
            if not self.config: raise await Exception("Error while init config")
            await self.start(PORT,KEY)
        except Exception as err:
            print("[x] ERROR - ", err)
            return False
        pass
    
    async def start(self,port,key):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', port))
            # message = "Hello, encrypted world!"
            # encrypted_data = await encrypt(message, key)
            # sock.sendall(encrypted_data)
            # response = sock.recv(1024)
            # while True:
            #     sock.connect(('localhost', port))
            #     if message == "exit": exit()
            #     message = input("Enter your message: ")
            #     encrypted_data = await encrypt(message, key)
            #     sock.sendall(encrypted_data)
            #     response = sock.recv(1024)
            #     print(f"Received: {response}")
            message = "Hello, encrypted world!"
            encrypted_data = await encrypt(message, key)
            sock.sendall(encrypted_data)
            response = sock.recv(1024)
            # raise await response
            print(f"Received: {response}")