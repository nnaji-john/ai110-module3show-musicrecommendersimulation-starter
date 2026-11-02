# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TuneJudge 1.0**

It "judges" every song in the catalog and gives it points, like a judge scoring contestants.

---

## 2. Intended Use  

**Goal:** TuneJudge suggests 5 songs a user will probably like. It doesn't predict exact ratings. It ranks songs by how well they match what the user says they want.

**How it works for the user:** The user gives a favorite genre, a favorite mood, a target energy level (0 to 1), and optionally whether they like acoustic music. The system returns the top 5 songs, each with the reasons it was picked.

**Assumptions:** It assumes the user knows their taste and can describe it with one genre and one mood. It also assumes the song labels are accurate.

**Intended use:**
- Classroom exploration of how recommender systems work.
- Seeing how changing weights or preferences changes the results.
- Learning about bias in simple scoring systems.

**Not intended for:**
- Real users or a real music app. The catalog has only 20 made-up songs.
- Making decisions about real artists, such as which songs get promoted.
- Users whose taste mixes several genres or moods. The system can only handle one of each.
- Any situation where fairness matters. The system favors genres that have more songs in the catalog.

---

## 3. How the Model Works  

The recommender works like a judge giving points. The user describes what they like: a favorite genre, a favorite mood, how energetic they want the music to be (from 0 = very calm to 1 = very intense), and optionally whether they prefer acoustic or electronic sound.

The system then looks at every song in the catalog, one at a time, and awards points:

- **2 points** if the song is the user's favorite genre.
- **1.5 points** if the song has the user's favorite mood.
- **Up to 2 points** for energy, depending on how *close* the song's energy is to what the user wants. A song with exactly the right energy gets the full 2 points, and a song that is far off gets very few. This means a user who wants calm music is rewarded with calm songs, not just the loudest ones.
- **Up to 1 point** for sound, if the user said whether they like acoustic music. Acoustic songs earn more for acoustic fans, and electronic songs earn more for everyone else.

After every song has a score, the system sorts them from highest to lowest and shows the top 5. Each recommendation comes with a list of reasons, such as "genre match" or "energy close to your target," and how many points each one was worth, so the user can see exactly why a song was picked.

Genre is worth the most because getting the wrong genre usually feels like the biggest mistake. Mood comes next because it captures the feeling of a song in a way the numbers can't. Energy matters a lot too, and it decides the order once genre and mood stop matching.

**Changes from the starter logic:** the starter code simply returned the first few songs in the file with no scoring. I replaced it with the point system above, added explanations for every score, and added a tie-breaker so the same profile always gets the same results in the same order.

---

## 4. Data  

- **Size:** 20 songs in `data/songs.csv`. The starter file had 10. I added 10 more to cover genres and moods that were missing.
- **Features per song:** title, artist, genre, mood, energy, tempo (BPM), valence (how positive it sounds), danceability, and acousticness. The number features run from 0 to 1, except tempo.
- **Genres (17):** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, country, classical, metal, r&b, edm, reggae, folk, blues, latin.
- **Moods (16):** happy, chill, intense, relaxed, moody, focused, confident, nostalgic, peaceful, angry, romantic, energetic, uplifting, sad, melancholic, playful.

**Limits:**
- It's very small. 16 of the 17 genres have only one or two songs.
- The songs and artists are made up. The labels and numbers were assigned by hand, not measured from real audio.
- There are no songs with energy between 0.60 and 0.75.
- There are no loud acoustic songs and no energetic sad songs.
- Lyrics, vocals, language, popularity, and release year are all missing.
- There is no listening history from real users, so the system can't learn from what people actually play or skip.

---

## 5. Strengths  

- **It works best when a genre has several songs.** The Chill Lofi profile got the best list: three lofi songs, then a chill ambient song.
- **It clearly separates opposite tastes.** Pop and lofi users got completely different lists. Rock and lofi users got opposite scores for the same songs.
- **Energy closeness works well.** Calm users get calm songs and loud users get loud songs. It doesn't just favor the loudest music.
- **The #1 pick usually feels right.** For every normal profile, the top song matched the genre, the mood, and the energy.
- **It explains itself.** Every song comes with the reasons and points behind its score, so it's easy to see why it was picked.
- **It's consistent.** The same profile always gets the same results.

