from module_crypto import decrypt_message
from functions import *
import socket, asyncio

class Server_subprocess:
    """Server class for client app (receive data)"""
    
    async def ainit(self):
        """ You need to init .env file before using this class"""
        
        try:
            self.config = await load_env()
            self.key = self.config['KEY'].encode()
            self.port_receive = int(self.config['PORT_RECEIVE'])
            self.name = self.config['NAME']
            self.ip = self.config['IP']
            await self.start()
        except Exception as err:
            print(err)
        
    async def start(self):
        """start socket server"""
        
      
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', self.port_receive))
            s.listen()
            while True:
                conn, addr = s.accept()
                if 1== 0: print(f"Connected by {addr}")# Forced to use addr ...
                
                with conn:
                    while True:
                        encrypted_data = conn.recv(1024)
                        if not encrypted_data:
                            break
                        data = decrypt_message(encrypted_data, self.key)
                        #Debug data sender
                        print(data)
                        conn.sendall(data.encode())
                        
                     
       
asyncio.run(Server_subprocess().ainit())