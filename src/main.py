"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

# Supports both `python -m src.main` and `python src/main.py`
try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs


# Standard taste profiles
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
}

# Adversarial / edge-case profiles designed to stress the scoring logic
EDGE_CASE_PROFILES = {
    "Conflicting: High-Energy Sad": {"genre": "folk", "mood": "sad", "energy": 0.9},
    "Wrong Case: 'Pop' / 'Happy'": {"genre": "Pop", "mood": "Happy", "energy": 0.8},
    "Out of Range Energy (1.5)": {"genre": "classical", "mood": "peaceful", "energy": 1.5},
    "Acoustic EDM Fan": {"genre": "edm", "mood": "energetic", "energy": 0.95, "likes_acoustic": True},
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in {**PROFILES, **EDGE_CASE_PROFILES}.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Prints the profile and ranked recommendations in a readable layout."""
    width = 60
    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())

    print()
    print("=" * width)
    print(f"  {name.upper()}: TOP {len(recommendations)} RECOMMENDATIONS")
    print(f"  Profile: {profile}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  #{rank}  {song['title']} - {song['artist']}")
        print(f"      {song['genre']} | {song['mood']} | Score: {score:.2f}")
        print("      Why:")
        for reason in explanation.split("; "):
            print(f"        - {reason}")

    print()
    print("=" * width)


if __name__ == "__main__":
    main()
