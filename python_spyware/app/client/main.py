from app._client import Client_socket as csock
from m_server import Main_Sub_Server_Socket as ssock
from app.functions import redirect_output
from app.tasks_functions import PAUSE_SERVER
import asyncio, subprocess, time, queue,threading



URL = 'http://localhost:3000/give_me_your_data/'
PATH_JSON = "./.log/config.json"
PATH_LOG = "./.log/"
threads_done = threading.Event()

class client:
    """ Main client class """
    
    async def ainit(self, force = False) -> None:
        """ Init client """
        self.force = force
        try:
            
            if threads_done.is_set():pass # If the thread is already running, do nothing
            elif not threads_done.is_set(): threads_done.set() # Set the thread as running

            #Controler => (Init & Server_socket & capture)
            server_output_queue = queue.Queue()
            server = self.run_server()
            server_output_thread = threading.Thread(target=redirect_output, args=(server.stdout, server_output_queue))
            server_output_thread.start()

            
            #CLIENT SOCKET
            generate_csock = csock()
            if not await generate_csock.ainit(): raise Exception()
            
            
            print("Client started")
            while True:
                while True:
                    time.sleep(1)
                    if subprocess.Popen.poll(server) != None:# Forced restart if the server is closed by ? entity
                        server = PAUSE_SERVER(1,server)
                        server_output_queue = queue.Queue()
                        server_output_thread = threading.Thread(target=redirect_output, args=(server.stdout, server_output_queue))
                        server_output_thread.start()
                    elif subprocess.Popen.poll(server) == None:
                        if not server_output_queue.empty(): # Check if the server has sent any output
                            line = server_output_queue.get()
                            if not line:# If the server has closed reset the queue and thread
                                server_output_queue = queue.Queue()
                                server_output_thread = threading.Thread(target=redirect_output, args=(server.stdout, server_output_queue))
                                server_output_thread.start()
                            else:
                                print(line)
                                if line == "stop":break
                                await generate_csock.send(message=line)
                                line = None
                        else:
                            break
                
                #Give var if none => rien
                
                
                
               
            #run server multiprocess
            #Run while 
           
        except: 
            time.sleep(5)
            return await self.ainit()
        finally: 
            print("Client restarted")
    
    def run_server(self):
        """ Run server on subprocess """
        
        arguments = ["python", "-u", "m_server.py", f"URL={URL}", f"PATH_JSON={PATH_JSON}", f"PATH_LOG={PATH_LOG}", f"force={self.force}"]
        
        server_socket = subprocess.Popen(
            arguments,
            stdout=subprocess.PIPE,  # Capture output
            bufsize=1,  # Line-buffered
            universal_newlines=True,  # Translate to UTF-8
            shell=False  # No shell injection risk
        )
        return server_socket
    
if __name__ == "__main__":
    asyncio.run(client().ainit())
    
    
#ne pas oublier de changer dans send le port de send et de receive car ici on est en local