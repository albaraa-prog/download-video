# Video Downloader Pro - Full Stack

A modern, beautiful React application with Express backend for real video downloading. Features a stunning dark theme, intuitive user interface, and actual video download capabilities using yt-dlp!

## 🚀 Features

- **Modern React Architecture**: Built with React 18, TypeScript, and modern hooks
- **Beautiful UI**: Stunning dark theme with smooth animations using Framer Motion
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Real-time Progress**: Live download progress tracking with visual feedback
- **State Management**: Efficient state management with React Query and Context API
- **Type Safety**: Full TypeScript support for better development experience
- **Performance**: Optimized with React.memo, useMemo, and useCallback
- **Accessibility**: WCAG compliant with proper focus management

## 🎨 UI/UX Features

- **Dark Theme**: Beautiful dark theme with gradient accents
- **Smooth Animations**: Framer Motion for fluid transitions and micro-interactions
- **Modern Icons**: Lucide React icons for consistent visual language
- **Responsive Grid**: CSS Grid and Flexbox for perfect layouts
- **Loading States**: Elegant loading spinners and skeleton screens
- **Toast Notifications**: React Hot Toast for user feedback
- **Progress Indicators**: Visual progress bars with shimmer effects

## 📋 Prerequisites

- Node.js 16.0.0 or higher
- npm or yarn package manager
- Modern web browser with ES6+ support
- **yt-dlp** (for video downloading) - See [INSTALL_YTDLP.md](INSTALL_YTDLP.md) for installation instructions

## 🛠️ Installation

### **Option 1: Quick Setup (Windows)**
```bash
cd video-downloader
setup.bat
npm start
```

### **Option 2: Manual Setup**
```bash
cd video-downloader

# Install all dependencies (frontend + backend)
npm run install-all

# Start both servers automatically
npm start
```

### **Option 3: Individual Setup**
```bash
# Install frontend dependencies
npm install

# Install backend dependencies
cd backend && npm install && cd ..

# Start both servers
npm start
```

## 🚀 **Running the App**

After installation, simply run:
```bash
npm start
```

This will automatically:
- Start the backend server on `http://localhost:5000`
- Start the React app on `http://localhost:3000`
- Open your browser to the app

## ⚠️ Troubleshooting

If you get JSON parsing errors:
1. Delete `package-lock.json` if it exists
2. Delete `node_modules` folder if it exists  
3. Run `npm install` again

If PowerShell issues occur, use Command Prompt instead of PowerShell.

## 🧹 Cleanup

To remove unused files and reinstall dependencies:
```bash
# Remove backend directory (if exists)
rmdir /s /q backend

# Remove node_modules and reinstall
rmdir /s /q node_modules
del package-lock.json
npm install
```

## 🎯 How It Works

This is a **full-stack** application that:

- **Real video analysis** - Uses yt-dlp to extract actual video information
- **Actual downloads** - Downloads real video files to your computer
- **Backend server** - Express server with yt-dlp integration
- **Supports 1000+ sites** - YouTube, Vimeo, Twitter, Instagram, TikTok, and more
- **Real-time progress** - Shows actual download progress with smooth animations
- **File management** - View and download your downloaded files

## 🏗️ Project Structure

```
video-downloader/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── VideoDownloader.tsx
│   │   ├── VideoPreview.tsx
│   │   ├── FormatSelector.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── DownloadsList.tsx
│   │   └── Footer.tsx
│   ├── context/
│   │   └── DownloadContext.tsx
│   ├── config/
│   │   └── api.ts
│   ├── App.tsx
│   ├── index.tsx
│   └── index.css
├── backend/
│   ├── server.js
│   ├── package.json
│   └── downloads/ (created automatically)
├── package.json
├── tailwind.config.js
└── README.md
```

## 🎯 Key Components

### VideoDownloader
Main component handling video analysis and download initiation.

### VideoPreview
Displays video information including thumbnail, title, duration, and metadata.

### FormatSelector
Interactive quality selection with visual format options.

### ProgressBar
Real-time download progress with status indicators.

### DownloadsList
File management interface with download and delete actions.

## 🔧 Configuration

### Tailwind CSS
The project uses Tailwind CSS for styling. Configuration is in `tailwind.config.js`.

### React Query
Configured for efficient data fetching and caching.

### Framer Motion
Used for smooth animations and transitions.

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🎨 Theme Colors

- **Primary**: Blue gradient (#0ea5e9 to #a855f7)
- **Secondary**: Purple gradient
- **Accent**: Cyan (#06b6d4)
- **Dark**: Slate color palette
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Error**: Red (#ef4444)

## 🚀 Performance Optimizations

- **Code Splitting**: React.lazy for component-based splitting
- **Memoization**: React.memo for preventing unnecessary re-renders
- **Virtual Scrolling**: For large lists (if needed)
- **Image Optimization**: Lazy loading and proper sizing
- **Bundle Analysis**: Webpack Bundle Analyzer integration

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## 📦 Building for Production

```bash
# Create production build
npm run build

# Serve production build locally
npm install -g serve
serve -s build
```

## 🔌 API Integration

The React app expects a backend API with the following endpoints:

- `GET /api/health` - Health check
- `POST /api/get-info` - Get video information
- `POST /api/download` - Start video download
- `GET /api/status` - Get download status
- `GET /api/downloads` - List downloaded files
- `GET /api/download/:filename` - Download a file

## 🎯 Supported Sites

- YouTube
- Vimeo
- Twitter/X
- Instagram
- TikTok
- And 1000+ other sites (via yt-dlp)

## 🔒 Security Features

- **Input Validation**: Client-side validation for all inputs
- **XSS Protection**: React's built-in XSS protection
- **CSRF Protection**: Axios with proper headers
- **Content Security Policy**: Configured in HTML meta tags
- **Rate Limiting**: Backend rate limiting for API protection

## 🚀 Deployment

### Frontend (Vercel/Netlify)
```bash
npm run build
# Upload build folder to Vercel/Netlify
```

### Backend (Heroku/Railway)
```bash
cd backend
# Deploy to your preferred platform
```

### Docker
```dockerfile
# Frontend
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]

# Backend
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 5000
CMD ["npm", "start"]
```

## 📊 Bundle Analysis

```bash
# Analyze bundle size
npm run build
npx webpack-bundle-analyzer build/static/js/*.js
```

## 🛠️ Development Tools

- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting
- **React DevTools**: Browser extension for debugging
- **TypeScript**: Type checking and IntelliSense

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

**Module not found**: Run `npm install` to install dependencies
**Port already in use**: Change the port in package.json scripts
**Build fails**: Check Node.js version and dependencies
**Styling issues**: Ensure Tailwind CSS is properly configured
**Backend not working**: Make sure yt-dlp is installed on your system

## 📞 Support

If you encounter any issues, please check the troubleshooting section or create an issue on GitHub.

## 🆚 Comparison with Other Versions

| Feature | Flask | Node.js | FastAPI | React |
|---------|-------|---------|---------|-------|
| Frontend | Basic HTML | Basic HTML | Basic HTML | **Modern React** |
| UI/UX | Good | Good | Good | **Excellent** |
| Animations | CSS only | CSS only | CSS only | **Framer Motion** |
| State Management | Manual | Manual | Manual | **React Query + Context** |
| Performance | Good | Good | Excellent | **Excellent** |
| Developer Experience | Good | Good | Good | **Excellent** |
| Mobile Support | Basic | Basic | Basic | **Full Responsive** |
| Type Safety | No | No | Yes | **Full TypeScript** |
