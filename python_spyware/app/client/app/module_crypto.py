from cryptography.fernet import Fernet
import base64

async def generate_key():
    """Generate a key for Fernet"""
    
    try: return Fernet.generate_key().decode()
    except Exception: return False

async def encrypt_message(message, key):
    """Encrypt a message with Fernet"""
    
    try:
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message
    except Exception: raise await "[x] - Error while encrypting message."

async def decrypt_message(encrypted_message, key):
    """Decrypt a message with Fernet"""
    
    try:
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        return decrypted_message
    except Exception: raise await "[x] - Error while decrypting message."

async def is_valid_fernet_key(key):
    """Check if key is valid"""
    
    try: return len(base64.urlsafe_b64decode(key)) == 32
    except Exception: return False