"""
Domain exceptions for the video downloader application.
"""


class VideoDownloaderException(Exception):
    """Base exception for video downloader."""
    pass


class InvalidUrlException(VideoDownloaderException):
    """Raised when URL is invalid."""
    pass


class VideoInfoException(VideoDownloaderException):
    """Raised when video information cannot be retrieved."""
    pass


class FormatNotAvailableException(VideoDownloaderException):
    """Raised when requested format is not available."""
    pass


class DownloadException(VideoDownloaderException):
    """Raised when download fails."""
    pass


class ConfigurationException(VideoDownloaderException):
    """Raised when configuration is invalid."""
    pass
