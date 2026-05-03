# UI Specification

## Goal

Create a simple Streamlit interface that lets a student enter profile information and receive course recommendations.

The interface should be understandable without extra explanation.

## Page Title

```text
Personalized Elective Course Recommender
```

## Intro Text

Show a short paragraph:

```text
This prototype recommends elective and transferable-skills courses based on your study programme, completed courses, and interests. It uses a simplified content-based recommender with an optional exploration mode to surface niche courses.
```

## Inputs

### Study Programme

Text input.

Default example:

```text
Business Informatics
```

### Completed Courses

Text area.

Default example:

```text
Databases, Software Engineering, Statistics, Project Management
```

### Interests and Learning Goals

Text area.

Default example:

```text
I am interested in sustainability, artificial intelligence, ethics, and communication skills.
```

### Number of Recommendations

Slider from 3 to 10.

Default:

```text
5
```

### Language Filter

Select box:

```text
Any
English
German
```

### University Filter

Select box:

```text
Any
TU Wien
Uni Wien
BOKU
WU
```

### Semester Filter

Select box:

```text
Any
Winter
Summer
Both
```

### Exploration Mode

Select box:

```text
Safe
Balanced
Exploratory
```

Explanation:

- Safe: ranks mostly by content similarity
- Balanced: adds a moderate bonus for niche courses
- Exploratory: gives stronger visibility to less popular courses

## Button

```text
Get recommendations
```

## Output

Display each recommendation as a card or bordered section.

Each recommendation should include:

```text
Rank
Course title
University
ECTS
Language
Semester
Description
Why recommended
Content score
Niche bonus
Final score
```

## Example Output Card

```text
#1 Sustainable Urban Mobility

TU Wien · 3 ECTS · English · Summer

Students learn about sustainable transport systems, urban planning, and climate-friendly mobility concepts.

Why recommended:
Matches your interests in sustainability and climate. This is also a less mainstream course, so it supports exploration beyond the most popular options.

Scores:
Content match: 0.62
Niche bonus: 0.59
Final score: 0.61
```

## Design Requirements

The app should be simple and clean.

Use:

- `st.title`
- `st.write`
- `st.sidebar` or clear input sections
- `st.button`
- `st.markdown`
- `st.expander` if useful

Do not overcomplicate the UI.

## Error Handling

If the dataset is missing, show a clear error.

If no recommendations are found after filtering, show:

```text
No courses matched the selected filters. Try using fewer filters or another exploration mode.
```

If the user leaves all profile fields empty, show a warning:

```text
Please enter at least your study programme or interests.
```

## Optional Nice-to-Have Features

Only implement these after the core app works:

- show a short explanation of the scoring formula
- show a small table of all available courses
- add an option to expand course details
- add a reset button
- show a note that the data is mocked
