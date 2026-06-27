from pathlib import Path

import pandas as pd
import pytest

from recommender import CourseRecommender, available_values


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "courses.csv"


@pytest.fixture(scope="module")
def recommender() -> CourseRecommender:
    return CourseRecommender(DATA_PATH)


def test_recommend_returns_ranked_top_n_results(recommender: CourseRecommender) -> None:
    results = recommender.recommend(
        study_program="Business Informatics",
        completed_courses="Databases, Software Engineering",
        interests="I care about artificial intelligence, sustainability, and ethics.",
        top_n=5,
    )

    assert len(results) == 5
    assert list(results["final_score"]) == sorted(results["final_score"], reverse=True)
    assert {"title", "explanation", "content_score", "niche_bonus", "final_score"}.issubset(
        results.columns
    )


def test_filters_limit_recommendations(recommender: CourseRecommender) -> None:
    results = recommender.recommend(
        study_program="Environmental Engineering",
        interests="climate policy and sustainable cities",
        language="English",
        university="BOKU",
        semester="Winter",
        top_n=10,
    )

    assert not results.empty
    assert set(results["language"]) == {"English"}
    assert set(results["university"]) == {"BOKU"}
    assert set(results["semester"]).issubset({"Winter", "Both"})


def test_exploratory_mode_changes_scores(recommender: CourseRecommender) -> None:
    profile = {
        "study_program": "Business Informatics",
        "completed_courses": "Databases",
        "interests": "ethics artificial intelligence sustainability",
        "top_n": 10,
    }

    safe = recommender.recommend(**profile, exploration_mode="Safe")
    exploratory = recommender.recommend(**profile, exploration_mode="Exploratory")

    merged = safe[["course_id", "final_score"]].merge(
        exploratory[["course_id", "final_score"]],
        on="course_id",
        suffixes=("_safe", "_exploratory"),
    )
    assert (merged["final_score_safe"] != merged["final_score_exploratory"]).any()


def test_completed_courses_are_excluded(recommender: CourseRecommender) -> None:
    results = recommender.recommend(
        interests="communication negotiation conflict",
        completed_courses="Negotiation and Conflict Management",
        top_n=10,
    )

    assert "Negotiation and Conflict Management" not in set(results["title"])


def test_empty_profile_returns_empty_dataframe(recommender: CourseRecommender) -> None:
    assert recommender.recommend().empty


def test_missing_required_columns_raise_error(tmp_path: Path) -> None:
    invalid_catalogue = tmp_path / "courses.csv"
    pd.DataFrame({"title": ["Only a title"]}).to_csv(invalid_catalogue, index=False)

    with pytest.raises(ValueError, match="missing required columns"):
        CourseRecommender(invalid_catalogue)


def test_available_values_are_cleaned() -> None:
    assert available_values(["TU Wien", "", None, float("nan"), "WU", "TU Wien"]) == [
        "Any",
        "TU Wien",
        "WU",
    ]
