import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { motion } from 'framer-motion';

import Header from './components/Header';
import VideoDownloader from './components/VideoDownloader';
import DownloadsList from './components/DownloadsList';
import Footer from './components/Footer';
import BackendStatus from './components/BackendStatus';
import { DownloadProvider } from './context/DownloadContext';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <DownloadProvider>
        <Router>
          <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-700">
            <Header />
            
            <motion.main
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="container mx-auto px-4 py-8"
            >
              <Routes>
                <Route path="/" element={<VideoDownloader />} />
                <Route path="/downloads" element={<DownloadsList />} />
              </Routes>
            </motion.main>
            
            <Footer />
            
            <BackendStatus />
            
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#1e293b',
                  color: '#f8fafc',
                  border: '1px solid #475569',
                },
                success: {
                  iconTheme: {
                    primary: '#10b981',
                    secondary: '#f8fafc',
                  },
                },
                error: {
                  iconTheme: {
                    primary: '#ef4444',
                    secondary: '#f8fafc',
                  },
                },
              }}
            />
          </div>
        </Router>
      </DownloadProvider>
    </QueryClientProvider>
  );
}

export default App;
