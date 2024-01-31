from app._server import Server as server
from app.functions import take_api, redirect_output, load_env, run_server_sub
import  threading, queue, subprocess, sys, asyncio #close terminal 

threads_done = threading.Event()

class Main_Sub_Server_Socket:
    """ Main server socket class """
    
    async def ainit(self,URL=""):
        """main function"""
        
        try:
            self.config = None
            
            if threads_done.is_set():pass # If the thread is already running, do nothing
            elif not threads_done.is_set(): threads_done.set() # Set the thread as running

            #if .env file is not valid, we create it
            self.config = take_api(URL)
            with open("./data.txt", "a") as file:
                file.write(str(self.config)+"\n")
            # Queue for the server subprocess
            server_output_queue = queue.Queue()
            
            # Starting the server with the configuration
            start_server = server()
            if not await start_server.ainit(): return await self.ainit(URL=URL)#if error, restart the main function
                
            # Run the server subprocess
            server_process = run_server_sub()
            
            
            # Create a thread to read output
            server_output_thread = threading.Thread(target=redirect_output, args=(server_process.stdout, server_output_queue))

            ## /!\ Start subprocess server /!\ ###
            try:
                server_output_thread.start()
            except: return await self.ainit(URL=URL) #if error, restart the main function
            ## /!\ Start subprocess server /!\ ###
            
            while True:
                if subprocess.Popen.poll(server_process) != None:# Forced restart if the server is closed by ? entity
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
                                print(line)
                                line = None
                                
        
        finally: 
            print("[x] - Server close") # Signal the end of the thread

if sys.argv[0] == 'm_server.py':
    """ Run the server with arguments """

    if len(sys.argv) >= 2:
        url = None

        # Parcourir les arguments et les analyser
        for arg in sys.argv[1:]:
            if arg.startswith("URL="):url = arg.split("=", 1)[1]
        server_c = Main_Sub_Server_Socket()
        asyncio.run(server_c.ainit(URL=url))
        threads_done.clear()
        sys.exit() #close terminal if exist
    else:pass#osef
