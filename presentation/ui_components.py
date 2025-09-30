"""
UI components for the video downloader application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Callable, Optional
from ..domain.entities import VideoInfo, VideoFormat


class ModernButton(tk.Button):
    """Modern styled button."""
    
    def __init__(self, parent, **kwargs):
        default_style = {
            'bg': '#0078d4',
            'fg': 'white',
            'font': ('Segoe UI', 10, 'bold'),
            'relief': 'flat',
            'bd': 0,
            'padx': 20,
            'pady': 8,
            'cursor': 'hand2'
        }
        default_style.update(kwargs)
        super().__init__(parent, **default_style)
        
        # Bind hover effects
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        self.config(bg='#106ebe')
    
    def _on_leave(self, event):
        self.config(bg='#0078d4')


class ModernEntry(tk.Entry):
    """Modern styled entry widget."""
    
    def __init__(self, parent, placeholder="", **kwargs):
        default_style = {
            'font': ('Segoe UI', 10),
            'relief': 'flat',
            'bd': 1,
            'highlightthickness': 2,
            'highlightcolor': '#0078d4',
            'highlightbackground': '#e1e1e1'
        }
        default_style.update(kwargs)
        super().__init__(parent, **default_style)
        
        self.placeholder = placeholder
        self.placeholder_color = '#999999'
        self.normal_color = 'black'
        
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=self.placeholder_color)
            self.bind('<FocusIn>', self._on_focus_in)
            self.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.normal_color)
    
    def _on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)


class VideoInfoFrame(tk.Frame):
    """Frame for displaying video information."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.video_info = None
        self._create_widgets()
    
    def _create_widgets(self):
        # Title
        self.title_label = tk.Label(
            self,
            text="Video Information",
            font=('Segoe UI', 12, 'bold'),
            fg='#333333'
        )
        self.title_label.pack(pady=(0, 10))
        
        # Video details frame
        self.details_frame = tk.Frame(self, bg='#f8f9fa', relief='solid', bd=1)
        self.details_frame.pack(fill='x', pady=(0, 10))
        
        # Title
        self.video_title = tk.Label(
            self.details_frame,
            text="No video selected",
            font=('Segoe UI', 11, 'bold'),
            fg='#0078d4',
            wraplength=400,
            justify='left',
            bg='#f8f9fa'
        )
        self.video_title.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Duration and uploader
        self.meta_info = tk.Label(
            self.details_frame,
            text="",
            font=('Segoe UI', 9),
            fg='#666666',
            wraplength=400,
            justify='left',
            bg='#f8f9fa'
        )
        self.meta_info.pack(anchor='w', padx=10, pady=(0, 10))
    
    def update_video_info(self, video_info: VideoInfo):
        """Update the video information display."""
        self.video_info = video_info
        self.video_title.config(text=video_info.title)
        
        meta_text = []
        if video_info.duration_formatted != "Unknown":
            meta_text.append(f"Duration: {video_info.duration_formatted}")
        if video_info.uploader:
            meta_text.append(f"Uploader: {video_info.uploader}")
        if video_info.view_count:
            meta_text.append(f"Views: {video_info.view_count:,}")
        
        self.meta_info.config(text=" | ".join(meta_text))


class FormatSelectionFrame(tk.Frame):
    """Frame for format selection."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.formats = []
        self.selected_format = None
        self.format_var = tk.StringVar()
        self._create_widgets()
    
    def _create_widgets(self):
        # Title
        self.title_label = tk.Label(
            self,
            text="Select Video Format",
            font=('Segoe UI', 12, 'bold'),
            fg='#333333'
        )
        self.title_label.pack(pady=(0, 10))
        
        # Format listbox with scrollbar
        list_frame = tk.Frame(self)
        list_frame.pack(fill='both', expand=True)
        
        self.format_listbox = tk.Listbox(
            list_frame,
            font=('Consolas', 9),
            selectmode='single',
            height=8,
            bg='white',
            fg='#333333',
            selectbackground='#0078d4',
            selectforeground='white',
            relief='solid',
            bd=1
        )
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.format_listbox.yview)
        self.format_listbox.config(yscrollcommand=scrollbar.set)
        
        self.format_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.format_listbox.bind('<<ListboxSelect>>', self._on_format_select)
    
    def update_formats(self, formats: List[VideoFormat]):
        """Update the format list."""
        self.formats = formats
        self.format_listbox.delete(0, tk.END)
        
        for i, fmt in enumerate(formats):
            display_text = f"{i:2d}. {fmt.display_name}"
            self.format_listbox.insert(tk.END, display_text)
    
    def _on_format_select(self, event):
        """Handle format selection."""
        selection = self.format_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.formats):
                self.selected_format = self.formats[index]
                self.format_var.set(self.formats[index].format_id)
    
    def get_selected_format(self) -> Optional[VideoFormat]:
        """Get the selected format."""
        return self.selected_format


class ProgressFrame(tk.Frame):
    """Frame for download progress."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            self,
            text="Ready to download",
            font=('Segoe UI', 10),
            fg='#333333'
        )
        self.status_label.pack()
        
        # Speed label
        self.speed_label = tk.Label(
            self,
            text="",
            font=('Segoe UI', 9),
            fg='#666666'
        )
        self.speed_label.pack()
    
    def update_progress(self, percentage: float, speed: str = ""):
        """Update progress display."""
        self.progress_var.set(percentage)
        self.status_label.config(text=f"Downloading: {percentage:.1f}%")
        if speed:
            self.speed_label.config(text=f"Speed: {speed}")
    
    def set_status(self, status: str):
        """Set status message."""
        self.status_label.config(text=status)
        self.speed_label.config(text="")
    
    def reset(self):
        """Reset progress display."""
        self.progress_var.set(0)
        self.status_label.config(text="Ready to download")
        self.speed_label.config(text="")


class SettingsFrame(tk.Frame):
    """Frame for application settings."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
    
    def _create_widgets(self):
        # Title
        self.title_label = tk.Label(
            self,
            text="Settings",
            font=('Segoe UI', 12, 'bold'),
            fg='#333333'
        )
        self.title_label.pack(pady=(0, 10))
        
        # Download path
        path_frame = tk.Frame(self)
        path_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            path_frame,
            text="Download Path:",
            font=('Segoe UI', 10),
            fg='#333333'
        ).pack(anchor='w')
        
        path_input_frame = tk.Frame(path_frame)
        path_input_frame.pack(fill='x', pady=(5, 0))
        
        self.path_var = tk.StringVar()
        self.path_entry = ModernEntry(
            path_input_frame,
            placeholder="Enter download path...",
            textvariable=self.path_var
        )
        self.path_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.browse_button = ModernButton(
            path_input_frame,
            text="Browse",
            command=self._browse_path,
            width=8
        )
        self.browse_button.pack(side='right')
    
    def _browse_path(self):
        """Browse for download path."""
        path = filedialog.askdirectory(title="Select Download Directory")
        if path:
            self.path_var.set(path)
    
    def get_download_path(self) -> str:
        """Get the download path."""
        return self.path_var.get()
    
    def set_download_path(self, path: str):
        """Set the download path."""
        self.path_var.set(path)
