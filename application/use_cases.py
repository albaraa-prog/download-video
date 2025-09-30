"""
Use cases for the video downloader application.
"""

from typing import List, Optional
from ..domain.entities import VideoInfo, VideoFormat, DownloadRequest, DownloadResult
from ..domain.repositories import VideoRepository, ConfigurationRepository
from ..domain.exceptions import InvalidUrlException, VideoInfoException, FormatNotAvailableException, DownloadException


class GetVideoInfoUseCase:
    """Use case for getting video information."""
    
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository
    
    def execute(self, url: str) -> VideoInfo:
        """Execute the use case to get video information."""
        if not url or not url.strip():
            raise InvalidUrlException("URL cannot be empty")
        
        if not self.video_repository.is_url_valid(url):
            raise InvalidUrlException("Invalid video URL")
        
        video_info = self.video_repository.get_video_info(url)
        if not video_info:
            raise VideoInfoException("Could not retrieve video information")
        
        return video_info


class GetAvailableFormatsUseCase:
    """Use case for getting available video formats."""
    
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository
    
    def execute(self, url: str) -> List[VideoFormat]:
        """Execute the use case to get available formats."""
        if not url or not url.strip():
            raise InvalidUrlException("URL cannot be empty")
        
        formats = self.video_repository.get_available_formats(url)
        if not formats:
            raise FormatNotAvailableException("No video formats available")
        
        return formats


class DownloadVideoUseCase:
    """Use case for downloading a video."""
    
    def __init__(self, video_repository: VideoRepository, config_repository: ConfigurationRepository):
        self.video_repository = video_repository
        self.config_repository = config_repository
    
    def execute(self, request: DownloadRequest) -> DownloadResult:
        """Execute the use case to download a video."""
        if not request.url or not request.url.strip():
            raise InvalidUrlException("URL cannot be empty")
        
        if not self.video_repository.is_url_valid(request.url):
            raise InvalidUrlException("Invalid video URL")
        
        # Set default output path if not provided
        if not request.output_path:
            request.output_path = self.config_repository.get_download_path()
        
        try:
            result = self.video_repository.download_video(request)
            if not result.success:
                raise DownloadException(result.error_message or "Download failed")
            return result
        except Exception as e:
            raise DownloadException(f"Download failed: {str(e)}")


class ValidateUrlUseCase:
    """Use case for validating video URLs."""
    
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository
    
    def execute(self, url: str) -> bool:
        """Execute the use case to validate URL."""
        if not url or not url.strip():
            return False
        
        return self.video_repository.is_url_valid(url)
