# from pynput import keyboard

# def on_press(key):
#     try:
#         print('alphanumeric key {0} pressed'.format(
#             key.char))
#     except AttributeError:
#         print('special key {0} pressed'.format(
#             key))

# def on_release(key):
#     print('{0} released'.format(
#         key))
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False

# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()

from pynput import keyboard
class C_Keyboard:
    
    def __init__(self):
        
        # Collect events until released
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            listener.join()
        self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()
        
    def on_release(self,key):
        print('{0} released'.format(key))
        if key == keyboard.Key.esc:return False# Stop listener
        
    def on_press(self,key):
        try: print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError: print('special key {0} pressed'.format(key))