// Frontend-only video downloader configuration
export const DOWNLOADER_CONFIG = {
  // Supported video sites
  SUPPORTED_SITES: [
    'youtube.com',
    'youtu.be',
    'vimeo.com',
    'twitter.com',
    'x.com',
    'instagram.com',
    'tiktok.com',
    'facebook.com',
    'twitch.tv',
    'dailymotion.com'
  ],
  
  // Default download quality
  DEFAULT_QUALITY: 'best',
  
  // Download directory name
  DOWNLOAD_FOLDER: 'video-downloads'
};

// Check if URL is from a supported site
export const isSupportedSite = (url: string): boolean => {
  try {
    const urlObj = new URL(url);
    return DOWNLOADER_CONFIG.SUPPORTED_SITES.some(site => 
      urlObj.hostname.includes(site)
    );
  } catch {
    return false;
  }
};

// Generate filename from video info
export const generateFilename = (title: string, extension: string = 'mp4'): string => {
  const cleanTitle = title
    .replace(/[^\w\s-]/g, '') // Remove special characters
    .replace(/\s+/g, '-') // Replace spaces with hyphens
    .substring(0, 50); // Limit length
  return `${cleanTitle}.${extension}`;
};
