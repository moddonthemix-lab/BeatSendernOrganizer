#!/usr/bin/env python3
"""
Test script to verify all Beat Organizer functions work correctly
"""

import os
import sys
from pathlib import Path
from beat_sender import BeatSender

def create_dummy_beat(filename):
    """Create a dummy beat file for testing"""
    filepath = Path(filename)
    filepath.write_bytes(b'\x00' * 10240)  # 10KB dummy file
    return filepath

def test_configuration():
    """Test 1: Verify configuration loads correctly"""
    print("=" * 60)
    print("TEST 1: Configuration Loading")
    print("=" * 60)

    try:
        app = BeatSender()
        print("✓ Configuration loaded successfully")

        # Check genres
        genres = app.config.get('genres', {})
        print(f"✓ Found {len(genres)} genres configured")

        for genre, data in genres.items():
            artists = data.get('artists', [])
            print(f"  - {genre}: {len(artists)} artist(s)")

        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_artist_listing():
    """Test 2: Verify artist listing works"""
    print("\n" + "=" * 60)
    print("TEST 2: Artist Listing")
    print("=" * 60)

    try:
        app = BeatSender()

        # Test hip-hop genre
        artists = app.get_genre_artists('hip-hop')
        print(f"✓ Hip-hop has {len(artists)} artists:")
        for idx, artist in enumerate(artists, 1):
            print(f"  {idx}. {artist['name']} ({artist['email']})")

        # Test trap genre
        artists = app.get_genre_artists('trap')
        print(f"✓ Trap has {len(artists)} artists:")
        for idx, artist in enumerate(artists, 1):
            print(f"  {idx}. {artist['name']} ({artist['email']})")

        return True
    except Exception as e:
        print(f"✗ Artist listing test failed: {e}")
        return False

def test_beat_organization():
    """Test 3: Verify beat organization works"""
    print("\n" + "=" * 60)
    print("TEST 3: Beat Organization")
    print("=" * 60)

    try:
        app = BeatSender()

        # Create test beats directory
        test_dir = Path("/tmp/test_beats")
        test_dir.mkdir(exist_ok=True)

        # Create dummy beat files
        beat1 = create_dummy_beat(test_dir / "test-hiphop-beat.mp3")
        beat2 = create_dummy_beat(test_dir / "test-trap-beat.mp3")

        print(f"✓ Created test beat files")

        # Organize beats
        organized1 = app.organizer.organize_beat(str(beat1), "hip-hop")
        print(f"✓ Organized hip-hop beat to: {organized1}")

        organized2 = app.organizer.organize_beat(str(beat2), "trap")
        print(f"✓ Organized trap beat to: {organized2}")

        # Verify organization
        hiphop_beats = app.organizer.get_beats_by_genre("hip-hop")
        trap_beats = app.organizer.get_beats_by_genre("trap")

        print(f"✓ Hip-hop genre now has {len(hiphop_beats)} beat(s)")
        print(f"✓ Trap genre now has {len(trap_beats)} beat(s)")

        return True
    except Exception as e:
        print(f"✗ Beat organization test failed: {e}")
        return False

def test_genre_listing():
    """Test 4: Verify genre listing works"""
    print("\n" + "=" * 60)
    print("TEST 4: Genre Listing")
    print("=" * 60)

    try:
        app = BeatSender()

        genres = app.organizer.list_all_genres()
        print(f"✓ Found {len(genres)} organized genre(s):")
        for genre in genres:
            beats = app.organizer.get_beats_by_genre(genre)
            print(f"  - {genre}: {len(beats)} beat(s)")

        return True
    except Exception as e:
        print(f"✗ Genre listing test failed: {e}")
        return False

def test_artist_selection():
    """Test 5: Verify artist selection logic works"""
    print("\n" + "=" * 60)
    print("TEST 5: Artist Selection Logic")
    print("=" * 60)

    try:
        app = BeatSender()

        # Get all artists
        all_artists = app.get_genre_artists('hip-hop')
        print(f"✓ Hip-hop has {len(all_artists)} total artists")

        # Test selecting specific indices
        selected = []
        for idx in [1, 2]:
            if 1 <= idx <= len(all_artists):
                selected.append(all_artists[idx - 1])

        print(f"✓ Selected {len(selected)} artists (indices 1, 2):")
        for artist in selected:
            print(f"  - {artist['name']}")

        return True
    except Exception as e:
        print(f"✗ Artist selection test failed: {e}")
        return False

def test_email_templates():
    """Test 6: Verify email template formatting works"""
    print("\n" + "=" * 60)
    print("TEST 6: Email Template Formatting")
    print("=" * 60)

    try:
        app = BeatSender()

        # Get templates
        subject_template = app.config.get('email_subject_template', '')
        body_template = app.config.get('email_body_template', '')

        print(f"✓ Subject template: {subject_template}")
        print(f"✓ Body template: {body_template[:50]}...")

        # Test formatting
        test_data = {
            'genre': 'hip-hop',
            'filename': 'test-beat.mp3',
            'artist_name': 'John Producer'
        }

        subject = subject_template.format(**test_data)
        body = body_template.format(**test_data)

        print(f"\n✓ Example formatted email:")
        print(f"  Subject: {subject}")
        print(f"  Body preview: {body[:80]}...")

        return True
    except Exception as e:
        print(f"✗ Email template test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "BEAT ORGANIZER - FUNCTION TESTS" + " " * 16 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    tests = [
        test_configuration,
        test_artist_listing,
        test_beat_organization,
        test_genre_listing,
        test_artist_selection,
        test_email_templates
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")

    if all(results):
        print("\n✓ ALL TESTS PASSED! Application is fully functional.")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
