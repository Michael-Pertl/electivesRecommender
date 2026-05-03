# Data Specification

## File

The mock course catalogue should be stored at:

```text
data/courses.csv
```

## Required Columns

```csv
course_id,title,university,ects,language,semester,description,tags,popularity
```

## Column Descriptions

### `course_id`

Unique identifier for each course.

Example:

```csv
C001
```

### `title`

Human-readable course name.

Example:

```csv
Data Ethics and Society
```

### `university`

Institution offering the course.

Allowed values:

```text
TU Wien
Uni Wien
BOKU
WU
```

### `ects`

Number of ECTS credits.

Example:

```csv
3
```

### `language`

Language of instruction.

Allowed values:

```text
English
German
```

### `semester`

Semester in which the course is offered.

Allowed values:

```text
Winter
Summer
Both
```

### `description`

Short natural-language course description.

Example:

```csv
This course introduces ethical, legal, and societal questions around data-driven systems and artificial intelligence.
```

### `tags`

Comma-separated list of keywords.

Example:

```csv
ethics,AI,data,society,law
```

### `popularity`

Mock popularity value between 0 and 1.

Interpretation:

- `0.9` = very popular / well-known
- `0.5` = moderately popular
- `0.1` = niche / rarely selected

This is simulated data. It does not represent real enrolment data.

## Dataset Requirements

The dataset should contain at least 30 courses.

The courses should be diverse across:

- universities
- topics
- popularity values
- languages
- semesters

## Suggested Example Courses

Include courses similar to these:

```csv
course_id,title,university,ects,language,semester,description,tags,popularity
C001,Data Ethics and Society,TU Wien,3,English,Winter,"This course introduces ethical legal and societal questions around data-driven systems and artificial intelligence.","ethics,AI,data,society,law",0.72
C002,Sustainable Urban Mobility,TU Wien,3,English,Summer,"Students learn about sustainable transport systems urban planning and climate-friendly mobility concepts.","sustainability,mobility,climate,urban planning",0.41
C003,Public Speaking and Rhetoric,Uni Wien,4,German,Both,"The course trains presentation skills argumentation and confident communication in academic and professional contexts.","communication,presentation,soft skills,rhetoric",0.88
C004,Entrepreneurship Basics,WU,3,English,Winter,"Introduction to business model design startup thinking and entrepreneurial decision-making.","entrepreneurship,business,innovation,startups",0.76
C005,Climate Change and Society,BOKU,3,English,Summer,"This course discusses climate change mitigation adaptation and the social consequences of environmental transformation.","climate,sustainability,society,environment",0.52
```

## Recommended Topic Coverage

The mock dataset should contain realistic courses from at least these areas:

- artificial intelligence
- data science
- sustainability
- climate change
- ethics
- communication
- public speaking
- entrepreneurship
- economics
- law
- psychology
- project management
- design thinking
- intercultural skills
- health and wellbeing
- urban planning
- environmental policy

## Notes

The recommender should not assume that all text is English. However, for the prototype it is acceptable to use a simple TF-IDF vectorizer without advanced multilingual preprocessing.

The mock data should be realistic enough to make the prototype believable.

Do not use real student data.
