import React from 'react';
import { motion } from 'framer-motion';
import { Play, Clock, Eye, User } from 'lucide-react';

interface VideoInfo {
  title: string;
  duration: number;
  uploader: string;
  view_count: number;
  description: string;
  thumbnail: string;
}

interface VideoPreviewProps {
  videoInfo: VideoInfo;
}

const VideoPreview: React.FC<VideoPreviewProps> = ({ videoInfo }) => {
  const formatDuration = (seconds: number): string => {
    if (!seconds) return 'Unknown';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
      return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
  };

  const formatNumber = (num: number): string => {
    if (!num) return 'Unknown';
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-4"
    >
      <h3 className="text-lg font-semibold text-dark-100">Video Information</h3>
      
      <div className="flex space-x-4">
        {/* Thumbnail */}
        <div className="relative flex-shrink-0">
          <img
            src={videoInfo.thumbnail || '/placeholder-video.jpg'}
            alt="Video thumbnail"
            className="w-32 h-24 object-cover rounded-lg border border-dark-600"
            onError={(e) => {
              e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9Ijk2IiB2aWV3Qm94PSIwIDAgMTI4IDk2IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIxMjgiIGhlaWdodD0iOTYiIGZpbGw9IiMzMzQxNTUiLz48cGF0aCBkPSJNNDggMzJMMTAgNjRMMTAgMzJINDBaIiBmaWxsPSIjNjM2NmYxIi8+PC9zdmc+';
            }}
          />
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-8 h-8 rounded-full bg-black/50 flex items-center justify-center">
              <Play className="w-4 h-4 text-white ml-0.5" />
            </div>
          </div>
        </div>

        {/* Video Details */}
        <div className="flex-1 min-w-0">
          <h4 className="text-lg font-semibold text-dark-100 line-clamp-2 mb-2">
            {videoInfo.title}
          </h4>
          
          <div className="space-y-2">
            <div className="flex items-center space-x-4 text-sm text-dark-400">
              <div className="flex items-center space-x-1">
                <User className="w-4 h-4" />
                <span>{videoInfo.uploader || 'Unknown'}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{formatDuration(videoInfo.duration)}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Eye className="w-4 h-4" />
                <span>{formatNumber(videoInfo.view_count)} views</span>
              </div>
            </div>
            
            {videoInfo.description && (
              <p className="text-sm text-dark-300 line-clamp-2">
                {videoInfo.description}
              </p>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default VideoPreview;
