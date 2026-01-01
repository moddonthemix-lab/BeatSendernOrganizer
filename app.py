#!/usr/bin/env python3
"""
Flask Web Application for Beat Organizer and Sender
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import json
from beat_sender import BeatSender

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['BEATS_FOLDER'] = 'beats'

# Ensure upload directory exists
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'aiff', 'aif', 'ogg', 'm4a', 'wma'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    try:
        beat_sender = BeatSender()
        genres = beat_sender.config.get('genres', {})

        # Format for frontend
        config_data = {
            'genres': []
        }

        for genre_name, genre_data in genres.items():
            artists = genre_data.get('artists', [])
            config_data['genres'].append({
                'name': genre_name,
                'artists': artists
            })

        return jsonify(config_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/beats', methods=['GET'])
def get_beats():
    """Get all organized beats"""
    try:
        beat_sender = BeatSender()
        all_beats = beat_sender.organizer.get_all_beats()

        # Format for frontend
        beats_data = []
        for genre, beat_paths in all_beats.items():
            for beat_path in beat_paths:
                beats_data.append({
                    'genre': genre,
                    'filename': beat_path.name,
                    'path': str(beat_path)
                })

        return jsonify({'beats': beats_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/artists/<genre>', methods=['GET'])
def get_artists(genre):
    """Get artists for a specific genre"""
    try:
        beat_sender = BeatSender()
        artists = beat_sender.get_genre_artists(genre)

        return jsonify({
            'genre': genre,
            'artists': artists
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_beat():
    """Upload and organize a beat file"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        genre = request.form.get('genre')
        artist_indices = request.form.get('artists', '')
        send_email = request.form.get('sendEmail', 'false') == 'true'

        if not genre:
            return jsonify({'error': 'Genre is required'}), 400

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(str(upload_path))

        # Parse artist indices
        selected_artists = None
        if artist_indices:
            try:
                selected_artists = [int(x.strip()) for x in artist_indices.split(',') if x.strip()]
            except ValueError:
                return jsonify({'error': 'Invalid artist indices'}), 400

        # Organize beat
        beat_sender = BeatSender()

        if send_email:
            # Organize and send
            result = beat_sender.organize_and_send_beat(
                str(upload_path),
                genre,
                selected_artists
            )

            # Clean up uploaded file
            upload_path.unlink()

            return jsonify({
                'success': True,
                'message': 'Beat organized and emails sent',
                'organized': result['organized'],
                'sent': result['sent'],
                'failed': result['failed']
            })
        else:
            # Just organize
            organized_path = beat_sender.organizer.organize_beat(str(upload_path), genre)

            # Clean up uploaded file
            upload_path.unlink()

            return jsonify({
                'success': True,
                'message': 'Beat organized successfully',
                'organized': True,
                'path': str(organized_path)
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send', methods=['POST'])
def send_beats():
    """Send existing beats to artists"""
    try:
        data = request.get_json()
        genre = data.get('genre')
        artist_indices = data.get('artists', [])
        send_all = data.get('sendAll', False)

        beat_sender = BeatSender()

        if send_all:
            # Send all beats from all genres
            result = beat_sender.send_all_beats()
            return jsonify({
                'success': True,
                'message': 'All beats sent',
                'genres_processed': result['genres_processed'],
                'total_sent': result['total_sent'],
                'total_failed': result['total_failed']
            })
        elif genre:
            # Send beats from specific genre
            result = beat_sender.send_existing_beats_by_genre(
                genre,
                artist_indices if artist_indices else None
            )
            return jsonify({
                'success': True,
                'message': f'{genre} beats sent',
                'sent': result['sent'],
                'failed': result['failed']
            })
        else:
            return jsonify({'error': 'Genre or sendAll required'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config/save', methods=['POST'])
def save_config():
    """Save configuration"""
    try:
        data = request.get_json()

        # Load current config
        config_path = Path('config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Update genres
        genres = {}
        for genre_data in data.get('genres', []):
            genre_name = genre_data['name'].lower()
            genres[genre_name] = {
                'artists': genre_data['artists']
            }

        config['genres'] = genres

        # Save config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        return jsonify({
            'success': True,
            'message': 'Configuration saved'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-beat', methods=['POST'])
def send_beat_to_artist():
    """Send a beat file to a specific artist"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        genre = request.form.get('genre')
        artist_id = request.form.get('artist_id')
        subject = request.form.get('subject', '')
        message = request.form.get('message', '')

        if not genre or not artist_id:
            return jsonify({'error': 'Genre and artist_id are required'}), 400

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(str(upload_path))

        # Load config to find artist
        beat_sender = BeatSender()
        config = beat_sender.config

        # Find artist by ID
        artist = None
        genre_data = config.get('genres', {}).get(genre, {})
        for a in genre_data.get('artists', []):
            if a.get('id') == artist_id:
                artist = a
                break

        if not artist:
            upload_path.unlink()  # Clean up
            return jsonify({'error': f'Artist {artist_id} not found in genre {genre}'}), 404

        # Organize the beat
        organized_path = beat_sender.organizer.organize_beat(str(upload_path), genre)

        # Send email with custom message
        from email_sender import EmailSender
        email_sender = EmailSender()

        # Create custom email body
        custom_body = f"Hi {artist['name']},\n\n"
        custom_body += f"You've received new {genre.upper()} beats.\n\n"

        if message:
            custom_body += f"{message}\n\n"

        custom_body += "Please find the beat attached.\n\nBest regards"

        # Use custom subject or default
        email_subject = subject if subject else f"New {genre.upper()} Beats"

        # Send the email
        success = email_sender.send_beat(
            to_email=artist['email'],
            artist_name=artist['name'],
            genre=genre,
            beat_file=str(organized_path),
            custom_subject=email_subject,
            custom_body=custom_body
        )

        # Clean up uploaded file
        upload_path.unlink()

        if success:
            return jsonify({
                'success': True,
                'message': f'Beat sent successfully to {artist["name"]}',
                'organized_path': str(organized_path)
            })
        else:
            return jsonify({'error': 'Failed to send email'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check if email is configured
        from email_sender import EmailSender
        email_sender = EmailSender()

        return jsonify({
            'status': 'healthy',
            'email_configured': True
        })
    except ValueError as e:
        return jsonify({
            'status': 'healthy',
            'email_configured': False,
            'message': str(e)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎵 Beat Organizer and Sender - Web Interface")
    print("="*60)
    print("\n📡 Server starting...")

    # Get port from environment variable (for Railway) or use 5000
    port = int(os.environ.get('PORT', 5000))

    print(f"🌐 Access the web interface at: http://localhost:{port}")
    print("\n⚠️  Make sure your .env file is configured with SMTP credentials")
    print("   to enable email sending functionality.")
    print("\n" + "="*60 + "\n")

    app.run(debug=False, host='0.0.0.0', port=port)
