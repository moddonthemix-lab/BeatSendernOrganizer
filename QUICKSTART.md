# Quick Start Guide

## Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Email (Optional for Testing)

For testing without email, the demo .env is already set up. To actually send emails:

```bash
# Edit .env file with your real SMTP credentials
nano .env
```

### Step 3: Try It Out!

**View all configured genres and artists:**
```bash
python main.py list
```

**See artists for a specific genre:**
```bash
python main.py artists hip-hop
```

**Organize a beat file:**
```bash
python main.py organize /path/to/your-beat.mp3 hip-hop --no-send
```

**Organize and send to specific artists:**
```bash
# First see who's available
python main.py artists hip-hop

# Send to artists 1 and 2 only
python main.py organize /path/to/your-beat.mp3 hip-hop --artists 1 2
```

## Run Tests

**Automated function tests:**
```bash
python test_app.py
```

**Interactive demo:**
```bash
./demo.sh
```

## Common Commands

| Command | Description |
|---------|-------------|
| `python main.py list` | Show all genres, artists, and organized beats |
| `python main.py artists <genre>` | List all artists in a genre |
| `python main.py organize <file> <genre>` | Organize and send beat to all artists |
| `python main.py organize <file> <genre> --no-send` | Organize only, don't send |
| `python main.py organize <file> <genre> --artists 1 2` | Send to specific artists |
| `python main.py send --genre <genre>` | Send all beats in a genre |
| `python main.py send --genre <genre> --artists 1` | Send to specific artist |
| `python main.py send --all` | Send all beats to all artists |

## Add Your Own Artists

Edit `config.json`:

```json
{
  "genres": {
    "hip-hop": {
      "artists": [
        {"name": "Your Artist Name", "email": "artist@email.com"},
        {"name": "Another Artist", "email": "another@email.com"}
      ]
    }
  }
}
```

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- FLAC (.flac)
- AIFF (.aiff)
- OGG (.ogg)
- M4A (.m4a)
- WMA (.wma)

## Email Setup (For Actual Sending)

**Gmail Users:**
1. Go to Google Account settings
2. Enable 2-factor authentication
3. Create an App Password
4. Use the app password in `.env`

**Other SMTP Providers:**
- Update `SMTP_SERVER` and `SMTP_PORT` in `.env`
- Use your SMTP credentials

## File Structure

```
beats/
├── hip-hop/        # Hip-hop beats organized here
├── trap/           # Trap beats organized here
├── rnb/            # R&B beats organized here
└── ...             # Other genres

config.json         # Genre and artist configuration
.env                # Email credentials (keep private!)
```

## Need Help?

Run any command with `--help`:

```bash
python main.py --help
python main.py organize --help
python main.py send --help
```

## Testing Without Real Emails

The application is set up with demo credentials that won't actually send emails. This lets you:
- Organize beats into folders ✓
- Test all commands ✓
- See how artist selection works ✓

When you're ready to send real emails, just update `.env` with real SMTP credentials!
