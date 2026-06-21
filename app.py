from pathlib import Path

import streamlit as st

from recommender import CourseRecommender, available_values


DATA_PATH = Path("data/courses.csv")

PERSONAS = {
    "Business Informatics": {
        "study_program": "Business Informatics",
        "completed_courses": "Databases, Software Engineering, Statistics, Project Management",
        "interests": "I am interested in sustainability, artificial intelligence, ethics, and communication skills.",
    },
    "Environmental Engineering": {
        "study_program": "Environmental Engineering",
        "completed_courses": "Ecology, Environmental Systems, Resource Management",
        "interests": "I want to learn more about climate policy, sustainable cities, mobility, and environmental governance.",
    },
    "Psychology": {
        "study_program": "Psychology",
        "completed_courses": "Introduction to Psychology, Social Psychology, Research Methods",
        "interests": "I am interested in communication, wellbeing, learning, behavioral economics, and inclusive digital tools.",
    },
}


def score_label(value: float) -> str:
    if value >= 0.45:
        return "high"
    if value >= 0.20:
        return "medium"
    return "low"


def render_course_cards(results):
    for index, row in results.iterrows():
        st.markdown(
            f"""
<div style="border: 1px solid #d8dee4; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
  <h3 style="margin-top: 0;">#{index + 1} {row['title']}</h3>
  <p><strong>{row['university']}</strong> · {row['ects']:g} ECTS · {row['language']} · {row['semester']}</p>
  <p>{row['description']}</p>
  <p><strong>Why recommended:</strong><br>{row['explanation']}</p>
  <p><strong>Score interpretation:</strong>
    Content match is {score_label(row['content_score'])} ({row['content_score']:.2f}) ·
    Exploration bonus is {score_label(row['niche_bonus'])} ({row['niche_bonus']:.2f}) ·
    Final score: {row['final_score']:.2f}
  </p>
</div>
""",
            unsafe_allow_html=True,
        )


@st.cache_resource
def load_recommender() -> CourseRecommender:
    return CourseRecommender(str(DATA_PATH))


st.set_page_config(page_title="Personalized Elective Course Recommender", layout="wide")

st.title("Personalized Elective Course Recommender")
st.write(
    "This prototype recommends elective and transferable-skills courses based on your "
    "study programme, completed courses, and interests. It uses a simplified "
    "content-based recommender with an optional exploration mode to surface niche courses."
)

if not DATA_PATH.exists():
    st.error("Course dataset is missing. Expected file: data/courses.csv")
    st.stop()

try:
    recommender = load_recommender()
except Exception as exc:
    st.error(f"Could not load the course dataset: {exc}")
    st.stop()

with st.sidebar:
    st.header("Student Profile")
    persona_name = st.selectbox("Demo persona", list(PERSONAS), index=0)
    persona = PERSONAS[persona_name]
    study_program = st.text_input(
        "Study programme",
        value=persona["study_program"],
        key=f"study_program_{persona_name}",
    )
    completed_courses = st.text_area(
        "Completed courses",
        value=persona["completed_courses"],
        height=90,
        key=f"completed_courses_{persona_name}",
    )
    interests = st.text_area(
        "Interests and learning goals",
        value=persona["interests"],
        height=120,
        key=f"interests_{persona_name}",
    )

    st.header("Recommendation Settings")
    top_n = st.slider("Number of recommendations", min_value=3, max_value=10, value=5)
    language = st.selectbox("Language filter", ["Any", "English", "German"])
    university = st.selectbox(
        "University filter",
        available_values(recommender.courses["university"]),
    )
    semester = st.selectbox("Semester filter", ["Any", "Winter", "Summer", "Both"])
    exploration_mode = st.selectbox(
        "Exploration mode",
        ["Safe", "Balanced", "Exploratory"],
        index=1,
    )
    submitted = st.button("Get recommendations", type="primary")

mode_explanations = {
    "Safe": "Safe ranks courses by content similarity only.",
    "Balanced": "Balanced adds a moderate bonus for less popular courses.",
    "Exploratory": "Exploratory gives stronger visibility to niche courses.",
}

st.info(mode_explanations[exploration_mode])

