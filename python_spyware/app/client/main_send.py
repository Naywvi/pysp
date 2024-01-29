from app._init_client import Env as env
from app._config import Config as client_config
from app._client import Client as client
from app._server import Server as server
from app.functions import send_api
import asyncio

async def main(url):
    """main function"""
    
    try:
        generate_client = client()
        if not await generate_client.ainit(): return main() #if error, restart the main function
        
        while True:
            await generate_client.send(message="HELLO WORLD")
            await asyncio.sleep(1)
            
      
    except Exception as err: print(err)
    finally: pass
        
if __name__ == "__main__":
    asyncio.run(main("http://localhost:8000/api/"))