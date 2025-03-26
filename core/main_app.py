import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core.security_manager import SecurityManager
from core.file_operations import AdvancedFileOperations
from core.ui_components import SecureConsole, KeyManagerUI, ImagePreview

class CyberShieldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberShield v3.0")
        self.root.geometry("1200x800")
        
        # Initialize core components
        self.security = SecurityManager()
        self.file_ops = AdvancedFileOperations()
        
        # Create UI elements
        self.create_widgets()
        self.setup_menu()
        
        # Security initialization
        self.security.generate_keys()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Operations")
        file_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(file_frame, text="Upload Payload", command=self.load_payload).pack(side=tk.LEFT)
        ttk.Button(file_frame, text="Upload Image", command=self.load_image).pack(side=tk.LEFT)
        
        # Image preview frame
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Image preview component
        self.preview = ImagePreview(preview_frame)
        self.preview.pack(fill=tk.BOTH, expand=True)
        
        # Console
        console_frame = ttk.LabelFrame(main_frame, text="Log Console")
        console_frame.pack(fill=tk.BOTH, expand=True)
        self.console = SecureConsole(console_frame)
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=10)
        ttk.Button(action_frame, text="Generate", command=self.process).pack(side=tk.LEFT)
        ttk.Button(action_frame, text="Download", command=self.save).pack(side=tk.LEFT)

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Reset", command=self.reset_session)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def load_payload(self):
        file_types = [("All Files", "*.*")]
        path = filedialog.askopenfilename(filetypes=file_types)
        if path:
            self.payload_path = path
            self.console.log(f"Payload loaded: {path}", 'success')

    def load_image(self):
        img_types = [("Images", "*.jpg *.png *.bmp")]
        path = filedialog.askopenfilename(filetypes=img_types)
        if path:
            self.image_path = path
            self.preview.load_image(path)
            self.console.log(f"Image loaded: {path}", 'success')

    def process(self):
        try:
            output_path = self.file_ops.process(
                self.payload_path,
                self.image_path,
                self.security.encryption_key
            )
            self.console.log(f"Created: {output_path}", 'success')
            self.show_success_message()
        except Exception as e:
            self.console.log(str(e), 'error')

    def save(self):
        file_types = [("JPEG", "*.jpg"), ("All Files", "*.*")]
        path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=file_types)
        if path:
            self.file_ops.save_result(path)
            self.console.log(f"Saved to: {path}", 'success')

    def show_success_message(self):
        self.preview.create_text(
            self.preview.winfo_width()//2,
            self.preview.winfo_height()//2,
            text="✅ Embedding Successful!",
            fill="green",
            font=('Helvetica', 24, 'bold')
        )

    def reset_session(self):
        self.payload_path = ""
        self.image_path = ""
        self.preview.delete("all")
        self.console.configure(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberShieldApp(root)
    root.mainloop()