st.subheader("What Was Important in This Prototype")
priority_cols = st.columns(5)
priority_cols[0].metric("Personal relevance", "TF-IDF match")
priority_cols[1].metric("Cold start", "free-text input")
priority_cols[2].metric("User control", "filters + mode")
priority_cols[3].metric("Transparency", "why + scores")
priority_cols[4].metric("Less popularity bias", "niche bonus")

with st.expander("Scoring formula"):
    st.code(
        "niche_bonus = 1 - popularity\n"
        "final_score = (1 - niche_weight) * content_score + niche_weight * niche_bonus",
        language="python",
    )

recommendations_tab, comparison_tab, evaluation_tab = st.tabs(
    ["Recommendations", "Safe vs Exploratory", "Evaluation"]
)

with recommendations_tab:
    if submitted:
        if not any([study_program.strip(), interests.strip()]):
            st.warning("Please enter at least your study programme or interests.")
            st.stop()

        results = recommender.recommend(
            study_program=study_program,
            completed_courses=completed_courses,
            interests=interests,
            top_n=top_n,
            language=language,
            university=university,
            semester=semester,
            exploration_mode=exploration_mode,
        )

        if results.empty:
            st.warning(
                "No courses matched the selected filters. Try using fewer filters or another exploration mode."
            )
        else:
            st.subheader("Recommended Courses")
            render_course_cards(results)
    else:
        st.write("Choose a persona or enter your own profile, then click Get recommendations.")

with comparison_tab:
    if not any([study_program.strip(), interests.strip()]):
        st.warning("Please enter at least your study programme or interests.")
        st.stop()

    safe_results = recommender.recommend(
        study_program=study_program,
        completed_courses=completed_courses,
        interests=interests,
        top_n=top_n,
        language=language,
        university=university,
        semester=semester,
        exploration_mode="Safe",
    )
    exploratory_results = recommender.recommend(
        study_program=study_program,
        completed_courses=completed_courses,
        interests=interests,
        top_n=top_n,
        language=language,
        university=university,
        semester=semester,
        exploration_mode="Exploratory",
    )

    safe_col, exploratory_col = st.columns(2)
    with safe_col:
        st.subheader("Safe")
        st.caption("Ranks by content similarity only.")
        st.dataframe(
            safe_results[["title", "content_score", "niche_bonus", "final_score"]],
            width="stretch",
            hide_index=True,
        )
    with exploratory_col:
        st.subheader("Exploratory")
        st.caption("Keeps relevance, but gives niche courses more visibility.")
        st.dataframe(
            exploratory_results[["title", "content_score", "niche_bonus", "final_score"]],
            width="stretch",
            hide_index=True,
        )

    if not safe_results.empty and not exploratory_results.empty:
        safe_avg_niche = safe_results["niche_bonus"].mean()
        exploratory_avg_niche = exploratory_results["niche_bonus"].mean()
        st.metric(
            "Average exploration bonus in top results",
            f"{exploratory_avg_niche:.2f}",
            delta=f"{exploratory_avg_niche - safe_avg_niche:+.2f} vs Safe",
        )

with evaluation_tab:
    st.subheader("How We Evaluate the Prototype")
    st.write(
        "Because the catalogue and popularity values are mocked, the current evaluation is "
        "qualitative rather than based on historical clicks, ratings, or enrolments."
    )
    st.markdown(
        """
- **Functional check:** the app accepts a student profile, applies filters, and returns a ranked top-N list.
- **Persona check:** predefined student profiles should receive plausible courses for their interests.
- **Transparency check:** each course shows an explanation and visible score components.
- **Exploration check:** Safe and Exploratory mode should produce different rankings when niche courses are relevant.
- **Ethics check:** the prototype uses no real student data and does not store user profiles.
"""
    )
    st.write(
        "A stronger future evaluation would add manually labelled relevant courses for each "
        "persona and report Precision@5, topic coverage, and diversity across universities."
    )

st.caption(
    "The course catalogue and popularity values are mocked for demonstration. "
    "No real student data is stored."
)

with st.expander("Available mock courses"):
    st.dataframe(
        recommender.courses[
            ["course_id", "title", "university", "ects", "language", "semester", "tags", "popularity"]
        ],
        use_container_width=True,
        hide_index=True,
    )