---

## 6. Limitations and Bias 

The biggest weakness I found is that most users get only one or two real matches, and the rest of their list is filled with whatever songs are loudest. Sixteen of the seventeen genres in the catalog have only one or two songs. Once the genre and mood matches run out, songs are ranked almost entirely by energy, and only four songs have energy above 0.9. Because of this, Gym Hero, an upbeat pop workout song, showed up in 5 of my 7 test profiles, including the rock, sad folk, and EDM lists, without ever being the best match. Lofi listeners are treated better than everyone else simply because the catalog has three lofi songs, so the system unintentionally favors users whose taste happens to be well represented in the data.

---

## 7. Evaluation  

I ran the recommender with three standard profiles and four adversarial ("edge case") profiles designed to trick the scoring logic. All profiles are defined in `src/main.py`, and the output below comes from `python -m src.main`.

| Profile | Genre | Mood | Energy | Acoustic? | What it tests |
|---|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.8 | not set | A normal, upbeat listener |
| Chill Lofi | lofi | chill | 0.35 | yes | A calm listener, the opposite of pop |
| Deep Intense Rock | rock | intense | 0.9 | no | A loud listener with only one matching song |
| Conflicting: High-Energy Sad | folk | sad | 0.9 | not set | Preferences that contradict each other |
| Wrong Case | Pop | Happy | 0.8 | not set | The same as High-Energy Pop, but with capital letters |
| Out of Range Energy | classical | peaceful | 1.5 | not set | An impossible energy value |
| Acoustic EDM Fan | edm | energetic | 0.95 | yes | A sound preference that no loud song can satisfy |

### Standard profiles

#### High-Energy Pop

```
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

**Observation:** As expected. Sunrise City matches everything and wins clearly. Rooftop Lights (indie pop) gets no genre credit because only exact genre names count.

#### Chill Lofi

```
============================================================
  CHILL LOFI: TOP 5 RECOMMENDATIONS
  Profile: genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
============================================================

  #1  Library Rain - Paper Lanterns
      lofi | chill | Score: 6.36
      Why:
        - genre match: lofi (+2.00)
        - mood match: chill (+1.50)
        - energy 0.35 vs target 0.35 (+2.00)
        - acoustic fit (+0.86)

  #2  Midnight Coding - LoRoom
      lofi | chill | Score: 6.07
      Why:
        - genre match: lofi (+2.00)
        - mood match: chill (+1.50)
        - energy 0.42 vs target 0.35 (+1.86)
        - acoustic fit (+0.71)

  #3  Focus Flow - LoRoom
      lofi | focused | Score: 4.68
      Why:
        - genre match: lofi (+2.00)
        - energy 0.40 vs target 0.35 (+1.90)
        - acoustic fit (+0.78)

  #4  Spacewalk Thoughts - Orbit Bloom
      ambient | chill | Score: 4.28
      Why:
        - mood match: chill (+1.50)
        - energy 0.28 vs target 0.35 (+1.86)
        - acoustic fit (+0.92)

  #5  Coffee Shop Stories - Slow Stereo
      jazz | relaxed | Score: 2.85
      Why:
        - energy 0.37 vs target 0.35 (+1.96)
        - acoustic fit (+0.89)

============================================================
```

**Observation:** As expected. The two lofi/chill songs are at the top, and Spacewalk Thoughts (ambient, chill) is a sensible #4. This profile works best because the catalog has three lofi songs.

#### Deep Intense Rock

```
============================================================
  DEEP INTENSE ROCK: TOP 5 RECOMMENDATIONS
  Profile: genre=rock, mood=intense, energy=0.9, likes_acoustic=False
