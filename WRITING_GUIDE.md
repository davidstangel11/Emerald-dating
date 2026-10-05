# Emerald Dating blog: how each post is made

The blog publishes 3 times a week (Monday, Wednesday, Friday). Each run adds one post.

## 1. Pick the topic
- Search the web for what men are searching and talking about in dating right now: Hinge, Bumble, Tinder, Raya and The League updates and features, dating app trends, seasonal moments (cuffing season, holidays, Dating Sunday, Valentine's Day, summer), viral dating terms, new studies and surveys.
- Choose one topic with clear search intent from our reader: a busy, high-earning man (roughly 25 to 45) who wants more and better dates with less time on apps.
- Good formats: "how to" guides (Hinge prompts for men, best first photos, opening lines that get replies), explainers of a trend or feature, data-backed myth busting, comparisons (Hinge vs Bumble for men over 30), city guides (best first date spots in a big US city).
- Check `topics.md` and the existing `posts/` folder. Never repeat a topic or target the same main keyword twice. Rotate formats.
- Add the chosen topic and its main keyword to `topics.md`.

## 2. Write the post
- 1,000 to 1,600 words. Markdown in `posts/YYYY-MM-DD-slug.md` with the front matter fields shown in `build.py`.
- Title: include the main keyword naturally, under 65 characters when possible. Description: 140 to 160 characters, includes the keyword.
- Voice: David, founder of Emerald Dating, who has helped men with dating for over 10 years. Direct, practical, warm, confident. Short paragraphs. No fluff, no hype.
- Structure: a 2 to 3 sentence intro that names the problem, H2 sections, specific actionable advice, a short bottom line.
- Use real numbers only from sources you actually opened and checked this run, linked inline. Never invent statistics, studies, quotes or client stories.
- One natural mention of Emerald Dating near the end with this exact guarantee wording: **16+ new quality matches in your first 7 days, or your money back.** Link to https://emerald.dating/?utm_source=blog&utm_medium=article&utm_campaign=SLUG. The page template already adds a call to action box, so do not add another.
- Link to 1 or 2 earlier posts on https://blog.emerald.dating when relevant.
- House style rules: never use em dashes, en dashes or double hyphens (use commas, periods, colons or parentheses). `build.py` refuses to build if any appear. Do not make claims about anyone's personal attributes. Do not name or disparage real private people.

## 3. Publish
- Run `python3 build.py` (it fails loudly on style problems), check the generated page, then commit `posts/`, `topics.md` and `docs/` and push to `main`.
