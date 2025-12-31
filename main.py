#!/usr/bin/env python3
"""
Beat Organizer and Sender - Main CLI Interface
"""

import argparse
import sys
from pathlib import Path
from beat_sender import BeatSender

def main():
    parser = argparse.ArgumentParser(
        description='Beat Organizer and Sender - Organize and send beats by genre via email'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Organize command
    organize_parser = subparsers.add_parser('organize', help='Organize a beat file by genre')
    organize_parser.add_argument('beat_file', help='Path to the beat file')
    organize_parser.add_argument('genre', help='Genre of the beat')
    organize_parser.add_argument('--no-send', action='store_true',
                                help='Only organize, do not send via email')

    # Send command
    send_parser = subparsers.add_parser('send', help='Send beats by genre')
    send_parser.add_argument('--genre', help='Send beats of a specific genre')
    send_parser.add_argument('--all', action='store_true', help='Send all organized beats')

    # List command
    list_parser = subparsers.add_parser('list', help='List configuration and organized beats')

    # Config command
    config_parser = subparsers.add_parser('config', help='Show current configuration')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        app = BeatSender()

        if args.command == 'organize':
            beat_file = args.beat_file
            genre = args.genre

            if not Path(beat_file).exists():
                print(f"✗ Error: File not found: {beat_file}")
                sys.exit(1)

            if args.no_send:
                # Only organize
                organized_path = app.organizer.organize_beat(beat_file, genre)
                print(f"\n✓ Beat organized successfully!")
                print(f"  Location: {organized_path}")
            else:
                # Organize and send
                print(f"\n📁 Organizing and sending beat...")
                results = app.organize_and_send_beat(beat_file, genre)

                print(f"\n✓ Operation completed!")
                print(f"  Organized: {results['organized']}")
                print(f"  Emails sent: {results['sent']}")
                print(f"  Failed: {results['failed']}")

        elif args.command == 'send':
            if args.all:
                print("\n📧 Sending all organized beats...")
                results = app.send_all_beats()

                print(f"\n✓ Operation completed!")
                print(f"  Genres processed: {results['genres_processed']}")
                print(f"  Total emails sent: {results['total_sent']}")
                print(f"  Total failed: {results['total_failed']}")

            elif args.genre:
                genre = args.genre
                print(f"\n📧 Sending {genre} beats...")
                results = app.send_existing_beats_by_genre(genre)

                print(f"\n✓ Operation completed!")
                print(f"  Emails sent: {results['sent']}")
                print(f"  Failed: {results['failed']}")

            else:
                print("✗ Error: Please specify --genre or --all")
                send_parser.print_help()
                sys.exit(1)

        elif args.command == 'list':
            app.list_configuration()

        elif args.command == 'config':
            app.list_configuration()

    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
