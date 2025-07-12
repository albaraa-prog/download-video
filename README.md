# Video Downloader Script with Resolution Selection

A Python script that downloads videos from the internet (e.g., YouTube) with interactive resolution selection.

## Features

- 🎬 Downloads videos from various platforms (YouTube, Vimeo, etc.)
- 📊 Lists all available video resolutions and formats
- 🎯 Interactive format selection
- 📁 Custom output path support
- 📈 Download progress tracking (with tqdm)
- 🛡️ Error handling and graceful failure recovery

## Installation

1. **Clone or download this repository**
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:

   ```bash
   pip install yt-dlp>=2023.03.04
   pip install tqdm>=4.64.0  # Optional, for progress bars
   ```

## Usage

1. **Run the script:**

   ```bash
   python video_downloader.py
   ```

2. **Enter the video URL when prompted**

3. **Select your preferred resolution from the displayed list**

4. **Optionally specify a custom output path**

5. **Wait for the download to complete**

## Example Output

```
🎬 Video Downloader with Resolution Selection
==================================================
Enter video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Fetching video information...

📹 Video: Rick Astley - Never Gonna Give You Up (Official Music Video)
============================================================
Available formats:
------------------------------------------------------------
 1. 1920x1080 (1080p) - MP4 - 45.2 MB
    Note: 1080p
 2. 1280x720 (720p) - MP4 - 28.7 MB
    Note: 720p
 3. 854x480 (480p) - MP4 - 18.3 MB
    Note: 480p
 4. 640x360 (360p) - MP4 - 12.1 MB
    Note: 360p
------------------------------------------------------------

Select format (1-4): 2

Enter output path (or press Enter for default):

Downloading video with format: 1280x720 (720p) - MP4
This may take a while...
Downloading: 45.2% - 2.1 MB/s
✅ Download completed!
```

## Supported Platforms

This script works with any platform supported by `yt-dlp`, including:

- YouTube
- Vimeo
- Dailymotion
- Facebook
- Twitter
- Instagram
- And many more...

## Dependencies

- **yt-dlp** (>=2023.03.04): Core video downloading functionality
- **tqdm** (>=4.64.0): Progress bar display (optional but recommended)

## Error Handling

The script includes comprehensive error handling for:

- Invalid URLs
- Network connectivity issues
- Unsupported video formats
- Permission errors
- Disk space issues

## Customization

You can modify the script to:

- Change default download options
- Add custom format filters
- Implement batch downloading
- Add audio-only download options
- Customize output naming patterns

## Troubleshooting

### Common Issues

1. **"yt-dlp not found" error:**

   ```bash
   pip install yt-dlp
   ```

2. **Permission errors:**

   - Ensure you have write permissions in the target directory
   - Try running as administrator (Windows) or with sudo (Linux/Mac)

3. **Network issues:**

   - Check your internet connection
   - Try using a VPN if the content is region-restricted

4. **Format not available:**
   - Some videos may have limited format options
   - Try a different video or check if the video is still available

## License

This script is provided as-is for educational and personal use. Please respect copyright laws and terms of service of the platforms you're downloading from.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this script.
