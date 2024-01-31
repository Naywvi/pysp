import asyncio, json, subprocess, threading
from app.functions import check_log

class Capture_Main:
    """ Capture class """
    
    def __init__(self,path_json,path_log,name,ip):
        """ Constructor & init config """
        
        self.sub_keyboard_prog = None
        self.sub_mouse_prog = None
        self.sub_picture_prog = None
        
        self.name = name
        self.ip = ip
        self.path_json = path_json
        self.path_log = path_log
        self.config = self.get_config()
        if not(self.config):
            asyncio.run(check_log(force=True))
            return self.__init__(self,path_json,path_log)
        
    def get_config(self):
        """ Get json config """
        
        try:
            
            with open(self.path_json, 'r') as file:
                data = json.load(file)
                return data
            
        except:return False
        
        
    def start_capture(self):
        """ Start capture """
        
        if not self.sub_keyboard():return False
        elif not self.sub_mouse():return False
        elif not self.sub_picture():return False
        else:return True
       
        
    def sub_keyboard(self):
        """ Start capture with sub_process """
            
        if self.config['CAPTURE_KEYBOARD']['STATE'] == True:
            arguments = ["python", "-u", "./app/capture/keyboard_capture/main_keyboard.py", f"start={True}", f"ip={self.ip}", f"name={self.name}", f"PATH_LOG={self.path_log}", f"PATH_JSON={self.path_json}"]
            
            self.sub_keyboard_prog = subprocess.Popen(
                arguments,
                stdout=subprocess.PIPE,  # Capture output
                bufsize=1,  # Line-buffered
                universal_newlines=True,  # Translate to UTF-8
                shell=False  # No shell injection risk
            )
            
            return True
            
        elif self.config['CAPTURE_KEYBOARD']['STATE'] == False:subprocess.Popen.kill(self.sub_keyboard_prog)
        else: return False
            
        
    def sub_mouse(self):
        """ Start capture with sub_process """
        
        if self.config['CAPTURE_MOUSE']['STATE'] == True:
            
            arguments = ["python", "-u", "./app/capture/mouse_capture/main_mouse.py", f"start={True}", f"ip={self.ip}", f"name={self.name}", f"PATH_LOG={self.path_log}", f"PATH_JSON={self.path_json}"]
        
            self.sub_mouse_prog = subprocess.Popen(
                arguments,
                stdout=subprocess.PIPE,  # Capture output
                bufsize=1,  # Line-buffered
                universal_newlines=True,  # Translate to UTF-8
                shell=False  # No shell injection risk
            )
            
            return True
            
        elif self.config['CAPTURE_MOUSE']['STATE'] == False:subprocess.Popen.kill(self.sub_mouse_prog) 
        else:return False
        
    def sub_picture(self):
        """ Start capture with sub_process """
        
        if self.config['CAPTURE_PICTURE']['STATE'] == True:
            
            arguments = ["python", "-u", "./app/capture/picture_capture/main_picture.py", f"start={True}", f"ip={self.ip}", f"name={self.name}", f"PATH_LOG={self.path_log}", f"PATH_JSON={self.path_json}"]
        
            self.sub_picture_prog = subprocess.Popen(
                arguments,
                stdout=subprocess.PIPE,  # Capture output
                bufsize=1,  # Line-buffered
                universal_newlines=True,  # Translate to UTF-8
                shell=False  # No shell injection risk
            )
            
            return True
            
        elif self.config['CAPTURE_PICTURE']['STATE'] == False: subprocess.Popen.kill(self.sub_picture_prog)
        else:return False
        