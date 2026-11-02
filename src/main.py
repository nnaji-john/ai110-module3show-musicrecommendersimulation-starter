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


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Default taste profile: upbeat pop listener
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(user_prefs, recommendations)


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Prints the profile and ranked recommendations in a readable layout."""
    width = 60
    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())

    print()
    print("=" * width)
    print(f"  TOP {len(recommendations)} RECOMMENDATIONS")
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
