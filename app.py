#!/usr/bin/env python3
"""
Video Downloader Application - Clean Architecture Implementation

This is the main entry point for the video downloader application.
It uses clean architecture principles with dependency injection.
"""

import sys
import os
from di_container import DIContainer
from domain.exceptions import VideoDownloaderException


def check_dependencies():
    """Check if all required dependencies are available."""
    try:
        import yt_dlp
        import tkinter
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install yt-dlp")
        print("pip install -r requirements.txt")
        return False


def main():
    """Main application entry point."""
    print("🎬 Video Downloader - Clean Architecture")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Create dependency injection container
        container = DIContainer()
        
        # Create and run the main window
        app = container.create_main_window()
        app.run()
        
    except VideoDownloaderException as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