============================================================

  #1  Storm Runner - Voltline
      rock | intense | Score: 6.38
      Why:
        - genre match: rock (+2.00)
        - mood match: intense (+1.50)
        - energy 0.91 vs target 0.90 (+1.98)
        - acoustic fit (+0.90)

  #2  Gym Hero - Max Pulse
      pop | intense | Score: 4.39
      Why:
        - mood match: intense (+1.50)
        - energy 0.93 vs target 0.90 (+1.94)
        - acoustic fit (+0.95)

  #3  Neon Pulse - Volt Theory
      edm | energetic | Score: 2.88
      Why:
        - energy 0.95 vs target 0.90 (+1.90)
        - acoustic fit (+0.98)

  #4  Iron Furnace - Grave Signal
      metal | angry | Score: 2.83
      Why:
        - energy 0.97 vs target 0.90 (+1.86)
        - acoustic fit (+0.97)

  #5  Sunrise City - Neon Echo
      pop | happy | Score: 2.66
      Why:
        - energy 0.82 vs target 0.90 (+1.84)
        - acoustic fit (+0.82)

============================================================
```

**Observation:** Storm Runner is a clear #1, but there is only one rock song. After that, the list is filled by energy alone. Gym Hero (upbeat pop) ranks above Iron Furnace (metal), which a rock fan would probably prefer.

### Adversarial / edge-case profiles

#### Conflicting: High-Energy Sad

```
============================================================
  CONFLICTING: HIGH-ENERGY SAD: TOP 5 RECOMMENDATIONS
  Profile: genre=folk, mood=sad, energy=0.9
============================================================

  #1  Rainy Window Letters - Hazel Pines
      folk | sad | Score: 4.20
      Why:
        - genre match: folk (+2.00)
        - mood match: sad (+1.50)
        - energy 0.25 vs target 0.90 (+0.70)

  #2  Storm Runner - Voltline
      rock | intense | Score: 1.98
      Why:
        - energy 0.91 vs target 0.90 (+1.98)

  #3  Gym Hero - Max Pulse
      pop | intense | Score: 1.94
      Why:
        - energy 0.93 vs target 0.90 (+1.94)

  #4  Neon Pulse - Volt Theory
      edm | energetic | Score: 1.90
      Why:
        - energy 0.95 vs target 0.90 (+1.90)

  #5  Iron Furnace - Grave Signal
      metal | angry | Score: 1.86
      Why:
        - energy 0.97 vs target 0.90 (+1.86)

============================================================
```

**Observation:** **The labels beat the numbers.** The only sad folk song wins even though its energy (0.25) is the opposite of what the user asked for (0.9), because genre + mood (3.5 points) outweighs a big energy miss. Places #2–#5 are all loud, intense songs with no sadness at all. The system can't find "energetic but sad" music, and the dataset has none.

#### Wrong Case: 'Pop' / 'Happy'

```
============================================================
  WRONG CASE: 'POP' / 'HAPPY': TOP 5 RECOMMENDATIONS
  Profile: genre=Pop, mood=Happy, energy=0.8
============================================================

  #1  Fuego Lento - Sol y Luna
      latin | playful | Score: 2.00
      Why:
        - energy 0.80 vs target 0.80 (+2.00)

  #2  Sunrise City - Neon Echo
      pop | happy | Score: 1.96
      Why:
        - energy 0.82 vs target 0.80 (+1.96)

  #3  Concrete Crown - Kilo Verse
      hip hop | confident | Score: 1.96
      Why:
        - energy 0.78 vs target 0.80 (+1.96)

  #4  Rooftop Lights - Indigo Parade
      indie pop | happy | Score: 1.92
      Why:
        - energy 0.76 vs target 0.80 (+1.92)

  #5  Night Drive Loop - Neon Echo
      synthwave | moody | Score: 1.90
      Why:
        - energy 0.75 vs target 0.80 (+1.90)

============================================================
```

**Observation:** **Tricked by capital letters.** "Pop" doesn't equal "pop," so no genre or mood points are awarded. Sunrise City, the perfect match, drops to #2 behind a latin song. Labels should be compared in lowercase.

#### Out of Range Energy (1.5)

```
============================================================
  OUT OF RANGE ENERGY (1.5): TOP 5 RECOMMENDATIONS
  Profile: genre=classical, mood=peaceful, energy=1.5
