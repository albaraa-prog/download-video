#!/usr/bin/env python3
"""
Flask-based Video Downloader Web Application

A simple web interface for downloading videos from any website using yt-dlp.
"""

import os
import json
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import yt_dlp
from urllib.parse import urlparse
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'webm', 'avi', 'mov', 'flv', 'wmv', 'm4a', 'mp3', 'wav'}

# Ensure downloads directory exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Global variable to track download status
download_status = {
    'in_progress': False,
    'progress': 0,
    'status': '',
    'filename': '',
    'error': None
}

class VideoDownloader:
    """Video downloader class using yt-dlp."""
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'retries': 5,
            'fragment_retries': 5,
            'socket_timeout': 60,
            'ignoreerrors': False,
            'no_check_certificate': True,
            'prefer_insecure': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
            'cookiesfrombrowser': None,
            'extractor_retries': 3,
            'fragment_retries': 5,
            'skip_unavailable_fragments': True,
            'keep_fragments': True,
            'http_chunk_size': 10485760,  # 10MB chunks
        }
    
    def is_valid_url(self, url):
        """Check if URL is valid for video download."""
        if not url or not url.strip():
            return False
        
        try:
            parsed = urlparse(url)
            return parsed.scheme in ['http', 'https'] and parsed.netloc
        except:
            return False

    def get_video_info(self, url):
        """Get video information from URL."""
        try:
            # Enhanced options for better compatibility
            info_opts = self.ydl_opts.copy()
            info_opts.update({
                'extract_flat': False,
                'writethumbnail': False,
                'writeinfojson': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
            })
            
            with yt_dlp.YoutubeDL(info_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                    'thumbnail': info.get('thumbnail', ''),
                    'formats': self._extract_formats(info)
                }
        except Exception as e:
            error_msg = str(e)
            if "HTTP Error 403" in error_msg:
                if "movies4us" in url.lower() or "streaming" in url.lower():
                    raise Exception("This appears to be a streaming site with strong anti-bot protection. These sites typically don't allow direct downloads. Try using a supported platform like YouTube, Vimeo, or other major video sites.")
                else:
                    raise Exception("Access denied. This video may be private, region-restricted, or require authentication. Please try a different video or check if the video is publicly available.")
            elif "Video unavailable" in error_msg:
                raise Exception("This video is unavailable. It may have been removed, made private, or is not accessible.")
            elif "Requested format is not available" in error_msg:
                raise Exception("The requested video format is not available. Please try a different video or check the video URL.")
            elif "Sign in to confirm your age" in error_msg:
                raise Exception("This video requires age verification. Please try a different video.")
            elif "No video formats found" in error_msg:
                raise Exception("No downloadable video formats found. This site may not be supported or may require special access.")
            elif "Unsupported URL" in error_msg:
                raise Exception("This URL is not supported. Please try a video from YouTube, Vimeo, or other supported platforms.")
            else:
                raise Exception(f"Error extracting video info: {error_msg}")
    
    def _extract_formats(self, info):
        """Extract available formats from video info."""
        formats = []
        
        if 'formats' in info:
            for fmt in info['formats']:
                # Skip audio-only formats for simplicity
                if fmt.get('vcodec') == 'none':
                    continue
                
                # Skip formats that are not available
                if fmt.get('filesize') == 0 and not fmt.get('url'):
                    continue
                
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
                
                # Check if format has audio
                has_audio = fmt.get('acodec') != 'none'
                
                # Get format quality info
                format_note = fmt.get('format_note', '')
                if not format_note and height:
                    if height >= 1080:
                        format_note = "High Quality"
                    elif height >= 720:
                        format_note = "Medium Quality"
                    elif height >= 480:
                        format_note = "Standard Quality"
                    else:
                        format_note = "Low Quality"
                
                formats.append({
                    'format_id': fmt.get('format_id', 'N/A'),
                    'resolution': resolution,
                    'height': height,
                    'width': width,
                    'extension': fmt.get('ext', 'N/A'),
                    'file_size': size_str,
                    'has_audio': has_audio,
                    'format_note': format_note
                })
        
        # Sort by height (resolution) in descending order, then by audio availability
        formats.sort(key=lambda x: (x['height'], x['has_audio']), reverse=True)
        
        # Limit to top 15 formats to avoid overwhelming the UI
        return formats[:15]
    
    def download_video(self, url, format_id='best', custom_filename=None):
        """Download video with specified format."""
        global download_status
        
        try:
            # Set up download options
            output_path = os.path.join(DOWNLOAD_FOLDER, custom_filename) if custom_filename else os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')
            
            # Enhanced download options for better compatibility
            # Create fallback format selection
            if format_id == 'best':
                format_selector = 'best[height<=1080]/best[height<=720]/best[height<=480]/best'
            else:
                format_selector = f'{format_id}+bestaudio/bestaudio/best'
            
            download_opts = {
                'format': format_selector,
                'outtmpl': output_path,
                'progress_hooks': [self._progress_hook],
                'merge_output_format': 'mp4',
                'writethumbnail': False,
                'writeinfojson': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'postprocessors': [{
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mp4',
                }],
                'postprocessor_args': {
                    'ffmpeg': ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart']
                }
            }
            
            # Update with base options
            download_opts.update(self.ydl_opts)
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                ydl.download([url])
            
            return True, "Download completed successfully!"
            
        except Exception as e:
            error_msg = str(e)
            if "HTTP Error 403" in error_msg:
                if "movies4us" in url.lower() or "streaming" in url.lower():
                    return False, "This appears to be a streaming site with strong anti-bot protection. These sites typically don't allow direct downloads. Try using a supported platform like YouTube, Vimeo, or other major video sites."
                else:
                    return False, "Access denied. This video may be private, region-restricted, or require authentication. Please try a different video."
            elif "Video unavailable" in error_msg:
                return False, "This video is unavailable. It may have been removed or made private."
            elif "Requested format is not available" in error_msg:
                return False, "The requested video format is not available. Please try selecting a different quality option."
            elif "Sign in to confirm your age" in error_msg:
                return False, "This video requires age verification. Please try a different video."
            elif "No video formats found" in error_msg:
                return False, "No downloadable video formats found. This site may not be supported or may require special access."
            elif "Unsupported URL" in error_msg:
                return False, "This URL is not supported. Please try a video from YouTube, Vimeo, or other supported platforms."
            else:
                return False, f"Download failed: {error_msg}"
    
    def _progress_hook(self, d):
        """Progress hook for download progress."""
        global download_status
        
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                percentage = (downloaded / total) * 100
                speed = d.get('speed', 0)
                speed_mb = speed / (1024 * 1024) if speed else 0
                
                download_status['progress'] = percentage
                download_status['status'] = f"Downloading: {percentage:.1f}% - {speed_mb:.1f} MB/s"
        
        elif d['status'] == 'finished':
            download_status['progress'] = 100
            download_status['status'] = 'Download completed!'
            download_status['filename'] = d.get('filename', 'Unknown')

