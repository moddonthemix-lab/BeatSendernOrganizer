# Beat Organizer and Sender

A Python application that organizes beat files by genre and automatically sends them to designated email addresses based on their genre.

## Features

- **Genre-based Organization**: Automatically organizes beat files into folders by genre
- **Email Distribution**: Sends beats to configured email addresses based on genre
- **Multiple Format Support**: Works with MP3, WAV, FLAC, AIFF, OGG, M4A, and WMA files
- **Flexible Configuration**: JSON-based configuration for genre-to-email mapping
- **CLI Interface**: Easy-to-use command-line interface
- **Batch Operations**: Send individual beats or all beats at once

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BeatSendernOrganizer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure email settings**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your SMTP credentials:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SENDER_EMAIL=your-email@gmail.com
   SENDER_NAME=Beat Producer
   ```

   **For Gmail users**: You'll need to create an [App Password](https://support.google.com/accounts/answer/185833) instead of using your regular password.

4. **Configure genre-to-email mappings**:
   Edit `config.json` to set up which email addresses should receive beats for each genre:
   ```json
   {
     "genre_emails": {
       "hip-hop": ["producer1@example.com", "producer2@example.com"],
       "trap": ["producer3@example.com"],
       "rnb": ["artist1@example.com"]
     }
   }
   ```

## Usage

### Organize and Send a Beat

Organize a beat file by genre and send it to the configured email addresses:

```bash
python main.py organize path/to/beat.mp3 hip-hop
```

### Organize Only (Don't Send)

If you want to organize a beat without sending it:

```bash
python main.py organize path/to/beat.mp3 trap --no-send
```

### Send Beats by Genre

Send all previously organized beats of a specific genre:

```bash
python main.py send --genre hip-hop
```

### Send All Beats

Send all organized beats to their respective email addresses:

```bash
python main.py send --all
```

### List Configuration

View your current configuration and organized beats:

```bash
python main.py list
```

## Directory Structure

```
BeatSendernOrganizer/
├── beats/                  # Beats organized by genre
│   ├── hip-hop/
│   ├── trap/
│   ├── rnb/
│   └── ...
├── beat_organizer.py       # Beat organization logic
├── email_sender.py         # Email sending functionality
├── beat_sender.py          # Main application logic
├── main.py                 # CLI interface
├── config.json             # Genre-to-email mappings
├── .env                    # Email credentials (not in git)
├── .env.example            # Example environment file
└── requirements.txt        # Python dependencies
```

## Configuration

### Email Templates

You can customize email subject and body templates in `config.json`:

```json
{
  "genre_emails": { ... },
  "email_subject_template": "New {genre} Beat: {filename}",
  "email_body_template": "Hi,\n\nPlease find attached a new {genre} beat: {filename}\n\nBest regards"
}
```

Available template variables:
- `{genre}`: The genre of the beat
- `{filename}`: The name of the beat file

### Supported Audio Formats

- MP3 (`.mp3`)
- WAV (`.wav`)
- FLAC (`.flac`)
- AIFF (`.aiff`)
- OGG (`.ogg`)
- M4A (`.m4a`)
- WMA (`.wma`)

## Examples

### Example 1: Add and send a new hip-hop beat

```bash
python main.py organize "/path/to/my-new-beat.mp3" hip-hop
```

This will:
1. Copy the beat to `beats/hip-hop/my-new-beat.mp3`
2. Send it to all email addresses configured for the "hip-hop" genre

### Example 2: Organize multiple beats without sending

```bash
python main.py organize "beat1.mp3" trap --no-send
python main.py organize "beat2.mp3" trap --no-send
python main.py organize "beat3.mp3" trap --no-send
```

Then send all trap beats at once:

```bash
python main.py send --genre trap
```

### Example 3: Send all beats from all genres

```bash
python main.py send --all
```

## Troubleshooting

### Email Not Sending

1. **Check your .env file**: Make sure all SMTP credentials are correct
2. **Gmail users**: Use an App Password, not your regular password
3. **Firewall**: Ensure port 587 is not blocked
4. **Test SMTP connection**: Try sending a test email using your credentials

### File Not Found

Make sure you provide the full path to your beat file, or run the command from the directory containing the beat.

### Invalid File Format

Only audio files with supported extensions can be organized. Check the supported formats list above.

## Security Notes

- Never commit your `.env` file to git (it's in `.gitignore`)
- Use app-specific passwords for email services
- Keep your `config.json` private if it contains sensitive email addresses

## License

MIT License

## Contributing

Feel free to submit issues and pull requests!