============================================================

  #1  Moonlit Sonata No. 3 - Clara Wren
      classical | peaceful | Score: 2.86
      Why:
        - genre match: classical (+2.00)
        - mood match: peaceful (+1.50)
        - energy 0.18 vs target 1.50 (+-0.64)

  #2  Iron Furnace - Grave Signal
      metal | angry | Score: 0.94
      Why:
        - energy 0.97 vs target 1.50 (+0.94)

  #3  Neon Pulse - Volt Theory
      edm | energetic | Score: 0.90
      Why:
        - energy 0.95 vs target 1.50 (+0.90)

  #4  Gym Hero - Max Pulse
      pop | intense | Score: 0.86
      Why:
        - energy 0.93 vs target 1.50 (+0.86)

  #5  Storm Runner - Voltline
      rock | intense | Score: 0.82
      Why:
        - energy 0.91 vs target 1.50 (+0.82)

============================================================
```

**Observation:** **Bug: negative points.** Energy is supposed to be 0–1, but nothing stops a value of 1.5. Moonlit Sonata gets **−0.64** energy points (shown as "+-0.64"). It still wins on labels, and the rest of the list is just the loudest songs. Energy targets should be limited to the 0–1 range, or points should never go below 0.

#### Acoustic EDM Fan

```
============================================================
  ACOUSTIC EDM FAN: TOP 5 RECOMMENDATIONS
  Profile: genre=edm, mood=energetic, energy=0.95, likes_acoustic=True
============================================================

  #1  Neon Pulse - Volt Theory
      edm | energetic | Score: 5.52
      Why:
        - genre match: edm (+2.00)
        - mood match: energetic (+1.50)
        - energy 0.95 vs target 0.95 (+2.00)
        - acoustic fit (+0.02)

  #2  Storm Runner - Voltline
      rock | intense | Score: 2.02
      Why:
        - energy 0.91 vs target 0.95 (+1.92)
        - acoustic fit (+0.10)

  #3  Gym Hero - Max Pulse
      pop | intense | Score: 2.01
      Why:
        - energy 0.93 vs target 0.95 (+1.96)
        - acoustic fit (+0.05)

  #4  Fuego Lento - Sol y Luna
      latin | playful | Score: 2.00
      Why:
        - energy 0.80 vs target 0.95 (+1.70)
        - acoustic fit (+0.30)

  #5  Iron Furnace - Grave Signal
      metal | angry | Score: 1.99
      Why:
        - energy 0.97 vs target 0.95 (+1.96)
        - acoustic fit (+0.03)

