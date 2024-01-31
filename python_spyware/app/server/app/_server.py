from app.module_crypto import decrypt_message
from app.functions import *
# import socket

class Server:
    """Server class for client app (receive data)"""
        
    async def ainit(self,config = None):
        """You need to init .env file before using this class"""
        
        try:
            self.config = config
            self.key = self.config['KEY'].encode() # Encode the key in bytes
            self.port_receive = int(self.config['PORT_RECEIVE'])
            if not await is_valid_fernet_key(self.key): return False
            else: return True
        except Exception as err: return "[x] - Error server ", err