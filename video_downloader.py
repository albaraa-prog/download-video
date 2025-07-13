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
                # Skip audio-only formats
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
                
                # Check if format has audio
                has_audio = fmt.get('acodec') != 'none'
                audio_info = "🔊 With Audio" if has_audio else "🔇 No Audio"
                
                formats.append({
                    'format_id': format_id,
                    'resolution': resolution,
                    'height': height,
                    'width': width,
                    'ext': ext,
                    'filesize': size_str,
                    'format_note': fmt.get('format_note', ''),
                    'format': fmt,
                    'has_audio': has_audio,
                    'audio_info': audio_info
                })
        
        # Sort by height (resolution) in descending order, prioritizing formats with audio
        formats.sort(key=lambda x: (x['height'], not x['has_audio']), reverse=True)
        return formats
    
    def display_formats(self, formats: List[Dict], video_title: str):
        """Display available formats in a numbered list."""
        print(f"\n📹 Video: {video_title}")
        print("=" * 60)
        print("Available formats:")
        print("-" * 60)
        
        # Add "Best with Audio" option at the top
        print(" 0. 🎯 Best Quality with Audio (Recommended)")
        print(" 1. 🔧 Best Compatible Format (Works everywhere)")
        print("-" * 60)
        
        for i, fmt in enumerate(formats, 2):
            resolution = fmt['resolution']
            height = fmt['height']
            ext = fmt['ext']
            size = fmt['filesize']
            note = fmt['format_note']
            audio_info = fmt['audio_info']
            
            print(f"{i:2d}. {resolution} ({height}p) - {ext.upper()} - {size} - {audio_info}")
            if note:
                print(f"    Note: {note}")
        
        print("-" * 60)
    
    def get_user_selection(self, formats: List[Dict]) -> Optional[Dict]:
        """Get user's format selection."""
        while True:
            try:
                choice = input(f"\nSelect format (0-{len(formats)+1}): ").strip()
                if choice.lower() == 'q':
                    return None
                
                choice_num = int(choice)
                if choice_num == 0:
                    # Return special format for "best with audio"
                    return {
                        'format_id': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'resolution': 'Best Available',
                        'height': 9999,
                        'width': 9999,
                        'ext': 'mp4',
                        'filesize': 'Unknown',
                        'format_note': 'Best quality with audio (automatic selection)',
                        'has_audio': True,
                        'audio_info': '🔊 With Audio (Best)',
                        'is_auto': True
                    }
                elif choice_num == 1:
                    # Return special format for "best compatible"
                    return {
                        'format_id': 'best[height<=720][ext=mp4]/best[height<=720]/best[ext=mp4]/best',
                        'resolution': '720p or lower (Compatible)',
                        'height': 720,
                        'width': 1280,
                        'ext': 'mp4',
                        'filesize': 'Unknown',
                        'format_note': 'Best compatible format for all players',
                        'has_audio': True,
                        'audio_info': '🔊 With Audio (Compatible)',
                        'is_compatible': True
                    }
                elif 2 <= choice_num <= len(formats)+1:
                    return formats[choice_num - 2]
                else:
                    print(f"Please enter a number between 0 and {len(formats)+1}")
            except ValueError:
                print("Please enter a valid number or 'q' to quit")
    
    def download_video(self, url: str, selected_format: Dict, output_path: str = None):
        """Download the video with the selected format."""
        format_id = selected_format['format_id']
        
        # Set default output path to downloads folder
        if not output_path:
            output_path = os.path.join('downloads', '%(title)s.%(ext)s')
        elif not os.path.isabs(output_path) and not output_path.startswith('downloads'):
            # If relative path doesn't start with downloads, put it in downloads folder
            output_path = os.path.join('downloads', output_path)
        
        # Set up download options
        if selected_format.get('is_auto', False):
            # For automatic "best with audio" selection
            download_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': output_path,
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mp4',
                }],
                'postprocessor_args': {
                    'ffmpeg': ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k']
                }
            }
        elif selected_format.get('is_compatible', False):
            # For "best compatible" selection
            download_opts = {
                'format': 'best[height<=720][ext=mp4]/best[height<=720]/best[ext=mp4]/best',
                'outtmpl': output_path,
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mp4',
                }],
                'postprocessor_args': {
                    'ffmpeg': ['-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-b:a', '128k']
                }
            }
        else:
            # For specific format selection
            download_opts = {
                'format': f'{format_id}+bestaudio[ext=m4a]/bestaudio/best',  # Download video + best audio and merge
                'outtmpl': output_path,
                'merge_output_format': 'mp4',  # Ensure output is MP4
                'postprocessors': [{
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mp4',
                }],
                'postprocessor_args': {
                    'ffmpeg': ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k']
                }
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
            if selected_format['has_audio']:
                print("✅ This format includes audio")
            else:
                print("⚠️  This format doesn't include audio, but will be merged with best available audio")
            print(f"📁 Saving to: {output_path}")
            print("🔊 Audio will be encoded in AAC format for maximum compatibility")
            print("This may take a while...")
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                ydl.download([url])
            
            if TQDM_AVAILABLE:
                print("\n✅ Download completed!")
            else:
                print("✅ Download completed!")
            
            print("\n💡 Note: If audio doesn't play in some players (VS Code, File Explorer),")
            print("   try using VLC, Windows Media Player, or other dedicated video players.")
                
        except Exception as e:
            print(f"\n❌ Error during download: {e}")
    
    def run(self):
        """Main execution flow."""
        print("🎬 Video Downloader with Resolution Selection")
        print("=" * 50)
        print("📁 Videos will be saved in the 'downloads' folder")
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
        output_path = input("Enter output filename (or press Enter for default in downloads folder): ").strip()
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