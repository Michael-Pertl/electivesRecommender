# Project Brief: Personalized Elective Course Recommender

## Context

We are building a prototype recommender system for a university group project in the course Recommender Systems / Recommender Systems & User Modeling.

The report topic is:

**Personalized Elective Course Recommendations: Navigating Academic Paths in Higher Education**

The system is intended to help students choose elective and transferable-skills courses across Austrian universities such as TU Wien, Universität Wien, BOKU, and WU.

The use case is linked to **SDG 4: Quality Education**.

## Problem

Students often have to choose elective or transferable-skills courses from a large and fragmented pool of courses. Information is spread across several university catalogue systems, and students often rely on friends, hearsay, or convenience rather than informed exploration.

The prototype should demonstrate how a recommender system could help students discover relevant, diverse, and explainable course recommendations.

## Goal of the Prototype

The goal is **not** to build a production-ready recommender system.

The goal is to build a small, runnable, interactive prototype that shows the following flow:

1. A student enters profile information.
2. The system processes the input.
3. The system returns ranked course recommendations.
4. Each recommendation includes a short explanation.

## Target User

The target user is a student who needs to select elective or transferable-skills courses.

Example student:

- Study programme: Business Informatics
- Completed courses: Databases, Software Engineering, Statistics
- Interests: sustainability, artificial intelligence, communication skills
- Wants: course recommendations outside or adjacent to their main field

## Recommendation Task

Given:

1. A student's study programme
2. A list of completed courses
3. A free-text description of interests or learning goals
4. Optional filters such as language, university, semester, and exploration preference

Return:

A ranked list of N elective or transferable-skills courses from a mock course catalogue.

## Method

Use a simplified hybrid recommender.

### Main Component

Use content-based recommendation with TF-IDF and cosine similarity.

Each course is represented by:

- title
- description
- tags

The user profile is represented by:

- study programme
- completed courses
- interest text

The content score is the cosine similarity between the user profile vector and each course vector.

### Re-ranking Component

Add a simple popularity/niche adjustment to avoid recommending only popular courses.

Each course has a mock `popularity` value between 0 and 1.

- High popularity = well-known course
- Low popularity = niche course

The system should support an "exploration mode":

- Safe: mostly content similarity
- Balanced: content similarity plus some niche bonus
- Exploratory: stronger niche bonus

Example scoring:

```python
niche_bonus = 1 - popularity
final_score = (1 - niche_weight) * content_score + niche_weight * niche_bonus
```

## Ethical and Societal Design Requirements

The prototype should reflect the report's reflection section.

### Transparency

Each recommendation should show a short explanation.

Example:

> Recommended because it matches your interests in sustainability and AI, and it is a less mainstream course that may support exploration.

### Cold-start Support

The system should work even if the student has no history. The free-text interest input and study programme should be enough to generate recommendations.

### Popularity-bias Mitigation

The system should not only recommend the most popular courses. The exploration mode should make niche courses more visible.

### User Control

The user should be able to adjust filters and exploration preference.

## Technical Stack

Use Python and Streamlit.

Suggested files:

- `app.py`: Streamlit user interface
- `recommender.py`: recommender logic
- `data/courses.csv`: mock course data
- `requirements.txt`: dependencies
- `run_prototype.sh`: script to run the prototype
- `README_RecSys_Group10.md`: instructions for the teaching team

## Important Constraints

Keep the prototype simple, self-contained, and runnable.

Do not use:

- login
- database
- web scraping
- external APIs
- real student data
- persistent user profiles
- matrix factorization
- user-user collaborative filtering
- item-item collaborative filtering

The prototype should work entirely from the local mock CSV file.
