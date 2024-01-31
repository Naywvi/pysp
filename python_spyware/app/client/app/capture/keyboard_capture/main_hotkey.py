from pynput import keyboard
import pyscreenshot, datetime, sys, asyncio, threading

threads_done = threading.Event()

class C_Keyboard_hotkey:
    """ Capture keyboard events """
    
    def __init__(self,start=False):
        """Start the listener"""
    
        if start == True:
            
            self.hotkey_copy = keyboard.HotKey(
                keyboard.HotKey.parse('<ctrl>+c'),
            self.on_activate_copy)
            
            self.hotkey_past = keyboard.HotKey(
                keyboard.HotKey.parse('<ctrl>+v'),
            self.on_activate_paste)
            
            with keyboard.Listener(
                on_press=self.for_canonical_copy(self.hotkey_copy.press),
                on_release=self.for_canonical_copy(self.hotkey_copy.release)) as self.copy_listener:
                
            
                with keyboard.Listener(
                    on_press=self.for_canonical_past(self.hotkey_past.press),
                    on_release=self.for_canonical_past(self.hotkey_past.release)) as self.past_listener:
                    
                    self.copy_listener.join()
                    self.past_listener.join()
        
    def on_activate_copy(self):
        """ Print Hotkey copy """
    
        print('copy')
        
    def on_activate_paste(self):
        """ Print Hotkey paste """
        
        print('paste')
        
    def for_canonical_copy(self,f):
        """ Return a callback that converts a keycode to a character """
        
        return lambda k: f(self.copy_listener.canonical(k))
    
    def for_canonical_past(self,f):
        """ Return a callback that converts a keycode to a character"""
        
        return lambda k: f(self.past_listener.canonical(k))
    
keyboard = C_Keyboard_hotkey(start=True)
