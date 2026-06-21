# Personalized Elective Course Recommender — Group 10

## Project Overview

This prototype demonstrates a recommender system for elective and transferable-skills courses in higher education.

The system is designed for students who need to choose courses from a large and fragmented pool of offerings across Austrian universities. It supports Sustainable Development Goal 4: Quality Education by helping students make more informed and personally meaningful course choices.

## What the Prototype Does

The user enters:

- study programme
- completed courses
- personal interests or learning goals
- optional filters such as language, university, and semester
- exploration preference

The system returns a ranked list of recommended elective courses.

Each recommendation includes a short explanation of why it was suggested.

## Recommendation Approach

The prototype uses a simplified hybrid approach.

The main component is content-based recommendation:

- Course texts are built from title, description, and tags.
- User profile text is built from study programme, completed courses, and interests.
- TF-IDF is used to vectorize the texts.
- Cosine similarity is used to compute the content match.

A simple re-ranking component is added to reduce popularity bias:

```python
niche_bonus = 1 - popularity
final_score = (1 - niche_weight) * content_score + niche_weight * niche_bonus
```

The user can choose between three exploration modes:

- Safe: mostly content similarity
- Balanced: moderate niche-course bonus
- Exploratory: stronger niche-course bonus

## Data

The prototype uses a mock course catalogue stored in:

```text
data/courses.csv
```

The data is simulated and does not represent real university enrolment data.

The mock data includes:

- course title
- university
- ECTS
- language
- semester
- description
- tags
- simulated popularity score

## How to Run

### Option 1: Run with Windows demo launcher

From PowerShell or Command Prompt:

```powershell
.\start_demo.cmd
```

This creates a local Windows virtual environment on first run, installs dependencies if needed, and starts the Streamlit app.

### Option 2: Run with bash script

```bash
bash run_prototype.sh
```

### Option 3: Run manually

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the app:

```bash
streamlit run app.py
```

## How to Use

1. Open the Streamlit app.
2. Enter your study programme.
3. Enter completed courses.
4. Describe your interests or learning goals.
5. Optionally select filters.
6. Choose an exploration mode.
7. Click `Get recommendations`.
8. Review the ranked course cards and explanations.

## Simplifications

This is a prototype, not a production system.

The following aspects are simplified:

- Course data is mocked.
- User profiles are not stored.
- There is no login.
- There is no real enrolment history.
- Collaborative filtering is not implemented.
- Popularity values are simulated.
- Timetable conflicts and credit recognition are not checked.
- Cross-university catalogue integration is assumed to be preprocessed.

## Ethical and Societal Considerations

The prototype reflects several concerns from the project report.

### Transparency

Each recommendation includes a short explanation.

### Cold Start

The system works without prior user history because it uses explicit user input.

### Popularity Bias

The exploration mode can increase the visibility of niche courses.

### User Control

Users can adjust filters and exploration level.

## AI Usage Disclosure

Generative AI tools were used to support the implementation and structuring of the prototype.

Models/tools used:

- ChatGPT
- Codex

AI was used for:

- implementation planning
- code scaffolding
- README drafting
- debugging support

All generated code and text should be reviewed and adapted by the group before submission.
