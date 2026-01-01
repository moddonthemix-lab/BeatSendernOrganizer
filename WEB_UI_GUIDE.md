# Web UI Guide

## 🌐 Access the Web Interface

The Beat Organizer now has a **full web interface**!

### Starting the Web Server

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

The server will show:
```
============================================================
🎵 Beat Organizer and Sender - Web Interface
============================================================

📡 Server starting...
🌐 Access the web interface at: http://localhost:5000
============================================================
```

## 📱 Web Interface Features

### 1. **Upload Beat** Tab
- **Drag & drop or select** beat files
- **Choose genre** from dropdown
- **Select specific artists** or send to all
- **Toggle email sending** on/off
- See real-time upload progress

**How to use:**
1. Click "Choose file" and select your beat
2. Select the genre (hip-hop, trap, etc.)
3. Optionally select specific artists (or leave empty for all)
4. Check/uncheck "Send email to artists"
5. Click "Upload & Organize"

### 2. **Beat Library** Tab
- View all organized beats by genre
- See how many beats in each genre
- Refresh to see latest uploads

### 3. **Manage Artists** Tab
- View all genres and their artists
- Add new artists to any genre
- Edit artist names and emails
- Remove artists
- Save changes

**How to use:**
1. Click on any artist name or email to edit
2. Click "+ Add Artist" to add new artists
3. Click "✕" to remove an artist
4. Click "💾 Save Changes" when done

### 4. **Send Beats** Tab
- Send previously organized beats
- Choose genre and specific artists
- Or send all beats from all genres at once

**How to use:**
1. Select a genre from dropdown
2. Optionally select specific artists
3. Click "📧 Send Beats"

**Or:** Click "📧 Send All Beats" to send everything!

## 🎨 Modern UI Features

- **Beautiful gradient design**
- **Responsive** - works on mobile, tablet, desktop
- **Real-time feedback** with success/error messages
- **Progress indicators** during uploads
- **Organized layout** with easy navigation tabs
- **Color-coded status** (green = success, red = error, yellow = warning)

## 🔧 Technical Details

### API Endpoints

The web interface uses these API endpoints:

- `GET /api/health` - Check email configuration status
- `GET /api/config` - Get genres and artists
- `GET /api/beats` - Get all organized beats
- `GET /api/artists/<genre>` - Get artists for a genre
- `POST /api/upload` - Upload and organize a beat
- `POST /api/send` - Send beats to artists
- `POST /api/config/save` - Save configuration changes

### File Upload

- **Max file size:** 100MB
- **Supported formats:** MP3, WAV, FLAC, AIFF, OGG, M4A, WMA
- Files are temporarily uploaded, organized, and then cleaned up

### Email Sending

The web interface respects your `.env` configuration:
- If SMTP is configured ✓ emails will send
- If not configured ⚠️ you'll see a warning but can still organize beats

## 🚀 Quick Start Example

**Scenario:** Upload a hip-hop beat and send it to specific artists

1. Start the server: `python app.py`
2. Open browser: http://localhost:5000
3. Go to "Upload Beat" tab
4. Select your beat file (e.g., `my-beat.mp3`)
5. Choose genre: "hip-hop"
6. Select artists 1 and 2
7. Make sure "Send email" is checked
8. Click "Upload & Organize"
9. ✓ Done! Beat organized and emails sent!

## 📊 Example Workflow

### Add Beats Throughout the Day
```
1. Upload beat1.mp3 → hip-hop (no email)
2. Upload beat2.mp3 → trap (no email)
3. Upload beat3.mp3 → hip-hop (no email)
```

### Send All at End of Day
```
1. Go to "Send Beats" tab
2. Click "Send All Beats"
3. All beats sent to their respective artists!
```

## 💡 Pro Tips

1. **Organize First, Send Later**
   - Uncheck "Send email" when uploading
   - Review all beats in Library tab
   - Send all at once from Send tab

2. **Selective Sending**
   - Use artist checkboxes to target specific recipients
   - Great for sending exclusive beats

3. **Manage Artists Easily**
   - Use the web interface to update artist emails
   - No need to edit JSON files manually

4. **Check Email Status**
   - Top of page shows email configuration status
   - Green = Ready to send
   - Yellow = Configure .env to enable sending

## 🔐 Security Notes

- Web server runs on localhost by default (secure)
- File uploads are validated for type and size
- Uploaded files are cleaned up after processing
- No beats are exposed publicly

## 🛠️ Troubleshooting

**Server won't start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Then try again
python app.py
```

**Can't access http://localhost:5000:**
- Check if server is running
- Try http://127.0.0.1:5000 instead
- Check firewall settings

**Email not sending:**
- Check the status indicator at top of page
- Configure your `.env` file with SMTP credentials
- See README.md for email setup instructions

**File upload fails:**
- Check file format (must be audio file)
- Check file size (max 100MB)
- Try refreshing the page

## 📱 Mobile Support

The web interface works great on mobile!
- Responsive design adapts to screen size
- Touch-friendly buttons and controls
- Same features as desktop

## 🎯 Summary

The web interface makes the Beat Organizer super easy to use:
- ✅ No command line needed
- ✅ Visual interface for all operations
- ✅ Real-time feedback
- ✅ Manage everything in one place
- ✅ Perfect for daily use

**Start the server and try it now!**
```bash
python app.py
```

Then visit: **http://localhost:5000**