# Initialize downloader
downloader = VideoDownloader()

@app.route('/')
def index():
    """Main page with video download form."""
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_video_info():
    """Get video information from URL."""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'success': False, 'error': 'Please enter a URL'})
        
        if not downloader.is_valid_url(url):
            return jsonify({'success': False, 'error': 'Please enter a valid URL'})
        
        info = downloader.get_video_info(url)
        return jsonify({'success': True, 'info': info})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download', methods=['POST'])
def download_video():
    """Download video from URL."""
    global download_status
    
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        format_id = data.get('format', 'best')
        custom_filename = data.get('filename', '').strip()
        
        if not url:
            return jsonify({'success': False, 'error': 'Please enter a URL'})
        
        if not downloader.is_valid_url(url):
            return jsonify({'success': False, 'error': 'Please enter a valid URL'})
        
        # Check if download is already in progress
        if download_status['in_progress']:
            return jsonify({'success': False, 'error': 'A download is already in progress'})
        
        # Reset download status
        download_status = {
            'in_progress': True,
            'progress': 0,
            'status': 'Starting download...',
            'filename': '',
            'error': None
        }
        
        # Start download in a separate thread
        def download_thread():
            global download_status
            try:
                success, message = downloader.download_video(url, format_id, custom_filename)
                if success:
                    download_status['status'] = 'Download completed!'
                    download_status['progress'] = 100
                else:
                    download_status['error'] = message
                    download_status['status'] = 'Download failed'
                download_status['in_progress'] = False
            except Exception as e:
                download_status['error'] = str(e)
                download_status['status'] = 'Download failed'
                download_status['in_progress'] = False
        
        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'message': 'Download started'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/status')
def get_download_status():
    """Get current download status."""
    return jsonify(download_status)

@app.route('/downloads')
def list_downloads():
    """List downloaded files."""
    try:
        files = []
        for filename in os.listdir(DOWNLOAD_FOLDER):
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': stat.st_mtime
                })
        
        # Sort by modification time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🎬 Video Downloader Web App")
    print("=" * 50)
    print(f"📁 Downloads will be saved to: {os.path.abspath(DOWNLOAD_FOLDER)}")
    print("🌐 Starting Flask server on http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)