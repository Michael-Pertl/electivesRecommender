# Elective Recommender Prototype: System and Evaluation Discussion

## 1. What the Current Prototype Does

The prototype recommends elective courses from a mock catalogue of 44 courses. It is designed as an embedded study-management feature rather than a standalone recommender.

The student can:

- inspect all mock courses under **Course offer > Courses**;
- adjust a demo study programme, completed courses, interests, and learning goals;
- apply language, university, semester, ECTS workload, and result-count filters;
- choose Safe, Balanced, or Exploratory recommendation mode;
- read a reason for every recommendation;
- save courses as favourites;
- mark courses as not interesting, which removes them from the recommendation list and replaces them with the next-ranked eligible course;
- compare selected courses;
- open **Prototype notes** to inspect the scoring formula and evaluation snapshot.

All course data, student profiles, and popularity values are mocked. The prototype does not store real student data or learn from user behaviour.

## 2. How Ranking Works

### 2.1 Content-based component

The system combines the student's study programme, completed-course names, interests, and learning goals into one profile text. It tokenises this text and compares it with tokens from each course's title, description, and tags.

The current content score is a cosine-like overlap over unique tokens:

```text
content_score = overlapping_tokens / sqrt(profile_token_count * course_token_count)
```

This component is responsible for **personal relevance**. For example, a profile containing `sustainability`, `mobility`, and `climate` should score courses containing the same concepts more highly.

### 2.2 Rule-based component

Rules are applied before ranking:

- enforce the selected language, university, semester, and ECTS workload filters;
- remove a course if its title appears in the completed-course record;
- remove courses marked as not interesting so the next eligible result is shown;
- limit the result to the selected top-N value.

These rules are responsible for **eligibility and workflow correctness**, not semantic relevance. A ranking model should not be expected to learn hard requirements such as language or semester availability.

### 2.3 Popularity-aware re-ranking

The prototype calculates:

```text
niche_bonus = 1 - popularity
final_score = (1 - niche_weight) * content_score + niche_weight * niche_bonus
```

The mode controls `niche_weight`:

| Mode | Niche weight | Intended behaviour |
| --- | ---: | --- |
| Safe | 0.00 | Rank only by profile-course content similarity. |
| Balanced | 0.15 | Preserve relevance while giving less popular courses moderate visibility. |
| Exploratory | 0.30 | Increase exposure of niche courses more strongly. |

Popularity is therefore not treated as quality. It is used to counteract popularity bias and support discovery.

## 3. Why This Hybrid Approach?

The prototype is hybrid in the practical sense that it combines **content scoring, deterministic rules, and popularity-aware re-ranking**. It is not a collaborative-filtering hybrid.

This combination was selected for specific reasons:

| Requirement | Mechanism | Why this mechanism fits |
| --- | --- | --- |
| Match personal interests and learning goals | Content-based scoring | Course text and student-entered goals are available immediately. No interaction history is required. |
| Handle new students | Content-based scoring | It reduces user cold-start because recommendations can be generated from profile text and study records. |
| Handle new courses | Content-based scoring | A new course can be recommended as soon as its title, description, and tags exist. |
| Respect language, semester, and university choices | Rules | These are explicit constraints. A learned score could otherwise rank an unavailable or unsuitable course highly. |
| Avoid recommending completed courses | Rule | Completion is a hard exclusion, not a preference signal. |
| Respect negative feedback | Rule | Courses marked as not interesting leave the recommendation pool and are replaced automatically. |
| Reduce popularity bias | Niche re-ranking | A controlled weight exposes less popular courses without discarding relevance. |
| Explain results | Token matches and explicit score components | The reason can be traced to matched course metadata and a small, inspectable formula. |

### Would one model be enough?

A content-only model is a valid baseline and is effectively the Safe mode. It is enough to produce an initial relevance ranking, but it does not enforce all planning constraints or address popularity concentration by itself.

Rules alone would be insufficient because they can filter eligible courses but cannot meaningfully rank several eligible courses by individual interests. Collaborative filtering is not currently appropriate because the prototype has no reliable enrolment, rating, click, or completion-interaction matrix. Adding it now would create an unsupported claim rather than a better prototype.

For a production system, collaborative or learning-to-rank components should only be considered after sufficient consented interaction data exists. They should be evaluated against the current content-based baseline.

## 4. Explainability in the Prototype

Explainability is shown at two levels.

### Student-facing explanation

Every recommendation row contains:

- **Why recommended:** a sentence identifying matched profile topics or related course wording;
- matched topic tags shown below the course metadata;
- qualitative labels for content match and exploration value (`low`, `medium`, or `high`).

