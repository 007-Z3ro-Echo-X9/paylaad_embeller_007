# core/ui_components.py
import tkinter as tk  # Base Tkinter import
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import threading

class SecureConsole(scrolledtext.ScrolledText):
    """Secure logging console with colored output"""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            wrap=tk.WORD,
            bg='#1e1e1e',
            fg='white',
            state='disabled'
        )
        self.tag_configure('error', foreground='red')
        self.tag_configure('success', foreground='green')
        self.tag_configure('warning', foreground='yellow')
        
    def log(self, message, category='info'):
        self.configure(state='normal')
        self.insert(tk.END, f"{message}\n", category)
        self.configure(state='disabled')
        self.see(tk.END)

class AsyncImageLoader:
    """Asynchronous image loading with thumbnail support"""
    
    def __init__(self, path, max_size=(800, 600)):
        self.path = path
        self.max_size = max_size
        self.image = None
        self.thumbnail = None
        
    def start_load(self):
        """Start async image loading"""
        thread = threading.Thread(target=self._load_image)
        thread.start()
        return thread
        
    def _load_image(self):
        """Load with progressive decoding"""
        img = Image.open(self.path)
        img.draft("RGB", self.max_size)
        self.thumbnail = img.copy()
        self.thumbnail.thumbnail(self.max_size)
        self.image = img.copy()

class KeyManagerUI:
    """Cryptographic key management interface"""
    
    def __init__(self, parent, security_manager):
        self.parent = parent
        self.security = security_manager
        self.frame = ttk.LabelFrame(parent, text="Key Management")
        
        self.gen_button = ttk.Button(self.frame, text="Generate Keys", 
                                   command=self.generate_keys)
        self.wipe_button = ttk.Button(self.frame, text="Wipe Memory", 
                                    command=self.wipe_memory)
        self.status_label = ttk.Label(self.frame, text="Status: Idle")
        
        self.gen_button.pack(side=tk.LEFT, padx=5)
        self.wipe_button.pack(side=tk.LEFT, padx=5)
        self.status_label.pack(side=tk.LEFT, padx=10)
        
    def generate_keys(self):
        try:
            self.security.generate_keys()
            self.status_label.config(text="Status: Active", foreground="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
            
    def wipe_memory(self):
        self.security.wipe_keys()
        self.status_label.config(text="Status: Wiped", foreground="orange")

class ImagePreview(tk.Canvas):
    """Advanced image preview component"""
    
    def __init__(self, parent):
        super().__init__(parent, bg='#2e2e2e', highlightthickness=0)
        self.image_tk = None  # Keep reference to prevent garbage collection
        self.zoom_level = 1.0
        self.current_loader = None
        self.bind("<Configure>", self._resize_image)
        
    def load_image(self, path):
        """Async-safe image loading with error handling"""
        self.delete("all")
        try:
            self.current_loader = AsyncImageLoader(path)
            self.current_loader.start_load()
            self.after(100, self._check_loading)
        except Exception as e:
            self._handle_error(f"Image error: {str(e)}")
        
    def _check_loading(self):
        if self.current_loader.thumbnail:
            self.image_tk = ImageTk.PhotoImage(self.current_loader.thumbnail)
            self._resize_image()
        else:
            self.after(100, self._check_loading)

    def _resize_image(self, event=None):
        if self.image_tk and self.current_loader:
            try:
                self.delete("all")
                img = self.current_loader.thumbnail.copy()
                
                canvas_width = self.winfo_width()
                canvas_height = self.winfo_height()
                
                scale = min(canvas_width/img.width, canvas_height/img.height)
                new_size = (
                    int(img.width * scale),
                    int(img.height * scale)
                )
                
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                self.image_tk = ImageTk.PhotoImage(resized_img)
                
                self.create_image(
                    canvas_width//2,
                    canvas_height//2,
                    anchor=tk.CENTER,
                    image=self.image_tk
                )
            except Exception as e:
                self._handle_error(f"Resize error: {str(e)}")

    def _handle_error(self, message):
        self.delete("all")
        self.create_text(
            self.winfo_width()//2,
            self.winfo_height()//2,
            text=message,
            fill="red",
            font=('Helvetica', 12)
        )

    def clear(self):
        """Clear the preview"""
        self.delete("all")
        self.image_tk = None
        self.current_loader = None