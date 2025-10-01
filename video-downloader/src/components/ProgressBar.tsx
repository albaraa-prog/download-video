import React from 'react';
import { motion } from 'framer-motion';
import { Download, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

interface DownloadStatus {
  in_progress: boolean;
  progress: number;
  status: string;
  filename: string;
  error: string | null;
  currentUrl: string | null;
}

interface ProgressBarProps {
  status: DownloadStatus;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ status }) => {
  const getStatusIcon = () => {
    if (status.error) return <XCircle className="w-5 h-5 text-red-400" />;
    if (status.progress === 100) return <CheckCircle className="w-5 h-5 text-green-400" />;
    return <Download className="w-5 h-5 text-primary-400" />;
  };

  const getStatusColor = () => {
    if (status.error) return 'text-red-400';
    if (status.progress === 100) return 'text-green-400';
    return 'text-primary-400';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-4"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <span className={`font-medium ${getStatusColor()}`}>
            {status.status}
          </span>
        </div>
        
        <span className="text-sm text-dark-400">
          {Math.round(status.progress)}%
        </span>
      </div>

      <div className="progress-bar">
        <motion.div
          className="progress-fill"
          initial={{ width: 0 }}
          animate={{ width: `${status.progress}%` }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
        />
      </div>

      {status.error && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="flex items-center space-x-2 p-3 bg-red-500/10 border border-red-500/20 rounded-lg"
        >
          <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
          <span className="text-sm text-red-400">{status.error}</span>
        </motion.div>
      )}

      {status.filename && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="flex items-center space-x-2 p-3 bg-green-500/10 border border-green-500/20 rounded-lg"
        >
          <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0" />
          <span className="text-sm text-green-400">
            Downloaded as: {status.filename}
          </span>
        </motion.div>
      )}
    </motion.div>
  );
};

export default ProgressBar;
