# core/__init__.py
from .security_manager import SecurityManager, SecurityError
from .file_operations import AdvancedFileOperations
from .ui_components import SecureConsole, KeyManagerUI, ImagePreview
from .advanced_operations import AdvancedOperations

# In CyberShieldApp __init__:
def __init__(self, root):
    self.security = SecurityManager()
    self.operations = AdvancedOperations(self.security)
    
    # Initialize security components
    try:
        self.security.generate_keys()
        if self.security.encryption_key:  # Only enable if keys generated
            self.operations.enable_anti_forensics()
    except SecurityError as e:
        messagebox.showerror("Security Error", str(e))

__all__ = [
    'SecurityManager',
    'SecurityError',
    'AdvancedFileOperations',
    'SecureConsole',
    'KeyManagerUI',
    'ImagePreview',
    'AdvancedOperations'
]