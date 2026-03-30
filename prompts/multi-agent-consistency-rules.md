# The Covenant Rendering — Multi-Agent Consistency Rules

**Purpose:** This document addresses quality issues caused by parallel agent generation. When multiple agents generate different chapters of the same book simultaneously, they make independent choices about term rendering, expanded_rendering usage, and style. This produces inconsistency within a single book. These rules MUST be followed by every agent generating TCR content.

---

## RULE 1: Default Term Register — Consistency With Contextual Freedom

Hebrew words carry a range of meanings, and the correct English rendering depends on context. A rigid "one word always" rule would flatten the Hebrew rather than honor it. But when parallel agents generate different chapters independently, they often choose different renderings for the same word in the same semantic context — not because the context demands it, but because they made independent, uncoordinated choices. That is the problem this rule addresses.

### The principle

**Same word + same type of context = same rendering. Different context = different rendering is expected and welcome, but must be documented.**

### Default Term Register

The following terms have a **default** rendering — use it unless the context genuinely calls for something different. When you depart from the default, you MUST explain why in a `translator_notes` entry on that verse.

| Hebrew | Transliteration | Default Rendering | When to vary | Example of valid variation |
|--------|----------------|------------------|-------------|--------------------------|
| חֶסֶד | chesed | **faithful love** | When the relationship is not covenantal (e.g., treaty partners, political allies) | Gen 21:23 Abimelech asks for "good faith"; 1 Sam 15:6 Kenites showed "kindness" — non-covenant contexts |
| בְּרִית | berit | **covenant** | Rarely varies | — |
| גֹּאֵל | go'el | **kinsman-redeemer** (when kinship is the point) | When applied to God (Isaiah, Exodus) where the kinship is metaphorical | Isa 41:14 "your Redeemer" — God acts as if He were kin, but "kinsman-redeemer" is awkward for deity |
| גָּאַל | ga'al (verb) | **redeem** | Rarely varies | — |
| נָגִיד | nagid | **leader** | When the military or administrative sense dominates over the "divinely appointed" sense | — |
| מָשִׁיחַ | mashiach | **anointed** / **anointed one** | Rarely varies | — |
| מְשִׁיחַ יְהוָה | meshiach YHWH | **the LORD's anointed** | Rarely varies | — |
| רוּחַ יְהוָה | ruach YHWH | **Spirit of the LORD** | Rarely varies (always capitalize Spirit) | — |
| רוּחַ אֱלֹהִים | ruach Elohim | **Spirit of God** | Rarely varies (always capitalize Spirit) | — |
| נָבִיא | navi | **prophet** | When the text itself uses an older synonym | 1 Sam 9:9 editorial note explains ro'eh ("seer") |
| כָּבוֹד | kavod | **glory** | When the physical "weight/heaviness" sense is primary | 1 Sam 4:18 Eli was "heavy" (kaved) — same root, different sense |
| שָׁלוֹם | shalom | **peace** | When "well-being" or "wholeness" is clearly the point | Greeting formulas: "Is it well?" (ha-shalom?) |
| קָדוֹשׁ | qadosh | **holy** | Rarely varies | — |
| חֵרֶם | cherem | **devoted to destruction** | Rarely varies in conquest/ban contexts | — |
| סַרְנֵי | sarnei (Philistine) | **tyrants** | This is a title, not a common noun — always the same | — |

### How to apply this register

1. **Start with the default.** If the context fits the default rendering, use it. Do not invent variation for variety's sake.
2. **Vary when the context demands it.** If the Hebrew word genuinely means something different in this specific passage, render it differently. Hebrew words have real semantic ranges — honor that.
3. **Document every departure.** When you use a rendering other than the default, add a `translator_notes` entry explaining why. Example: "Here chesed describes the Kenites' practical assistance to Israel during the Exodus — closer to 'kindness' than to covenantal 'faithful love,' since the Kenites are not in a formal covenant with Israel."
4. **The `key_terms` `rendered_as` field must match what you actually used** in the `rendering` text of that verse. Do not put the default if you used something different.
5. **Within a single book, the same context should produce the same rendering.** If nagid refers to God's appointed leader in ch 9, ch 10, and ch 13 of 1 Samuel, it should be the same English word in all three — not "prince," "ruler," and "leader" with no explanation.

