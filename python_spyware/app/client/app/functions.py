from dotenv import load_dotenv
import base64, os, requests, datetime, platform, ctypes
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
       
async def check_log():
    """Check if the arborescence is valid"""
    try:
        system_os = await detect_os()
        
        log_folder_path = './.log'
        # Verify if the file exist
        if not os.path.exists(log_folder_path):# if not, create it
            os.makedirs(log_folder_path) # Create empty folder
            if system_os == 'Windows':# if windows, hide the folder
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ret = ctypes.windll.kernel32.SetFileAttributesW(log_folder_path, FILE_ATTRIBUTE_HIDDEN)
    except Exception: return False

    
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

        #check if .env file is valid
        load_dotenv()
        if os.getenv("KEY") == None: return False
        elif os.getenv("PORT_SEND") == None: return False
        elif os.getenv("PORT_RECEIVE") == None: return False
        elif os.getenv("IP") == None: return False
        elif os.getenv("NAME") == None: return False
        elif os.getenv("DATE") == None: return False
        elif os.getenv("DATE") == datetime.datetime.now(): return False #check if date is valid
        else: return True
    except Exception: return False
    
async def load_env():
    """load env file"""
    
    try:
        config = {
            "KEY": os.getenv("KEY"),
            "PORT_SEND": os.getenv("PORT_SEND"),
            "PORT_RECEIVE": os.getenv("PORT_RECEIVE"),
            "IP": os.getenv("IP"),
            "NAME": os.getenv("NAME")
        }
        return config
    except Exception: raise await Exception("[x] - Error while loading .env file.")