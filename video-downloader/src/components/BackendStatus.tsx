import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, CheckCircle, Wifi, WifiOff } from 'lucide-react';
import { isBackendAvailable } from '../config/api';

const BackendStatus: React.FC = () => {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(false);

  const checkBackendStatus = async () => {
    setIsChecking(true);
    try {
      const available = await isBackendAvailable();
      setIsOnline(available);
    } catch (error) {
      setIsOnline(false);
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkBackendStatus();
    // Check every 30 seconds
    const interval = setInterval(checkBackendStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  if (isOnline === null) return null;

  return (
    <AnimatePresence>
      {!isOnline && (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          className="fixed top-4 right-4 z-50"
        >
          <div className="bg-red-600 text-white px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3 max-w-sm">
            <WifiOff className="w-5 h-5 flex-shrink-0" />
            <div className="flex-1">
              <h4 className="font-semibold text-sm">Backend Offline</h4>
              <p className="text-xs opacity-90">
                Please start the backend server on http://localhost:5000
              </p>
            </div>
            <button
              onClick={checkBackendStatus}
              disabled={isChecking}
              className="text-white hover:text-gray-200 transition-colors disabled:opacity-50"
            >
              {isChecking ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Wifi className="w-4 h-4" />
              )}
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default BackendStatus;
