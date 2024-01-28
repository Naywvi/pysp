from app._init_client import Env as env
from app._config import Config as client_config
from app._client import Client as client
import asyncio

async def main():
    """main function"""
    
    try:
        # creating a suitable configuration
        if not await env().ainit(): raise Exception("Error while init .env file")
        
        #applying the configuration & save it on .env file
        config = await client_config().ainit()
        if not config: raise Exception("Error while init config")

        # #starting the client with the configuration
        # await client().ainit(config)
      
    except Exception as err:
        print("[x] ERROR - ",err)
   
if __name__ == "__main__":
    asyncio.run(main())