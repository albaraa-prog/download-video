import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Download, Play, Settings, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

import { useDownload } from '../context/DownloadContext';
import { API_ENDPOINTS, isBackendAvailable } from '../config/api';
import VideoPreview from './VideoPreview';
import FormatSelector from './FormatSelector';
import ProgressBar from './ProgressBar';

interface VideoInfo {
  title: string;
  duration: number;
  uploader: string;
  view_count: number;
  description: string;
  thumbnail: string;
  formats: Array<{
    format_id: string;
    resolution: string;
    height: number;
    width: number;
    extension: string;
    file_size: string;
    has_audio: boolean;
    format_note: string;
  }>;
}

const VideoDownloader: React.FC = () => {
  const [url, setUrl] = useState('');
  const [customFilename, setCustomFilename] = useState('');
  const [selectedFormat, setSelectedFormat] = useState('best');
  const [videoInfo, setVideoInfo] = useState<VideoInfo | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  const { downloadStatus, startDownload } = useDownload();
  const urlInputRef = useRef<HTMLInputElement>(null);

  const isValidUrl = (string: string): boolean => {
    try {
      new URL(string);
      return true;
    } catch (_) {
      return false;
    }
  };

  const analyzeVideo = async () => {
    if (!url.trim()) {
      toast.error('Please enter a video URL');
      return;
    }

    if (!isValidUrl(url)) {
      toast.error('Please enter a valid URL');
      return;
    }

    // Check if backend is available
    const backendAvailable = await isBackendAvailable();
    if (!backendAvailable) {
      toast.error('Backend server is not running. Please start the backend server on http://localhost:5000');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await fetch(API_ENDPOINTS.GET_INFO, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (data.success) {
        setVideoInfo(data.info);
        toast.success('Video information loaded successfully!');
      } else {
        throw new Error(data.error || 'Failed to get video information');
      }
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDownload = async () => {
    if (!videoInfo) {
      toast.error('Please analyze video information first');
      return;
    }

    // Check if backend is available
    const backendAvailable = await isBackendAvailable();
    if (!backendAvailable) {
      toast.error('Backend server is not running. Please start the backend server on http://localhost:5000');
      return;
    }

    try {
      await startDownload(url, selectedFormat, customFilename);
      toast.success('Download started successfully!');
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Unknown error');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      analyzeVideo();
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center space-y-4"
      >
        <h1 className="text-4xl md:text-6xl font-bold gradient-text">
          Download Videos
        </h1>
        <p className="text-xl text-dark-300 max-w-2xl mx-auto">
          Download videos from YouTube, Vimeo, Twitter, Instagram, TikTok, and more
          with our modern, fast, and reliable downloader.
        </p>
      </motion.div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Download Form */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="card p-8 space-y-6"
        >
          <div className="space-y-4">
            <label className="block text-sm font-medium text-dark-200">
              Video URL
            </label>
            <div className="flex space-x-3">
              <input
                ref={urlInputRef}
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="https://www.youtube.com/watch?v=..."
                className="input flex-1"
                disabled={isAnalyzing}
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={analyzeVideo}
                disabled={isAnalyzing || !url.trim()}
                className="btn btn-primary px-6"
              >
                {isAnalyzing ? (
                  <div className="spinner w-4 h-4" />
                ) : (
                  <Search className="w-4 h-4" />
                )}
                <span className="ml-2">Analyze</span>
              </motion.button>
            </div>
            <p className="text-sm text-dark-400">
              Supports YouTube, Vimeo, Twitter, Instagram, TikTok, and 1000+ other sites
            </p>
          </div>

          {/* Video Preview */}
          <AnimatePresence>
            {videoInfo && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <VideoPreview videoInfo={videoInfo} />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Format Selection */}
          <AnimatePresence>
            {videoInfo && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3, delay: 0.1 }}
              >
                <FormatSelector
                  formats={videoInfo.formats || []}
                  selectedFormat={selectedFormat}
                  onFormatSelect={setSelectedFormat}
                />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Custom Filename */}
          <AnimatePresence>
            {videoInfo && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3, delay: 0.2 }}
                className="space-y-2"
              >
                <label className="block text-sm font-medium text-dark-200">
                  Custom Filename (optional)
                </label>
                <input
                  type="text"
                  value={customFilename}
                  onChange={(e) => setCustomFilename(e.target.value)}
                  placeholder="Leave empty for automatic naming"
                  className="input"
                />
                <p className="text-xs text-dark-400">
                  Use %(title)s for video title, %(uploader)s for channel name
                </p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Download Button */}
          <AnimatePresence>
            {videoInfo && (
              <motion.button
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleDownload}
                disabled={downloadStatus.in_progress}
                className="btn btn-primary btn-lg w-full"
              >
                {downloadStatus.in_progress ? (
                  <>
                    <div className="spinner w-5 h-5" />
                    <span>Downloading...</span>
                  </>
                ) : (
                  <>
                    <Download className="w-5 h-5" />
                    <span>Download Video</span>
                  </>
                )}
              </motion.button>
            )}
          </AnimatePresence>

          {/* Progress Bar */}
          <AnimatePresence>
            {downloadStatus.in_progress && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <ProgressBar status={downloadStatus} />
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Features & Info */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="space-y-6"
        >
          {/* Features */}
          <div className="card p-6">
            <h3 className="text-xl font-semibold text-dark-100 mb-4">
              Why Choose Our Downloader?
            </h3>
            <div className="space-y-4">
              {[
                {
                  icon: <Download className="w-5 h-5" />,
                  title: 'High Speed Downloads',
                  description: 'Fast and reliable downloads with progress tracking'
                },
                {
                  icon: <Settings className="w-5 h-5" />,
                  title: 'Multiple Quality Options',
                  description: 'Choose from various video qualities and formats'
                },
                {
                  icon: <AlertCircle className="w-5 h-5" />,
                  title: '1000+ Supported Sites',
                  description: 'Works with YouTube, Vimeo, Twitter, Instagram, and more'
                },
                {
                  icon: <Play className="w-5 h-5" />,
                  title: 'Modern Interface',
                  description: 'Beautiful, responsive design with dark theme'
                }
              ].map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: 0.6 + index * 0.1 }}
                  className="flex items-start space-x-3"
                >
                  <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-500/10 flex items-center justify-center text-primary-400">
                    {feature.icon}
                  </div>
                  <div>
                    <h4 className="font-medium text-dark-100">{feature.title}</h4>
                    <p className="text-sm text-dark-400">{feature.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 gap-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4, delay: 0.8 }}
              className="card p-4 text-center"
            >
              <div className="text-2xl font-bold text-primary-400">1000+</div>
              <div className="text-sm text-dark-400">Supported Sites</div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4, delay: 0.9 }}
              className="card p-4 text-center"
            >
              <div className="text-2xl font-bold text-secondary-400">99.9%</div>
              <div className="text-sm text-dark-400">Success Rate</div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default VideoDownloader;
