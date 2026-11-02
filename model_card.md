# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
