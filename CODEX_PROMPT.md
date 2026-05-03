# Prompt for Codex

Read the following files first:

- `PROJECT_BRIEF.md`
- `IMPLEMENTATION_PLAN.md`
- `DATA_SPEC.md`
- `UI_SPEC.md`
- `README_RecSys_Group10.md`

Then implement the prototype described there.

Create the following files if they do not exist:

- `app.py`
- `recommender.py`
- `requirements.txt`
- `run_prototype.sh`
- `data/courses.csv`

Use Python, Streamlit, pandas, scikit-learn, and numpy.

Keep the implementation simple and self-contained.

Do not use:

- external APIs
- databases
- scraping
- login
- persistent storage
- real student data

The app should:

1. Load the mock course data from `data/courses.csv`.
2. Let the user enter study programme, completed courses, and interests.
3. Let the user choose filters for language, university, semester, and exploration mode.
4. Compute TF-IDF cosine similarity between the user profile and course descriptions.
5. Re-rank using a niche bonus based on simulated popularity.
6. Display ranked course recommendations with explanations and scores.
7. Handle missing data and empty results gracefully.

After implementation, make sure the app can be launched with:

```bash
bash run_prototype.sh
```

After coding, briefly summarize what was implemented and mention any assumptions.
