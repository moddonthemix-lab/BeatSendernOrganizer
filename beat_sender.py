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

    def get_genre_artists(self, genre: str) -> List[dict]:
        """
        Get artists for a specific genre.

        Args:
            genre: Genre name

        Returns:
            List of artist dictionaries with 'name' and 'email' keys
        """
        genres = self.config.get('genres', {})
        genre_data = genres.get(genre.lower(), {})
        return genre_data.get('artists', [])

    def get_genre_emails(self, genre: str) -> List[str]:
        """
        Get email addresses for a specific genre.

        Args:
            genre: Genre name

        Returns:
            List of email addresses
        """
        artists = self.get_genre_artists(genre)
        return [artist['email'] for artist in artists]

    def list_available_artists(self, genre: str) -> None:
        """
        Display available artists for a genre.

        Args:
            genre: Genre name
        """
        artists = self.get_genre_artists(genre)

        if not artists:
            print(f"⚠ No artists configured for genre: {genre}")
            return

        print(f"\n👥 Artists in {genre} genre:")
        for idx, artist in enumerate(artists, 1):
            print(f"  {idx}. {artist['name']} ({artist['email']})")

    def send_beat_to_artist(self, beat_path: Path, artist: dict, genre: str) -> bool:
        """
        Send a beat to a specific artist.

        Args:
            beat_path: Path to the beat file
            artist: Artist dictionary with 'name' and 'email'
            genre: Genre of the beat

        Returns:
            True if sent successfully
        """
        subject_template = self.config.get('email_subject_template',
                                          'New {genre} Beat: {filename}')
        body_template = self.config.get('email_body_template',
                                       'Please find attached a new {genre} beat.')

        subject = subject_template.format(
            genre=genre,
            filename=beat_path.name,
            artist_name=artist['name']
        )
        body = body_template.format(
            genre=genre,
            filename=beat_path.name,
            artist_name=artist['name']
        )

        return self.sender.send_beat(beat_path, artist['email'], subject, body)

    def organize_and_send_beat(self, beat_file: str, genre: str, artist_indices: List[int] = None) -> dict:
        """
        Organize a beat file and send it to the corresponding email addresses.

        Args:
            beat_file: Path to the beat file
            genre: Genre of the beat
            artist_indices: Optional list of artist indices (1-based) to send to. If None, sends to all.

        Returns:
            Dictionary with results
        """
        # Organize the beat
        organized_path = self.organizer.organize_beat(beat_file, genre)

        # Get artists for this genre
        artists = self.get_genre_artists(genre)

        if not artists:
            print(f"⚠ No artists configured for genre: {genre}")
            return {'organized': True, 'sent': 0, 'failed': 0}

        # Filter artists if specific indices provided
        if artist_indices:
            selected_artists = []
            for idx in artist_indices:
                if 1 <= idx <= len(artists):
                    selected_artists.append(artists[idx - 1])
                else:
                    print(f"⚠ Invalid artist index: {idx}")
            artists = selected_artists

        if not artists:
            print(f"⚠ No valid artists selected")
            return {'organized': True, 'sent': 0, 'failed': 0}

        # Send to selected artists
        sent = 0
        failed = 0

        for artist in artists:
            if self.send_beat_to_artist(organized_path, artist, genre):
                sent += 1
            else:
                failed += 1

        return {
            'organized': True,
            'sent': sent,
            'failed': failed
        }

    def send_existing_beats_by_genre(self, genre: str, artist_indices: List[int] = None) -> dict:
        """
        Send all existing beats of a specific genre to the configured artists.

        Args:
            genre: Genre name
            artist_indices: Optional list of artist indices to send to. If None, sends to all.

        Returns:
            Dictionary with results
        """
        beats = self.organizer.get_beats_by_genre(genre)

        if not beats:
            print(f"⚠ No beats found for genre: {genre}")
            return {'sent': 0, 'failed': 0}

        # Get artists for this genre
        artists = self.get_genre_artists(genre)

        if not artists:
            print(f"⚠ No artists configured for genre: {genre}")
            return {'sent': 0, 'failed': 0}

        # Filter artists if specific indices provided
        if artist_indices:
            selected_artists = []
            for idx in artist_indices:
                if 1 <= idx <= len(artists):
                    selected_artists.append(artists[idx - 1])
                else:
                    print(f"⚠ Invalid artist index: {idx}")
            artists = selected_artists

        if not artists:
            print(f"⚠ No valid artists selected")
            return {'sent': 0, 'failed': 0}

        total_sent = 0
        total_failed = 0

        for beat_path in beats:
            for artist in artists:
                if self.send_beat_to_artist(beat_path, artist, genre):
                    total_sent += 1
                else:
                    total_failed += 1

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
        print("\n👥 Genres and Artists:")

        genres = self.config.get('genres', {})

        if not genres:
            print("  No genres configured")
        else:
            for genre, genre_data in genres.items():
                artists = genre_data.get('artists', [])
                print(f"\n  {genre.upper()}:")
                if artists:
                    for idx, artist in enumerate(artists, 1):
                        print(f"    {idx}. {artist['name']} - {artist['email']}")
                else:
                    print("    No artists configured")

        print("\n📁 Organized Beats:")
        all_beats = self.organizer.get_all_beats()

        if not all_beats:
            print("  No beats organized yet")
        else:
            for genre, beats in all_beats.items():
                print(f"  {genre}: {len(beats)} beat(s)")
