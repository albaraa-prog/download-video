// API Configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Check if backend is available
export const isBackendAvailable = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`, {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.ok;
  } catch (error) {
    console.warn('Backend not available:', error);
    return false;
  }
};

export const API_ENDPOINTS = {
  HEALTH: `${API_BASE_URL}/api/health`,
  GET_INFO: `${API_BASE_URL}/api/get-info`,
  DOWNLOAD: `${API_BASE_URL}/api/download`,
  STATUS: `${API_BASE_URL}/api/status`,
  DOWNLOADS: `${API_BASE_URL}/api/downloads`,
  DOWNLOAD_FILE: (filename: string) => `${API_BASE_URL}/api/download/${filename}`,
};
