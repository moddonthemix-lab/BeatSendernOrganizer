import json
from pathlib import Path
from typing import Dict, List, Optional
from beat_organizer import BeatOrganizer
from email_sender import EmailSender

class BeatSender:
    """Main application for organizing and sending beats by genre."""

    def __init__(self, config_file: str = "config.json", beats_dir: str = "beats"):
        """
        Initialize the BeatSender.

        Args:
            config_file: Path to the configuration JSON file
            beats_dir: Directory where beats are organized
        """
        self.config_file = Path(config_file)
        self.organizer = BeatOrganizer(beats_dir)
        self.sender = EmailSender()
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

        with open(self.config_file, 'r') as f:
            return json.load(f)

    def get_genre_emails(self, genre: str) -> List[str]:
        """
        Get email addresses for a specific genre.

        Args:
            genre: Genre name

        Returns:
            List of email addresses
        """
        genre_emails = self.config.get('genre_emails', {})
        return genre_emails.get(genre.lower(), [])

    def organize_and_send_beat(self, beat_file: str, genre: str) -> dict:
        """
        Organize a beat file and send it to the corresponding email addresses.

        Args:
            beat_file: Path to the beat file
            genre: Genre of the beat

        Returns:
            Dictionary with results
        """
        # Organize the beat
        organized_path = self.organizer.organize_beat(beat_file, genre)

        # Get recipient emails for this genre
        recipients = self.get_genre_emails(genre)

        if not recipients:
            print(f"⚠ No email addresses configured for genre: {genre}")
            return {'organized': True, 'sent': 0, 'failed': 0}

        # Prepare email content
        subject_template = self.config.get('email_subject_template',
                                          'New {genre} Beat: {filename}')
        body_template = self.config.get('email_body_template',
                                       'Please find attached a new {genre} beat.')

        subject = subject_template.format(genre=genre, filename=organized_path.name)
        body = body_template.format(genre=genre, filename=organized_path.name)

        # Send to all recipients
        results = self.sender.send_beats_to_recipients(organized_path, recipients, subject, body)

        return {
            'organized': True,
            'sent': results['success'],
            'failed': results['failed']
        }

    def send_existing_beats_by_genre(self, genre: str) -> dict:
        """
        Send all existing beats of a specific genre to the configured email addresses.

        Args:
            genre: Genre name

        Returns:
            Dictionary with results
        """
        beats = self.organizer.get_beats_by_genre(genre)

        if not beats:
            print(f"⚠ No beats found for genre: {genre}")
            return {'sent': 0, 'failed': 0}

        recipients = self.get_genre_emails(genre)

        if not recipients:
            print(f"⚠ No email addresses configured for genre: {genre}")
            return {'sent': 0, 'failed': 0}

        total_sent = 0
        total_failed = 0

        # Prepare email templates
        subject_template = self.config.get('email_subject_template',
                                          'New {genre} Beat: {filename}')
        body_template = self.config.get('email_body_template',
                                       'Please find attached a new {genre} beat.')

        for beat_path in beats:
            subject = subject_template.format(genre=genre, filename=beat_path.name)
            body = body_template.format(genre=genre, filename=beat_path.name)

            results = self.sender.send_beats_to_recipients(beat_path, recipients, subject, body)
            total_sent += results['success']
            total_failed += results['failed']

        return {'sent': total_sent, 'failed': total_failed}

    def send_all_beats(self) -> dict:
        """
        Send all organized beats to their respective email addresses based on genre.

        Returns:
            Dictionary with overall results
        """
        all_beats = self.organizer.get_all_beats()

        if not all_beats:
            print("⚠ No beats found in any genre")
            return {'total_sent': 0, 'total_failed': 0, 'genres_processed': 0}

        total_sent = 0
        total_failed = 0
        genres_processed = 0

        for genre, beats in all_beats.items():
            print(f"\n📧 Processing {genre} genre ({len(beats)} beats)...")
            results = self.send_existing_beats_by_genre(genre)
            total_sent += results['sent']
            total_failed += results['failed']
            genres_processed += 1

        return {
            'total_sent': total_sent,
            'total_failed': total_failed,
            'genres_processed': genres_processed
        }

    def list_configuration(self) -> None:
        """Display current configuration."""
        print("\n📋 Current Configuration:")
        print("\nGenre Email Mappings:")

        genre_emails = self.config.get('genre_emails', {})

        if not genre_emails:
            print("  No genre mappings configured")
        else:
            for genre, emails in genre_emails.items():
                print(f"  {genre}:")
                for email in emails:
                    print(f"    - {email}")

        print("\n📁 Organized Beats:")
        all_beats = self.organizer.get_all_beats()

        if not all_beats:
            print("  No beats organized yet")
        else:
            for genre, beats in all_beats.items():
                print(f"  {genre}: {len(beats)} beat(s)")
