from pynput import mouse
import pyscreenshot, datetime, sys, asyncio, threading

threads_done = threading.Event()

class C_Mouse:
    """ Capture mouse events """
    
    def __init__(self,start=False,name="None",ip="None"):
        """ Start the listener """
        self.name = name
        self.ip = ip
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

if sys.argv[0] == 'main_mouse.py':
    """ Run the server with arguments """
    
    # Récupérer les arguments
    if len(sys.argv) >= 2:

        # Parcourir les arguments et les analyser
        for arg in sys.argv[1:]:
            if arg == "start=True":start = True
            elif arg == "ip=":ip = sys.argv[2]
            elif arg == "name=":name = sys.argv[2]
        server_c_picture = C_Mouse()
        
        asyncio.run(server_c_picture.__init__(start=start,name=name,ip=ip))
        threads_done.clear()
        sys.exit() #close terminal if exist
    else:pass#osef
