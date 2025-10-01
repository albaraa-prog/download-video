import React from 'react';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';
import { Download, FileVideo, Calendar, HardDrive, RefreshCw, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { API_ENDPOINTS } from '../config/api';

interface DownloadFile {
  name: string;
  size: number;
  modified: number;
  type: string;
}

const DownloadsList: React.FC = () => {
  const { data: downloads, isLoading, refetch } = useQuery(
    'downloads',
    async () => {
      const response = await fetch(API_ENDPOINTS.DOWNLOADS);
      const data = await response.json();
      return data.files || [];
    },
    {
      refetchInterval: 30000, // Refetch every 30 seconds
    }
  );

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (timestamp: number): string => {
    const date = new Date(timestamp * 1000);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return Math.floor(diff / 60000) + 'm ago';
    if (diff < 86400000) return Math.floor(diff / 3600000) + 'h ago';
    if (diff < 604800000) return Math.floor(diff / 86400000) + 'd ago';
    
    return date.toLocaleDateString();
  };

  const handleRefresh = () => {
    refetch();
    toast.success('Downloads refreshed');
  };

  const handleClearAll = () => {
    if (window.confirm('Are you sure you want to clear all downloaded files? This action cannot be undone.')) {
      toast.success('Clear all feature coming soon!');
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card p-8">
          <div className="flex items-center justify-center space-x-3">
            <div className="spinner w-6 h-6" />
            <span className="text-dark-300">Loading downloads...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold gradient-text">Downloads</h1>
          <p className="text-dark-300 mt-1">
            Manage your downloaded videos
          </p>
        </div>
        
        <div className="flex space-x-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleRefresh}
            className="btn btn-secondary"
          >
            <RefreshCw className="w-4 h-4" />
            <span className="ml-2">Refresh</span>
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleClearAll}
            className="btn btn-secondary"
          >
            <Trash2 className="w-4 h-4" />
            <span className="ml-2">Clear All</span>
          </motion.button>
        </div>
      </motion.div>

      {/* Downloads List */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="card p-6"
      >
        {downloads && downloads.length > 0 ? (
          <div className="space-y-4">
            {downloads.map((file: DownloadFile, index: number) => (
              <motion.div
                key={file.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="flex items-center justify-between p-4 bg-dark-700/50 rounded-lg border border-dark-600 hover:bg-dark-700 hover:border-dark-500 transition-all duration-200 group"
              >
                <div className="flex items-center space-x-4 flex-1 min-w-0">
                  <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-primary-500/10 flex items-center justify-center">
                    <FileVideo className="w-6 h-6 text-primary-400" />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-dark-100 truncate">
                      {file.name}
                    </h3>
                    <div className="flex items-center space-x-4 mt-1 text-sm text-dark-400">
                      <div className="flex items-center space-x-1">
                        <HardDrive className="w-4 h-4" />
                        <span>{formatFileSize(file.size)}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Calendar className="w-4 h-4" />
                        <span>{formatDate(file.modified)}</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <motion.a
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  href={API_ENDPOINTS.DOWNLOAD_FILE(file.name)}
                  download
                  className="btn btn-primary btn-sm opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                >
                  <Download className="w-4 h-4" />
                  <span className="ml-2">Download</span>
                </motion.a>
              </motion.div>
            ))}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
            className="text-center py-12"
          >
            <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-dark-700 flex items-center justify-center">
              <FileVideo className="w-12 h-12 text-dark-400" />
            </div>
            <h3 className="text-xl font-semibold text-dark-200 mb-2">
              No downloads yet
            </h3>
            <p className="text-dark-400 mb-6">
              Start by downloading your first video!
            </p>
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="/"
              className="btn btn-primary"
            >
              Go to Downloader
            </motion.a>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

export default DownloadsList;
