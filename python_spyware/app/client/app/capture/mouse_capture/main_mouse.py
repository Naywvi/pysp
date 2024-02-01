from pynput import mouse
import datetime, time, sys, threading,json

threads_done = threading.Event()

class C_Mouse:
    """ Capture mouse events """
    
    def __init__(self,start=False,name="None",ip="None",path_json=None,path_log=None):
        """ Start the listener """
        
        self.name = name
        self.ip = ip
        self.path_json = path_json
        self.path_log = path_log
        self.config = self.get_config()
        
        if start == True:
            # Collect events until released
            while True:
                if self.config['CAPTURE_MOUSE']['LOG'] == True:
                    while True:
                        self.now = datetime.datetime.now()
                        self.format_date = str(self.now.strftime("%d_%m_%Y"))
                        with mouse.Listener(
                                on_move=self.on_move,
                                on_click=self.on_click,
                                on_scroll=self.on_scroll
                                ) as listener:
                            
                            listener.join()
                            time.sleep(self.config['CAPTURE_MOUSE']['TIME'])    
                else:
                    while True:
                        pass
            # ...or, in a non-blocking fashion:
            # listener = mouse.Listener(
            #     on_move=self.on_move,
            #     on_click=self.on_click,
            #     on_scroll=self.on_scroll)

            # listener.start()
            
    def get_config(self):
        """ Get json config beceause i have la flemme """
        
        try:
            
            with open(self.path_json, 'r') as file:
                data = json.load(file)
                return data
            
        except:return False
        
    def on_move(self, x, y):
        """ Capture mouse movement """
        
        with open("{}.mouse/log_{}.log".format(self.path_log, self.format_date), "a") as file:
            file.write('Pointer moved to {}\n'.format((x, y)))

    def on_scroll(self, x, y, dy, dx):
        """ Capture mouse scroll """
      
        with open("{}.mouse/log_{}.log".format(self.path_log, self.format_date), "a") as file:
            file.write('Scrolled {} at {}\n'.format('down' if dy < 0 else 'up', (x, y)))

    def on_click(self, x, y, button, pressed):
        """ Capture mouse click """
        
        with open("{}.mouse/log_{}.log".format(self.path_log, self.format_date), "a") as file:
            file.write('{} at {}\n'.format('Pressed' if pressed else 'Released', (x, y)))
        # if you want to stop listener with click
        # if not pressed:
        #     return False
        
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

    server_c_mouse = C_Mouse(start=start,name=name,ip=ip,path_json=path_json,path_log=path_log)

    
    threads_done.clear()
    sys.exit() #close terminal if exist
else:pass#osef
