# TISS-Inspired UI/UX Guide for the Elective Recommender Prototype

## Source Observations

The screenshots show a study-management interface with a dense administrative layout rather than a modern card-heavy dashboard.

Core visual patterns:

- Dark teal header band with a large system identity on the left.
- Thin light utility bar below the header for user, language, help, and logout.
- Pale blue left navigation column with an orange section header.
- White central content area with generous horizontal width.
- Page titles are simple black text with a dotted separator line.
- Tables are compact, bordered, and alternating very light blue/white rows.
- Primary links and selected navigation items use orange.
- Buttons use an orange gradient/solid fill and small dimensions.
- Information panels use pale blue backgrounds, thin borders, and gray title strips.
- The interface is practical and information-dense; it avoids large decorative cards.

## Design Direction for the Prototype

The recommender should look like an additional study-management module, not a separate product page.

Recommended information architecture:

1. Header: system shell and utility links.
2. Left navigation: study-management categories and the recommender entry.
3. Main content: recommendations as compact course rows.
4. Student context: a small administrative form block, not the visual center.
5. Prototype notes: hidden behind a utility action, not shown as normal student content.

## Component Rules

### Header

- Use dark teal as the top shell color.
- Use a light utility bar underneath.
- Keep navigation text small and administrative.
- Avoid marketing-style hero sections.

### Left Navigation

- Use pale blue background.
- Use orange for the active section.
- Group links under bold category headings.
- Keep link spacing compact.

### Main Content

- Use a white content canvas.
- Use simple page title and dotted separator.
- Recommendations should feel like course catalogue rows.
- Prefer tables or compact row cards over large visual cards.

### Recommendation Rows

Each row should show:

- rank
- course title as orange link-style text
- course metadata: university, ECTS, language, semester
- matched tags
- short explanation
- compact actions: Shortlist, Compare

Avoid:

- large card padding
- repeated badges
- raw score details in the normal student flow
- formulas outside prototype notes

### Student Context

Completed courses should look imported from the student record:

- display as chips or compact record items
- allow demo adjustment
- make clear that real integration would prefill the data

### Prototype Notes

Keep the following hidden from normal students:

- scoring formula
- evaluation metrics
- design priorities
- popularity-bias diagnostics

Expose it through a small top-right utility button for presentation.

## Color Tokens

Suggested palette based on the screenshots:

- Header teal: `#004763`
- Deep teal: `#00384f`
- Pale navigation blue: `#eef7fc`
- Border blue-gray: `#bfd3df`
- Orange action/link: `#d46b00`
- Orange active header: `#ed8b00`
- White content: `#ffffff`
- Table alternate row: `#f2f8fb`
- Text: `#111827`
- Muted text: `#667985`

## UX Rationale

This direction should be more convincing for professors because it demonstrates that the recommender can be embedded into an existing study-management workflow instead of behaving like a standalone recommender demo.

The important story becomes:

- student data is already available,
- recommendations appear inside course planning,
- shortlisted courses become planning candidates,
- prototype-only algorithm details are available for evaluation but hidden from students.
