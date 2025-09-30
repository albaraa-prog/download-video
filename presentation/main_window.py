"""
Main window for the video downloader application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Optional
from ..domain.entities import VideoInfo, VideoFormat, DownloadRequest
from ..application.use_cases import (
    GetVideoInfoUseCase,
    GetAvailableFormatsUseCase,
    DownloadVideoUseCase,
    ValidateUrlUseCase
)
from ..application.services import FormatSelectionService, PathService
from .ui_components import (
    ModernButton,
    ModernEntry,
    VideoInfoFrame,
    FormatSelectionFrame,
    ProgressFrame,
    SettingsFrame
)


class VideoDownloaderWindow:
    """Main window for the video downloader application."""
    
    def __init__(self, use_cases, services):
        self.use_cases = use_cases
        self.services = services
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Video Downloader - Clean Architecture")
        self.root.geometry("800x700")
        self.root.configure(bg='#f5f5f5')
        
        # State
        self.current_video_info: Optional[VideoInfo] = None
        self.current_formats: list[VideoFormat] = []
        self.is_downloading = False
        
        self._create_widgets()
        self._setup_layout()
        self._setup_bindings()
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#f5f5f5')
        
        # Header
        self.header_frame = tk.Frame(self.main_frame, bg='#f5f5f5')
        self.title_label = tk.Label(
            self.header_frame,
            text="🎬 Video Downloader",
            font=('Segoe UI', 16, 'bold'),
            fg='#0078d4',
            bg='#f5f5f5'
        )
        
        # URL input section
        self.url_frame = tk.Frame(self.main_frame, bg='#f5f5f5')
        self.url_label = tk.Label(
            self.url_frame,
            text="Video URL:",
            font=('Segoe UI', 10, 'bold'),
            fg='#333333',
            bg='#f5f5f5'
        )
        self.url_entry = ModernEntry(
            self.url_frame,
            placeholder="Paste video URL here...",
            width=60
        )
        self.fetch_button = ModernButton(
            self.url_frame,
            text="Get Video Info",
            command=self._fetch_video_info
        )
        
        # Video info section
        self.video_info_frame = VideoInfoFrame(
            self.main_frame,
            bg='#f5f5f5'
        )
        
        # Format selection section
        self.format_frame = FormatSelectionFrame(
            self.main_frame,
            bg='#f5f5f5'
        )
        
        # Download options
        self.download_options_frame = tk.Frame(self.main_frame, bg='#f5f5f5')
        self.filename_label = tk.Label(
            self.download_options_frame,
            text="Custom Filename (optional):",
            font=('Segoe UI', 10),
            fg='#333333',
            bg='#f5f5f5'
        )
        self.filename_entry = ModernEntry(
            self.download_options_frame,
            placeholder="Leave empty for default filename...",
            width=40
        )
        
        # Progress section
        self.progress_frame = ProgressFrame(
            self.main_frame,
            bg='#f5f5f5'
        )
        
        # Action buttons
        self.buttons_frame = tk.Frame(self.main_frame, bg='#f5f5f5')
        self.download_button = ModernButton(
            self.buttons_frame,
            text="Download Video",
            command=self._start_download,
            state='disabled'
        )
        self.cancel_button = ModernButton(
            self.buttons_frame,
            text="Cancel",
            command=self._cancel_download,
            state='disabled',
            bg='#dc3545'
        )
        self.settings_button = ModernButton(
            self.buttons_frame,
            text="Settings",
            command=self._show_settings,
            bg='#6c757d'
        )
        
        # Status bar
        self.status_frame = tk.Frame(self.main_frame, bg='#e9ecef', relief='sunken', bd=1)
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            font=('Segoe UI', 9),
            fg='#495057',
            bg='#e9ecef'
        )
    
    def _setup_layout(self):
        """Setup the layout of widgets."""
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.header_frame.pack(fill='x', pady=(0, 20))
        self.title_label.pack()
        
        # URL input
        self.url_frame.pack(fill='x', pady=(0, 15))
        self.url_label.pack(anchor='w')
        self.url_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.fetch_button.pack(side='right')
        
        # Video info
        self.video_info_frame.pack(fill='x', pady=(0, 15))
        
        # Format selection
        self.format_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Download options
        self.download_options_frame.pack(fill='x', pady=(0, 15))
        self.filename_label.pack(anchor='w')
        self.filename_entry.pack(anchor='w', pady=(5, 0))
        
        # Progress
        self.progress_frame.pack(fill='x', pady=(0, 15))
        
        # Buttons
        self.buttons_frame.pack(fill='x', pady=(0, 15))
        self.download_button.pack(side='left', padx=(0, 10))
        self.cancel_button.pack(side='left', padx=(0, 10))
        self.settings_button.pack(side='right')
        
        # Status bar
        self.status_frame.pack(fill='x', side='bottom')
        self.status_label.pack(side='left', padx=10, pady=5)
    
    def _setup_bindings(self):
        """Setup event bindings."""
        self.url_entry.bind('<Return>', lambda e: self._fetch_video_info())
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _fetch_video_info(self):
        """Fetch video information from URL."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL")
            return
        
        # Disable fetch button and show loading
        self.fetch_button.config(state='disabled', text="Loading...")
        self.status_label.config(text="Fetching video information...")
        self.root.update()
        
        # Run in separate thread to avoid blocking UI
        thread = threading.Thread(target=self._fetch_video_info_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _fetch_video_info_thread(self, url: str):
        """Thread function for fetching video info."""
        try:
            # Validate URL
            if not self.use_cases['validate_url'].execute(url):
                self.root.after(0, lambda: self._show_error("Invalid video URL"))
                return
            
            # Get video info
            video_info = self.use_cases['get_video_info'].execute(url)
            
            # Get available formats
            formats = self.use_cases['get_formats'].execute(url)
            
            # Get recommended formats
            recommended_formats = self.services['format_selection'].get_recommended_formats(formats)
            
            # Update UI in main thread
            self.root.after(0, lambda: self._update_video_info_ui(video_info, recommended_formats))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Error fetching video info: {str(e)}"))
    
    def _update_video_info_ui(self, video_info: VideoInfo, formats: list[VideoFormat]):
        """Update UI with video information."""
        self.current_video_info = video_info
        self.current_formats = formats
        
        # Update video info display
        self.video_info_frame.update_video_info(video_info)
        
        # Update format selection
        self.format_frame.update_formats(formats)
        
        # Enable download button
        self.download_button.config(state='normal')
        
        # Reset fetch button
        self.fetch_button.config(state='normal', text="Get Video Info")
        
        # Update status
        self.status_label.config(text=f"Found {len(formats)} formats")
    
    def _start_download(self):
        """Start video download."""
        if not self.current_video_info or not self.current_formats:
            messagebox.showerror("Error", "No video selected")
            return
        
        selected_format = self.format_frame.get_selected_format()
        if not selected_format:
            messagebox.showerror("Error", "Please select a video format")
            return
        
        # Get custom filename
        custom_filename = self.filename_entry.get().strip()
        if custom_filename:
            custom_filename = self.services['path'].sanitize_filename(custom_filename)
        
        # Create download request
        request = DownloadRequest(
            url=self.current_video_info.url,
            selected_format=selected_format,
            custom_filename=custom_filename
        )
        
        # Update UI for download
        self.is_downloading = True
        self.download_button.config(state='disabled')
        self.cancel_button.config(state='normal')
        self.fetch_button.config(state='disabled')
        self.progress_frame.reset()
        self.progress_frame.set_status("Starting download...")
        self.status_label.config(text="Downloading...")
        
        # Run download in separate thread
        thread = threading.Thread(target=self._download_thread, args=(request,))
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, request: DownloadRequest):
        """Thread function for downloading video."""
        try:
            # Get download path
            download_path = self.services['path'].get_download_path(
                filename=request.custom_filename
            )
            request.output_path = download_path
            
            # Ensure download directory exists
            self.services['path'].ensure_download_directory(download_path)
            
            # Start download
            result = self.use_cases['download_video'].execute(request)
            
            if result.success:
                self.root.after(0, lambda: self._download_completed(result))
            else:
                self.root.after(0, lambda: self._show_error(f"Download failed: {result.error_message}"))
                
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Download error: {str(e)}"))
    
    def _download_completed(self, result):
        """Handle download completion."""
        self.is_downloading = False
        self.download_button.config(state='normal')
        self.cancel_button.config(state='disabled')
        self.fetch_button.config(state='normal')
        self.progress_frame.set_status("Download completed!")
        self.status_label.config(text="Ready")
        
        messagebox.showinfo("Success", f"Video downloaded successfully!\n\nFile: {result.file_path}")
    
    def _cancel_download(self):
        """Cancel current download."""
        # Note: This is a simplified implementation
        # In a real application, you'd need to implement proper cancellation
        self.is_downloading = False
        self.download_button.config(state='normal')
        self.cancel_button.config(state='disabled')
        self.fetch_button.config(state='normal')
        self.progress_frame.set_status("Download cancelled")
        self.status_label.config(text="Ready")
    
    def _show_settings(self):
        """Show settings dialog."""
        settings_window = SettingsDialog(self.root, self.services)
        self.root.wait_window(settings_window.dialog)
    
    def _show_error(self, message: str):
        """Show error message."""
        self.fetch_button.config(state='normal', text="Get Video Info")
        self.status_label.config(text="Error")
        messagebox.showerror("Error", message)
    
    def _on_closing(self):
        """Handle window closing."""
        if self.is_downloading:
            if messagebox.askokcancel("Quit", "Download in progress. Are you sure you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


class SettingsDialog:
    """Settings dialog window."""
    
    def __init__(self, parent, services):
        self.services = services
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x300")
        self.dialog.configure(bg='#f5f5f5')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._load_settings()
    
    def _create_widgets(self):
        """Create settings widgets."""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Settings",
            font=('Segoe UI', 14, 'bold'),
            fg='#333333',
            bg='#f5f5f5'
        )
        title_label.pack(pady=(0, 20))
        
        # Settings frame
        self.settings_frame = SettingsFrame(main_frame, bg='#f5f5f5')
        self.settings_frame.pack(fill='x', pady=(0, 20))
        
        # Buttons
        buttons_frame = tk.Frame(main_frame, bg='#f5f5f5')
        buttons_frame.pack(fill='x')
        
        save_button = ModernButton(
            buttons_frame,
            text="Save",
            command=self._save_settings
        )
        save_button.pack(side='right', padx=(10, 0))
        
        cancel_button = ModernButton(
            buttons_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bg='#6c757d'
        )
        cancel_button.pack(side='right')
    
    def _load_settings(self):
        """Load current settings."""
        # This would load from configuration repository
        pass
    
    def _save_settings(self):
        """Save settings."""
        # This would save to configuration repository
        self.dialog.destroy()
