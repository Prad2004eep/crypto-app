from flask import Flask, render_template, request, send_file, flash, redirect, url_for, Response, jsonify, g
import os
import logging
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import RequestEntityTooLarge
from functools import wraps
import time
from datetime import timedelta
from steganography import encode, decode, encode_audio, decode_audio
import io
import secrets

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config.update(
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32)),
    UPLOAD_FOLDER='uploads',
    OUTPUT_FOLDER='outputs',
    MAX_CONTENT_LENGTH=100 * 1024 * 1024,  # 100MB max file size (reduced from 1GB for security)
    UPLOAD_EXTENSIONS={'.png', '.jpg', '.jpeg', '.bmp', '.mp3', '.wav', '.ogg', '.webm', '.m4a'},
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
    RATELIMIT_DEFAULT='200 per hour'
)

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Apply proxy fix if behind a reverse proxy
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'webm', 'm4a'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_audio_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['GET', 'POST'])
def encode_page():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'image' not in request.files:
            flash('No image file uploaded', 'error')
            return redirect(request.url)
        
        file = request.files['image']
        secret_message = request.form.get('message', '')
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if not secret_message:
            flash('No message provided', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # Encode message
            output_filename = 'encoded_' + filename.rsplit('.', 1)[0] + '.png'
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            try:
                encode(input_path, secret_message, output_path)
                flash('Message encoded successfully!', 'success')
                return send_file(output_path, as_attachment=True, download_name=output_filename)
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(request.url)
            except Exception as e:
                flash(f'Error encoding message: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload PNG, JPG, JPEG, or BMP', 'error')
            return redirect(request.url)
    
    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode_page():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'image' not in request.files:
            flash('No image file uploaded', 'error')
            return redirect(request.url)
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # Decode message
            try:
                decoded_message = decode(input_path)
                return render_template('decode.html', decoded_message=decoded_message)
            except Exception as e:
                flash(f'Error decoding message: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload PNG, JPG, JPEG, or BMP', 'error')
            return redirect(request.url)
    
    return render_template('decode.html')

@app.route('/encode-audio', methods=['GET', 'POST'])
def encode_audio_page():
    if request.method == 'POST':
        # Check if files were uploaded
        if 'image' not in request.files or 'audio' not in request.files:
            flash('Please upload both image and audio files', 'error')
            return redirect(request.url)

        image_file = request.files['image']
        audio_file = request.files['audio']

        if image_file.filename == '' or audio_file.filename == '':
            flash('Please select both files', 'error')
            return redirect(request.url)

        if image_file and allowed_file(image_file.filename):
            # Save uploaded image
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)

            # Read audio data
            audio_data = audio_file.read()

            # Encode audio
            output_filename = 'audio_encoded_' + image_filename.rsplit('.', 1)[0] + '.png'
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

            try:
                encode_audio(image_path, audio_data, output_path)
                flash('Audio encoded successfully!', 'success')
                return send_file(output_path, as_attachment=True, download_name=output_filename)
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(request.url)
            except Exception as e:
                flash(f'Error encoding audio: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid image file type. Please upload PNG, JPG, JPEG, or BMP', 'error')
            return redirect(request.url)

    return render_template('encode_audio.html')

@app.route('/decode-audio', methods=['GET', 'POST'])
def decode_audio_page():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'image' not in request.files:
            flash('No image file uploaded', 'error')
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)

            # Decode audio
            try:
                audio_data = decode_audio(input_path)

                # Save audio to temporary file
                audio_filename = 'decoded_audio.wav'
                audio_path = os.path.join(app.config['OUTPUT_FOLDER'], audio_filename)

                with open(audio_path, 'wb') as f:
                    f.write(audio_data)

                # Return template with audio file info
                return render_template('decode_audio.html',
                                     audio_decoded=True,
                                     audio_filename=audio_filename,
                                     audio_size=len(audio_data))
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(request.url)
            except Exception as e:
                flash(f'Error decoding audio: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload PNG, JPG, JPEG, or BMP', 'error')
            return redirect(request.url)

    return render_template('decode_audio.html')

@app.route('/download-audio/<filename>')
def download_audio(filename):
    """Serve the decoded audio file for download"""
    try:
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        if os.path.exists(audio_path):
            return send_file(audio_path, as_attachment=True, download_name=filename, mimetype='audio/wav')
        else:
            flash('Audio file not found', 'error')
            return redirect(url_for('decode_audio_page'))
    except Exception as e:
        flash(f'Error downloading audio: {str(e)}', 'error')
        return redirect(url_for('decode_audio_page'))

@app.route('/play-audio/<filename>')
def play_audio(filename):
    """Serve the decoded audio file for playback"""
    try:
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/wav')
        else:
            return "Audio file not found", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Server Error: {error}', exc_info=True)
    return render_template('error.html', error='Internal server error'), 500

@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    return render_template('error.html', error='File too large (max 100MB)'), 413

# Security Headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    return response

# Rate limiting decorator
def rate_limited(limit=100, per=60):
    def decorator(f):
        calls = []
        
        @wraps(f)
        def wrapped(*args, **kwargs):
            now = time.time()
            calls_in_time = [call for call in calls if call > now - per]
            
            if len(calls_in_time) >= limit:
                return jsonify({"error": "Rate limit exceeded"}), 429
                
            calls.append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


