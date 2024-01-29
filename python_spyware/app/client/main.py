from app._init_client import Env as env
from app._config import Config as client_config
from app._client import Client as client
from app._server import Server as server
from app.functions import send_api, redirect_output,check_env, load_env
import asyncio, threading, multiprocessing, queue, subprocess
import queue
import sys #close terminal 

threads_done = threading.Event()



    
async def main(url):
    """main function"""
    
    try:
        if threads_done.is_set(): return # If the thread is already running, do nothing
        elif not threads_done.is_set(): threads_done.set() # Set the thread as running
        
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
        
        # #starting the server with the configuration
        start_server = server()
        if not await start_server.ainit(generate_config): return main() #if error, restart the main function
        
        server_process = subprocess.Popen(
            ["python", "-u", "./app/server_subprocess.py"],
            stdout=subprocess.PIPE,  # Capture output
            bufsize=1, # Line-buffered
            universal_newlines=True, # Translate to UTF-8
            shell=False # No shell injection risk
        )
        # Create a thread to read output
        server_output_thread = threading.Thread(target=redirect_output, args=(server_process.stdout, server_output_queue))

        ## /!\ Start subprocess server /!\ ###
        try:
            server_output_thread.start()
        except: return main() #if error, restart the main function
        ## /!\ Start subprocess server /!\ ###
        
        #when all is good, we can send data to api ---------------------------------DONT LOST THAT NAGIB :D -----------------------------
        # await send_api(url, generated_config)
        
        #starting the client with the configuration
        generate_client = client()
        if not await generate_client.ainit(generate_config): return main() #if error, restart the main function

        while True:
            
            # Check if the server is still running
            if subprocess.Popen.poll(server_process) == 0:
                subprocess.Popen.kill(server_process)
                return
            
            # Check if the server has sent any output
            if not server_output_queue.empty():
                line = server_output_queue.get()
                print(line)  # Afficher la ligne de sortie du serveur
                
        
    except Exception as err: print(err)
    finally: print("[x] - Server close") # Signal the end of the thread
        
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    asyncio.run(main("http://localhost:8000/api/"))
    threads_done.clear()
    sys.exit() #close terminal if exist
    