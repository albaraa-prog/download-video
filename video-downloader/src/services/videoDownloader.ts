// Frontend-only video downloader service
import { DOWNLOADER_CONFIG, isSupportedSite, generateFilename } from '../config/api';

export interface VideoInfo {
  title: string;
  duration: number;
  uploader: string;
  view_count: number;
  description: string;
  thumbnail: string;
  formats: VideoFormat[];
}

export interface VideoFormat {
  format_id: string;
  resolution: string;
  height: number;
  width: number;
  extension: string;
  file_size: string;
  has_audio: boolean;
  format_note: string;
}

export interface DownloadProgress {
  percent: number;
  status: string;
  filename: string;
}

class FrontendVideoDownloader {
  private downloads: Map<string, DownloadProgress> = new Map();

  // Check if URL is valid and supported
  isValidUrl(url: string): boolean {
    try {
      const urlObj = new URL(url);
      return ['http:', 'https:'].includes(urlObj.protocol) && isSupportedSite(url);
    } catch {
      return false;
    }
  }

  // Get video information (simulated for frontend)
  async getVideoInfo(url: string): Promise<VideoInfo> {
    if (!this.isValidUrl(url)) {
      throw new Error('Invalid or unsupported video URL');
    }

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Extract basic info from URL
    const urlObj = new URL(url);
    const site = this.getSiteFromUrl(url);
    
    return {
      title: this.generateTitleFromUrl(url, site),
      duration: this.generateRandomDuration(),
      uploader: this.generateUploaderName(site),
      view_count: this.generateRandomViews(),
      description: this.generateDescription(site),
      thumbnail: this.generateThumbnailUrl(url, site),
      formats: this.generateFormats()
    };
  }

  // Start download (simulated for frontend)
  async startDownload(
    url: string, 
    format: string = 'best', 
    filename?: string
  ): Promise<void> {
    if (!this.isValidUrl(url)) {
      throw new Error('Invalid or unsupported video URL');
    }

    const downloadId = Date.now().toString();
    const finalFilename = filename || generateFilename('video', 'mp4');
    
    // Initialize download progress
    this.downloads.set(downloadId, {
      percent: 0,
      status: 'Starting download...',
      filename: finalFilename
    });

    // Simulate download progress
    this.simulateDownloadProgress(downloadId, url, finalFilename);
  }

  // Get download status
  getDownloadStatus(downloadId: string): DownloadProgress | null {
    return this.downloads.get(downloadId) || null;
  }

  // Get all downloads
  getAllDownloads(): DownloadProgress[] {
    return Array.from(this.downloads.values());
  }

  // Simulate download progress
  private simulateDownloadProgress(downloadId: string, url: string, filename: string) {
    const progress = this.downloads.get(downloadId);
    if (!progress) return;

    const interval = setInterval(() => {
      const currentProgress = this.downloads.get(downloadId);
      if (!currentProgress) {
        clearInterval(interval);
        return;
      }

      if (currentProgress.percent < 100) {
        const increment = Math.random() * 15 + 5; // 5-20% increment
        const newPercent = Math.min(100, currentProgress.percent + increment);
        
        this.downloads.set(downloadId, {
          ...currentProgress,
          percent: newPercent,
          status: newPercent < 100 ? `Downloading... ${Math.round(newPercent)}%` : 'Download completed!'
        });

        // Trigger custom event for progress updates
        window.dispatchEvent(new CustomEvent('downloadProgress', {
          detail: { downloadId, progress: this.downloads.get(downloadId) }
        }));
      } else {
        clearInterval(interval);
        // Simulate file download
        this.triggerFileDownload(url, filename);
      }
    }, 500);
  }

  // Trigger actual file download
  private triggerFileDownload(url: string, filename: string) {
    // Create a temporary link to trigger download
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // Helper methods for generating mock data
  private getSiteFromUrl(url: string): string {
    const urlObj = new URL(url);
    return urlObj.hostname;
  }

  private generateTitleFromUrl(url: string, site: string): string {
    const titles = {
      'youtube.com': 'Amazing Video Title',
      'youtu.be': 'Cool YouTube Video',
      'vimeo.com': 'Creative Vimeo Content',
      'twitter.com': 'Viral Twitter Video',
      'x.com': 'Trending X Video',
      'instagram.com': 'Instagram Reel',
      'tiktok.com': 'TikTok Dance Video',
      'facebook.com': 'Facebook Video Post',
      'twitch.tv': 'Twitch Stream Highlight',
      'dailymotion.com': 'Dailymotion Video'
    };
    return titles[site as keyof typeof titles] || 'Video Download';
  }

  private generateUploaderName(site: string): string {
    const uploaders = {
      'youtube.com': 'Popular YouTuber',
      'youtu.be': 'YouTube Creator',
      'vimeo.com': 'Vimeo Artist',
      'twitter.com': '@username',
      'x.com': '@user',
      'instagram.com': '@instagram_user',
      'tiktok.com': '@tiktok_creator',
      'facebook.com': 'Facebook User',
      'twitch.tv': 'Twitch Streamer',
      'dailymotion.com': 'Dailymotion User'
    };
    return uploaders[site as keyof typeof uploaders] || 'Unknown User';
  }

  private generateRandomDuration(): number {
    return Math.floor(Math.random() * 3600) + 60; // 1 minute to 1 hour
  }

  private generateRandomViews(): number {
    return Math.floor(Math.random() * 1000000) + 1000;
  }

  private generateDescription(site: string): string {
    return `This is a ${site} video with interesting content. Download it to watch offline!`;
  }

  private generateThumbnailUrl(url: string, site: string): string {
    // Generate a placeholder thumbnail URL
    const videoId = this.extractVideoId(url, site);
    if (site.includes('youtube') && videoId) {
      return `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
    }
    return `https://via.placeholder.com/640x360/1e293b/ffffff?text=${encodeURIComponent(site)}`;
  }

  private extractVideoId(url: string, site: string): string | null {
    if (site.includes('youtube')) {
      const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/);
      return match ? match[1] : null;
    }
    return null;
  }

  private generateFormats(): VideoFormat[] {
    const formats = [
      { height: 2160, width: 3840, extension: 'mp4', note: '4K Ultra HD' },
      { height: 1440, width: 2560, extension: 'mp4', note: '2K HD+' },
      { height: 1080, width: 1920, extension: 'mp4', note: 'Full HD' },
      { height: 720, width: 1280, extension: 'mp4', note: 'HD' },
      { height: 480, width: 854, extension: 'mp4', note: 'SD' },
      { height: 360, width: 640, extension: 'mp4', note: 'Low Quality' }
    ];

    return formats.map((format, index) => ({
      format_id: `format_${index + 1}`,
      resolution: `${format.width}x${format.height}`,
      height: format.height,
      width: format.width,
      extension: format.extension,
      file_size: this.formatFileSize(Math.random() * 500000000 + 10000000), // 10MB to 500MB
      has_audio: true,
      format_note: format.note
    }));
  }

  private formatFileSize(bytes: number): string {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
  }
}

// Export singleton instance
export const videoDownloader = new FrontendVideoDownloader();
