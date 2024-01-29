from module_crypto import decrypt_message
from functions import *
import socket, asyncio

class Server_subprocess:
    """Server class for client app (receive data)"""
    async def ainit(self):
        try:
            self.config = await take_config(server=True)
            self.key = self.config['key'].encode()
            self.port_receive = int(self.config['port'])
            await self.start()
        except Exception as err:
            print(err)
        
    async def start(self):
        """start socket server"""
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', self.port_receive))
                s.listen()
                
                while True:
                    conn, addr = s.accept()
                    with conn:
                        if 1 == 0 :print(f"Connected by {addr}")# Forced to use addr ...
                        while True:
                            encrypted_data = conn.recv(1024)
                            if not encrypted_data:
                                break

                            data = await decrypt_message(encrypted_data, self.key)
                            
                            #Debug data sender
                            print("[ SERVER ] : Data receive '{}'.".format(data))
                            
                            # Verify if the stop command is received
                            if data == "QUIT":
                                conn.sendall(b"[ SERVER ] : Server disconnected.")
                                return
                            
                            # Send response to client with "Message received"
                            conn.sendall(b"[ SERVER ] : Message received")

                            
        except Exception as err:
            return err
asyncio.run(Server_subprocess().ainit())