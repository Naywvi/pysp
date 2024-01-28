from dotenv import load_dotenv
from app.module_crypto import generate_key
import requests, os, socket

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
        
        self.ip = None
        self.key = None
        self.port = 9000
        
        try:
            self.ip = await self.take_ip()
            self.key = await generate_key()
            await self.take_port()
            await self.create_env()
            return True
        except Exception as err:
            print("[x] - Error ", err)
            return False
        
    
    async def take_ip(self):
        """take public ip"""
        
        try:
            load_dotenv()
            self.url = os.getenv("URL")
            response = requests.get(self.url)
            if response.status_code == 200: return response.text
            else: return " url '{}'".format(self.url)
        except Exception as err: return err
    
    async def take_port(self):
        """take port function"""
        
        while not await self.search_port(self.port):
            if self.port > 65535: raise "No available ports"
            self.port += 15
        
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
            update_env_file('.env', 'PORT', self.port)
            update_env_file('.env', 'IP', self.ip)
        except Exception : raise "while creating .env file." 