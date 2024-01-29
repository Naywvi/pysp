from dotenv import load_dotenv
import base64, os, requests, datetime

async def is_valid_fernet_key(key):
    """check if key is valid"""
    
    try:
        return len(base64.urlsafe_b64decode(key)) == 32
    except Exception:
        return False

async def send_api(url, data):
    """send data to api"""
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200: return True
        else: return False
    except Exception as err: return err
    
def redirect_output(source, target_queue):
    """redirect output from subprocess to queue"""
    
    for line in iter(source.readline, b''):
        target_queue.put(line)
       
async def check_env():
    """check if .env file is valid"""
    
    try:
        if not os.path.isfile('.env'): #create .env file if not exist
            with open('.env', 'w') as file: file.writelines("")
        
        #check if .env file is valid
        load_dotenv()
        if os.getenv("KEY") == None: return False
        elif os.getenv("PORT_SEND") == None: return False
        elif os.getenv("PORT_RECEIVE") == None: return False
        elif os.getenv("DATE") == None: return False
        elif os.getenv("DATE") == datetime.datetime.now(): return False #check if date is valid
        else: return True
    except Exception: return False
    
async def load_env():
    """load env file"""
    
    try:
        load_dotenv()
        config = {
            "KEY": os.getenv("KEY"),
            "PORT_SEND": os.getenv("PORT_SEND"),
            "PORT_RECEIVE": os.getenv("PORT_RECEIVE"),
            "IP": os.getenv("IP")
        }
        return config
    except Exception: raise await Exception("[x] - Error while loading .env file.")