### The coordination problem

When multiple agents generate chapters in parallel, they cannot see each other's choices. This is where most inconsistency originates. To prevent it:

- **Check the book's briefing addendum** (if one exists) for term decisions already made.
- **Check completed chapters** in the same book to see how recurring terms were rendered.
- **When you encounter a significant recurring term** not on this register and not in the briefing, choose a rendering and note it so subsequent chapters can match.

---

## RULE 2: expanded_rendering — Term-Focused, Not Commentary

The `expanded_rendering` field exists for ONE purpose: to explain a specific Hebrew term that carries more meaning than the English rendering can convey.

### What expanded_rendering IS

A 1-2 sentence explanation of a specific Hebrew word or phrase, starting with or quickly naming that Hebrew term, explaining its covenantal/theological depth.

**Good examples:**

```
"The Hebrew chesed — here rendered 'faithful love' — is not generic kindness. It is the loyalty that exists between parties bound in covenant relationship."
```

```
"The verb davaq ('to cling') is the same word used for the marriage bond in Genesis 2:24 and for Israel's covenant attachment to God in Deuteronomy 10:20."
```

```
"The phrase vayyiqer miqrehah ('her chance chanced') uses a deliberately redundant construction — the narrator deploys the language of randomness to describe an event the reader already knows is providential."
```

### What expanded_rendering IS NOT

- Verse-by-verse commentary
- Narrative summary or paraphrase
- Plot analysis or literary criticism
- Scene-setting or historical context
- Anything that does not name a specific Hebrew term

**Bad examples (these belong in translator_notes, not expanded_rendering):**

```
"David departed from Gath and fled to safety in the cave at Adullam."
→ This is narrative summary. Put it in translator_notes or omit it.
```

```
"This verse is the theological heart of Hannah's song."
→ This is literary commentary. Put it in translator_notes.
```

```
"The Philistine response is overwhelming and immediate."
→ This is scene analysis. Put it in translator_notes.
```

### Density target

- **5-20% of verses** in a chapter should have expanded_rendering. Not every verse.
- A chapter with 25 verses should have roughly 2-5 expanded_renderings.
- If you find yourself adding expanded_rendering to more than 1 in 4 verses, you are using the field as commentary. Stop and move the content to translator_notes.

### Self-check

Before finalizing a chapter, count your expanded_renderings. If the count exceeds 25% of the verse count, review each one and ask: "Does this start by naming a specific Hebrew term and explaining its theological depth?" If not, move it to translator_notes or delete it.

---

## RULE 3: key_terms Schema — Exact 5-Field Objects

Every entry in the `key_terms` array MUST be an object with exactly these 5 fields:

```json
{
  "hebrew": "חֶסֶד",
  "transliteration": "chesed",
  "rendered_as": "faithful love",
  "semantic_range": "steadfast love, faithful love, covenantal loyalty, lovingkindness, mercy, devotion",
  "note": "Explanation of this term's significance in this specific verse context."
}
```

### Violations that WILL be caught by automated QA

| Violation | Example | Fix |
|-----------|---------|-----|
| Bare string instead of object | `"key_terms": ["chesed"]` | Use the 5-field object |
| Wrong field names | `"register_translation"`, `"gloss"` | Use `"rendered_as"`, `"semantic_range"` |
| Missing fields | Object without `"note"` | Include all 5 fields |
| key_terms as dict instead of array | `"key_terms": {"chesed": "..."}` | Use an array `[{...}]` |

### expanded_rendering must be a string

The `expanded_rendering` field is a plain string. Never use an object like `{"text": "...", "note": "..."}`.

```json
// CORRECT
"expanded_rendering": "The Hebrew chesed means..."

// WRONG
"expanded_rendering": {"text": "The Hebrew chesed means...", "note": "..."}
```

---

## RULE 4: Cross-Chapter Consistency Checks

When generating chapters for a book, you MUST maintain consistency with previously generated chapters. Before finalizing any chapter:

1. **Check the briefing addendum** for the book (if one exists) — it contains term rendering decisions.
2. **Check completed chapters** in the same book for how recurring terms were rendered.
3. **Check the Default Term Register** (Rule 1 above) for any term that appears across books.

### Terms that commonly drift between agents

