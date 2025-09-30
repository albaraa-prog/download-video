"""
Dependency injection container for the video downloader application.
"""

from infrastructure.video_repository_impl import YtDlpVideoRepository
from infrastructure.config_repository_impl import JsonConfigurationRepository
from application.use_cases import (
    GetVideoInfoUseCase,
    GetAvailableFormatsUseCase,
    DownloadVideoUseCase,
    ValidateUrlUseCase
)
from application.services import FormatSelectionService, PathService
from presentation.main_window import VideoDownloaderWindow


class DIContainer:
    """Dependency injection container."""
    
    def __init__(self):
        self._instances = {}
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        """Setup all dependencies."""
        # Infrastructure layer
        self._instances['video_repository'] = YtDlpVideoRepository()
        self._instances['config_repository'] = JsonConfigurationRepository()
        
        # Application services
        self._instances['format_selection_service'] = FormatSelectionService(
            self._instances['config_repository']
        )
        self._instances['path_service'] = PathService(
            self._instances['config_repository']
        )
        
        # Use cases
        self._instances['get_video_info_use_case'] = GetVideoInfoUseCase(
            self._instances['video_repository']
        )
        self._instances['get_formats_use_case'] = GetAvailableFormatsUseCase(
            self._instances['video_repository']
        )
        self._instances['download_video_use_case'] = DownloadVideoUseCase(
            self._instances['video_repository'],
            self._instances['config_repository']
        )
        self._instances['validate_url_use_case'] = ValidateUrlUseCase(
            self._instances['video_repository']
        )
    
    def get(self, name: str):
        """Get dependency by name."""
        if name not in self._instances:
            raise ValueError(f"Dependency '{name}' not found")
        return self._instances[name]
    
    def get_use_cases(self):
        """Get all use cases as a dictionary."""
        return {
            'get_video_info': self.get('get_video_info_use_case'),
            'get_formats': self.get('get_formats_use_case'),
            'download_video': self.get('download_video_use_case'),
            'validate_url': self.get('validate_url_use_case')
        }
    
    def get_services(self):
        """Get all services as a dictionary."""
        return {
            'format_selection': self.get('format_selection_service'),
            'path': self.get('path_service')
        }
    
    def create_main_window(self):
        """Create the main window with all dependencies."""
        return VideoDownloaderWindow(
            use_cases=self.get_use_cases(),
            services=self.get_services()
        )
