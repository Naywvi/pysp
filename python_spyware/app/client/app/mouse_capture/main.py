from pynput import mouse

class C_Mouse:
    """ Capture mouse events """
    
    def __init__(self,start=False):
        """ Start the listener """
        
        if start == True:
            # Collect events until released
            with mouse.Listener(
                    on_move=self.on_move,
                    on_click=self.on_click,
                    on_scroll=self.on_scroll) as listener:
                listener.join()

            # ...or, in a non-blocking fashion:
            # listener = mouse.Listener(
            #     on_move=self.on_move,
            #     on_click=self.on_click,
            #     on_scroll=self.on_scroll)

            # listener.start()
    
    def on_move(self,x, y):
        """ Capture mouse movement """
        
        print('Pointer moved to {0}'.format((x, y)))
        
    def on_scroll(self,x, y, dy):
        """ Capture mouse scroll """
        
        print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))
        
    def on_click(self,x, y, button, pressed):
        """ Capture mouse click """
        
        print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
        if not pressed:return False

C_Mouse(start=True)