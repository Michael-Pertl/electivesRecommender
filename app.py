from pathlib import Path

import streamlit as st

from recommender import CourseRecommender, available_values


DATA_PATH = Path("data/courses.csv")


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
    study_program = st.text_input("Study programme", value="Business Informatics")
    completed_courses = st.text_area(
        "Completed courses",
        value="Databases, Software Engineering, Statistics, Project Management",
        height=90,
    )
    interests = st.text_area(
        "Interests and learning goals",
        value="I am interested in sustainability, artificial intelligence, ethics, and communication skills.",
        height=120,
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

with st.expander("Scoring formula"):
    st.code(
        "niche_bonus = 1 - popularity\n"
        "final_score = (1 - niche_weight) * content_score + niche_weight * niche_bonus",
        language="python",
    )

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
        for index, row in results.iterrows():
            st.markdown(
                f"""
<div style="border: 1px solid #d8dee4; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
  <h3 style="margin-top: 0;">#{index + 1} {row['title']}</h3>
  <p><strong>{row['university']}</strong> · {row['ects']:g} ECTS · {row['language']} · {row['semester']}</p>
  <p>{row['description']}</p>
  <p><strong>Why recommended:</strong><br>{row['explanation']}</p>
  <p><strong>Scores:</strong>
    Content match: {row['content_score']:.2f} ·
    Niche bonus: {row['niche_bonus']:.2f} ·
    Final score: {row['final_score']:.2f}
  </p>
</div>
""",
                unsafe_allow_html=True,
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
