#!/usr/bin/env python3
"""
Test script to verify the clean architecture implementation.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from domain.entities import VideoInfo, VideoFormat, DownloadRequest
        from domain.repositories import VideoRepository, ConfigurationRepository
        from domain.exceptions import VideoDownloaderException
        from application.use_cases import GetVideoInfoUseCase, DownloadVideoUseCase
        from application.services import FormatSelectionService, PathService
        from infrastructure.video_repository_impl import YtDlpVideoRepository
        from infrastructure.config_repository_impl import JsonConfigurationRepository
        from di_container import DIContainer
        print("+ All imports successful")
        return True
    except ImportError as e:
        print(f"X Import error: {e}")
        return False

def test_di_container():
    """Test dependency injection container."""
    try:
        container = DIContainer()
        use_cases = container.get_use_cases()
        services = container.get_services()
        
        assert 'get_video_info' in use_cases
        assert 'download_video' in use_cases
        assert 'format_selection' in services
        assert 'path' in services
        
        print("+ Dependency injection container working")
        return True
    except Exception as e:
        print(f"X DI container error: {e}")
        return False

def test_entities():
    """Test domain entities."""
    try:
        from domain.entities import VideoInfo, VideoFormat, DownloadRequest
        
        # Test VideoInfo
        video_info = VideoInfo(
            title="Test Video",
            url="https://example.com/video",
            duration=120
        )
        assert video_info.title == "Test Video"
        assert video_info.duration_formatted == "02:00"
        
        # Test VideoFormat
        video_format = VideoFormat(
            format_id="test_format",
            resolution="720p",
            height=720,
            width=1280,
            extension="mp4",
            file_size="10.5 MB",
            format_note="Test format",
            has_audio=True
        )
        assert video_format.display_name.startswith("720p")
        assert video_format.audio_info == "🔊 With Audio"
        
        print("+ Domain entities working")
        return True
    except Exception as e:
        print(f"X Entities error: {e}")
        return False

def test_services():
    """Test application services."""
    try:
        from application.services import FormatSelectionService, PathService
        from infrastructure.config_repository_impl import JsonConfigurationRepository
        
        config_repo = JsonConfigurationRepository("test_config.json")
        format_service = FormatSelectionService(config_repo)
        path_service = PathService(config_repo)
        
        # Test path service
        test_path = path_service.get_download_path("test_video.mp4")
        assert "test_video.mp4" in test_path
        
        print("+ Application services working")
        return True
    except Exception as e:
        print(f"X Services error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Clean Architecture Implementation")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_di_container,
        test_entities,
        test_services
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Clean architecture is working correctly.")
        return True
    else:
        print("Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
