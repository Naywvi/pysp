from pynput import keyboard
class C_Keyboard:
    """ Capture keyboard events """
    
    def __init__(self,start=False):
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
        
keyboard = C_Keyboard(start=True)