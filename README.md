# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube combine two approaches. **Collaborative filtering** recommends what similar users liked, based on behavior such as plays, skips, likes, and playlist adds. **Content-based filtering** recommends songs whose attributes, such as genre, mood, tempo, and energy, are similar to what you already enjoy. Big platforms mix both and use huge amounts of listening data to rank results. My version is a simple **content-based** recommender because the dataset only has song attributes and no other users. It prioritizes **genre** first, then **mood**, then how close a song's **energy** is to what the user wants, with a smaller bonus for matching the user's taste for acoustic or electronic sound.

**`Song` features**

- `genre` (e.g. pop, lofi, rock), used for genre matching
- `mood` (e.g. happy, chill, intense), used for mood matching
- `energy` (0–1), compared to the user's target energy
- `acousticness` (0–1), compared to the user's acoustic preference
- `id`, `title`, `artist`, `tempo_bpm`, `valence`, `danceability`: stored for display and future use, but not scored. Tempo, danceability, and acousticness mostly rise and fall with energy, so scoring all of them would count the same thing several times.

**`UserProfile` features**

- `favorite_genre`
- `favorite_mood`
- `target_energy` (0–1)
- `likes_acoustic` (True / False)

### Data Flow Plan

```
INPUT                      PROCESS (the loop)                    OUTPUT (the ranking)
data/songs.csv             for each song in the catalog:         sort all songs by score
  → load_songs()             score_song(user_prefs, song)          (highest first,
  → list of song dicts         genre, mood, energy, acoustic        ties → lower id)
user_prefs (main.py)         → (score, reasons)                  keep top k
                                                                 print title, score, reasons
```

Example: for a rock/intense user with target energy 0.9, Storm Runner earns 2.0 (genre) + 1.5 (mood) + 1.98 (energy) + 0.90 (acoustic) = **6.38** and ranks #1.

### Algorithm Recipe (finalized)

**Step 1: Scoring Rule (judges one song at a time)**

| Rule | Points |
|---|---|
| Genre matches | +2.0 |
| Mood matches | +1.5 |
| Energy closeness | 2.0 × (1 − \|song energy − target energy\|) |
| Acoustic fit | acousticness if the user likes acoustic, otherwise 1 − acousticness (up to +1.0) |

Energy is scored by *closeness*, so a user who wants calm music is rewarded with low-energy songs instead of the loudest ones. Genre is worth more than mood because a wrong genre feels like a bigger miss, and mood already partly overlaps with energy.

**Choosing the mood weight.** I compared a mood weight of 1.0 against 1.5 using four test profiles: rock/intense, lofi/chill, pop/happy, and folk/sad. The top 5 songs came out in the same order both times. I kept **1.5** so that a song matching the user's mood and energy, like Rooftop Lights for a pop/happy user (3.42), clearly beats a song that only matches on energy, like Fuego Lento (2.00). Genre is still worth more than mood (2.0 vs 1.5), so if two songs have similar energy and sound, the genre match wins.

**Step 2: Ranking Rule (compares the whole list)**

Every song is scored, the list is sorted from highest to lowest score (ties are broken by song id), and the top *k* songs are returned with an explanation of where their points came from.

### Expected Biases and Limitations

- **Genre can be over-prioritized.** A genre match is the single biggest reward, so a song in the right genre with the wrong feel can beat a great song in a related genre. For a rock/intense user, Gym Hero (pop, intense) ranks above Iron Furnace (metal, angry), even though metal is much closer to what a rock fan probably wants.
- **Exact matching ignores similar labels.** "indie pop" gets no credit for a "pop" fan, "playful" gets none for "happy," and "angry" gets none for "intense." Good songs are missed just because of how they were labeled.
- **The catalog is unbalanced.** There are three lofi songs but only one rock song, and most genres have just one. Lofi fans get several strong matches, while a rock fan gets one, and the rest of their list is filled by energy alone.
- **Energy takes over when nothing else matches.** After the genre and mood matches run out, songs are ranked mostly by energy, so the bottom of the list can mix very different styles like EDM, metal, and hip hop.
- **No bright-vs-dark preference.** Valence isn't scored, so the system can't tell upbeat intense music (Gym Hero) from dark intense music (Storm Runner).
- **Subjective labels.** Genre and mood labels were assigned by people. Someone else might label the same song differently, and the system trusts the labels completely.
- **No variety or discovery.** The same profile always gets the exact same list, so users are never pushed outside their stated taste.

### Reflection: Do energy and valence capture a song's "vibe"?

Mostly, yes. When I think about how a song feels, two questions come first: is it calm or intense, and is it bright or dark? Energy and valence measure exactly those. In the dataset, Sunrise City (high energy, high valence) feels like an upbeat morning song, and Library Rain (low energy, medium valence) feels like quiet background music. The numbers match what I'd expect.

They aren't the whole story, though. Focus Flow and Midnight Coding have almost identical energy and valence, but one is labeled "focused" and the other "chill." That tells me part of a vibe comes from what you're *doing* while you listen, like studying or relaxing, rather than from the sound alone. Also, Gym Hero and Storm Runner are both "intense," but Gym Hero feels like motivating workout music and Storm Runner feels darker and heavier. Energy treats them the same, and only valence and genre separate them.

Some things the data can't capture at all: whether a song has vocals, what the lyrics are about, and personal memories tied to a song. Two people can hear the same track and describe its vibe completely differently.

Because of this, my recommender uses energy as the main numeric feature but also gives weight to the mood label. Valence would be a good next feature to add. A simple formula like this can only approximate a vibe, not fully understand it.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` with the default pop/happy profile:

```
Loading songs from data/songs.csv...
Loaded songs: 20

============================================================
  HIGH-ENERGY POP: TOP 5 RECOMMENDATIONS
  Profile: genre=pop, mood=happy, energy=0.8
============================================================

  #1  Sunrise City - Neon Echo
      pop | happy | Score: 5.46
      Why:
        - genre match: pop (+2.00)
        - mood match: happy (+1.50)
        - energy 0.82 vs target 0.80 (+1.96)

  #2  Gym Hero - Max Pulse
      pop | intense | Score: 3.74
      Why:
        - genre match: pop (+2.00)
        - energy 0.93 vs target 0.80 (+1.74)

  #3  Rooftop Lights - Indigo Parade
      indie pop | happy | Score: 3.42
      Why:
        - mood match: happy (+1.50)
        - energy 0.76 vs target 0.80 (+1.92)

  #4  Fuego Lento - Sol y Luna
      latin | playful | Score: 2.00
      Why:
        - energy 0.80 vs target 0.80 (+2.00)

  #5  Concrete Crown - Kilo Verse
      hip hop | confident | Score: 1.96
      Why:
        - energy 0.78 vs target 0.80 (+1.96)

============================================================
```

These results match what I expected. Sunrise City is the only song that is pop, happy, and close to 0.8 energy, so it wins by a wide margin. Gym Hero and Rooftop Lights each match one category (genre or mood) and have energy close to 0.8, so they come next. Songs #4 and #5 match nothing by label and are ranked only by energy. One surprise is that Rooftop Lights (indie pop) gets no genre points, because the system only counts exact genre matches.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



