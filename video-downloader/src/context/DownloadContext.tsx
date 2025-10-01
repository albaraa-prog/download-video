import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { API_ENDPOINTS } from '../config/api';

interface DownloadStatus {
  in_progress: boolean;
  progress: number;
  status: string;
  filename: string;
  error: string | null;
  currentUrl: string | null;
}

interface DownloadContextType {
  downloadStatus: DownloadStatus;
  startDownload: (url: string, format: string, filename?: string) => Promise<void>;
  resetDownload: () => void;
}

const DownloadContext = createContext<DownloadContextType | undefined>(undefined);

const initialState: DownloadStatus = {
  in_progress: false,
  progress: 0,
  status: '',
  filename: '',
  error: null,
  currentUrl: null,
};

type DownloadAction =
  | { type: 'START_DOWNLOAD'; url: string }
  | { type: 'UPDATE_PROGRESS'; progress: number; status: string }
  | { type: 'COMPLETE_DOWNLOAD'; filename: string }
  | { type: 'ERROR_DOWNLOAD'; error: string }
  | { type: 'RESET' };

function downloadReducer(state: DownloadStatus, action: DownloadAction): DownloadStatus {
  switch (action.type) {
    case 'START_DOWNLOAD':
      return {
        ...state,
        in_progress: true,
        progress: 0,
        status: 'Starting download...',
        filename: '',
        error: null,
        currentUrl: action.url,
      };
    case 'UPDATE_PROGRESS':
      return {
        ...state,
        progress: action.progress,
        status: action.status,
      };
    case 'COMPLETE_DOWNLOAD':
      return {
        ...state,
        in_progress: false,
        progress: 100,
        status: 'Download completed!',
        filename: action.filename,
        error: null,
      };
    case 'ERROR_DOWNLOAD':
      return {
        ...state,
        in_progress: false,
        error: action.error,
        status: 'Download failed',
      };
    case 'RESET':
      return initialState;
    default:
      return state;
  }
}

export function DownloadProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(downloadReducer, initialState);

  // Poll for download status from backend
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (state.in_progress) {
      interval = setInterval(async () => {
        try {
          const response = await fetch(API_ENDPOINTS.STATUS);
          const status = await response.json();
          
          if (status.in_progress) {
            dispatch({
              type: 'UPDATE_PROGRESS',
              progress: status.progress,
              status: status.status,
            });
          } else {
            if (status.error) {
              dispatch({
                type: 'ERROR_DOWNLOAD',
                error: status.error,
              });
            } else {
              dispatch({
                type: 'COMPLETE_DOWNLOAD',
                filename: status.filename,
              });
            }
          }
        } catch (error) {
          console.error('Error checking download status:', error);
          dispatch({
            type: 'ERROR_DOWNLOAD',
            error: 'Failed to check download status',
          });
        }
      }, 1000);
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [state.in_progress]);

  const startDownload = async (url: string, format: string, filename?: string) => {
    try {
      dispatch({ type: 'START_DOWNLOAD', url });
      
      const response = await fetch(API_ENDPOINTS.DOWNLOAD, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, format, filename }),
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || 'Failed to start download');
      }
    } catch (error) {
      dispatch({ 
        type: 'ERROR_DOWNLOAD', 
        error: error instanceof Error ? error.message : 'Unknown error' 
      });
      throw error;
    }
  };

  const resetDownload = () => {
    dispatch({ type: 'RESET' });
  };

  const value: DownloadContextType = {
    downloadStatus: state,
    startDownload,
    resetDownload,
  };

  return (
    <DownloadContext.Provider value={value}>
      {children}
    </DownloadContext.Provider>
  );
}

export function useDownload() {
  const context = useContext(DownloadContext);
  if (!context) {
    throw new Error('useDownload must be used within a DownloadProvider');
  }
  return context;
}
