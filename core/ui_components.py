# core/ui_components.py
import socket
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import threading
from datetime import datetime

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
        self.tag_configure('debug', foreground='cyan')
        self.tag_configure('info', foreground='white')
        
    def log(self, message, category='info'):
        """Log message with timestamp and category"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}"
        
        self.configure(state='normal')
        self.insert(tk.END, formatted_msg + "\n", category)
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
        try:
            img = Image.open(self.path)
            img.draft("RGB", self.max_size)
            self.thumbnail = img.copy()
            self.thumbnail.thumbnail(self.max_size)
            self.image = img.copy()
        except Exception as e:
            raise Exception(f"Image loading failed: {str(e)}")

class KeyManagerUI:
    """Cryptographic key management interface"""
    
    def __init__(self, parent, security_manager, console):
        self.parent = parent
        self.security = security_manager
        self.console = console
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
            self.console.log("Keys generated successfully", 'success')
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
            self.console.log(f"Key generation failed: {str(e)}", 'error')
            
    def wipe_memory(self):
        self.security.wipe_keys()
        self.status_label.config(text="Status: Wiped", foreground="orange")
        self.console.log("Memory wiped", 'warning')

class PayloadConfigUI(ttk.Frame):
    """Advanced payload configuration interface"""
    
    def __init__(self, parent, console):
        super().__init__(parent)
        self.console = console
        self.encoders = {
            'x86/shikata_ga_nai': 'Polymorphic XOR additive feedback encoder',
            'x86/countdown': 'Single-byte XOR countdown encoder',
            'cmd/powershell_base64': 'Powershell Base64 encoder'
        }
        
        self.config = {
            'payload_type': tk.StringVar(value='meterpreter/reverse_tcp'),
            'lhost': tk.StringVar(),
            'lport': tk.StringVar(value="4444"),
            'arch': tk.StringVar(value="x86"),
            'platform': tk.StringVar(value="windows"),
            'encoder': tk.StringVar(),
            'iterations': tk.IntVar(value=1),
            'format': tk.StringVar(value="exe"),
            'stageless': tk.BooleanVar(value=False),
            'badchars': tk.StringVar(),
            'template': tk.StringVar()
        }

        self.create_widgets()
        self.console.log("Payload configuration initialized", 'info')

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        
        # Basic Configuration Tab
        basic_frame = ttk.Frame(notebook)
        self.create_basic_tab(basic_frame)
        notebook.add(basic_frame, text="Basic")

        # Advanced Configuration Tab
        advanced_frame = ttk.Frame(notebook)
        self.create_advanced_tab(advanced_frame)
        notebook.add(advanced_frame, text="Advanced")

        # Encoding Tab
        encoding_frame = ttk.Frame(notebook)
        self.create_encoding_tab(encoding_frame)
        notebook.add(encoding_frame, text="Encoding")

        notebook.pack(expand=True, fill='both')

    def create_basic_tab(self, parent):
        ttk.Label(parent, text="Payload Type:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        payload_combo = ttk.Combobox(parent, textvariable=self.config['payload_type'])
        payload_combo['values'] = [
            'meterpreter/reverse_tcp', 
            'meterpreter/bind_tcp',
            'shell/reverse_tcp',
            'shell/bind_tcp'
        ]
        payload_combo.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(parent, text="LHOST:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.config['lhost']).grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(parent, text="LPORT:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.config['lport']).grid(row=2, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(parent, text="Platform:").grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)
        platform_combo = ttk.Combobox(parent, textvariable=self.config['platform'])
        platform_combo['values'] = ['windows', 'linux', 'android', 'mac', 'php']
        platform_combo.grid(row=3, column=1, padx=5, pady=2, sticky=tk.EW)

    def create_advanced_tab(self, parent):
        ttk.Label(parent, text="Architecture:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        arch_combo = ttk.Combobox(parent, textvariable=self.config['arch'])
        arch_combo['values'] = ['x86', 'x64', 'armle', 'ppc']
        arch_combo.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(parent, text="Output Format:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        format_combo = ttk.Combobox(parent, textvariable=self.config['format'])
        format_combo['values'] = ['exe', 'ps1', 'apk', 'raw', 'dll', 'elf']
        format_combo.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Checkbutton(parent, text="Stageless Payload", 
                      variable=self.config['stageless']).grid(row=2, column=0, columnspan=2, pady=5)

    def create_encoding_tab(self, parent):
        ttk.Label(parent, text="Encoder:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        encoder_combo = ttk.Combobox(parent, textvariable=self.config['encoder'])
        encoder_combo['values'] = list(self.encoders.keys())
        encoder_combo.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(parent, text="Iterations:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Spinbox(parent, from_=1, to=10, 
                  textvariable=self.config['iterations']).grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(parent, text="Bad Characters:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Entry(parent, textvariable=self.config['badchars']).grid(row=2, column=1, padx=5, pady=2, sticky=tk.EW)

class ImagePreview(tk.Canvas):
    """Advanced image preview component with auto-scaling"""
    
    def __init__(self, parent, console):
        super().__init__(parent, bg='#2e2e2e', highlightthickness=0)
        self.console = console
        self.image_tk = None
        self.current_image = None
        self.bind("<Configure>", self._resize_image)
        
    def load_image(self, path):
        """Async-safe image loading with error handling"""
        self.delete("all")
        try:
            loader = AsyncImageLoader(path)
            loader.start_load()
            self.console.log(f"Loading image: {path}", 'info')
            self.after(100, self._check_loading, loader)
        except Exception as e:
            self._handle_error(f"Image error: {str(e)}")
            self.console.log(f"Image load failed: {str(e)}", 'error')
        
    def _check_loading(self, loader):
        if loader.thumbnail:
            self.current_image = loader.thumbnail
            self._resize_image()
            self.console.log("Image loaded successfully", 'success')
        else:
            self.after(100, self._check_loading, loader)

    def _resize_image(self, event=None):
        if self.current_image:
            try:
                self.delete("all")
                img = self.current_image.copy()
                
                canvas_width = self.winfo_width()
                canvas_height = self.winfo_height()
                
                scale = min(canvas_width/img.width, canvas_height/img.height)
                new_size = (int(img.width * scale), int(img.height * scale))
                
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
                self.console.log(f"Image resize failed: {str(e)}", 'error')

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
        self.current_image = None
        self.console.log("Image preview cleared", 'info')

class ReverseConfigUI(ttk.Frame):
    """Reverse connection configuration interface with validation"""
    
    def __init__(self, parent, console):
        super().__init__(parent)
        self.parent = parent
        self.console = console
        self.console = console
        self.lhost_var = tk.StringVar()
        self.lport_var = tk.StringVar(value="4444")
        
        # Input validation commands
        val_alpha = (self.register(self._validate_alpha), '%P')
        val_num = (self.register(self._validate_num), '%P')

        # LHOST Configuration
        ttk.Label(self, text="LHOST:").grid(row=0, column=0, padx=5, sticky='w')
        self.lhost_entry = ttk.Entry(self, 
                                   textvariable=self.lhost_var,
                                   width=18,
                                   validate='key',
                                   validatecommand=val_alpha)
        self.lhost_entry.grid(row=0, column=1, padx=5, sticky='ew')
        
        # LPORT Configuration
        ttk.Label(self, text="LPORT:").grid(row=0, column=2, padx=5, sticky='w')
        self.lport_entry = ttk.Entry(self, 
                                   textvariable=self.lport_var,
                                   width=8,
                                   validate='key',
                                   validatecommand=val_num)
        self.lport_entry.grid(row=0, column=3, padx=5, sticky='ew')
        
        # Auto-detection Button
        self.auto_detect_btn = ttk.Button(self, 
                                        text="🌐 Detect IP", 
                                        command=self.auto_detect_ip)
        self.auto_detect_btn.grid(row=0, column=4, padx=5, sticky='e')

        self.columnconfigure(1, weight=1)
        self.console.log("Reverse connection configuration initialized", 'info')
        
    def _validate_alpha(self, text):
        """Validate IP address characters"""
        return all(c in "0123456789.:abcdefABCDEF" for c in text)
        
    def _validate_num(self, text):
        """Validate port numbers"""
        return text.isdigit() or text == ""
        
    def auto_detect_ip(self):
        """Attempt to auto-detect local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            self.lhost_var.set(ip)
            self.console.log(f"Auto-detected IP: {ip}", 'success')
        except Exception as e:
            self.lhost_var.set("127.0.0.1")
            self.console.log(f"IP detection failed, using localhost: {str(e)}", 'warning')