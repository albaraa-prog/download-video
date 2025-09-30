"""
Implementation of video repository using yt-dlp.
"""

import os
import json
from typing import List, Optional
from domain.entities import VideoInfo, VideoFormat, DownloadRequest, DownloadResult
from domain.repositories import VideoRepository
from domain.exceptions import VideoInfoException, DownloadException

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class YtDlpVideoRepository(VideoRepository):
    """Video repository implementation using yt-dlp."""
    
    def __init__(self):
        if not YT_DLP_AVAILABLE:
            raise ImportError("yt-dlp is required but not installed")
        
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'retries': 3,
            'fragment_retries': 3,
            'socket_timeout': 30,
            'ignoreerrors': False,
        }
    
    def get_video_info(self, url: str) -> Optional[VideoInfo]:
        """Get video information from URL."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return self._convert_to_video_info(info)
        except Exception as e:
            error_msg = str(e)
            if "HTTP Error 403" in error_msg:
                raise VideoInfoException("Access denied. This might be due to regional restrictions or rate limiting. Please try again later or use a VPN.")
            elif "Requested format is not available" in error_msg:
                raise VideoInfoException("The requested video format is not available. Please try a different format.")
            elif "Video unavailable" in error_msg:
                raise VideoInfoException("This video is unavailable. It may have been removed or made private.")
            else:
                raise VideoInfoException(f"Error extracting video info: {error_msg}")
    
    def get_available_formats(self, url: str) -> List[VideoFormat]:
        """Get available video formats for a URL."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return self._extract_formats(info)
        except Exception as e:
            error_msg = str(e)
            if "HTTP Error 403" in error_msg:
                raise VideoInfoException("Access denied. This might be due to regional restrictions or rate limiting. Please try again later or use a VPN.")
            elif "Requested format is not available" in error_msg:
                raise VideoInfoException("The requested video format is not available. Please try a different format.")
            elif "Video unavailable" in error_msg:
                raise VideoInfoException("This video is unavailable. It may have been removed or made private.")
            else:
                raise VideoInfoException(f"Error extracting formats: {error_msg}")
    
    def download_video(self, request: DownloadRequest) -> DownloadResult:
        """Download video with specified format."""
        try:
            format_id = request.selected_format.format_id
            
            # Set up download options
            download_opts = self._get_download_options(request)
            
            # Add progress hook if tqdm is available
            if TQDM_AVAILABLE:
                download_opts['progress_hooks'] = [self._progress_hook]
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                ydl.download([request.url])
            
            return DownloadResult(success=True, file_path=request.output_path)
            
        except Exception as e:
            return DownloadResult(success=False, error_message=str(e))
    
    def is_url_valid(self, url: str) -> bool:
        """Check if URL is valid for video download."""
        if not url or not url.strip():
            return False
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.extract_info(url, download=False)
                return True
        except:
            return False
    
    def _convert_to_video_info(self, info: dict) -> VideoInfo:
        """Convert yt-dlp info to VideoInfo entity."""
        return VideoInfo(
            title=info.get('title', 'Unknown Title'),
            url=info.get('webpage_url', ''),
            duration=info.get('duration'),
            description=info.get('description'),
            uploader=info.get('uploader'),
            upload_date=info.get('upload_date'),
            view_count=info.get('view_count')
        )
    
    def _extract_formats(self, info: dict) -> List[VideoFormat]:
        """Extract formats from yt-dlp info."""
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
                
                formats.append(VideoFormat(
                    format_id=format_id,
                    resolution=resolution,
                    height=height,
                    width=width,
                    extension=ext,
                    file_size=size_str,
                    format_note=fmt.get('format_note', ''),
                    has_audio=has_audio
                ))
        
        # Sort by height (resolution) in descending order, prioritizing formats with audio
        formats.sort(key=lambda x: (x.height, not x.has_audio), reverse=True)
        return formats
    
    def _get_download_options(self, request: DownloadRequest) -> dict:
        """Get download options based on the request."""
        format_id = request.selected_format.format_id
        
        # Ensure output path has proper template format
        output_path = request.output_path
        if not output_path.endswith('.%(ext)s'):
            if '.' in output_path:
                # Replace existing extension with template
                base_name = output_path.rsplit('.', 1)[0]
                output_path = base_name + '.%(ext)s'
            else:
                # Add template extension
                output_path = output_path + '.%(ext)s'
        
        if request.selected_format.is_auto:
            # For automatic "best with audio" selection
            return {
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
        elif request.selected_format.is_compatible:
            # For "best compatible" selection
            return {
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
            return {
                'format': f'{format_id}+bestaudio[ext=m4a]/bestaudio/best',
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
    
    def _progress_hook(self, d):
        """Progress hook for download progress."""
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                percentage = (downloaded / total) * 100
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / (1024 * 1024)
                    print(f"\rDownloading: {percentage:.1f}% - {speed_mb:.1f} MB/s", end='', flush=True)
