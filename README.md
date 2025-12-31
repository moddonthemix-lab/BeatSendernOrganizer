# Beat Organizer and Sender

A Python application that organizes beat files by genre and automatically sends them to designated email addresses based on their genre.

## Features

- **Genre-based Organization**: Automatically organizes beat files into folders by genre
- **Artist Management**: Manage artists under each genre with names and email addresses
- **Email Distribution**: Sends beats to configured artists based on genre
- **Selective Sending**: Choose specific artists to send to, or send to all artists in a genre
- **Multiple Format Support**: Works with MP3, WAV, FLAC, AIFF, OGG, M4A, and WMA files
- **Flexible Configuration**: JSON-based configuration for genre-to-artist mappings
- **CLI Interface**: Easy-to-use command-line interface
- **Batch Operations**: Send individual beats or all beats at once
- **Personalized Emails**: Email templates with artist name personalization

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

4. **Configure genres and artists**:
   Edit `config.json` to set up artists for each genre:
   ```json
   {
     "genres": {
       "hip-hop": {
         "artists": [
           {"name": "Jay Producer", "email": "jay@example.com"},
           {"name": "Mike Beats", "email": "mike@example.com"}
         ]
       },
       "trap": {
         "artists": [
           {"name": "Trap Master", "email": "trapmaster@example.com"}
         ]
       }
     }
   }
   ```

## Usage

### List Artists for a Genre

See all artists configured for a specific genre:

```bash
python main.py artists hip-hop
```

This will show:
```
👥 Artists in hip-hop genre:
  1. Jay Producer (jay@example.com)
  2. Mike Beats (mike@example.com)
```

### Organize and Send a Beat to All Artists

Organize a beat file by genre and send it to all artists in that genre:

```bash
python main.py organize path/to/beat.mp3 hip-hop
```

### Organize and Send to Specific Artists

Send a beat to specific artists only (use artist indices from the `artists` command):

```bash
# Send to artists 1 and 2 only
python main.py organize path/to/beat.mp3 hip-hop --artists 1 2
```

### Organize Only (Don't Send)

If you want to organize a beat without sending it:

```bash
python main.py organize path/to/beat.mp3 trap --no-send
```

### Send Previously Organized Beats

Send all previously organized beats of a specific genre to all artists:

```bash
python main.py send --genre hip-hop
```

### Send to Specific Artists Only

Send previously organized beats to specific artists:

```bash
python main.py send --genre hip-hop --artists 1 3
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
├── config.json             # Genre and artist configurations
├── .env                    # Email credentials (not in git)
├── .env.example            # Example environment file
└── requirements.txt        # Python dependencies
```

## Configuration

### Email Templates

You can customize email subject and body templates in `config.json`:

```json
{
  "genres": { ... },
  "email_subject_template": "New {genre} Beat: {filename}",
  "email_body_template": "Hi {artist_name},\n\nPlease find attached a new {genre} beat: {filename}\n\nBest regards"
}
```

Available template variables:
- `{artist_name}`: The name of the artist receiving the email
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

### Example 1: Add and send a new hip-hop beat to all artists

```bash
python main.py organize "/path/to/my-new-beat.mp3" hip-hop
```

This will:
1. Copy the beat to `beats/hip-hop/my-new-beat.mp3`
2. Send it to all artists configured for the "hip-hop" genre

### Example 2: Send to specific artists only

First, check who the artists are:

```bash
python main.py artists hip-hop
```

Output:
```
👥 Artists in hip-hop genre:
  1. Jay Producer (jay@example.com)
  2. Mike Beats (mike@example.com)
```

Then send to specific artists (e.g., only Jay Producer):

```bash
python main.py organize "/path/to/beat.mp3" hip-hop --artists 1
```

### Example 3: Organize multiple beats without sending

```bash
python main.py organize "beat1.mp3" trap --no-send
python main.py organize "beat2.mp3" trap --no-send
python main.py organize "beat3.mp3" trap --no-send
```

Then send all trap beats to specific artists:

```bash
python main.py send --genre trap --artists 1 2
```

### Example 4: Send all beats from all genres

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
