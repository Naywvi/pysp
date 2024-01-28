from app.module_crypto import is_valid_fernet_key
from dotenv import load_dotenv
import os

class Config:
    """Config class for client app"""
    
    async def ainit(self):
        """You need to init .env file before using this class"""
        
        self.key = None
        self.port_send = None
        self.port_receive = None
        self.ip = None
        
        try:
            await self.load_env()
            await self.check_key()
            await self.check_port(self.port_send)
            await self.check_port(self.port_receive)
            await self.check_ip()
            config = {
                "key": self.key,
                "port_send": int(self.port_send),
                "port_receive": int(self.port_receive),
                "ip": self.ip
            }
            return config
        except Exception as err:
            print(err)
            return False

    async def load_env(self):
        """load env file"""
        
        try:
            load_dotenv()
            self.key =  os.getenv("KEY")
            self.port_send = os.getenv("PORT_SEND")
            self.port_receive = os.getenv("PORT_RECEIVE")
            self.ip = os.getenv("IP")
        except Exception: raise await Exception("[x] - Error while loading .env file.")
           
    async def check_key(self):
        """check if key is valid"""
        
        if not await is_valid_fernet_key(self.key): raise await Exception("[x] - Key is not valid.")
        
    async def check_port(self,port):
        """check if port is valid"""
        
        if not port: raise await Exception("[x] - Port is not valid.")

    async def check_ip(self):
        """check if ip is valid"""
        
        if not self.ip: raise await Exception("[x] - IP is not valid.")


