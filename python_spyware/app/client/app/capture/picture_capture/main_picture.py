from pynput.mouse import Listener
import pyscreenshot, datetime, sys, threading, json, time
threads_done = threading.Event()

class C_Picture:
    """ Capture picture of the screen when the mouse is clicked or every x seconds"""
    
    def __init__(self,start=False,name="None",ip="None",path_json=None,path_log=None):
        """Start the listener"""
        
        # if path_json == None or path_log == None: return False
            
        self.name = name
        self.ip = ip
        self.path_json = path_json
        self.path_log = path_log
        self.config = self.get_config()
        self.click = 0
        #if click()
        if start == True:
            if self.config['CAPTURE_PICTURE']['TYPE'] == "CLICK":
                with Listener(on_click=self.on_click) as listener:
                    listener.join()
            elif self.config['CAPTURE_PICTURE']['TYPE'] == "TIMER":
                while True:
                    self.on_timer()
                    time.sleep(self.config['CAPTURE_PICTURE']['TIME'])
        
    def get_config(self):
        """ Get json config beceause i have la flemme """
        
        try:
            
            with open(self.path_json, 'r') as file:
                data = json.load(file)
                return data
            
        except:return False
        
    def on_click(self, x, y, button, pressed):
        """Capture picture of the screen when the mouse is clicked"""
        self.now = datetime.datetime.now()
        self.format_date = str(self.now.strftime("%d_%m_%Y_%H_%M_%S"))
        
        #Capture picture of the screen when the mouse is clicked
        if pressed:
            self.click += 1
            if self.click == self.config['CAPTURE_PICTURE']['NUMBER_CLICK']:
                self.click = 0
                screenshot = pyscreenshot.grab()
                screenshot.save("{}.pictures/{}_{}sc_{}_clickEvent.png".format(self.path_log,self.format_date,self.name,self.ip))
    
    def on_timer(self):
        """Capture picture of the screen every x seconds"""
        
        #Capture picture of the screen every x seconds
        self.now = datetime.datetime.now()
        self.format_date = str(self.now.strftime("%d_%m_%Y_%H_%M_%S"))
        import pyscreenshot 
        image = pyscreenshot.grab()  #bbox=(10, 10, 500, 500) > FLEMME
        image.save("{}.pictures/{}_{}sc_{}_timerEvent.png".format(self.path_log,self.format_date,self.name,self.ip))
        

if sys.argv[0] == './app/capture/picture_capture/main_picture.py':
 
        
    """ Run the server with arguments """
    
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
        
    server_c_picture = C_Picture(start=start,name=name,ip=ip,path_json=path_json,path_log=path_log)
    
    threads_done.clear()
    sys.exit() #close terminal if exist
else:pass#osef
# server_c_picture = C_Picture(True,"test","test")