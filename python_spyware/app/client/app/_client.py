from app.module_crypto import encrypt_message
from app.functions import *
import socket
class Client:
    """Client class for client app (send data)"""
    
    async def ainit(self,config = None):
        """You need to init .env file before using this class"""
       
        try:
            self.config = config
            self.port_send = int(self.config['PORT_SEND'])
            self.key = self.config['KEY'].encode() # Encode the key in bytes
         
            if not await is_valid_fernet_key(self.key):
                return False 
            else: return True
        except Exception as err: return "[x] - Error client ", err
    
    async def send(self,message):
        """start socket client"""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
            client_sock.connect(('localhost', self.port_send))
            encrypted_data = await encrypt_message(message, self.key)
            client_sock.sendall(encrypted_data)
            response = client_sock.recv(1024)
            print(f"Received: {response}")