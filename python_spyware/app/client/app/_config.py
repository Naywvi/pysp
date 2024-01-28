from app.module_crypto import is_valid_fernet_key
from dotenv import load_dotenv
import os

class Config:
    """Config class for client app"""
    
    async def ainit(self):
        """You need to init .env file before using this class"""
        
        self.key = None
        self.port = None
        self.ip = None
        try:
            await self.load_env()
            await self.check_key()
            await self.check_port()
            await self.check_ip()
            config = {
                "key": self.key,
                "port": int(self.port),
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
            self.port = os.getenv("PORT")
            self.ip = os.getenv("IP")
        except Exception: raise await Exception("[x] - Error while loading .env file.")
           
    async def check_key(self):
        """check if key is valid"""
        
        if not await is_valid_fernet_key(self.key): raise await Exception("[x] - Key is not valid.")
        
    async def check_port(self):
        """check if port is valid"""
        
        if not self.port: raise await Exception("[x] - Port is not valid.")

    async def check_ip(self):
        """check if ip is valid"""
        
        if not self.ip: raise await Exception("[x] - IP is not valid.")


