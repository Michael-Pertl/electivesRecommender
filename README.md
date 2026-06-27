# Personalized Elective Course Recommender

Student prototype for a recommendation system that suggests elective and transferable-skills courses from a mock university catalogue.

The application is built with Streamlit and a small content-based recommender. It is intended as a transparent prototype, not as a production enrolment or credit-recognition system.

## Features

- Free-text student profile with study programme, completed courses, and interests
- Top-N elective course recommendations
- Language, university, and semester filters
- Safe, Balanced, and Exploratory ranking modes
- Short explanation and score components for every recommendation
- Static HTML demo for quick review without installing Python packages

## Repository Structure

```text
.
├── app.py                         # Streamlit user interface
├── recommender.py                 # Recommendation logic
├── data/courses.csv               # Mock course catalogue
├── DATA_SPEC.md                   # Data documentation
├── tests/                         # Unit tests for recommender behavior
├── prototype_static.html          # Static demo export
├── index.html                     # Redirect to static demo
├── run_prototype.sh               # Streamlit launcher
├── start_demo.sh / start_demo.cmd # Static demo launchers
├── requirements.txt               # Runtime dependencies
├── requirements-dev.txt           # Test dependencies
└── pyproject.toml                 # Python project metadata and pytest config
```

The `models/` and `results/` directories are included as placeholders for course-template submissions that expect these folders. This prototype currently does not train or persist a model.

## Quick Start

### Static Demo

The static prototype does not require dependency installation:

```bash
./start_demo.sh
```

On Windows:

```powershell
.\start_demo.cmd
```

Then open `http://localhost:8600/`.

### Streamlit App

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Alternatively, use the launcher:

```bash
bash run_prototype.sh
```

## Testing

Install test dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the tests:

```bash
python -m pytest
```

## Recommendation Method

The recommender builds a text profile from the student's programme, completed courses, and interests. Course text is built from title, description, and tags. Both are vectorized with TF-IDF, and cosine similarity gives the content match.

The prototype also adds an exploration component:

```python
niche_bonus = 1 - popularity
final_score = (1 - niche_weight) * content_score + niche_weight * niche_bonus
```

The ranking mode controls `niche_weight`:

- `Safe`: no niche bonus
- `Balanced`: moderate niche bonus
- `Exploratory`: stronger niche bonus

## Data and Limitations

The catalogue in `data/courses.csv` is mocked. Popularity values are simulated, and the app does not store user profiles. There is no login, collaborative filtering, timetable validation, or credit-recognition check.

For a production system, the next steps would be real catalogue integration, labelled evaluation data, privacy review, and metrics such as Precision@5, diversity, and topic coverage.

## AI Usage

Generative AI tools were used to support planning, implementation, documentation, and debugging. The final code and text should be reviewed by the submitting group.
