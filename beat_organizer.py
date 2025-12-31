import os
import shutil
from pathlib import Path
from typing import List, Dict

class BeatOrganizer:
    """Organizes beat files by genre into separate directories."""

    AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aiff', '.ogg', '.m4a', '.wma'}

    def __init__(self, beats_dir: str = "beats"):
        """
        Initialize the BeatOrganizer.

        Args:
            beats_dir: Base directory where beats are organized by genre
        """
        self.beats_dir = Path(beats_dir)
        self.beats_dir.mkdir(exist_ok=True)

    def create_genre_folder(self, genre: str) -> Path:
        """
        Create a folder for a specific genre.

        Args:
            genre: Genre name (e.g., 'hip-hop', 'trap', 'rnb')

        Returns:
            Path to the genre folder
        """
        genre_folder = self.beats_dir / genre.lower()
        genre_folder.mkdir(exist_ok=True)
        return genre_folder

    def organize_beat(self, beat_file: str, genre: str) -> Path:
        """
        Organize a beat file into its genre folder.

        Args:
            beat_file: Path to the beat file
            genre: Genre to organize the beat under

        Returns:
            Path to the organized beat file
        """
        beat_path = Path(beat_file)

        if not beat_path.exists():
            raise FileNotFoundError(f"Beat file not found: {beat_file}")

        if beat_path.suffix.lower() not in self.AUDIO_EXTENSIONS:
            raise ValueError(f"Invalid audio file format: {beat_path.suffix}")

        genre_folder = self.create_genre_folder(genre)
        destination = genre_folder / beat_path.name

        # Copy the file to the genre folder
        shutil.copy2(beat_path, destination)
        print(f"✓ Organized '{beat_path.name}' into {genre} folder")

        return destination

    def get_beats_by_genre(self, genre: str) -> List[Path]:
        """
        Get all beat files for a specific genre.

        Args:
            genre: Genre name

        Returns:
            List of beat file paths
        """
        genre_folder = self.beats_dir / genre.lower()

        if not genre_folder.exists():
            return []

        beats = []
        for file_path in genre_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.AUDIO_EXTENSIONS:
                beats.append(file_path)

        return sorted(beats)

    def list_all_genres(self) -> List[str]:
        """
        List all available genres.

        Returns:
            List of genre names
        """
        genres = []
        for item in self.beats_dir.iterdir():
            if item.is_dir():
                genres.append(item.name)

        return sorted(genres)

    def get_all_beats(self) -> Dict[str, List[Path]]:
        """
        Get all beats organized by genre.

        Returns:
            Dictionary mapping genre names to lists of beat files
        """
        all_beats = {}

        for genre in self.list_all_genres():
            beats = self.get_beats_by_genre(genre)
            if beats:
                all_beats[genre] = beats

        return all_beats
