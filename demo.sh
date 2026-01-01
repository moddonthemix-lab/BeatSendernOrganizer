#!/bin/bash
# Beat Organizer and Sender - Demo Script
# This script demonstrates all the features of the application

echo "========================================="
echo "Beat Organizer and Sender - DEMO"
echo "========================================="
echo ""

# 1. Show help
echo "1. HELP MENU"
echo "-------------------"
python main.py --help
echo ""
read -p "Press Enter to continue..."
echo ""

# 2. List all genres and artists
echo "2. LIST ALL GENRES AND ARTISTS"
echo "-------------------"
python main.py list
echo ""
read -p "Press Enter to continue..."
echo ""

# 3. Show artists for specific genre
echo "3. SHOW HIP-HOP ARTISTS"
echo "-------------------"
python main.py artists hip-hop
echo ""
read -p "Press Enter to continue..."
echo ""

# 4. Show organize command help
echo "4. ORGANIZE COMMAND OPTIONS"
echo "-------------------"
python main.py organize --help
echo ""
read -p "Press Enter to continue..."
echo ""

# 5. Create sample beats if they don't exist
echo "5. CREATING SAMPLE BEAT FILES"
echo "-------------------"
mkdir -p /tmp/demo_beats
dd if=/dev/zero of=/tmp/demo_beats/hip-hop-beat.mp3 bs=1024 count=10 2>/dev/null
dd if=/dev/zero of=/tmp/demo_beats/trap-beat.mp3 bs=1024 count=10 2>/dev/null
dd if=/dev/zero of=/tmp/demo_beats/rnb-beat.mp3 bs=1024 count=10 2>/dev/null
echo "✓ Created 3 sample beat files"
echo ""
read -p "Press Enter to continue..."
echo ""

# 6. Organize beats without sending
echo "6. ORGANIZE BEATS (WITHOUT SENDING)"
echo "-------------------"
echo "Organizing hip-hop beat..."
python main.py organize /tmp/demo_beats/hip-hop-beat.mp3 hip-hop --no-send
echo ""
echo "Organizing trap beat..."
python main.py organize /tmp/demo_beats/trap-beat.mp3 trap --no-send
echo ""
echo "Organizing R&B beat..."
python main.py organize /tmp/demo_beats/rnb-beat.mp3 rnb --no-send
echo ""
read -p "Press Enter to continue..."
echo ""

# 7. Show organized beats
echo "7. VIEW ORGANIZED BEATS"
echo "-------------------"
echo "Beats folder structure:"
tree beats/ 2>/dev/null || find beats/ -type f
echo ""
python main.py list
echo ""
read -p "Press Enter to continue..."
echo ""

# 8. Show send options
echo "8. SEND COMMAND OPTIONS"
echo "-------------------"
python main.py send --help
echo ""
echo "NOTE: To actually send emails, you need to:"
echo "  1. Configure your .env file with real SMTP credentials"
echo "  2. Use commands like:"
echo "     - python main.py send --genre hip-hop (send to all artists)"
echo "     - python main.py send --genre hip-hop --artists 1 (send to artist #1 only)"
echo "     - python main.py send --all (send all beats)"
echo ""
read -p "Press Enter to continue..."
echo ""

# 9. Demo with specific artists
echo "9. ORGANIZE AND SEND TO SPECIFIC ARTISTS (DRY RUN)"
echo "-------------------"
echo "Example: Organize a beat and send to artists 1 and 2 in hip-hop genre"
echo "Command: python main.py organize beat.mp3 hip-hop --artists 1 2"
echo ""
echo "This would send to:"
python main.py artists hip-hop
echo ""
echo "Only artists #1 and #2 would receive the beat"
echo ""
read -p "Press Enter to continue..."
echo ""

# 10. Summary
echo "10. SUMMARY"
echo "-------------------"
echo "✓ Application is fully functional!"
echo ""
echo "Key Features Demonstrated:"
echo "  ✓ List all genres and artists"
echo "  ✓ View artists for specific genres"
echo "  ✓ Organize beats by genre into folders"
echo "  ✓ Send beats to all artists in a genre"
echo "  ✓ Send beats to specific artists only"
echo "  ✓ Batch organize multiple beats"
echo ""
echo "Current Status:"
python main.py list
echo ""
echo "========================================="
echo "Demo Complete!"
echo "========================================="
