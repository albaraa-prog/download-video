# Troubleshooting Guide

## Common Issues and Solutions

### 1. HTTP 403 Forbidden Error
**Problem**: "Access denied" or "HTTP Error 403" when trying to download videos.

**Solutions**:
- The video may be private, region-restricted, or require authentication
- Try a different video that is publicly available
- Some videos may have age restrictions
- Check if the video URL is correct and accessible
- **For streaming sites** (like movies4us.co, 123movies, etc.): These sites have strong anti-bot protection and typically don't allow downloads. Try using supported platforms instead.

### 1.1 Streaming Sites Not Supported
**Problem**: Trying to download from streaming/movie sites that block downloads.

**Why it happens**:
- Sites like movies4us.co, 123movies, putlocker, etc. have anti-bot protection
- They use DRM (Digital Rights Management) to prevent downloads
- They require special authentication or browser sessions
- They may be region-restricted or have legal restrictions

**Solutions**:
- Use supported platforms: YouTube, Vimeo, Twitter, Instagram, TikTok
- Look for official sources of the content
- Check if the content is available on legitimate platforms

### 2. "Requested format is not available" Error
**Problem**: The selected video quality format is not available.

**Solutions**:
- Try selecting a different quality option from the dropdown
- Use the "Best Quality (Recommended)" option for automatic selection
- The video may only be available in certain formats

### 3. "Video unavailable" Error
**Problem**: The video cannot be accessed or has been removed.

**Solutions**:
- Check if the video URL is correct
- The video may have been deleted or made private
- Try refreshing the page and entering the URL again

### 4. Download Progress Stuck at 0%
**Problem**: Download starts but doesn't progress.

**Solutions**:
- Check your internet connection
- The video may be very large and taking time to start
- Try a different quality option
- Some videos may have slow servers

### 5. No Video Formats Available
**Problem**: After clicking "Get Info", no quality options appear.

**Solutions**:
- The video may not be downloadable
- Try a different video URL
- Some videos may require special permissions
- Check if the website is supported by yt-dlp

### 6. Application Won't Start
**Problem**: Flask app doesn't start or shows import errors.

**Solutions**:
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if Python 3.7+ is installed
- Try running: `python run.py`
- Check if port 5000 is available

### 7. Slow Downloads
**Problem**: Downloads are very slow.

**Solutions**:
- This is normal for large video files
- Try selecting a lower quality option
- Check your internet connection speed
- Some video servers may be slow

## Supported Websites

The app supports downloading from most major video platforms:
- YouTube
- Vimeo
- Twitter/X
- Instagram
- TikTok
- Facebook
- Twitch
- And many more!

## Getting Help

If you continue to have issues:
1. Check the terminal/console for error messages
2. Try downloading a different video to test
3. Make sure your internet connection is stable
4. Check if the video is publicly available in your region

## Technical Notes

- The app uses yt-dlp for video downloading
- Downloads are saved to the `downloads/` folder
- The app automatically handles format conversion to MP4
- Progress tracking works for most video formats
