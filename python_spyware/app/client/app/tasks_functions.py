import subprocess
import time
from app.functions import run_server_sub
def PAUSE_SERVER(x,server_process):
    """Server will be paused (kill and restart after x seconds)"""
    
    print("Server will be paused for {} seconds.".format(x))
    subprocess.Popen.kill(server_process)
    time.sleep(x)
    server_process = run_server_sub()
    return server_process


async def PAUSE_CAPTURE_KEYBOARD():
    """Keyboard capture will be paused"""
    pass

async def PAUSE_CAPTURE_MOUSE():
    """Mouse capture will be paused"""
    pass

async def PAUSE_CAPTURE_PICTURE():
    """Picture capture will be paused"""
    pass

async def STOP_SERVER():
    """Server will be stopped"""
    pass

async def STOP_CAPTURE_KEYBOARD():
    """Keyboard capture will be stopped"""
    pass

async def STOP_CAPTURE_MOUSE():
    """Mouse capture will be stopped"""
    pass

async def STOP_CAPTURE_PICTURE():
    """Picture capture will be stopped"""
    pass

async def RESTART_SERVER():
    """Server will be restarted"""
    pass

async def RESTART_CAPTURE_KEYBOARD():
    """Restart keyboard capture"""
    pass

async def RESTART_CAPTURE_MOUSE():
    """Restart mouse capture"""
    pass

async def RESTART_CAPTURE_PICTURE():
    """Restart picture capture"""
    pass

async def STOP_LOG_KEYBOARD():
    """Keyboard log will be stopped"""
    pass

async def STOP_LOG_MOUSE():
    """Mouse log will be stopped"""
    pass

async def STOP_LOG_PICTURE():
    """Picture log will be stopped"""
    pass

async def START_LOG_KEYBOARD():
    """Keyboard log will be started"""
    pass

async def START_LOG_MOUSE():
    """Mouse log will be started"""
    pass

async def START_LOG_PICTURE():
    """Picture log will be started"""
    pass

async def STATUS_SERVER():
    """Server status"""
    pass

async def STATUS_LOG():
    """Log status"""
    pass

async def STATUS_CAPTURE():
    """Capture status"""
    pass

async def RESET_CONFIG():
    """Reset configuration"""
    pass

async def KILL():
    """Kill client"""
    pass

async def LOG_TIMER():
    """Add log timer"""
    pass

async def DELETE_LOG():
    """Delete log"""
    pass

async def MOVE():
    """Move the client"""
    pass