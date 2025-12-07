import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from storage import StorageManager
import os
from datetime import datetime

class HostelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏠 Hostel Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        self.root.state('zoomed')  # Maximize window
        
        # Configure modern style
        self.setup_styles()
        
        # Initialize storage
        self.storage = StorageManager()
        
        self.logged_in = False
        self.role = None
        self.username = None
        
        # Color scheme
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71', 
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'white': '#ffffff',
            'gray': '#95a5a6',
            'success': '#27ae60'
        }
        
        self.show_login()
        
        # Setup global keyboard shortcuts
        self.setup_keyboard_shortcuts()
    
    def setup_keyboard_shortcuts(self):
        """Setup global keyboard shortcuts"""
        # Global shortcuts
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<Alt-Left>', lambda e: self.go_back() if hasattr(self, 'go_back') else None)
        
        # Admin shortcuts
        if hasattr(self, 'role') and self.role == 'admin':
            self.root.bind('<Control-d>', lambda e: self.show_admin_dashboard())
            self.root.bind('<Control-s>', lambda e: self.show_manage_students())
            self.root.bind('<Control-r>', lambda e: self.show_manage_rooms())
    
    def show_help(self):
        """Show keyboard shortcuts help"""
        help_text = """
Keyboard Shortcuts:

• Ctrl+Q: Quit application
• F1: Show this help
• Alt+←: Go back
• Escape: Close dialogs

Admin Shortcuts:
• Ctrl+D: Dashboard
• Ctrl+S: Student Management
• Ctrl+R: Room Management

Login:
• Enter: Login
• Tab: Navigate fields
"""
        messagebox.showinfo("📚 Keyboard Shortcuts", help_text)
    
    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style
        style.configure('TNotebook', background='#ecf0f1', borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 10, 'bold'))
        
        # Configure treeview style
        style.configure('Treeview', background='#ffffff', foreground='#2c3e50', 
                       fieldbackground='#ffffff', font=('Arial', 9))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), 
                       background='#3498db', foreground='white')

    def show_login(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Main container with gradient effect
        main_container = tk.Frame(self.root, bg=self.colors['dark'])
        main_container.pack(fill='both', expand=True)
        
        # Left side - Welcome panel
        left_panel = tk.Frame(main_container, bg=self.colors['primary'], width=500)
        left_panel.pack(side='left', fill='y')
        left_panel.pack_propagate(False)
        
        # Welcome content
        welcome_frame = tk.Frame(left_panel, bg=self.colors['primary'])
        welcome_frame.pack(expand=True, fill='both', padx=40, pady=60)
        
        tk.Label(welcome_frame, text="🏠", font=('Arial', 80), 
                bg=self.colors['primary'], fg='white').pack(pady=20)
        
        tk.Label(welcome_frame, text="Welcome to", font=('Arial', 18), 
                bg=self.colors['primary'], fg='white').pack()
        
        tk.Label(welcome_frame, text="Hostel Management", font=('Arial', 28, 'bold'), 
                bg=self.colors['primary'], fg='white').pack()
        
        tk.Label(welcome_frame, text="System", font=('Arial', 28, 'bold'), 
                bg=self.colors['primary'], fg='white').pack()
        
        tk.Label(welcome_frame, text="Manage students, rooms, and facilities\nwith ease and efficiency", 
                font=('Arial', 12), bg=self.colors['primary'], fg='white', justify='center').pack(pady=30)
        
        # Right side - Login form
        right_panel = tk.Frame(main_container, bg=self.colors['light'])
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Login form container
        login_container = tk.Frame(right_panel, bg=self.colors['white'], relief='flat', bd=0)
        login_container.pack(expand=True, fill='none', padx=80, pady=100)
        
        # Login header
        header_frame = tk.Frame(login_container, bg=self.colors['white'])
        header_frame.pack(fill='x', pady=(30, 40))
        
        tk.Label(header_frame, text="🔐 Sign In", font=('Arial', 24, 'bold'), 
                bg=self.colors['white'], fg=self.colors['dark']).pack()
        
        tk.Label(header_frame, text="Enter your credentials to access the system", 
                font=('Arial', 11), bg=self.colors['white'], fg=self.colors['gray']).pack(pady=(5, 0))
        
        # Form fields
        form_frame = tk.Frame(login_container, bg=self.colors['white'])
        form_frame.pack(fill='x', padx=30)
        
        # Username field
        tk.Label(form_frame, text="👤 Username", font=('Arial', 11, 'bold'), 
                bg=self.colors['white'], fg=self.colors['dark']).pack(anchor='w', pady=(0, 5))
        
        username_frame = tk.Frame(form_frame, bg=self.colors['white'], relief='solid', bd=1)
        username_frame.pack(fill='x', pady=(0, 20))
        
        self.username_entry = tk.Entry(username_frame, font=('Arial', 12), bd=0, 
                                      bg=self.colors['white'], fg=self.colors['dark'], 
                                      relief='flat', insertbackground=self.colors['primary'])
        self.username_entry.pack(fill='x', padx=15, pady=12)
        
        # Password field
        tk.Label(form_frame, text="🔒 Password", font=('Arial', 11, 'bold'), 
                bg=self.colors['white'], fg=self.colors['dark']).pack(anchor='w', pady=(0, 5))
        
        password_frame = tk.Frame(form_frame, bg=self.colors['white'], relief='solid', bd=1)
        password_frame.pack(fill='x', pady=(0, 30))
        
        self.password_entry = tk.Entry(password_frame, font=('Arial', 12), bd=0, show='*',
                                      bg=self.colors['white'], fg=self.colors['dark'], 
                                      relief='flat', insertbackground=self.colors['primary'])
        self.password_entry.pack(fill='x', padx=15, pady=12)
        
        # Login button
        login_btn = tk.Button(form_frame, text="🚀 Sign In", font=('Arial', 12, 'bold'), 
                             bg=self.colors['primary'], fg='white', bd=0, relief='flat',
                             cursor='hand2', command=self.login, height=2)
        login_btn.pack(fill='x', pady=(0, 20))
        
        # Hover effects
        def on_enter(e):
            login_btn.configure(bg=self.colors['secondary'])
        def on_leave(e):
            login_btn.configure(bg=self.colors['primary'])
        
        login_btn.bind('<Enter>', on_enter)
        login_btn.bind('<Leave>', on_leave)
        
        # Default credentials info
        info_frame = tk.Frame(login_container, bg=self.colors['light'], relief='flat')
        info_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(info_frame, text="💡 Default Credentials", font=('Arial', 10, 'bold'), 
                bg=self.colors['light'], fg=self.colors['dark']).pack(pady=(10, 5))
        
        tk.Label(info_frame, text="Admin: admin / admin123", font=('Arial', 9), 
                bg=self.colors['light'], fg=self.colors['gray']).pack()
        
        tk.Label(info_frame, text="Student: student1 / student123", font=('Arial', 9), 
                bg=self.colors['light'], fg=self.colors['gray']).pack(pady=(0, 10))
        
        # Bind keyboard shortcuts for login
        self.root.bind('<Return>', lambda e: self.login())
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Focus on username entry
        self.username_entry.focus()
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        role = self.storage.authenticate_user(username, password)
        if role:
            self.logged_in = True
            self.role = role
            self.username = username
            messagebox.showinfo("Success", "Login successful!")
            if role == 'admin':
                self.show_admin_dashboard()
            else:
                self.show_student_view()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def logout(self):
        self.logged_in = False
        self.role = None
        self.username = None
        self.show_login()

    def create_header(self, parent, title, subtitle):
        """Create a modern header with title and user info"""
        header_frame = tk.Frame(parent, bg=self.colors['white'], height=80)
        header_frame.pack(fill='x', padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        # Left side - title
        left_frame = tk.Frame(header_frame, bg=self.colors['white'])
        left_frame.pack(side='left', fill='y', padx=20)
        
        tk.Label(left_frame, text=title, font=('Arial', 22, 'bold'), 
                bg=self.colors['white'], fg=self.colors['dark']).pack(anchor='w')
        
        if subtitle:
            tk.Label(left_frame, text=subtitle, font=('Arial', 11), 
                    bg=self.colors['white'], fg=self.colors['gray']).pack(anchor='w')
        
        # Right side - user actions
        right_frame = tk.Frame(header_frame, bg=self.colors['white'])
        right_frame.pack(side='right', fill='y', padx=20)
        
        # Current time
        current_time = datetime.now().strftime("%B %d, %Y - %I:%M %p")
        tk.Label(right_frame, text=f"🕒 {current_time}", font=('Arial', 9), 
                bg=self.colors['white'], fg=self.colors['gray']).pack(anchor='e')
        
        # Navigation buttons
        nav_frame = tk.Frame(right_frame, bg=self.colors['white'])
        nav_frame.pack(anchor='e', pady=(5, 0))
        
        # Back button (only show if not on dashboard)
        if hasattr(self, 'current_page') and self.current_page != 'dashboard':
            back_btn = tk.Button(nav_frame, text="⬅️ Back", font=('Arial', 10, 'bold'), 
                                bg=self.colors['gray'], fg='white', bd=0, relief='flat',
                                cursor='hand2', command=self.go_back, padx=15, pady=8)
            back_btn.pack(side='left', padx=(0, 10))
        
        # Help button
        help_btn = tk.Button(nav_frame, text="❓ Help", font=('Arial', 9), 
                            bg=self.colors['gray'], fg='white', bd=0, relief='flat',
                            cursor='hand2', command=self.show_help, padx=15, pady=6)
        help_btn.pack(side='left', padx=(0, 5))
        
        # Logout button
        logout_btn = tk.Button(nav_frame, text="🚪 Logout", font=('Arial', 10, 'bold'), 
                              bg=self.colors['danger'], fg='white', bd=0, relief='flat',
                              cursor='hand2', command=self.logout, padx=20, pady=8)
        logout_btn.pack(side='left')

    def create_modern_button(self, parent, text, color, command):
        """Create a modern styled button"""
        btn = tk.Button(parent, text=text, font=('Arial', 11, 'bold'), 
                       bg=color, fg='white', bd=0, relief='flat',
                       cursor='hand2', command=command, padx=20, pady=10)
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=self.darken_color(color))
        def on_leave(e):
            btn.configure(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def darken_color(self, color):
        """Darken a color for hover effect"""
        color_map = {
            self.colors['primary']: '#2980b9',
            self.colors['secondary']: '#27ae60',
            self.colors['danger']: '#c0392b',
            self.colors['warning']: '#d68910',
            self.colors['success']: '#229954',
            self.colors['gray']: '#7f8c8d'
        }
        return color_map.get(color, color)

    def show_admin_dashboard(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set current page for navigation
        self.current_page = 'dashboard'
        
        # Update keyboard shortcuts for admin
        self.setup_keyboard_shortcuts()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_container, "👨💼 Admin Dashboard", f"Welcome back, {self.username}!")
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['light'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Metrics cards
        metrics_container = tk.Frame(content_frame, bg=self.colors['light'])
        metrics_container.pack(fill='x', pady=(0, 30))
        
        data = self.storage.get_dashboard_data()
        metrics = [
            ("👥 Total Students", data.get('total_students', 0), self.colors['primary']),
            ("🏠 Total Rooms", data.get('total_rooms', 0), self.colors['secondary']),
            ("🔒 Occupied Rooms", data.get('occupied_rooms', 0), self.colors['warning']),
            ("🛏️ Available Beds", data.get('available_beds', 0), self.colors['success'])
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            self.create_metric_card(metrics_container, label, value, color, i)
        
        # Quick actions
        actions_frame = tk.Frame(content_frame, bg=self.colors['light'])
        actions_frame.pack(fill='both', expand=True)
        
        tk.Label(actions_frame, text="🚀 Quick Actions", font=('Arial', 18, 'bold'), 
                bg=self.colors['light'], fg=self.colors['dark']).pack(anchor='w', pady=(0, 20))
        
        # Action buttons grid
        buttons_frame = tk.Frame(actions_frame, bg=self.colors['light'])
        buttons_frame.pack(fill='x')
        
        actions = [
            ("👥 Manage Students", "Add, edit, and manage student records", self.colors['primary'], self.show_manage_students),
            ("🏠 Manage Rooms", "Configure rooms and capacity", self.colors['secondary'], self.show_manage_rooms),
            ("📊 Generate Reports", "Export data and analytics", self.colors['warning'], self.show_reports),
            ("⚙️ System Settings", "Configure system preferences", self.colors['gray'], self.show_settings)
        ]
        
        for i, (title, desc, color, command) in enumerate(actions):
            self.create_action_card(buttons_frame, title, desc, color, command, i)
    
    def create_metric_card(self, parent, label, value, color, index):
        """Create a metric card with modern styling"""
        card_frame = tk.Frame(parent, bg=self.colors['white'], relief='flat', bd=0)
        card_frame.grid(row=0, column=index, padx=15, pady=10, sticky='ew')
        
        # Configure grid weights
        parent.grid_columnconfigure(index, weight=1)
        
        # Card content
        content_frame = tk.Frame(card_frame, bg=self.colors['white'])
        content_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Value
        tk.Label(content_frame, text=str(value), font=('Arial', 32, 'bold'), 
                bg=self.colors['white'], fg=color).pack()
        
        # Label
        tk.Label(content_frame, text=label, font=('Arial', 11), 
                bg=self.colors['white'], fg=self.colors['gray']).pack()
        
        # Add shadow effect
        card_frame.configure(relief='solid', bd=1, highlightbackground=self.colors['light'])
    
    def create_action_card(self, parent, title, description, color, command, index):
        """Create an action card button"""
        card_frame = tk.Frame(parent, bg=self.colors['white'], relief='flat', bd=1, cursor='hand2')
        card_frame.grid(row=index//2, column=index%2, padx=15, pady=15, sticky='ew')
        
        # Configure grid weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Card content
        content_frame = tk.Frame(card_frame, bg=self.colors['white'])
        content_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text=title, font=('Arial', 14, 'bold'), 
                              bg=self.colors['white'], fg=color)
        title_label.pack(anchor='w')
        
        # Description
        desc_label = tk.Label(content_frame, text=description, font=('Arial', 10), 
                             bg=self.colors['white'], fg=self.colors['gray'])
        desc_label.pack(anchor='w', pady=(5, 0))
        
        # Bind click events
        def on_click(event):
            command()
        
        def on_enter(event):
            card_frame.configure(bg=self.colors['light'])
            content_frame.configure(bg=self.colors['light'])
            title_label.configure(bg=self.colors['light'])
            desc_label.configure(bg=self.colors['light'])
        
        def on_leave(event):
            card_frame.configure(bg=self.colors['white'])
            content_frame.configure(bg=self.colors['white'])
            title_label.configure(bg=self.colors['white'])
            desc_label.configure(bg=self.colors['white'])
        
        for widget in [card_frame, content_frame, title_label, desc_label]:
            widget.bind('<Button-1>', on_click)
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
    
    def show_reports(self):
        """Show reports dialog"""
        messagebox.showinfo("Reports", "Reports feature coming soon!")
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Settings", "Settings feature coming soon!")
    
    def go_back(self):
        """Navigate back to previous page"""
        if hasattr(self, 'previous_page'):
            if self.previous_page == 'dashboard':
                self.show_admin_dashboard()
            elif self.previous_page == 'students':
                self.show_manage_students()
            elif self.previous_page == 'rooms':
                self.show_manage_rooms()
        else:
            # Default back to dashboard for admin, or stay on student portal
            if self.role == 'admin':
                self.show_admin_dashboard()
            else:
                self.show_student_view()

    def show_manage_students(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set current page for navigation
        self.current_page = 'students'
        self.previous_page = 'dashboard'
        
        # Update keyboard shortcuts
        self.setup_keyboard_shortcuts()
            
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True)
        
        # Header with back navigation
        self.create_header(main_frame, "👥 Student Management", "Manage student records and information")
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['light'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Notebook for tabs
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill='both', expand=True)
        
        # View Students Tab
        view_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(view_frame, text='📋 View Students')
        
        # Students list
        list_frame = tk.Frame(view_frame, bg=self.colors['white'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview for students
        columns = ('ID', 'Name', 'Email', 'Phone', 'Room', 'Status')
        self.students_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        self.students_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Export buttons
        export_frame = tk.Frame(view_frame, bg=self.colors['white'])
        export_frame.pack(fill='x', padx=20, pady=10)
        
        self.create_modern_button(export_frame, "📄 Export CSV", self.colors['secondary'], 
                                 self.export_students_csv).pack(side='left', padx=5)
        self.create_modern_button(export_frame, "📑 Export PDF", self.colors['danger'], 
                                 self.export_students_pdf).pack(side='left', padx=5)
        self.create_modern_button(export_frame, "🔄 Refresh", self.colors['primary'], 
                                 self.refresh_students).pack(side='left', padx=5)
        
        # Add Student Tab
        add_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(add_frame, text='➕ Add Student')
        
        add_form = tk.Frame(add_frame, bg=self.colors['white'])
        add_form.pack(expand=True, padx=40, pady=40)
        
        # Form fields with modern styling
        fields = [
            ("👤 Full Name", "add_name_entry"),
            ("📧 Email Address", "add_email_entry"),
            ("📱 Phone Number", "add_phone_entry"),
            ("🏠 Room Number", "add_room_entry")
        ]
        
        for i, (label, attr) in enumerate(fields):
            self.create_form_field(add_form, label, attr, i)
        
        # Submit button
        submit_btn = self.create_modern_button(add_form, "➕ Add Student", self.colors['secondary'], 
                                              self.add_student_action)
        submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=30, sticky='ew')
        
        # Update/Delete Student Tab
        edit_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(edit_frame, text='✏️ Edit Student')
        
        edit_form = tk.Frame(edit_frame, bg=self.colors['white'])
        edit_form.pack(expand=True, padx=40, pady=40)
        
        # Student ID field
        tk.Label(edit_form, text="🆔 Student ID", font=('Arial', 12, 'bold'), 
                bg=self.colors['white'], fg=self.colors['dark']).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        id_frame = tk.Frame(edit_form, bg=self.colors['white'])
        id_frame.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='ew')
        
        self.edit_id_entry = tk.Entry(id_frame, font=('Arial', 12), width=15, 
                                     bg=self.colors['light'], relief='flat', bd=5)
        self.edit_id_entry.pack(side='left', padx=(0, 10))
        
        load_btn = self.create_modern_button(id_frame, "🔍 Load", self.colors['primary'], self.load_student)
        load_btn.pack(side='left')
        
        # Edit form fields
        edit_fields = [
            ("👤 Full Name", "edit_name_entry"),
            ("📧 Email Address", "edit_email_entry"),
            ("📱 Phone Number", "edit_phone_entry"),
            ("🏠 Room Number", "edit_room_entry")
        ]
        
        for i, (label, attr) in enumerate(edit_fields):
            self.create_form_field(edit_form, label, attr, i+1)
        
        # Status field
        tk.Label(edit_form, text="📊 Status", font=('Arial', 12, 'bold'), 
                bg=self.colors['white'], fg=self.colors['dark']).grid(row=6, column=0, padx=10, pady=10, sticky='w')
        
        self.edit_status_var = tk.StringVar(value="active")
        status_combo = ttk.Combobox(edit_form, textvariable=self.edit_status_var, 
                                   values=["active", "inactive"], width=30, font=('Arial', 11))
        status_combo.grid(row=6, column=1, padx=10, pady=10, sticky='ew')
        
        # Action buttons
        button_frame = tk.Frame(edit_form, bg=self.colors['white'])
        button_frame.grid(row=7, column=0, columnspan=3, pady=30)
        
        update_btn = self.create_modern_button(button_frame, "✏️ Update Student", self.colors['warning'], 
                                              self.update_student_action)
        update_btn.pack(side='left', padx=10)
        
        delete_btn = self.create_modern_button(button_frame, "🗑️ Delete Student", self.colors['danger'], 
                                              self.delete_student_action)
        delete_btn.pack(side='left', padx=10)
        
        self.refresh_students()
    
    def create_form_field(self, parent, label, attr_name, row):
        """Create a modern form field"""
        tk.Label(parent, text=label, font=('Arial', 12, 'bold'), 
                bg=self.colors['white'], fg=self.colors['dark']).grid(row=row, column=0, padx=10, pady=10, sticky='w')
        
        entry = tk.Entry(parent, font=('Arial', 12), width=30, 
                        bg=self.colors['light'], relief='flat', bd=5)
        entry.grid(row=row, column=1, padx=10, pady=10, sticky='ew')
        
        setattr(self, attr_name, entry)
        parent.grid_columnconfigure(1, weight=1)

    def show_manage_rooms(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set current page for navigation
        self.current_page = 'rooms'
        self.previous_page = 'dashboard'
        
        # Update keyboard shortcuts
        self.setup_keyboard_shortcuts()
            
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True)
        
        # Header with back navigation
        self.create_header(main_frame, "🏠 Room Management", "Manage room information and capacity")
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['light'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Notebook for tabs
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill='both', expand=True)
        
        # View Rooms Tab
        view_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(view_frame, text='📋 View Rooms')
        
        # Rooms list
        list_frame = tk.Frame(view_frame, bg=self.colors['white'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview for rooms
        columns = ('ID', 'Room Number', 'Capacity', 'Type', 'Occupied')
        self.rooms_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.rooms_tree.heading(col, text=col)
            self.rooms_tree.column(col, width=150)
        
        scrollbar2 = ttk.Scrollbar(list_frame, orient='vertical', command=self.rooms_tree.yview)
        self.rooms_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.rooms_tree.pack(side='left', fill='both', expand=True)
        scrollbar2.pack(side='right', fill='y')
        
        # Export buttons
        export_frame2 = tk.Frame(view_frame, bg=self.colors['white'])
        export_frame2.pack(fill='x', padx=20, pady=10)
        
        self.create_modern_button(export_frame2, "📄 Export CSV", self.colors['secondary'], 
                                 self.export_rooms_csv).pack(side='left', padx=5)
        self.create_modern_button(export_frame2, "📑 Export PDF", self.colors['danger'], 
                                 self.export_rooms_pdf).pack(side='left', padx=5)
        self.create_modern_button(export_frame2, "🔄 Refresh", self.colors['primary'], 
                                 self.refresh_rooms).pack(side='left', padx=5)
        
        # Add Room Tab
        add_room_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(add_room_frame, text='➕ Add Room')
        
        add_room_form = tk.Frame(add_room_frame, bg=self.colors['white'])
        add_room_form.pack(expand=True, padx=40, pady=40)
        
        # Room form fields
        room_fields = [
            ("🏠 Room Number", "room_number_entry"),
            ("👥 Capacity", "capacity_entry"),
            ("🏷️ Room Type", "room_type_entry")
        ]
        
        for i, (label, attr) in enumerate(room_fields):
            self.create_form_field(add_room_form, label, attr, i)
        
        # Submit button
        submit_btn = self.create_modern_button(add_room_form, "➕ Add Room", self.colors['secondary'], 
                                              self.add_room_action)
        submit_btn.grid(row=len(room_fields), column=0, columnspan=2, pady=30, sticky='ew')
        
        self.refresh_rooms()

    def show_student_view(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set current page for navigation
        self.current_page = 'student_portal'
        
        # Update keyboard shortcuts
        self.setup_keyboard_shortcuts()
            
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_frame, "👨🎓 Student Portal", f"Welcome, {self.username}!")
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['light'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Student details card
        details_frame = tk.Frame(content_frame, bg=self.colors['white'], relief='flat', bd=1)
        details_frame.pack(fill='both', expand=True, padx=50, pady=50)
        
        # Card header
        header_frame = tk.Frame(details_frame, bg=self.colors['primary'])
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="📋 My Information", font=('Arial', 18, 'bold'), 
                bg=self.colors['primary'], fg='white').pack(pady=20)
        
        # Fetch student details
        students = self.storage.get_students()
        student = next((s for s in students if s['email'] == self.username or str(s['id']) == self.username), None)
        
        if student:
            details = [
                ("Name:", student['name']),
                ("Email:", student['email']),
                ("Phone:", student.get('phone', 'N/A')),
                ("Room Number:", student.get('room_number', 'N/A')),
                ("Check-in Date:", str(student.get('check_in_date', 'N/A'))),
                ("Status:", student['status'])
            ]
            
            # Details content
            content_area = tk.Frame(details_frame, bg=self.colors['white'])
            content_area.pack(fill='both', expand=True, padx=40, pady=30)
            
            for i, (label, value) in enumerate(details):
                detail_frame = tk.Frame(content_area, bg=self.colors['white'])
                detail_frame.pack(fill='x', pady=15)
                
                tk.Label(detail_frame, text=label, font=('Arial', 12, 'bold'), 
                        bg=self.colors['white'], fg=self.colors['dark']).pack(side='left')
                
                value_frame = tk.Frame(detail_frame, bg=self.colors['light'], relief='flat')
                value_frame.pack(side='right', padx=20)
                
                tk.Label(value_frame, text=str(value), font=('Arial', 12), 
                        bg=self.colors['light'], fg=self.colors['dark']).pack(padx=15, pady=8)
        else:
            content_area = tk.Frame(details_frame, bg=self.colors['white'])
            content_area.pack(fill='both', expand=True, padx=40, pady=30)
            
            tk.Label(content_area, text="❌ Student details not found", 
                    font=('Arial', 16), bg=self.colors['white'], fg=self.colors['danger']).pack(pady=50)

    # Helper methods for student management
    def refresh_students(self):
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        students = self.storage.get_students()
        for student in students:
            self.students_tree.insert('', 'end', values=(
                student['id'], student['name'], student['email'], 
                student.get('phone', ''), student.get('room_number', ''), student['status']
            ))
    
    def add_student_action(self):
        name = self.add_name_entry.get().strip()
        email = self.add_email_entry.get().strip()
        phone = self.add_phone_entry.get().strip()
        room_number = self.add_room_entry.get().strip()
        
        # Validate required fields
        if not all([name, email]):
            messagebox.showerror("Error", "Name and Email are required")
            return
        
        # Validate email format
        if '@' not in email:
            messagebox.showerror("Error", "Email must contain @ symbol")
            return
        
        # Validate phone number
        if phone:
            if not phone.isdigit() or len(phone) != 10:
                messagebox.showerror("Error", "Phone number must be exactly 10 digits")
                return
        
        # Validate room number
        if room_number:
            if not room_number.isdigit() or len(room_number) > 3:
                messagebox.showerror("Error", "Room number must be maximum 3 digits")
                return
            
            # Check room occupancy limit
            students = self.storage.get_students()
            room_count = sum(1 for s in students if s.get('room_number') == room_number and s['status'] == 'active')
            if room_count >= 2:
                messagebox.showerror("Error", f"Room {room_number} is full (maximum 2 students per room)")
                return
        
        if self.storage.add_student(name, email, phone, room_number):
            messagebox.showinfo("Success", "Student added successfully!")
            # Clear entries
            for entry in [self.add_name_entry, self.add_email_entry, self.add_phone_entry, self.add_room_entry]:
                entry.delete(0, tk.END)
            self.refresh_students()
        else:
            messagebox.showerror("Error", "Error adding student")
    
    def load_student(self):
        try:
            student_id = int(self.edit_id_entry.get())
            students = self.storage.get_students()
            student = next((s for s in students if s['id'] == student_id), None)
            if student:
                self.edit_name_entry.delete(0, tk.END)
                self.edit_name_entry.insert(0, student['name'])
                self.edit_email_entry.delete(0, tk.END)
                self.edit_email_entry.insert(0, student['email'])
                self.edit_phone_entry.delete(0, tk.END)
                self.edit_phone_entry.insert(0, student.get('phone', ''))
                self.edit_room_entry.delete(0, tk.END)
                self.edit_room_entry.insert(0, student.get('room_number', ''))
                self.edit_status_var.set(student['status'])
            else:
                messagebox.showerror("Error", "Student not found")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Student ID")
    
    def update_student_action(self):
        try:
            student_id = int(self.edit_id_entry.get())
            name = self.edit_name_entry.get().strip()
            email = self.edit_email_entry.get().strip()
            phone = self.edit_phone_entry.get().strip()
            room_number = self.edit_room_entry.get().strip()
            status = self.edit_status_var.get()
            
            # Validate required fields
            if not all([name, email]):
                messagebox.showerror("Error", "Name and Email are required")
                return
            
            # Validate email format
            if '@' not in email:
                messagebox.showerror("Error", "Email must contain @ symbol")
                return
            
            # Validate phone number
            if phone:
                if not phone.isdigit() or len(phone) != 10:
                    messagebox.showerror("Error", "Phone number must be exactly 10 digits")
                    return
            
            # Validate room number
            if room_number:
                if not room_number.isdigit() or len(room_number) > 3:
                    messagebox.showerror("Error", "Room number must be maximum 3 digits")
                    return
                
                # Check room occupancy limit (exclude current student)
                students = self.storage.get_students()
                room_count = sum(1 for s in students if s.get('room_number') == room_number and s['status'] == 'active' and s['id'] != student_id)
                if room_count >= 2:
                    messagebox.showerror("Error", f"Room {room_number} is full (maximum 2 students per room)")
                    return
            
            if self.storage.update_student(student_id, name, email, phone, room_number, status):
                messagebox.showinfo("Success", "Student updated successfully!")
                self.refresh_students()
            else:
                messagebox.showerror("Error", "Error updating student")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Student ID")
    
    def delete_student_action(self):
        try:
            student_id = int(self.edit_id_entry.get())
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
                if self.storage.delete_student(student_id):
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    # Clear entries
                    for entry in [self.edit_id_entry, self.edit_name_entry, self.edit_email_entry, 
                                 self.edit_phone_entry, self.edit_room_entry]:
                        entry.delete(0, tk.END)
                    self.refresh_students()
                else:
                    messagebox.showerror("Error", "Error deleting student")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Student ID")
    
    # Helper methods for room management
    def refresh_rooms(self):
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)
        
        rooms = self.storage.get_rooms()
        for room in rooms:
            self.rooms_tree.insert('', 'end', values=(
                room['id'], room['room_number'], room['capacity'], 
                room.get('room_type', ''), room.get('occupied', 0)
            ))
    
    def add_room_action(self):
        room_number = self.room_number_entry.get().strip()
        room_type = self.room_type_entry.get().strip()
        
        try:
            capacity = int(self.capacity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Capacity must be a number")
            return
        
        if not room_number:
            messagebox.showerror("Error", "Room number is required")
            return
        
        # Validate room number
        if not room_number.isdigit() or len(room_number) > 3:
            messagebox.showerror("Error", "Room number must be maximum 3 digits")
            return
        
        if self.storage.add_room(room_number, capacity, room_type):
            messagebox.showinfo("Success", "Room added successfully!")
            # Clear entries
            for entry in [self.room_number_entry, self.capacity_entry, self.room_type_entry]:
                entry.delete(0, tk.END)
            self.refresh_rooms()
        else:
            messagebox.showerror("Error", "Error adding room")
    
    # Export methods
    def export_students_csv(self):
        try:
            filename = self.storage.export_students_to_csv()
            messagebox.showinfo("Success", f"Students exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_students_pdf(self):
        try:
            filename = self.storage.export_students_to_pdf()
            if filename:
                messagebox.showinfo("Success", f"Students exported to {filename}")
            else:
                messagebox.showerror("Error", "PDF export not available")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_rooms_csv(self):
        try:
            filename = self.storage.export_rooms_to_csv()
            messagebox.showinfo("Success", f"Rooms exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_rooms_pdf(self):
        try:
            filename = self.storage.export_rooms_to_pdf()
            if filename:
                messagebox.showinfo("Success", f"Rooms exported to {filename}")
            else:
                messagebox.showerror("Error", "PDF export not available")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HostelManagementApp(root)
    root.mainloop()