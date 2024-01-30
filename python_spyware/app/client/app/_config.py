from app.functions import is_valid_fernet_key, load_env
from dotenv import load_dotenv
import os

class Config:
    """Config class for client app"""
    
    async def ainit(self):
        """You need to init .env file before using this class"""
        
        try:
            config = await load_env()
        
            self.key = config["KEY"]
            self.port_send = config["PORT_SEND"]
            self.port_receive = config["PORT_RECEIVE"]
            self.ip = config["IP"]
            self.date = config["DATE"]
            self.name = config["NAME"]
            
            await self.check_key()
            await self.check_port(self.port_send)
            await self.check_port(self.port_receive)
            await self.check_ip()
            config = {
                "KEY": self.key,
                "PORT_SEND": int(self.port_send),
                "PORT_RECEIVE": int(self.port_receive),
                "IP": self.ip,
                "DATE": self.date,
                "NAME": self.name
            }
            return config
        except Exception as err: return "[x] - Error config ", err
           
    async def check_key(self):
        """check if key is valid"""
        
        if not await is_valid_fernet_key(self.key): raise await Exception("[x] - Key is not valid.")
        
    async def check_port(self,port):
        """check if port is valid"""
        
        if not port: raise await Exception("[x] - Port is not valid.")

    async def check_ip(self):
        """check if ip is valid"""
        
        if not self.ip: raise await Exception("[x] - IP is not valid.")


