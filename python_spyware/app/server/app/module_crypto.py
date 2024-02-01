from cryptography.fernet import Fernet

async def generate_key():
    """Generate a key for Fernet"""
    
    try: return Fernet.generate_key().decode()
    except Exception: return False

def encrypt_message(message, key):
    """Encrypt a message with Fernet"""
    
    try:
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message
    except Exception: raise  "[x] - Error while encrypting message."

def decrypt_message(encrypted_message, key):
    """Decrypt a message with Fernet"""
    
    try:
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        return decrypted_message
    except Exception: raise "[x] - Error while decrypting message."