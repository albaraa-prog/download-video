"""
Repository interfaces for the video downloader application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import VideoInfo, VideoFormat, DownloadResult, DownloadRequest


class VideoRepository(ABC):
    """Abstract repository for video operations."""
    
    @abstractmethod
    def get_video_info(self, url: str) -> Optional[VideoInfo]:
        """Get video information from URL."""
        pass
    
    @abstractmethod
    def get_available_formats(self, url: str) -> List[VideoFormat]:
        """Get available video formats for a URL."""
        pass
    
    @abstractmethod
    def download_video(self, request: DownloadRequest) -> DownloadResult:
        """Download video with specified format."""
        pass
    
    @abstractmethod
    def is_url_valid(self, url: str) -> bool:
        """Check if URL is valid for video download."""
        pass


class ConfigurationRepository(ABC):
    """Abstract repository for configuration operations."""
    
    @abstractmethod
    def get_download_path(self) -> str:
        """Get default download path."""
        pass
    
    @abstractmethod
    def set_download_path(self, path: str) -> None:
        """Set default download path."""
        pass
    
    @abstractmethod
    def get_preferred_format(self) -> Optional[str]:
        """Get preferred format preference."""
        pass
    
    @abstractmethod
    def set_preferred_format(self, format_id: str) -> None:
        """Set preferred format preference."""
        pass
