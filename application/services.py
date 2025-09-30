"""
Application services for the video downloader application.
"""

import os
from typing import List, Optional
from domain.entities import VideoFormat, VideoInfo
from domain.repositories import ConfigurationRepository
from domain.exceptions import ConfigurationException


class FormatSelectionService:
    """Service for handling format selection logic."""
    
    def __init__(self, config_repository: ConfigurationRepository):
        self.config_repository = config_repository
    
    def get_recommended_formats(self, formats: List[VideoFormat]) -> List[VideoFormat]:
        """Get recommended formats with special options."""
        recommended = []
        
        # Add "Best with Audio" option
        best_audio = VideoFormat(
            format_id='bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            resolution='Best Available',
            height=9999,
            width=9999,
            extension='mp4',
            file_size='Unknown',
            format_note='Best quality with audio (automatic selection)',
            has_audio=True,
            is_auto=True
        )
        recommended.append(best_audio)
        
        # Add "Best Compatible" option
        best_compatible = VideoFormat(
            format_id='best[height<=720][ext=mp4]/best[height<=720]/best[ext=mp4]/best',
            resolution='720p or lower (Compatible)',
            height=720,
            width=1280,
            extension='mp4',
            file_size='Unknown',
            format_note='Best compatible format for all players',
            has_audio=True,
            is_compatible=True
        )
        recommended.append(best_compatible)
        
        # Add actual formats
        recommended.extend(formats)
        
        return recommended
    
    def sort_formats(self, formats: List[VideoFormat]) -> List[VideoFormat]:
        """Sort formats by quality and audio availability."""
        return sorted(formats, key=lambda x: (x.height, not x.has_audio), reverse=True)


class PathService:
    """Service for handling file paths."""
    
    def __init__(self, config_repository: ConfigurationRepository):
        self.config_repository = config_repository
    
    def get_download_path(self, custom_path: Optional[str] = None, filename: Optional[str] = None) -> str:
        """Get the full download path."""
        if custom_path:
            if os.path.isabs(custom_path):
                return custom_path
            else:
                base_path = self.config_repository.get_download_path()
                return os.path.join(base_path, custom_path)
        
        base_path = self.config_repository.get_download_path()
        if filename:
            # If filename is provided, use it as a template with extension
            if not filename.endswith('.%(ext)s'):
                filename = filename + '.%(ext)s'
            return os.path.join(base_path, filename)
        
        return os.path.join(base_path, '%(title)s.%(ext)s')
    
    def ensure_download_directory(self, path: str) -> None:
        """Ensure the download directory exists."""
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file system usage."""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:200-len(ext)] + ext
        
        return filename