These terms are especially prone to inconsistency when parallel agents generate different chapters:

- **chesed** — agents choose "faithful love," "steadfast love," "loyal kindness," or "covenant loyalty"
- **nagid** — agents choose "leader," "ruler," "prince," or "commander"
- **go'el** — agents choose "redeemer" or "kinsman-redeemer"
- **Philistine titles** (sarnei) — agents choose "rulers," "lords," or "tyrants"
- **cherem** — agents choose "devoted to destruction," "utterly destroyed," or "banned"

The Default Term Register provides the starting point. Use its defaults unless the context genuinely demands variation — and if you vary, document it.

### Recurring narrative formulas

Some phrases recur across chapters and must be rendered identically each time:

- Judges refrain: "In those days there was no king in Israel; everyone did what was right in his own eyes" — must be word-for-word identical in every occurrence (Judges 17:6, 18:1, 19:1, 21:25).
- **Regnal death formula** (vayyishkav im avotav): **"X slept with his fathers"** — not "rested with his ancestors," not "lay down with his ancestors." Same Hebrew, same rendering, every time.
- **Succession formula** (vayyimlokh tachtav): **"X reigned in his place"** — not "became king in his place."
- **Prophetic messenger formula** (ko amar YHWH): **"This is what the LORD says"** — rendered identically every time.
- **Temple inner sanctuary** (qodesh ha-qodashim): **"Holy of Holies"** — not "Most Holy Place." The Hebrew superlative construct ("the holy of holies") is preserved in this literal rendering.

---

## RULE 5: Preamble Requirements

Every chapter gets a first-pass preamble with exactly 4 fields:

```json
"preamble": {
  "summary": "1-3 sentences: what happens in this chapter.",
  "remarkable": "What makes this chapter theologically or literarily distinctive.",
  "friction": "Translation challenges — specific Hebrew terms or constructions that resist clean English rendering, and how we handled them.",
  "connections": "How this chapter connects to other Scripture — specific cross-references, not vague gestures."
}
```

### Preamble quality rules

- **summary**: Factual, concise, no interpretation. Just what happens.
- **remarkable**: Must identify something specific — a Hebrew wordplay, a structural pattern, a theological concept. Not "this chapter is important."
- **friction**: Must name specific Hebrew terms and explain the translation decision. Not "the Hebrew is difficult here."
- **connections**: Must cite specific passages (e.g., "Genesis 12:10," not "the Genesis narratives"). Cross-references should be precise.

---

## RULE 6: Run QA Before Declaring Complete

After generating a chapter, run the automated QA script:

```bash
python3 scripts/qa_validate.py <book>/chapter-XX.json
```

The script checks:
1. JSON integrity
2. Verse numbering
3. Required fields present
4. No KJV pass-through (>92% similarity)
5. No boilerplate translator notes
6. No archaic language
7. Meta fields correct (prompt_version ≥ 1.3, license CC-BY-4.0)
8. key_terms schema (list of 5-field dicts, correct field names)
9. expanded_rendering type (must be string, not object)

**A chapter is not complete until the QA script reports PASS.**

After completing all chapters of a book, run:

```bash
python3 scripts/qa_validate.py <book>/
```

to verify the entire book passes.

---

## Summary of Multi-Agent Failure Modes

These are the specific failures that occur when parallel agents generate chapters independently:

| Failure | Root Cause | Prevention |
|---------|-----------|------------|
| Same Hebrew term rendered 3 different ways in the same context | Each agent picks independently | Use Default Term Register; document departures (Rule 1) |
| expanded_rendering on 90%+ of verses | Agent treats ER as commentary field | Follow density target of 5-20% (Rule 2) |
| key_terms as bare strings or wrong field names | Agent uses a different schema | Use exact 5-field schema (Rule 3) |
| Recurring formulas rendered differently (regnal, prophetic, temple terms) | Agents don't check each other's work | Use locked formulas in Rule 4; check completed chapters |
| expanded_rendering as object instead of string | Schema confusion | Always use plain string (Rule 3) |

---

*This document supplements the master generation prompt, addendum v1.2, and quality correction addendum v1.3. All rules in those documents remain in effect. These rules address additional issues identified during QA of Judges, Ruth, and 1 Samuel.*