============================================================
```

**Observation:** **The acoustic preference is almost ignored.** It's worth only up to 1 point, and loud songs are rarely acoustic, so this user simply gets loud electronic music. Places #2–#5 are within 0.03 points of each other, which shows how close to a tie the ranking gets once labels stop matching.

### Summary of what surprised me

- Genre and mood labels together (3.5 points) usually outweigh any energy difference, so a song can win while sounding nothing like what the user asked for.
- Small input mistakes, like capital letters or an energy value above 1, quietly break the results instead of causing an error.
- Once genre and mood stop matching, many songs end up within a few hundredths of a point of each other, so the order is almost arbitrary.
- The two automated tests in `tests/test_recommender.py` pass, but they only check the "happy path." None of the problems above are caught by tests.

### Comparing profiles side by side

- **High-Energy Pop vs. Chill Lofi:** Their top 5 lists have no songs in common. The pop profile gets bright, energetic songs (energy 0.76–0.93), while the lofi profile shifts to quiet, acoustic songs (energy 0.28–0.42). This makes sense because the two users asked for opposite energy levels, and the lofi user also asked for acoustic sound.
- **Chill Lofi vs. Deep Intense Rock:** These are complete opposites. Storm Runner scores 6.38 for the rock fan but under 1 point for the lofi fan, and Library Rain is the reverse. Every feature (genre, mood, energy, and sound) points in the opposite direction, so the system separates them easily.
- **High-Energy Pop vs. Deep Intense Rock:** Both lists include Gym Hero and Sunrise City. Both users want loud music, and once their genre matches run out, the same loud songs fill the remaining spots. This shows that energy alone can't tell "happy loud" from "dark loud."
- **High-Energy Pop vs. Wrong Case:** These two users asked for exactly the same thing, only typed differently. Sunrise City drops from 5.46 points (#1) to 1.96 points (#2). This does **not** make sense to a person. It's a weakness in how the system compares words, not a real difference in taste.
- **Deep Intense Rock vs. Conflicting High-Energy Sad:** Both users want energy around 0.9, and both lists contain the same four loud songs: Storm Runner, Gym Hero, Neon Pulse, and Iron Furnace. The only difference is that each profile has one song that matches its labels (Storm Runner for rock, Rainy Window Letters for sad folk), and that song goes to #1. The sad listener ends up with a list of intense songs, which shows that the system fills the gaps with energy instead of mood.
- **Chill Lofi vs. Out of Range Energy:** Both users ask for calm genres (lofi; classical with a "peaceful" mood), but the lofi fan gets quiet songs, while the classical fan gets metal, EDM, pop, and rock in places #2–#5. An energy of 1.5 is read as "louder than the loudest song," so the system recommends the loudest music. The math is consistent, but the result is the opposite of what a "peaceful" listener wants.
- **Deep Intense Rock vs. Acoustic EDM Fan:** Switching the acoustic preference from "no" to "yes" barely changes the list. Storm Runner, Gym Hero, and Iron Furnace appear in both. The catalog has no loud acoustic songs, so for an acoustic fan every loud song earns almost no acoustic points (0.02–0.10). Since they all lose about the same amount, their order hardly changes.

### Why does "Gym Hero" keep showing up for people who want happy pop?

The recommender works like a checklist that hands out points. For a happy pop listener, Gym Hero ticks the "pop" box (2 points) and is about as energetic as the user wants (1.74 points), for 3.74 total. It doesn't tick the "happy" box because it's labeled "intense," but the system never *takes away* points for the wrong mood. It just doesn't add any. Meanwhile, Rooftop Lights is a happy song, but it's labeled "indie pop" instead of "pop," so it misses the 2-point genre box and scores only 3.42. The result: a gym workout song beats a genuinely happy song because of how one song was labeled. Gym Hero also shows up on the rock, sad, and EDM lists because it's one of only four songs with energy above 0.9, so any user who asks for loud music will see it.

### Experiment: doubling energy, halving genre

To test how sensitive the system is, I temporarily changed the weights from genre 2.0 / energy 2.0 to **genre 1.0 / energy 4.0**, then reran all seven profiles.

- **High-Energy Pop got better.** Rooftop Lights (happy, indie pop) moved above Gym Hero (intense pop), which matches the "happy" request better.
- **Deep Intense Rock didn't change at all.** Neither Gym Hero nor Iron Furnace matches the rock genre, so changing the genre weight couldn't fix their order.
- **Conflicting High-Energy Sad got worse.** Storm Runner, an intense rock song, became #1 for a user who asked for sad folk music.
- **Out of Range Energy got worse.** The negative energy points doubled, and the only classical song fell out of the top 5 entirely.

Overall, the change made the results **different, not more accurate**. With energy worth more than half of the possible points, the system mostly asks "how loud is this song?" and ignores what the user said they like. I switched back to the original balanced weights.

---

## 8. Future Work  

1. **Fix the input bugs.** Compare genres and moods in lowercase so "Pop" matches "pop". Keep energy targets between 0 and 1 so a song can never get negative points.
2. **Give partial credit for related labels.** Rock and metal, or pop and indie pop, should count as close matches. The same goes for moods like happy and playful, or intense and angry.
3. **Add a valence (bright vs. dark) preference.** This would keep happy songs like Sunrise City off a dark rock list. It would also let the system tell upbeat workout music from heavy, dark music.

Other ideas: add more songs so every genre has several options, let users pick more than one genre, and limit each artist to one song in the top 5 for more variety.

---

## 9. Personal Reflection  

I learned that a recommender is really two steps: scoring each song, then ranking the list. Even a simple point system can give results that feel smart when the data is good.

The biggest surprise was how much the data matters. Most of the problems I found didn't come from the math. They came from having only one or two songs per genre. Gym Hero kept showing up in lists where it didn't belong, just because it's one of the few loud songs.

I was also surprised how easy it was to trick the system. Capital letters or an impossible energy value broke the results without any error.

This changed how I think about apps like Spotify. When a weird song shows up in a recommendation list, it might not mean the app misunderstood the listener. It might just mean there wasn't a better match, or that the song was labeled in a way that happened to fit. Real apps also use what millions of other people listen to, which my content-only system can't do.  
