# Video Downloader Web App

A simple Flask-based web application for downloading videos from any website using yt-dlp.

## Features

- 🌐 Download videos from any website (YouTube, Vimeo, etc.)
- 🎯 Multiple quality options
- 📱 Responsive web interface
- 📊 Real-time download progress
- 📁 Organized file management
- ⚡ Fast and reliable downloads

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and go to: http://localhost:5000

3. Enter a video URL and click "Get Info" to see available formats

4. Select your preferred quality and click "Download Video"

## Supported Websites

This app supports downloading from most major video platforms that yt-dlp supports, including:
- **YouTube** - All public videos
- **Vimeo** - Public videos
- **Twitter/X** - Video tweets
- **Instagram** - Public posts and stories
- **TikTok** - Public videos
- **Facebook** - Public videos
- **Twitch** - Clips and highlights
- **And many more!**

### ⚠️ Not Supported
- **Streaming sites** (movies4us.co, 123movies, putlocker, etc.) - These have anti-bot protection
- **DRM-protected content** - Cannot bypass copyright protection
- **Private/restricted videos** - Require authentication
- **Age-restricted content** - May require verification

## File Structure

```
download-video/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Web interface
├── static/
│   └── style.css         # Styling
├── downloads/            # Downloaded videos (created automatically)
└── requirements.txt      # Python dependencies
```

## Requirements

- Python 3.7+
- Flask 2.3.0+
- yt-dlp 2023.03.04+
- tqdm 4.64.0+
- Werkzeug 2.3.0+

## License

This project is open source and available under the MIT License.