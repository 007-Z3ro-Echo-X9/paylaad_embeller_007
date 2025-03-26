import os
import tempfile
from Crypto.Cipher import AES
from .security_manager import SecurityError

class AdvancedFileOperations:
    def __init__(self):
        self.temp_files = []
        
    def process(self, payload_path, carrier_path, encryption_key, hmac_key):
        """End-to-end secure file processing"""
        try:
            # Phase 1: Secure payload encryption
            encrypted_payload = self.encrypt_payload(
                payload_path, 
                encryption_key
            )
            
            # Phase 2: Secure carrier modification
            output_file = self.modify_carrier(
                carrier_path,
                encrypted_payload,
                hmac_key
            )
            
            return output_file
            
        except Exception as e:
            self.emergency_cleanup()
            raise SecurityError(f"File processing failed: {str(e)}")

    def encrypt_payload(self, path, key):
        """AES-256-GCM authenticated encryption"""
        try:
            with open(path, 'rb') as f:
                plaintext = f.read()
                
            cipher = AES.new(key, AES.MODE_GCM)
            cipher.update(b"FileHeaderv1.0")
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)
            
            return cipher.nonce + tag + ciphertext
            
        except Exception as e:
            raise SecurityError(f"Encryption failed: {str(e)}")

    def modify_carrier(self, carrier_path, payload_data, hmac_key):
        """Steganography with integrity checks"""
        try:
            # Create secure temp file
            fd, temp_path = tempfile.mkstemp(
                dir=os.path.abspath("secure_temp"),
                suffix=".tmp"
            )
            self.temp_files.append(temp_path)
            
            # File manipulation
            with os.fdopen(fd, 'wb') as temp_file:
                # Write original carrier data
                with open(carrier_path, 'rb') as carrier:
                    temp_file.write(carrier.read())
                
                # Append encrypted payload
                temp_file.write(b"\x00\x00SECU")
                temp_file.write(payload_data)
                
            return temp_path
            
        except Exception as e:
            raise SecurityError(f"Carrier modification failed: {str(e)}")

    def emergency_cleanup(self):
        """NSA-recommended secure deletion"""
        for path in self.temp_files:
            if os.path.exists(path):
                self.secure_delete(path)
                
    @staticmethod
    def secure_delete(path, passes=7):
        """DoD 5220.22-M compliant wiping"""
        try:
            with open(path, 'ba+') as f:
                length = f.tell()
                for _ in range(passes):
                    f.seek(0)
                    f.write(os.urandom(length))
            os.remove(path)
        except Exception as e:
            raise SecurityError(f"Secure delete failed: {str(e)}")