# Content guidelines

Cards in this repository are independently authored study aids for the WSET Level 3 Award in Wines. They are **not** official WSET materials.

## Original wording

- Write questions and explanations in your own words.
- Do **not** copy sentences, tables, diagrams, or exam items from WSET textbooks, workbooks, or past papers.
- Facts (grape names, AOCs, climate patterns, winemaking steps) are fine. The *expression* of those facts must be original.
- Never add textbook page numbers or quotations. A future `source` field may point to the public specification, not the book.

This project is not affiliated with, endorsed by, or connected to the Wine & Spirit Education Trust.

## Card design

- Prefer a single, exam-style **MCQ** with one correct answer and a short **Why** explanation.
- Name the **answer text** in the explanation, never “option B”. Choice order may change later.
- Keep the question stem focused on one idea. Avoid double-barrelled “which is true AND why” items.
- Use `basic` for a simple prompt/response and `cloze` for lists you must recall in order (AOCs, grapes).
- Markdown is allowed in questions and explanations (`**bold**`, lists, short paragraphs).
- Always quote choice `text` if it contains a comma: `{ text: "High alcohol, low acidity", correct: false }`. Otherwise YAML treats the comma as a new key.

## IDs, decks, and status

- `id` is permanent (`chapter-topic-001`). Never reuse or rename an id after it has been released.
- `deck` becomes the Anki path under `WSET 3 VIN::`. Use `France::Bordeaux`, not a one-off spelling.
- `status`:
  - `draft` — work in progress; omitted from release builds
  - `reviewed` — ready to study
  - `needs-translation` — English is ready, French is missing or stale
- `fr:` is optional. The French package simply skips cards without it. Keep the same number of choices and the **same correct index** as `en:`.

## Translation

- Translate in the same YAML file, on the same `id`.
- Preserve meaning, not word-for-word textbook French.
- Keep wine names, appellations, and grape varieties in their usual form (Saint-Émilion, Cabernet Sauvignon).
- If you change the English fact, update the French block in the same PR.

## Tone

Write as a fellow candidate: precise, calm, no marketing, no “trick” questions that hinge on a single adjective.
