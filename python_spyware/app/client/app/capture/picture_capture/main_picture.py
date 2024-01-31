from pynput.mouse import Listener
import pyscreenshot, datetime, sys, asyncio, threading

# threads_done = threading.Event()

class C_Picture:
    """ Capture picture of the screen when the mouse is clicked or every x seconds"""
    
    def __init__(self,start=False,name="None",ip="None"):
        """Start the listener"""
  
        self.name = name
        self.ip = ip
        
        self.now = datetime.datetime.now()
        self.format_date = str(self.now.strftime("%d_%m_%Y_%H_%M_%S"))
        
        #if click()
        if start == True:
            with Listener(on_click=self.on_click) as listener:
                listener.join()
        # elif timer()
        # self.on_timer()
    
    def on_click(self, pressed):
        """Capture picture of the screen when the mouse is clicked"""
        print("ok")
        if pressed:
            
            # Capture de l'écran au moment du clic
            screenshot = pyscreenshot.grab()
            # screenshot.save("{}_{}sc_{}_clickEvent.png".format(self.format_date,self.name,self.ip))
            screenshot.save("Event.png")
            print("capture click event")
    
    def on_timer(self):
        """Capture picture of the screen every x seconds"""
        
        import pyscreenshot 
        image = pyscreenshot.grab(bbox=(10, 10, 500, 500))  
        # image.save("{}_{}sc_{}.png".format(self.format_date,self.name,self.ip))
        print("capture timer event")

# if sys.argv[0] == 'main_picture.py':
#     """ Run the server with arguments """
    
#     # Récupérer les arguments
#     if len(sys.argv) >= 2:

#         # Parcourir les arguments et les analyser
#         for arg in sys.argv[1:]:
#             if arg == "start=True":start = True
#             elif arg == "ip=":ip = sys.argv[2]
#             elif arg == "name=":name = sys.argv[2]
#         server_c_picture = C_Picture()
        
#         asyncio.run(server_c_picture.__init__(start=start,name=name,ip=ip))
#         threads_done.clear()
#         sys.exit() #close terminal if exist
#     else:pass#osef
server_c_picture = C_Picture(True,"test","test")