#!/usr/bin/env python3
"""
Video Downloader Script with Resolution Selection

This script downloads videos from the internet (e.g., YouTube) using a URL.
It offers a list of available resolutions, allows the user to select one,
and downloads the video accordingly.
"""

import json
import os
import subprocess
import sys
from typing import Dict, List, Optional

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    print("Warning: yt-dlp not found. Please install it with: pip install yt-dlp")

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("Note: tqdm not found. Progress bars will not be shown. Install with: pip install tqdm")


class VideoDownloader:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        """Extract video information and available formats."""
        if not YT_DLP_AVAILABLE:
            print("Error: yt-dlp is required but not installed.")
            print("Install it with: pip install yt-dlp")
            return None
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            print(f"Error extracting video info: {e}")
            return None
    
    def get_available_formats(self, info: Dict) -> List[Dict]:
        """Get available video formats with resolution information."""
        formats = []
        
        if 'formats' in info:
            for fmt in info['formats']:
                # Skip formats without video
                if fmt.get('vcodec') == 'none':
                    continue
                
                # Get resolution info
                resolution = fmt.get('resolution', 'N/A')
                height = fmt.get('height', 0)
                width = fmt.get('width', 0)
                
                # Get file size if available
                filesize = fmt.get('filesize', 0)
                if filesize:
                    filesize_mb = filesize / (1024 * 1024)
                    size_str = f"{filesize_mb:.1f} MB"
                else:
                    size_str = "Unknown"
                
                # Get format info
                format_id = fmt.get('format_id', 'N/A')
                ext = fmt.get('ext', 'N/A')
                
                formats.append({
                    'format_id': format_id,
                    'resolution': resolution,
                    'height': height,
                    'width': width,
                    'ext': ext,
                    'filesize': size_str,
                    'format_note': fmt.get('format_note', ''),
                    'format': fmt
                })
        
        # Sort by height (resolution) in descending order
        formats.sort(key=lambda x: x['height'], reverse=True)
        return formats
    
    def display_formats(self, formats: List[Dict], video_title: str):
        """Display available formats in a numbered list."""
        print(f"\n📹 Video: {video_title}")
        print("=" * 60)
        print("Available formats:")
        print("-" * 60)
        
        for i, fmt in enumerate(formats, 1):
            resolution = fmt['resolution']
            height = fmt['height']
            ext = fmt['ext']
            size = fmt['filesize']
            note = fmt['format_note']
            
            print(f"{i:2d}. {resolution} ({height}p) - {ext.upper()} - {size}")
            if note:
                print(f"    Note: {note}")
        
        print("-" * 60)
    
    def get_user_selection(self, formats: List[Dict]) -> Optional[Dict]:
        """Get user's format selection."""
        while True:
            try:
                choice = input(f"\nSelect format (1-{len(formats)}): ").strip()
                if choice.lower() == 'q':
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(formats):
                    return formats[choice_num - 1]
                else:
                    print(f"Please enter a number between 1 and {len(formats)}")
            except ValueError:
                print("Please enter a valid number or 'q' to quit")
    
    def download_video(self, url: str, selected_format: Dict, output_path: str = None):
        """Download the video with the selected format."""
        format_id = selected_format['format_id']
        
        # Set up download options
        download_opts = {
            'format': format_id,
            'outtmpl': output_path or '%(title)s.%(ext)s',
        }
        
        if TQDM_AVAILABLE:
            # Custom progress hook for tqdm
            def progress_hook(d):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    downloaded = d.get('downloaded_bytes', 0)
                    if total > 0:
                        percentage = (downloaded / total) * 100
                        speed = d.get('speed', 0)
                        if speed:
                            speed_mb = speed / (1024 * 1024)
                            print(f"\rDownloading: {percentage:.1f}% - {speed_mb:.1f} MB/s", end='', flush=True)
            
            download_opts['progress_hooks'] = [progress_hook]
        
        try:
            print(f"\nDownloading video with format: {selected_format['resolution']} ({selected_format['ext'].upper()})")
            print("This may take a while...")
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                ydl.download([url])
            
            if TQDM_AVAILABLE:
                print("\n✅ Download completed!")
            else:
                print("✅ Download completed!")
                
        except Exception as e:
            print(f"\n❌ Error during download: {e}")
    
    def run(self):
        """Main execution flow."""
        print("🎬 Video Downloader with Resolution Selection")
        print("=" * 50)
        
        # Get video URL
        url = input("Enter video URL: ").strip()
        if not url:
            print("No URL provided. Exiting.")
            return
        
        # Get video information
        print("Fetching video information...")
        info = self.get_video_info(url)
        if not info:
            print("Failed to get video information. Please check the URL.")
            return
        
        # Get available formats
        formats = self.get_available_formats(info)
        if not formats:
            print("No video formats found.")
            return
        
        # Display formats
        video_title = info.get('title', 'Unknown Title')
        self.display_formats(formats, video_title)
        
        # Get user selection
        selected_format = self.get_user_selection(formats)
        if not selected_format:
            print("Download cancelled.")
            return
        
        # Get output path (optional)
        output_path = input("Enter output path (or press Enter for default): ").strip()
        if not output_path:
            output_path = None
        
        # Download the video
        self.download_video(url, selected_format, output_path)


def main():
    """Main function."""
    if not YT_DLP_AVAILABLE:
        print("❌ yt-dlp is required but not installed.")
        print("Please install it with: pip install yt-dlp")
        print("Or: pip install -r requirements.txt")
        return
    
    downloader = VideoDownloader()
    
    try:
        downloader.run()
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main() 