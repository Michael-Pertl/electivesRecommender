from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


REQUIRED_COLUMNS = {
    "course_id",
    "title",
    "university",
    "ects",
    "language",
    "semester",
    "description",
    "tags",
    "popularity",
}


class CourseRecommender:
    """Small content-based course recommender for the Streamlit prototype."""

    def __init__(self, courses_path: str | Path):
        self.courses_path = Path(courses_path)
        if not self.courses_path.exists():
            raise FileNotFoundError(f"Course dataset not found: {self.courses_path}")

        self.courses = pd.read_csv(self.courses_path)
        missing_columns = REQUIRED_COLUMNS.difference(self.courses.columns)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Course dataset is missing required columns: {missing}")
        if self.courses.empty:
            raise ValueError("Course dataset must contain at least one course")

        self.courses = self.courses.copy()
        for column in ["title", "university", "language", "semester", "description", "tags"]:
            self.courses[column] = self.courses[column].fillna("").astype(str)

        self.courses["popularity"] = (
            pd.to_numeric(self.courses["popularity"], errors="coerce")
            .fillna(0.5)
            .clip(0, 1)
        )
        self.courses["ects"] = pd.to_numeric(self.courses["ects"], errors="coerce").fillna(0)

        self.courses["combined_text"] = (
            self.courses["title"]
            + " "
            + self.courses["description"]
            + " "
            + self.courses["tags"].str.replace(",", " ", regex=False)
        )

        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.course_matrix = self.vectorizer.fit_transform(self.courses["combined_text"])

    def recommend(
        self,
        study_program: str = "",
        completed_courses: str = "",
        interests: str = "",
        top_n: int = 5,
        language: str = "Any",
        university: str = "Any",
        semester: str = "Any",
        exploration_mode: str = "Balanced",
    ) -> pd.DataFrame:
        profile_text = " ".join(
            part.strip()
            for part in [study_program, completed_courses, interests]
            if isinstance(part, str) and part.strip()
        )

        if not profile_text:
            return pd.DataFrame()

        top_n = max(1, int(top_n))

        user_vector = self.vectorizer.transform([profile_text])
        content_scores = np.asarray(cosine_similarity(user_vector, self.course_matrix)).flatten()

        results = self.courses.copy()
        results["content_score"] = content_scores
        results["niche_bonus"] = 1 - results["popularity"]

        niche_weight = self._niche_weight(exploration_mode)
        results["final_score"] = (
            (1 - niche_weight) * results["content_score"]
            + niche_weight * results["niche_bonus"]
        )

        results = self._apply_filters(results, language, university, semester)
        results = self._exclude_completed_courses(results, completed_courses)

        if results.empty:
            return results

        user_terms = self._tokenize_profile(profile_text)
        results["explanation"] = results.apply(
            lambda row: self.generate_explanation(row, user_terms, exploration_mode),
            axis=1,
        )

        display_columns = [
            "course_id",
            "title",
            "university",
            "ects",
            "language",
            "semester",
            "description",
            "tags",
            "popularity",
            "content_score",
            "niche_bonus",
            "final_score",
            "explanation",
        ]
        return (
            results.sort_values("final_score", ascending=False)
            .head(top_n)
            .loc[:, display_columns]
            .reset_index(drop=True)
        )

    def generate_explanation(
        self,
        course: pd.Series,
        user_terms: set[str],
        exploration_mode: str,
    ) -> str:
        matching_tags = self._matching_tags(course.get("tags", ""), user_terms)

        if matching_tags:
            tag_text = ", ".join(matching_tags[:3])
            reason = f"matches your profile around {tag_text}"
        elif course["content_score"] > 0:
            reason = "has related wording in its title, description, or tags"
        else:
            reason = "is one of the closest available options after the selected filters"

        explanation = f"Recommended because it {reason}."
        if exploration_mode in {"Balanced", "Exploratory"} and course["niche_bonus"] >= 0.45:
            explanation += " It is also a less mainstream option, which supports exploration beyond the most popular courses."
        elif course["popularity"] >= 0.75:
            explanation += " It is a relatively well-known option in the mock catalogue."
        return explanation

    def _apply_filters(
        self,
        results: pd.DataFrame,
        language: str,
        university: str,
        semester: str,
    ) -> pd.DataFrame:
        filtered = results
        if language != "Any":
            filtered = filtered[filtered["language"] == language]
        if university != "Any":
            filtered = filtered[filtered["university"] == university]
        if semester != "Any":
            filtered = filtered[filtered["semester"].isin([semester, "Both"])]
        return filtered

    def _exclude_completed_courses(
        self,
        results: pd.DataFrame,
        completed_courses: str,
    ) -> pd.DataFrame:
        completed_text = (completed_courses or "").lower()
        if not completed_text:
            return results

        mask = ~results["title"].str.lower().apply(lambda title: title in completed_text)
        return results[mask]

    def _matching_tags(self, tags: str, user_terms: set[str]) -> list[str]:
        matched = []
        for tag in self._split_tags(tags):
            tag_tokens = self._tokenize_profile(tag)
            if tag_tokens.intersection(user_terms):
                matched.append(tag)
        return matched

    def _split_tags(self, tags: str) -> list[str]:
        return [tag.strip() for tag in str(tags).split(",") if tag.strip()]

    def _tokenize_profile(self, text: str) -> set[str]:
        normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
        return {token for token in normalized.split() if len(token) > 2}

    def _niche_weight(self, exploration_mode: str) -> float:
        weights = {
            "Safe": 0.00,
            "Balanced": 0.15,
            "Exploratory": 0.30,
        }
        return weights.get(exploration_mode, 0.15)


def available_values(values: Iterable[str]) -> list[str]:
    clean_values = {
        str(value).strip()
        for value in values
        if value is not None and str(value).strip() and str(value).strip().lower() != "nan"
    }
    return ["Any"] + sorted(clean_values)
