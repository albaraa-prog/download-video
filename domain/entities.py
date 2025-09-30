"""
Domain entities for the video downloader application.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class VideoFormatType(Enum):
    """Video format types."""
    VIDEO_ONLY = "video_only"
    AUDIO_ONLY = "audio_only"
    VIDEO_AUDIO = "video_audio"


@dataclass
class VideoFormat:
    """Represents a video format option."""
    format_id: str
    resolution: str
    height: int
    width: int
    extension: str
    file_size: Optional[str]
    format_note: str
    has_audio: bool
    is_auto: bool = False
    is_compatible: bool = False
    
    @property
    def audio_info(self) -> str:
        """Get audio information string."""
        return "🔊 With Audio" if self.has_audio else "🔇 No Audio"
    
    @property
    def display_name(self) -> str:
        """Get display name for the format."""
        if self.is_auto:
            return "🎯 Best Quality with Audio (Recommended)"
        elif self.is_compatible:
            return "🔧 Best Compatible Format (Works everywhere)"
        else:
            return f"{self.resolution} ({self.height}p) - {self.extension.upper()} - {self.file_size or 'Unknown'} - {self.audio_info}"


@dataclass
class VideoInfo:
    """Represents video information."""
    title: str
    url: str
    duration: Optional[int] = None
    description: Optional[str] = None
    uploader: Optional[str] = None
    upload_date: Optional[str] = None
    view_count: Optional[int] = None
    
    @property
    def duration_formatted(self) -> str:
        """Get formatted duration string."""
        if not self.duration:
            return "Unknown"
        
        hours = self.duration // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"


@dataclass
class DownloadRequest:
    """Represents a download request."""
    url: str
    selected_format: VideoFormat
    output_path: Optional[str] = None
    custom_filename: Optional[str] = None


@dataclass
class DownloadResult:
    """Represents the result of a download operation."""
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    file_size: Optional[int] = None
    duration: Optional[float] = None