Example interpretation:

> Recommended because it matches your profile around sustainability and climate. It is also a less mainstream option, which supports exploration beyond the most popular courses.

This answers two separate questions: **Why is this relevant to me?** and **Why is this course visible in the selected mode?**

### Evaluator-facing explanation

The top-right **Prototype notes** view contains:

- the exact scoring formula;
- the current mode explanation;
- top-list university and topic diversity;
- average popularity;
- overlap between Safe and Exploratory results;
- a popularity-bias comparison.

These details are hidden from normal student use because raw formulas and diagnostics add interface noise without supporting the student's immediate decision.

### Explainability limitation

The explanation is faithful to the implemented token matching, but it is still coarse. It does not distinguish whether a match came from the programme, completed courses, or manually entered goals. A stronger version should label the source, for example: `Matches learning goal: sustainable mobility`.

## 5. How the System Should Be Tested

Evaluation should combine software tests, offline recommender metrics, fairness and bias audits, and user evaluation. No single metric is sufficient.

### 5.1 Functional tests

Test deterministic behaviour first:

- language, university, and semester filters never return ineligible courses;
- completed courses are excluded;
- marking a course as not interesting removes it from recommendations and loads the next-ranked eligible course;
- favourites do not change ranking;
- Safe mode equals content-only ranking;
- repeated runs with the same profile return the same order;
- empty or restrictive profiles fail gracefully;
- every recommendation has a non-empty explanation.

### 5.2 Relevance evaluation

Create a small expert-labelled test set. For each representative student profile, lecturers or domain experts mark courses as highly relevant, relevant, or not relevant. Then report:

- **Precision@5:** proportion of the top five that are relevant;
- **Recall@5:** proportion of all labelled relevant courses found in the top five;
- **nDCG@5:** rewards highly relevant courses appearing near the top;
- **MRR:** useful if finding at least one strong elective quickly is important.

The content-only Safe mode should be the baseline. Balanced and Exploratory modes should only be accepted if their gains in novelty and coverage do not cause an unacceptable relevance loss.

### 5.3 Fairness and bias evaluation

There are two fairness perspectives.

#### Student-side fairness

Check whether profiles with comparable interests receive comparable recommendation quality regardless of study programme, language preference, or profile length.

Suggested tests:

- create matched profile pairs that differ in only one attribute;
- compare Precision@5 and nDCG@5 across programmes and language settings;
- test short and detailed versions of the same learning goal;
- inspect whether English or German descriptions systematically receive better matches due to tokenisation;
- verify that manually entered interests can surface cross-disciplinary courses rather than only programme-matching courses.

The prototype has no demographic or protected-attribute data, so it cannot currently claim demographic fairness. Such data should not be inferred from names or study programmes. A production fairness study would require a lawful, privacy-preserving evaluation design.

#### Course/provider-side fairness

Check whether exposure is concentrated on popular courses or one university.

Report:

- exposure share by university, language, semester, and popularity band;
- average rank by provider group;
- Gini coefficient or entropy of item exposure;
- long-tail exposure: share of recommendations belonging to the least-popular 50% of courses;
- relevance-adjusted exposure, so equal exposure is not pursued at the cost of obvious irrelevance.

Safe, Balanced, and Exploratory modes should be compared using the same profile set. The expected result is that Exploratory lowers average popularity and increases long-tail exposure while retaining acceptable relevance.

### 5.4 Robustness tests

- spelling variants and synonyms in learning goals;
- German versus English wording for the same interest;
- missing tags or descriptions;
- extremely broad and extremely narrow profiles;
- duplicate or malformed completed-course entries;
- sensitivity to one added or removed profile term;
- ranking stability when unrelated catalogue items are added.

## 6. Catalogue Coverage

### What high catalogue coverage means

Catalogue coverage is the proportion of eligible catalogue items that appear in at least one recommendation list across a representative set of users:

```text
catalogue_coverage@k = unique_items_recommended_at_k / eligible_catalogue_items
```

It should be measured over many representative profiles, not from one student's top-N list. Useful related metrics are:

- **aggregate diversity:** number of distinct recommended courses;
- **long-tail coverage:** coverage among less popular courses;
- **provider coverage:** number and share of universities represented;
- **topic coverage:** number and share of catalogue topics represented;
- **user coverage:** proportion of profiles for which the system can produce enough recommendations.

### Has the current prototype evaluated coverage?

