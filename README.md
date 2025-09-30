# Video Downloader - Clean Architecture Implementation

This is an enhanced version of the video downloader application that follows clean architecture principles and includes a modern GUI.

## 🏗️ Architecture Overview

The application is structured using clean architecture principles with clear separation of concerns:

```
download-video/
├── domain/                 # Business logic and entities
│   ├── entities.py        # Domain models (VideoInfo, VideoFormat, etc.)
│   ├── repositories.py    # Repository interfaces
│   └── exceptions.py      # Domain exceptions
├── application/           # Use cases and application services
│   ├── use_cases.py      # Business use cases
│   └── services.py       # Application services
├── infrastructure/        # External dependencies
│   ├── video_repository_impl.py    # yt-dlp implementation
│   └── config_repository_impl.py   # JSON config implementation
├── presentation/          # UI layer
│   ├── ui_components.py   # Reusable UI components
│   └── main_window.py     # Main application window
├── di_container.py        # Dependency injection container
├── app.py                # Main application entry point
└── video_downloader.py   # Original CLI version (preserved)
```

## 🎯 Key Features

### Clean Architecture Benefits
- **Separation of Concerns**: Each layer has a specific responsibility
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Testability**: Easy to unit test each component in isolation
- **Maintainability**: Changes in one layer don't affect others
- **Extensibility**: Easy to add new features or change implementations

### Modern GUI Features
- **Clean Interface**: Modern, intuitive design with Windows 11 styling
- **Real-time Progress**: Live download progress with speed indicators
- **Format Selection**: Easy-to-use format selection with recommendations
- **Settings Management**: Configurable download paths and preferences
- **Error Handling**: User-friendly error messages and validation
- **Responsive Design**: Adapts to different window sizes

### Technical Improvements
- **Dependency Injection**: Loose coupling between components
- **Repository Pattern**: Abstracted data access layer
- **Use Case Pattern**: Clear business logic encapsulation
- **Exception Handling**: Comprehensive error management
- **Configuration Management**: Persistent settings storage
- **Threading**: Non-blocking UI with background operations

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip package manager

### Installation
1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### GUI Version (Recommended)
```bash
python app.py
```

#### CLI Version (Original)
```bash
python video_downloader.py
```

## 🎨 GUI Usage

1. **Enter Video URL**: Paste any supported video URL (YouTube, etc.)
2. **Get Video Info**: Click "Get Video Info" to fetch video details
3. **Select Format**: Choose from available formats or use recommendations
4. **Customize**: Optionally set a custom filename
5. **Download**: Click "Download Video" to start the download
6. **Monitor Progress**: Watch real-time download progress
7. **Settings**: Configure download path and other preferences

## 🔧 Configuration

The application stores settings in `config.json`:
- `download_path`: Default download directory
- `preferred_format`: Preferred video format
- `ui_theme`: UI theme preference
- `auto_download`: Auto-download setting
- `show_progress`: Progress display setting

## 🧪 Testing

The clean architecture makes testing straightforward:

```python
# Example unit test for a use case
def test_get_video_info_use_case():
    # Mock the repository
    mock_repo = MockVideoRepository()
    use_case = GetVideoInfoUseCase(mock_repo)
    
    # Test the use case
    video_info = use_case.execute("https://youtube.com/watch?v=example")
    assert video_info.title == "Test Video"
```

## 🔄 Extending the Application

### Adding New Video Sources
1. Implement the `VideoRepository` interface
2. Register in the DI container
3. No changes needed in other layers

### Adding New UI Components
1. Create component in `presentation/ui_components.py`
2. Use in `presentation/main_window.py`
3. Follow the existing patterns

### Adding New Use Cases
1. Create use case in `application/use_cases.py`
2. Register in DI container
3. Use in presentation layer

## 📁 File Structure Details

### Domain Layer
- **entities.py**: Core business objects
- **repositories.py**: Data access interfaces
- **exceptions.py**: Domain-specific exceptions

### Application Layer
- **use_cases.py**: Business operations
- **services.py**: Application-specific services

### Infrastructure Layer
- **video_repository_impl.py**: yt-dlp integration
- **config_repository_impl.py**: Configuration persistence

### Presentation Layer
- **ui_components.py**: Reusable UI widgets
- **main_window.py**: Main application window

## 🎯 Design Patterns Used

1. **Clean Architecture**: Layered architecture with dependency inversion
2. **Repository Pattern**: Abstracted data access
3. **Use Case Pattern**: Encapsulated business logic
4. **Dependency Injection**: Loose coupling
5. **Observer Pattern**: UI event handling
6. **Factory Pattern**: Object creation
7. **Strategy Pattern**: Different format selection strategies

## 🔮 Future Enhancements

- **Playlist Support**: Download entire playlists
- **Batch Downloads**: Multiple video downloads
- **Format Conversion**: Convert between video formats
- **Metadata Editing**: Edit video metadata
- **Cloud Storage**: Direct upload to cloud services
- **API Integration**: REST API for external access
- **Plugin System**: Extensible plugin architecture

## 🤝 Contributing

When contributing to this project:
1. Follow clean architecture principles
2. Write unit tests for new features
3. Update documentation
4. Use type hints
5. Follow existing code style

## 📄 License

This project is licensed under the same terms as the original video downloader.
