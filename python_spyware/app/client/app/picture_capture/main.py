from pynput.mouse import Listener
import pyscreenshot,datetime

class C_Mouse:
    """ Capture picture of the screen when the mouse is clicked or every x seconds"""
    
    def __init__(self,name,ip):
        """Start the listener"""
        
        self.name = name
        self.ip = ip
        
        self.now = datetime.datetime.now()
        self.format_date = str(self.now.strftime("%d_%m_%Y_%H_%M_%S"))
        
        #if click()
        with Listener(on_click=self.on_click) as listener:
            listener.join()
        #elif timer()
        self.on_timer()
    
    def on_click(self, pressed):
        """Capture picture of the screen when the mouse is clicked"""
        
        if pressed:
            # Capture de l'écran au moment du clic
            screenshot = pyscreenshot.grab()
            screenshot.save("{}_{}sc_{}_clickEvent.png".format(self.format_date,self.name,self.ip))
            print("capture click event")
    
    def on_timer(self):
        """Capture picture of the screen every x seconds"""
        
        import pyscreenshot 
        image = pyscreenshot.grab(bbox=(10, 10, 500, 500))  
        image.save("{}_{}sc_{}.png".format(self.format_date,self.name,self.ip))
        print("capture timer event")