**Partially, but not formally.** The Prototype notes currently calculate university diversity and topic-tag coverage within the current top-N list. They also compare average popularity between modes. These are useful diagnostics, but they are not catalogue coverage.

The **Courses** page exposing all 44 mock courses improves transparency, but it also does not prove recommendation coverage.

### Proposed coverage experiment

1. Define at least 15-30 representative profiles across programmes, interests, languages, and profile lengths.
2. Run every profile in Safe, Balanced, and Exploratory modes at `k = 5` and `k = 10`.
3. Record every recommended course and rank.
4. Calculate catalogue coverage, aggregate diversity, long-tail coverage, and exposure by university.
5. Report relevance metrics alongside coverage.

The goal should not be 100% coverage at any cost. A course that is irrelevant or ineligible should not be recommended merely to increase the metric. The defensible claim is **higher relevant coverage with controlled exposure concentration**.

## 7. Important Recommender-System Trade-offs

### Accuracy versus diversity

The highest content matches may be repetitive. Balanced and Exploratory modes intentionally trade a limited amount of similarity for broader discovery. This trade-off must be shown with both relevance and diversity metrics.

### Popularity bias versus quality

Popular courses are not necessarily better, and niche courses are not necessarily more relevant. The popularity term should remain a bounded re-ranking signal rather than dominate the score.

### Cold start

The current design addresses new-user and new-item cold start using explicit profile text and course metadata. It does not solve cases where both are sparse; those should trigger broader browsing or ask the student for additional goals.

### Feedback loops

If future versions learn from clicks or enrolments, already-visible courses may accumulate more interactions and become even more visible. Evaluation should use exposure-aware logging and distinguish a click from genuine course suitability.

### Privacy and autonomy

Production integration should use only necessary study-record fields, explain their use, avoid sensitive inference, and let students edit exploration goals. Recommendations should support decisions rather than automatically enrol students or hide the full catalogue.

## 8. Current Limitations

- Token matching does not understand synonyms, negation, or semantic similarity.
- The tokenizer is primarily suitable for simple Latin/English-style tokens and does not perform stemming or multilingual mapping.
- All profile fields are merged, so programme, completed courses, and learning goals have equal implicit importance.
- Completed-course exclusion uses title text matching rather than stable course IDs.
- Popularity values are mocked and are not based on a defined observation window.
- The model has not been evaluated against expert relevance labels.
- Formal catalogue coverage, exposure fairness, and demographic fairness have not yet been measured.
- Favourites and not-interested interactions are kept only in browser memory and are not persisted.

These limitations should be presented directly. The prototype demonstrates interaction design and a transparent baseline, not a production-ready recommendation model.

## 9. Suggested Slide Narrative

### Model slide

**Title: Why content scoring plus rules?**

- Content scoring ranks courses by overlap with the student's programme, completed courses, and stated goals.
- Rules enforce hard planning constraints: language, semester, university, completion status, and not-interested state.
- Popularity-aware re-ranking gives less popular but still relevant courses controlled visibility.
- This design works without historical interaction data and handles new students and new courses.
- Safe mode is the content-only baseline; Balanced and Exploratory add explicit discovery trade-offs.

### Explainability slide

**Title: Explanations are part of the decision workflow**

- Each recommendation shows matched topics and a plain-language `Why recommended` reason.
- Content match explains relevance; exploration value explains niche-course visibility.
- Prototype notes expose the exact formula and diagnostics to evaluators, but hide them from the normal student view.
- Explanations are faithful to the implemented features rather than generated after the fact.

### Evaluation slide

**Title: Evaluate relevance, reach, and exposure together**

- Relevance: Precision@5, Recall@5, and nDCG@5 using expert-labelled profile-course pairs.
- Coverage: catalogue coverage@5/@10 and aggregate diversity across representative profiles.
- Bias: exposure by university, language, and popularity band; long-tail exposure and exposure Gini.
- Robustness: matched profiles, multilingual wording, profile length, missing metadata, and ranking stability.
- Current status: top-list diversity and popularity diagnostics exist; formal relevance and catalogue-coverage experiments remain future work.

## 10. Defensible Summary

The strongest current claim is:

> The prototype demonstrates a transparent, cold-start-friendly recommendation baseline that combines profile-course content similarity with explicit study-planning rules and controlled niche-course exposure. It exposes explanations in the student workflow and evaluation diagnostics in a separate prototype view. Formal relevance, catalogue coverage, and fairness evaluation are specified but have not yet been completed.

This is more defensible than claiming that the prototype is already fair, unbiased, or proven to achieve high catalogue coverage.
