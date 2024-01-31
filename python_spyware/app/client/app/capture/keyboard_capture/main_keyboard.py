from pynput import keyboard
import pyscreenshot, datetime, sys, asyncio, threading

threads_done = threading.Event()

class C_Keyboard:
    """ Capture keyboard events """
    
    def __init__(self,start=False,name="None",ip="None"):
        """Start the listener"""
        
        # Collect events until released
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            listener.join()
            
        if start == True:
            self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
            self.listener.start()
        
    def on_release(self,key):
        """ Capture keyboard release """
            
        if str(key) == '<97>':print(1)
        elif str(key) == '<98>':print(2)
        elif str(key) == '<99>':print(3)
        elif str(key) == '<100>':print(4)
        elif str(key) == '<101>':print(5)
        elif str(key) == '<102>':print(6)
        elif str(key) == '<103>':print(7)
        elif str(key) == '<104>':print(8)
        elif str(key) == '<105>':print(9)
        elif key == keyboard.Key.esc:return False# Stop listener
        else:print(key)
        
    def on_press(self,key):
        """ Capture keyboard press """
        
        try: 
            if key.char != None: pass#print(key.char)
        except AttributeError: print(key)
        
if sys.argv[0] == 'main_mouse.py':
    """ Run the server with arguments """
    
    # Récupérer les arguments
    if len(sys.argv) >= 2:

        # Parcourir les arguments et les analyser
        for arg in sys.argv[1:]:
            if arg == "start=True":start = True
            elif arg == "ip=":ip = sys.argv[2]
            elif arg == "name=":name = sys.argv[2]
        server_c_picture = C_Keyboard()
        
        asyncio.run(server_c_picture.__init__(start=start,name=name,ip=ip))
        threads_done.clear()
        sys.exit() #close terminal if exist
    else:pass#osef