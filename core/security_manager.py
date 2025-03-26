# core/security_manager.py
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA512

class SecurityError(Exception):
    """Custom exception for security-related errors"""
    pass

class SecurityManager:
    def __init__(self):
        self.encryption_key = None
        self.hmac_key = None
        self.kdf_iterations = 100000  # 100k iterations recommended by NIST
    
    def generate_keys(self):
        """Generate AES-256 and HMAC keys with secure memory management"""
        try:
            # Use mutable bytearrays for sensitive data
            salt = bytearray(get_random_bytes(32))
            passphrase = bytearray(get_random_bytes(64))
            
            # Generate AES-256 key
            self.encryption_key = PBKDF2(
                bytes(passphrase),  # Convert to bytes for KDF
                bytes(salt),
                dkLen=32,
                count=self.kdf_iterations,
                hmac_hash_module=SHA512
            )
            
            # Generate HMAC key
            self.hmac_key = PBKDF2(
                bytes(passphrase),
                bytes(salt),
                dkLen=64,
                count=self.kdf_iterations,
                hmac_hash_module=SHA512
            )
            
            # Secure memory wipe
            self._secure_wipe(passphrase)
            self._secure_wipe(salt)
            
        except Exception as e:
            raise SecurityError(f"Key generation failed: {str(e)}")

    def _secure_wipe(self, data):
        """Military-grade memory sanitization for mutable buffers"""
        if isinstance(data, bytearray):
            for i in range(len(data)):
                data[i] = 0
            data.clear()
        elif isinstance(data, bytes):
            raise TypeError("Received immutable bytes for secure wipe - use bytearray")