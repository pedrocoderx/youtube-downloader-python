# 🎥 YouTube Video Downloader

A modern, web-based YouTube video downloader built with Flask that allows you to download YouTube videos with quality selection, progress tracking, and a beautiful user interface.

![YouTube Downloader](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🌐 **Web-based Interface**: Beautiful, responsive web UI accessible from any browser
- 📹 **Quality Selection**: Choose from available video qualities (720p, 1080p, 4K, etc.)
- 📊 **Real-time Progress**: Live progress tracking with percentage and status updates
- 🎵 **Audio Downloads**: Download audio-only versions
- 🔍 **Video Information**: View video details before downloading (title, duration, views, uploader)
- ⚡ **Background Processing**: Non-blocking downloads with threading
- ✅ **Smart Error Handling**: Comprehensive error handling with user-friendly messages
- 🔗 **URL Validation**: Validates YouTube URLs before processing
- 🎨 **Modern UI**: Clean, professional design with gradient backgrounds and smooth animations
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

## 🚀 Live Demo

Deployed on Railway: [Coming Soon]

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, Flask 2.3+
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Video Processing**: yt-dlp, FFmpeg
- **Deployment**: Railway (with Nixpacks for FFmpeg)

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- FFmpeg (for video merging capabilities)
- Internet connection

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/pedrocoderx/youtube-downloader-python.git
   cd youtube-downloader-python
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (optional but recommended)
   - **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

4. **Run the application**
   ```bash
   python app_simple.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5001`

## 🌐 Usage

### Web Interface

1. **Open the application** in your web browser
2. **Enter YouTube URL** - Paste any YouTube video URL
   - Regular URLs: `https://www.youtube.com/watch?v=VIDEO_ID`
   - Shortened URLs: `https://youtu.be/VIDEO_ID`
   - Embedded URLs: `https://www.youtube.com/embed/VIDEO_ID`

3. **Fetch Video Information** - Click "Get Video Info" to load video details
   - Displays video title, duration, view count, and uploader
   - Shows available quality options with file sizes

4. **Select Quality** - Choose your preferred video quality
   - Video qualities: 720p, 1080p, 4K, etc.
   - Audio-only option for MP3 downloads
   - File size estimates for each quality

5. **Download** - Click "Download Video" to start
   - Real-time progress tracking
   - Background processing (you can use other tabs)
   - Success/error notifications

### Supported URL Formats

- ✅ `https://www.youtube.com/watch?v=VIDEO_ID`
- ✅ `https://youtu.be/VIDEO_ID`
- ✅ `https://www.youtube.com/embed/VIDEO_ID`
- ✅ `https://m.youtube.com/watch?v=VIDEO_ID`

## 🚀 Deployment

### Railway Deployment (Recommended)

This project is optimized for Railway deployment with automatic FFmpeg installation.

1. **Fork/Clone this repository**
2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Create new project → "Deploy from GitHub repo"
   - Select your repository
3. **Deploy** - Railway will automatically:
   - Install Python dependencies
   - Install FFmpeg via Nixpacks
   - Deploy your web app

### Alternative: Render Deployment

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app_simple:app --bind 0.0.0.0:$PORT`
6. Deploy!

## 📁 Project Structure

```
youtube-downloader-python/
├── app_simple.py              # Main Flask application
├── requirements.txt            # Python dependencies
├── Procfile                   # Railway deployment config
├── runtime.txt                # Python version specification
├── railway.json               # Railway configuration
├── templates/
│   └── index_simple.html      # Web interface template
├── test_download.py           # Testing utilities
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

- `PORT`: Server port (default: 5001)
- `FLASK_ENV`: Environment mode (development/production)

### Download Settings

- **Default download location**: `/tmp` (cloud) or `~/Downloads` (local)
- **Supported formats**: MP4 (video), MP3 (audio)
- **Quality options**: Based on video availability

## 🐛 Troubleshooting

### Common Issues

1. **"Error fetching video information"**
   - Check internet connection
   - Verify YouTube URL is valid and accessible
   - Some videos may be restricted or private

2. **"FFmpeg not found"**
   - App will fall back to single-file downloads
   - Install FFmpeg for better quality merging
   - Railway automatically installs FFmpeg

3. **"Download failed"**
   - Check available disk space
   - Verify download directory permissions
   - Some videos have download restrictions

4. **"Import errors"**
   - Install dependencies: `pip install -r requirements.txt`
   - Ensure Python 3.11+ is installed

### Performance Tips

- Use high-quality videos for better viewing experience
- Check available qualities before downloading
- Monitor disk space for large video files
- Keep the browser tab open during downloads

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add feature'`
6. Push: `git push origin feature-name`
7. Submit a pull request

### Code Style

- Follow PEP 8 Python style guidelines
- Add comments for complex logic
- Test your changes before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Notice

This application is for **personal use only**. Please respect YouTube's Terms of Service and only download videos you have permission to download. The developers are not responsible for any misuse of this software.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube video downloading
- [FFmpeg](https://ffmpeg.org/) - Video processing
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Railway](https://railway.app/) - Deployment platform

---

⭐ **Star this repository if you find it helpful!** 