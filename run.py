#!/usr/bin/env python3
"""
Simple runner script for the Video Downloader Flask app.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import flask
        import yt_dlp
        import tqdm
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install -r requirements.txt")
        return False

def main():
    """Main entry point."""
    print("🎬 Video Downloader Web App")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Ensure downloads directory exists
    os.makedirs('downloads', exist_ok=True)
    
    print("✅ Dependencies OK")
    print("🌐 Starting Flask server...")
    print("📁 Downloads will be saved to: downloads/")
    print("🔗 Open your browser to: http://localhost:5000")
    print("=" * 50)
    
    # Import and run the Flask app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
