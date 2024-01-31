from dotenv import load_dotenv
from datetime import datetime
import base64, os, requests, platform, subprocess

async def detect_os():
    os_name = platform.system()
    if os_name == 'Windows':
        return 'Windows'
    elif os_name == 'Linux':
        return 'Linux'
    else:
        return 'Autre'
async def is_valid_fernet_key(key):
    """check if key is valid"""
    
    try:
        return len(base64.urlsafe_b64decode(key)) == 32
    except Exception:
        return False

def take_api(url):
    """send data to api"""
   
    response = requests.get(url)
    if response.status_code == 200: return response.content
    else: print(response.status_code)

    
def redirect_output(source, target_queue):
    """redirect output from subprocess to queue"""
    
    for line in iter(source.readline, b''):
        target_queue.put(line)
       
async def check_env():
    """check if .env file is valid"""

    try:
        if not os.path.isfile('.env'): #create .env file if not exist
            with open('.env', 'w') as file:
                file.write("KEY=\n")
                file.write("PORT_SEND=\n")
                file.write("PORT_RECEIVE=\n")
                file.write("IP=\n")
                file.write("DATE=\n")
                file.write("NAME=\n") 
                file.close()
        
        #check if .env file is valid
        load_dotenv()
        if os.getenv("KEY") == "": return False
        elif os.getenv("PORT_SEND") == None: return False
        elif os.getenv("PORT_RECEIVE") == None: return False
        elif os.getenv("IP") == None: return False
        elif os.getenv("NAME") == None: return False
        elif os.getenv("DATE") == None: return False
        elif os.getenv("DATE") != datetime.now().strftime("%d-%m-%Y"): return False #check if date is valid
        else: return True
        
    except Exception as err : print(err); return False
    
async def load_env():
    """load env file"""
    
    try:
        load_dotenv()
        config = {
            "KEY": os.getenv("KEY"),
            "PORT_SEND": os.getenv("PORT_SEND"),
            "PORT_RECEIVE": os.getenv("PORT_RECEIVE"),
            "IP": os.getenv("IP"),
            "NAME": os.getenv("NAME"),
            "DATE": os.getenv("DATE")
        }
        return config
    except Exception: return await Exception("[x] - Error while loading .env file.")
    
def run_server_sub():
    server = subprocess.Popen(
        ["python", "-u", "./app/server_subprocess.py"],
        stdout=subprocess.PIPE,  # Capture output
        bufsize=1, # Line-buffered
        universal_newlines=True, # Translate to UTF-8
        shell=False # No shell injection risk
    )
    return server