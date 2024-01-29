from dotenv import load_dotenv
from app.module_crypto import generate_key
import requests, socket, datetime

def update_env_file(file_path, key, value):
    """Update or add a key-value in a .env file."""
    lines = []
    found = False
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(key + '='):
                lines.append(f'{key}={value}\n')
                found = True
            else: lines.append(line)
    if not found: lines.append(f'{key}={value}\n')

    with open(file_path, 'w') as file: file.writelines(lines)
        
class Env:
    """Starts the application"""
    
    async def ainit(self):
        """initialisator .env file"""
        
        self.url = "https://api.ipify.org"
        self.ip = None
        self.key = None
        self.port_send = 9000
        self.port_receive = None
        self.date = datetime.datetime.now()
        try:
            self.ip = await self.take_ip()
            self.key = await generate_key()
            self.port_send = await self.take_port(self.port_send)
            self.port_receive = self.port_send + 1
            self.port_receive = await self.take_port(self.port_receive)
            await self.create_env()
            return True
        except Exception as err: return "[x] - Error client ", err
    
    async def take_ip(self):
        """take public ip"""
        
        try:
            load_dotenv()
            response = requests.get(self.url)
            if response.status_code == 200: return response.text
            else: return " url '{}'".format(self.url)
        except Exception as err: return err
    
    async def take_port(self,port):
        """take port function"""
        
        while not await self.search_port(port):
            if port > 65535: raise "No available ports"
            port += 1
        
        return port
        
    async def search_port(self, port, host='127.0.0.1'):
        """take port"""
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return True
            except Exception: return False
            
    async def create_env(self):
        """create .env file"""
        
        try:
            update_env_file('.env', 'KEY', self.key)
            update_env_file('.env', 'PORT_SEND', self.port_send)
            update_env_file('.env', 'PORT_RECEIVE', self.port_receive)
            update_env_file('.env', 'IP', self.ip)
            update_env_file('.env', 'DATE', self.date)
        except Exception : raise "while creating .env file." 