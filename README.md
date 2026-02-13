# 🔐 CryptoStego - Advanced LSB Steganography Web Application

A sophisticated web-based steganography tool that hides secret messages and audio recordings within images using Least Significant Bit (LSB) techniques. Built with Flask and featuring a modern, responsive interface.

## 🌟 Features

### 📝 Text Steganography
- **Encode**: Hide text messages in images with military-grade encryption
- **Decode**: Extract hidden messages from encoded images
- **Support**: PNG, JPG, JPEG, BMP formats
- **Security**: Message delimiters prevent corruption

### 🎵 Audio Steganography
- **Encode**: Hide audio recordings (voice, music) in images
- **Decode**: Extract and playback hidden audio files
- **Formats**: MP3, WAV, OGG, WebM, M4A support
- **Compression**: Automatic audio optimization (50-70% size reduction)
- **Browser Recording**: Direct audio capture via microphone

### 🛡️ Security & Performance
- **Rate Limiting**: Prevents abuse with configurable limits
- **File Size Limits**: 100MB max upload size
- **Security Headers**: XSS protection, content type validation
- **Session Management**: Secure cookie handling
- **Error Handling**: Comprehensive error reporting
- **Logging**: Detailed activity logs

### 🎨 User Interface
- **Modern Design**: Clean, responsive web interface
- **Real-time Feedback**: Flash messages for user actions
- **File Validation**: Client and server-side validation
- **Progress Indicators**: Visual feedback during operations

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Memory**: Minimum 4GB RAM (8GB recommended for large images)
- **Storage**: 500MB free space for dependencies and uploads
- **Browser**: Modern browser with HTML5 audio support

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd crypto
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup** (optional):
   ```bash
   # Create .env file for custom configuration
   echo "FLASK_SECRET_KEY=your-secret-key-here" > .env
   echo "PORT=5000" >> .env
   ```

### Running the Application

**Development Mode**:
```bash
python app.py
```

**Production Mode**:
```bash
python run_prod.py
# or using gunicorn
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Access the application at `http://localhost:5000`

## 📁 Project Structure

```
crypto/
├── app.py                 # Main Flask application
├── steganography.py       # Core steganography algorithms
├── requirements.txt       # Python dependencies
├── run_prod.py           # Production server runner
├── wsgi.py               # WSGI entry point
├── create_large_image.py # Utility for creating large images
├── test_capacity.py      # Storage capacity tester
├── .env                  # Environment variables
├── uploads/              # Temporary upload directory
├── outputs/              # Generated files directory
├── static/               # Static assets (CSS, JS, images)
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── encode.html       # Text encoding interface
│   ├── decode.html       # Text decoding interface
│   ├── encode_audio.html # Audio encoding interface
│   └── decode_audio.html # Audio decoding interface
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_SECRET_KEY` | Auto-generated | Flask session encryption key |
| `PORT` | 5000 | Server port |
| `MAX_CONTENT_LENGTH` | 100MB | Maximum upload file size |

### Application Settings

Modify `app.py` to customize:
- Upload file size limits
- Allowed file extensions
- Rate limiting parameters
- Security configurations
- Logging levels

## 📊 Storage Capacity Calculator

### Image Capacity for Audio Storage

| Image Resolution | Approx. Audio Storage |
|------------------|----------------------|
| 1920×1080 (Full HD) | ~0.74 MB |
| 3840×2160 (4K) | ~3 MB |
| 7680×4320 (8K) | ~12 MB |
| 10000×10000 | ~36 MB |
| 20000×20000 | ~143 MB |

### Creating Large Images

For storing long audio files, generate large blank images:

```bash
python create_large_image.py
```

This utility creates images with sufficient pixel density for your audio storage needs.

## 🛠️ API Endpoints

### Text Steganography
- `GET/POST /encode` - Encode text messages
- `GET/POST /decode` - Decode text messages

### Audio Steganography
- `GET/POST /encode-audio` - Encode audio files
- `GET/POST /decode-audio` - Decode audio files
- `GET /download-audio/<filename>` - Download decoded audio
- `GET /play-audio/<filename>` - Stream decoded audio

### Utility
- `GET /` - Home page
- Error handlers for 404, 500, 413 status codes

## 🔒 Security Features

- **Input Validation**: Comprehensive file type and size validation
- **XSS Protection**: Content Security Policy headers
- **CSRF Protection**: Flask session security
- **Rate Limiting**: Configurable request rate limits
- **Secure Headers**: Security-focused HTTP headers
- **File Sanitization**: Secure filename handling
- **Session Security**: HTTP-only, secure cookies

## 🧪 Testing

### Test Storage Capacity
```bash
python test_capacity.py
```

### Manual Testing Checklist

1. **Text Encoding/Decoding**:
   - Upload various image formats
   - Test with different message lengths
   - Verify message integrity

2. **Audio Encoding/Decoding**:
   - Test various audio formats
   - Verify audio quality
   - Test browser recording feature

3. **Error Handling**:
   - Test invalid file types
   - Test oversized files
   - Test corrupted images

4. **Security**:
   - Test XSS protection
   - Verify rate limiting
   - Check file validation

## 🐛 Troubleshooting

### Common Issues

**"Message too large for this image"**
- Use a larger image or shorter message
- Check image dimensions and quality

**"Invalid file type"**
- Ensure image is PNG, JPG, JPEG, or BMP
- Verify audio is MP3, WAV, OGG, WebM, or M4A

**"Audio encoding failed"**
- Check audio file integrity
- Verify sufficient image capacity
- Ensure FFmpeg is installed for audio processing

**Performance Issues**:
- Use PNG format for better compression
- Optimize image dimensions
- Consider server resources for large files

### Debug Mode

Enable debug logging:
```python
# In app.py
app.config['DEBUG'] = True
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Dependencies

### Core Dependencies
- **Flask 3.0.0** - Web framework
- **Pillow 10.1.0** - Image processing
- **Werkzeug 3.0.1** - WSGI utilities
- **python-dotenv 1.0.0** - Environment variables

### Audio Processing
- **pydub 0.25.1** - Audio manipulation
- **ffmpeg-python 0.2.0** - FFmpeg bindings
- **pyaudio 0.2.13** - Audio recording

### Production
- **gunicorn 21.2.0** - WSGI server
- **requests 2.31.0** - HTTP client

### Utilities
- **python-magic** - File type detection
- **python-slugify** - URL-friendly strings
- **blinker 1.7.0** - Signaling support

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

### Heroku Deployment

1. Create `Procfile`:
   ```
   web: gunicorn --bind 0.0.0.0:$PORT wsgi:app
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Environment-Specific Notes

**Windows**:
- Install Microsoft Visual C++ Build Tools
- FFmpeg may require manual installation

**macOS**:
- Install FFmpeg via Homebrew: `brew install ffmpeg`
- Ensure Xcode command line tools are installed

**Linux**:
- Install FFmpeg: `sudo apt-get install ffmpeg`
- Install Python development headers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## ⚠️ Disclaimer

This tool is for educational and legitimate purposes only. Users are responsible for complying with applicable laws and regulations regarding steganography and data privacy.

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

---

**Built with ❤️ using Python, Flask, and modern web technologies**

