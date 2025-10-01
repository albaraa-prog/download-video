import React from 'react';
import { motion } from 'framer-motion';
import { Check, Volume2, VolumeX, Monitor } from 'lucide-react';

interface Format {
  format_id: string;
  resolution: string;
  height: number;
  width: number;
  extension: string;
  file_size: string;
  has_audio: boolean;
  format_note: string;
}

interface FormatSelectorProps {
  formats: Format[];
  selectedFormat: string;
  onFormatSelect: (formatId: string) => void;
}

const FormatSelector: React.FC<FormatSelectorProps> = ({ 
  formats, 
  selectedFormat, 
  onFormatSelect 
}) => {
  const getQualityBadge = (height: number) => {
    if (height >= 2160) return { label: '4K', color: 'status-info' };
    if (height >= 1440) return { label: 'HD+', color: 'status-success' };
    if (height >= 1080) return { label: 'HD', color: 'status-success' };
    if (height >= 720) return { label: 'HD', color: 'status-warning' };
    if (height >= 480) return { label: 'SD', color: 'status-warning' };
    return { label: 'Low', color: 'status-error' };
  };

  const formatOptions = [
    {
      id: 'best',
      name: 'Best Quality',
      details: 'Recommended',
      height: 1080,
      hasAudio: true,
      isRecommended: true,
    },
    ...formats.slice(0, 8).map(format => ({
      id: format.format_id,
      name: format.resolution || 'Unknown',
      details: `${format.extension.toUpperCase()} • ${format.file_size}`,
      height: format.height || 0,
      hasAudio: format.has_audio,
      isRecommended: false,
    }))
  ];

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      transition={{ duration: 0.3 }}
      className="space-y-4"
    >
      <h3 className="text-lg font-semibold text-dark-100">Select Quality</h3>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {formatOptions.map((format, index) => {
          const isSelected = selectedFormat === format.id;
          const qualityBadge = getQualityBadge(format.height);
          
          return (
            <motion.button
              key={format.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.2, delay: index * 0.05 }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onFormatSelect(format.id)}
              className={`relative p-4 rounded-lg border-2 transition-all duration-200 text-left ${
                isSelected
                  ? 'border-primary-500 bg-primary-500/10'
                  : 'border-dark-600 bg-dark-700/50 hover:border-dark-500 hover:bg-dark-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <Monitor className="w-4 h-4 text-dark-400" />
                  <span className="font-medium text-dark-100">{format.name}</span>
                  {format.isRecommended && (
                    <span className="px-2 py-0.5 text-xs bg-primary-500/20 text-primary-400 rounded-full">
                      Recommended
                    </span>
                  )}
                </div>
                
                {isSelected && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="w-5 h-5 rounded-full bg-primary-500 flex items-center justify-center"
                  >
                    <Check className="w-3 h-3 text-white" />
                  </motion.div>
                )}
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className={`status-indicator ${qualityBadge.color}`}>
                    {qualityBadge.label}
                  </span>
                  
                  {format.hasAudio ? (
                    <Volume2 className="w-4 h-4 text-green-400" />
                  ) : (
                    <VolumeX className="w-4 h-4 text-red-400" />
                  )}
                </div>
                
                <span className="text-xs text-dark-400">{format.details}</span>
              </div>
            </motion.button>
          );
        })}
      </div>
      
      {formats.length === 0 && (
        <div className="text-center py-8 text-dark-400">
          <Monitor className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p>No specific formats available. Best quality will be selected automatically.</p>
        </div>
      )}
    </motion.div>
  );
};

export default FormatSelector;
