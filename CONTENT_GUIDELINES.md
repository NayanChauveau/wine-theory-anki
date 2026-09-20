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
- Wrong choices must be **credible**. Same class as the key (grape vs grape, AOC vs AOC, climate label vs climate label) and inside the stem’s frame. A Level 3 candidate who half-remembers the chapter should hesitate. Cartoon or physically impossible foils fail even when the keyed fact is right (polar winter on the Gironde, seawater irrigation, Alps, apple as a legal grape, Chablis as a Bordeaux address, Cognac, “pour it down the drain”). If three foils are joke-easy, the card does not test the fact.
- **Choice length** must not give the answer away. The keyed choice must not be the obvious longest or the only detailed sentence. Prefer a short key and put the extra clause in Why; or write foils of the same class at a similar length. A glance at the block should not pick the winner.
- Use `basic` for a simple prompt/response and `cloze` for lists you must recall in order (AOCs, grapes).
- Markdown is allowed in questions and explanations (`**bold**`, lists, short paragraphs).
- Always quote choice `text` if it contains a comma: `{ text: "High alcohol, low acidity", correct: false }`. Otherwise YAML treats the comma as a new key.

## IDs, decks, and status

- `id` is permanent (`chapter-topic-001`). Never reuse or rename an id after it has been released.
- `deck` is a stable English key (`SAT`, `France::Burgundy`). The build localizes it (`WSET 3 Wine` / `WSET 3 VIN`, Bourgogne, ASD, …). Labels live in `templates/ui/decks.yaml`.
- Imported cards keep `source_id` and optional `review` (fact_check / sources). Those fields are editorial and are not shown in Anki.
- `status`:
  - `draft` — work in progress; omitted from release builds
  - `reviewed` — ready to study
  - `needs-translation` — English is ready, French is missing or stale
- `fr:` is optional. The French package simply skips cards without it. Keep the same number of choices and the **same correct index** as `en:`.

## Translation

- Translate in the same YAML file, on the same `id`.
- **Sense first.** Read the French stem, choices, and Why as if they were written in French. If a native speaker would say the sentence does not mean anything, recast it — a word-for-word calque that “matches” English is still a fail.
- Preserve meaning and exam register, not English word order. Use wine French (*cépages*, *élevage*, *pourriture noble*), not *variétés de raisins*, unless that is the teaching point.
- Keep wine names, appellations, and grape varieties in their usual form (Saint-Émilion, Cabernet Sauvignon).
- Why must name the **French** answer text and answer the question the French stem actually asks.
- Same choice count and the same correct index as `en:`. When you rewrite a foil for credibility, change **both** languages.
- If you change the English fact, update the French block in the same PR.

## Tone

Write as a fellow candidate: precise, calm, no marketing, no “trick” questions that hinge on a single adjective.
