# Implementation Plan

## Objective

Build a Streamlit prototype for a personalized elective course recommender.

The implementation should be simple, readable, and robust.

## Required Files

```text
app.py
recommender.py
requirements.txt
run_prototype.sh
README_RecSys_Group10.md
data/courses.csv
```

## Step 1: Create Mock Dataset

Create `data/courses.csv`.

It should contain around 30 to 60 mock elective or transferable-skills courses.

Required columns:

```csv
course_id,title,university,ects,language,semester,description,tags,popularity
```

Column details:

- `course_id`: unique integer or string
- `title`: course title
- `university`: one of `TU Wien`, `Uni Wien`, `BOKU`, `WU`
- `ects`: number, e.g. 3, 4, 6
- `language`: `English` or `German`
- `semester`: `Winter`, `Summer`, or `Both`
- `description`: realistic short course description
- `tags`: comma-separated keywords
- `popularity`: float between 0 and 1

The dataset should include courses from different areas:

- AI and data
- sustainability
- communication
- entrepreneurship
- psychology
- ethics
- law
- design
- climate
- economics
- urban planning
- language/intercultural skills
- health
- project management

## Step 2: Implement `recommender.py`

Create a class called `CourseRecommender`.

Expected behavior:

```python
recommender = CourseRecommender("data/courses.csv")

results = recommender.recommend(
    study_program="Business Informatics",
    completed_courses="Databases, Software Engineering, Statistics",
    interests="I am interested in sustainability, AI, and communication skills.",
    top_n=5,
    language="Any",
    university="Any",
    semester="Any",
    exploration_mode="Balanced"
)
```

The returned result should be a pandas DataFrame.

## Required Methods

### `__init__(self, courses_path: str)`

- Load the CSV file.
- Validate required columns.
- Create a combined text field from title, description, and tags.
- Fit a TF-IDF vectorizer on the course text.
- Store the course TF-IDF matrix.

### `recommend(...)`

Inputs:

- `study_program`
- `completed_courses`
- `interests`
- `top_n`
- `language`
- `university`
- `semester`
- `exploration_mode`

Behavior:

1. Build a user profile text from study programme, completed courses, and interests.
2. Transform the user profile with the existing TF-IDF vectorizer.
3. Compute cosine similarity against all courses.
4. Compute niche bonus as `1 - popularity`.
5. Set niche weight based on exploration mode:
   - Safe: `0.00`
   - Balanced: `0.15`
   - Exploratory: `0.30`
6. Compute final score:
   ```python
   final_score = (1 - niche_weight) * content_score + niche_weight * niche_bonus
   ```
7. Apply filters:
   - language, unless `Any`
   - university, unless `Any`
   - semester, unless `Any`
8. Exclude completed courses if their title appears in the completed courses text.
9. Sort by final score descending.
10. Return top N results.
11. Add an explanation string for each result.

### `generate_explanation(...)`

Create a short explanation using:

- top matching tags
- content score
- niche bonus
- exploration mode

Example explanation:

> Recommended because it matches your interests in AI, data, and ethics. It is also a less mainstream option, which supports exploration beyond the most popular courses.

## Step 3: Implement `app.py`

Build a Streamlit interface.

Required UI elements:

### Sidebar or Input Section

- Study programme text input
- Completed courses text area
- Interest / learning goals text area
- Number of recommendations slider
- Language filter
- University filter
- Semester filter
- Exploration mode select box:
  - Safe
  - Balanced
  - Exploratory

### Output Section

When the user clicks "Get recommendations", display recommended courses as cards or clearly separated sections.

Each card should show:

- rank
- course title
- university
- ECTS
- language
- semester
- description
- explanation
- content score
- niche bonus
- final score

Also include a short explanation of what the exploration mode means.

## Step 4: Add Requirements

Create `requirements.txt` with:

```txt
streamlit
pandas
scikit-learn
numpy
```

## Step 5: Add Run Script

Create `run_prototype.sh`:

```bash
#!/usr/bin/env bash
set -e

python -m pip install -r requirements.txt
streamlit run app.py
```

Make it executable if possible:

```bash
chmod +x run_prototype.sh
```

## Step 6: Add README

Create `README_RecSys_Group10.md`.

It should explain:

- project purpose
- how to run
- how to use the interface
- what data is mocked
- what simplifications were made
- how ethical/societal aspects are represented
- AI usage disclosure placeholder

## Step 7: Manual Test Cases

After implementation, test at least these examples.

### Test Case 1: Business Informatics Student

Input:

- Study programme: Business Informatics
- Completed courses: Databases, Software Engineering, Statistics
- Interests: sustainability, AI, ethics, communication

Expected:

- Courses related to AI, ethics, sustainability, communication, or interdisciplinary topics should appear.

### Test Case 2: Sustainability-oriented Student

Input:

- Study programme: Environmental Engineering
- Completed courses: Ecology, Environmental Systems
- Interests: climate, cities, mobility, policy

Expected:

- Courses related to climate, sustainability, urban planning, and policy should appear.

### Test Case 3: Empty Filters

Use `Any` for all filters.

Expected:

- The app should return recommendations without errors.

### Test Case 4: Overly Strict Filters

Choose filters that may return no courses.

Expected:

- The app should show a clear message instead of crashing.
