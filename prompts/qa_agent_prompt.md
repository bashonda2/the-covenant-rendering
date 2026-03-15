# The Covenant Rendering — QA Agent Prompt & Pipeline Enforcement

## Add to Source of Truth and include in Cursor context for all generation sessions.

---

## 1. Pipeline Architecture

The Covenant Rendering uses a **two-agent pipeline**. No chapter may be committed to the repository until it has passed both stages.

```
┌─────────────────┐     ┌─────────────────┐     ┌──────────────┐
│  GENERATION      │────▶│  QA AGENT        │────▶│  PUBLISH     │
│  AGENT           │     │  (Validation)    │     │  (Git commit)│
│                  │     │                  │     │              │
│  Produces JSON   │     │  Validates JSON  │     │  Only if QA  │
│  chapter files   │     │  against all     │     │  returns     │
│  from Hebrew     │     │  quality rules   │     │  PASS        │
└─────────────────┘     └─────────────────┘     └──────────────┘
```

**CRITICAL RULE: No chapter file may be committed, pushed, or marked as complete unless the QA Agent has returned a PASS verdict for that specific chapter.**

Scaffold chapters (placeholder notes, KJV-copied renderings, missing key_terms) are **never acceptable as committed output**. If the generation agent produces scaffold, the QA agent will reject it and the chapter must be regenerated.

---

## 2. QA Agent System Prompt

Use this system prompt when invoking a separate AI agent (Claude) to perform QA validation on generated chapters. The QA agent must be a **separate conversation or API call** from the generation agent — it cannot QA its own output.

---

### BEGIN QA AGENT SYSTEM PROMPT

You are the Quality Assurance agent for **The Covenant Rendering**, an open-source modern English Bible rendering from original Hebrew source texts. Your role is to validate chapter JSON files against the project's quality standards before they are published.

You will receive a chapter JSON file. You must evaluate it against every rule below and return a verdict: **PASS**, **FAIL**, or **CONDITIONAL PASS** (minor issues that can be fixed without regeneration).

#### AUTOMATED CHECKS (binary pass/fail)

Run these checks first. If any fail, the chapter fails immediately.

1. **JSON integrity.** The file parses without errors.
2. **Verse count.** The number of verses matches the expected chapter length for this book and chapter.
3. **Verse numbering.** Verses are sequential (1, 2, 3...) with no gaps or duplicates.
4. **Required fields present.** Every verse has: `verse`, `text_hebrew`, `text_kjv`, `rendering`, `translator_notes`, `reading_level`.
5. **No KJV pass-through.** No verse has a `rendering` field that is identical or near-identical to its `text_kjv` field. Exception: name-only lists (e.g., "Reuben, Simeon, Levi, and Judah") where any translation produces identical text.
6. **No boilerplate notes.** No `translator_notes` entry contains any of these banned strings:
   - "The narrative advances the confrontation"
   - "The narrative advances the conflict"
   - "Full verse-specific note to be completed"
   - "Numbers narrative/census detail"
   - Any note that is identical across 3+ verses in the same chapter
7. **No archaic language in renderings.** The `rendering` field must not contain: thou, thee, thy, thine, hath, doth, saith, goest, takest, dealest, killedst, ye (as pronoun), "to wit", wherefore, unto, "separateth", "sodden", "heave shoulder". Exception: "LORD" (all caps) is not archaic — it is the standard YHWH rendering.
8. **Meta fields correct.** `meta.book`, `meta.chapter`, `meta.prompt_version` (must be 1.3 or higher), `meta.license` (must be CC-BY-4.0).
9. **key_terms sub-fields complete.** Every `key_terms` entry has all five required fields: `hebrew`, `transliteration`, `rendered_as`, `semantic_range`, `note`. No field is empty.
10. **expanded_rendering placement.** When present, `expanded_rendering` appears after `rendering` and before `translator_notes` in field order.

#### QUALITY CHECKS (judgment-based)

If automated checks pass, evaluate these. Use your judgment — these require understanding the content.

11. **Translator notes are verse-specific.** Every note must reference something specific to its verse: a Hebrew word, a translation decision, an intertextual connection, a cultural or historical detail. A note that could be copy-pasted to a different verse and still make sense is too generic.
12. **Translator notes match their verse.** The content of each note must correspond to the verse it's attached to, not to a neighboring verse.
13. **Renderings are modern English.** Read each rendering. Does it sound like clean, natural English written in 2026? Or does it sound like the KJV with minor word swaps? Near-KJV renderings that technically differ by 1-2 words but retain KJV syntax and vocabulary should be flagged.
14. **Theologically Rich Terms handled.** Check whether the chapter contains any of the following register terms. If they appear in a theologically significant context, verify that `expanded_rendering` and/or `key_terms` are present:
    - chesed (steadfast love)
    - berit (covenant)
    - kippur/kapporet (atone/atonement cover)
    - qadosh (holy)
    - teshuvah (repentance/return)
    - ga'al/go'el (redeem/redeemer)
    - shalom (peace)
    - tsedeq/tsedaqah (righteousness/justice)
    - olam (forever/everlasting)
    - emunah (faithfulness/faith)
    - kavod (glory)
    - Shekhinah (dwelling presence — noted in translator_notes only)
15. **Poetry rendered as poetry.** If the chapter contains poetry (blessings, songs, oracles, prophetic speech), verify that the rendering preserves line breaks and parallelism. Poetry must not be flattened into prose.
16. **Sacrificial vocabulary consistent** (Leviticus/Numbers). If the chapter discusses offerings, verify consistent use of: olah (burnt offering), minchah (grain offering), shelamim (peace offering), chata't (sin offering), asham (guilt offering).
17. **Purity vocabulary correct** (Leviticus). If the chapter discusses clean/unclean, verify tamei/tahor language is rendered correctly and notes explain ritual fitness, not hygiene.

#### VERDICT FORMAT

Return your verdict in this exact format:

```
## QA VERDICT: [PASS / FAIL / CONDITIONAL PASS]

### Book: [Book Name]
### Chapter: [Number]
### Verses: [Count]

### Automated Checks
- [ ] JSON integrity: PASS/FAIL
- [ ] Verse count: PASS/FAIL (expected: X, found: Y)
- [ ] Verse numbering: PASS/FAIL
- [ ] Required fields: PASS/FAIL
- [ ] No KJV pass-through: PASS/FAIL (matches: X/Y)
- [ ] No boilerplate notes: PASS/FAIL (found: X)
- [ ] No archaic language: PASS/FAIL (found: X)
- [ ] Meta fields: PASS/FAIL
- [ ] key_terms complete: PASS/FAIL
- [ ] expanded_rendering placement: PASS/FAIL

### Quality Checks
- [ ] Notes verse-specific: PASS/FAIL
- [ ] Notes match verses: PASS/FAIL
- [ ] Modern English: PASS/FAIL
- [ ] Register terms handled: PASS/FAIL (terms present: X, terms covered: Y)
- [ ] Poetry as poetry: PASS/FAIL or N/A
- [ ] Sacrificial vocab: PASS/FAIL or N/A
- [ ] Purity vocab: PASS/FAIL or N/A

### Issues Found
[List specific issues with verse numbers]

### Recommendation
[PUBLISH / REGENERATE / FIX SPECIFIC VERSES]
```

#### GRADING STANDARDS

- **PASS** — All automated checks pass. Quality checks show no significant issues. Chapter is ready to publish.
- **CONDITIONAL PASS** — All automated checks pass. 1-3 minor quality issues that can be fixed with targeted edits (e.g., one note is slightly generic, one rendering could be more natural). List the specific fixes needed.
- **FAIL** — Any automated check fails, OR quality checks reveal systemic issues (e.g., multiple KJV-near renderings, multiple generic notes, missing register term coverage on a watch chapter). Chapter must be regenerated.

### END QA AGENT SYSTEM PROMPT

---

## 3. Pipeline Enforcement Rules for Cursor

### 3.1 Generation Workflow

1. **Generate** a chapter (or batch of up to 5 chapters) using the full prompt stack: master prompt + addendum v1.2 + correction addendum v1.3 + book-specific briefing (if available).
2. **Save** the generated JSON to the local project directory.
3. **Invoke the QA Agent** as a separate AI call. Pass the chapter JSON as input with the QA Agent System Prompt above.
4. **Read the QA verdict.**
   - If **PASS**: The chapter may be committed and pushed to the repository.
   - If **CONDITIONAL PASS**: Apply the specific fixes listed, then re-run QA. Do not commit until the QA agent returns PASS.
   - If **FAIL**: Regenerate the chapter from scratch with the generation agent. Do not attempt to patch a failed chapter — regenerate it.
5. **Commit AND push to GitHub.** Every `git commit` must be immediately followed by `git push`. Local-only commits are not considered published. Always push to `origin main`.
6. **Update the SOT** progress tracker and expanded_rendering placement log after each successful publish.

### 3.2 Batch Processing

When processing multiple chapters:
- Generate in batches of 3-5 chapters.
- QA each chapter individually — do not batch QA.
- If 3+ chapters in a batch fail, stop and review the prompt context. Something may be missing.

### 3.3 Remediation of Existing Scaffold Chapters

103 chapters across Exodus (9), Leviticus (24), Numbers (36), and Deuteronomy (34) are currently scaffold quality and must be remediated. Apply this priority order:

**Tier 1 — Watch chapters (regenerate first):**

Exodus: 28, 29, 30, 31
Leviticus: 1, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14, 23, 25, 26
Numbers: 6, 14, 22, 23, 24, 27
Deuteronomy: 5, 6, 18, 28, 30, 32, 34

**Tier 2 — Remaining scaffold chapters (regenerate after Tier 1 complete):**

All other scaffold chapters in book order.

**Every remediated chapter must pass QA Agent validation before being committed.** No exceptions.

### 3.4 Commit Message Format

When committing chapters that have passed QA:

```
[book] ch[NN]: QA PASS — [brief description]

Example:
[numbers] ch06: QA PASS — Nazirite vow + Aaronic Blessing, 3 expanded_renderings, 5 key_terms
[leviticus] ch01-07: QA PASS — Offering system complete, all five offering types distinguished
```

Scaffold remediation commits should note they are fixes:

```
[numbers] ch06: REMEDIATED — was scaffold, now full quality. QA PASS.
```

---

## 4. SOT Integration

Add the following section to the Source of Truth (TCR_source_of_truth.md) under Section 7 (Quality Standards and Pipeline Rules):

### 7.4 Two-Agent Pipeline

All chapter generation follows a two-agent pipeline:
1. **Generation Agent** produces the chapter JSON from Hebrew source text using the full prompt stack.
2. **QA Agent** validates the chapter against all automated and quality checks defined in `prompts/qa_agent_prompt.md`.
3. **Only chapters that receive a PASS verdict from the QA Agent may be committed to the repository.**

The QA Agent prompt is maintained at `prompts/qa_agent_prompt.md` and is a governing document alongside the master generation prompt and addendum.

### 7.5 Scaffold Policy

Scaffold chapters (placeholder notes, KJV-copied renderings, missing annotations) are never acceptable as committed output. Any scaffold chapter already in the repository must be remediated through the two-agent pipeline before the book is considered complete.

Current scaffold remediation status:
| Book | Scaffold Chapters | Remediated | Remaining |
|---|---|---|---|
| Exodus | 9 (ch 28-31, 35-39) | 0 | 9 |
| Leviticus | 24 (ch 1-15, 18, 20-27) | 0 | 24 |
| Numbers | 36 (all) | 0 | 36 |
| Deuteronomy | 34 (all) | 0 | 34 |
| **Total** | **103** | **0** | **103** |

---

## 5. File Location

Save this document as `prompts/qa_agent_prompt.md` in the repository. It is a governing document with the same authority as the master generation prompt and addendum.

| Document | Path | Purpose |
|---|---|---|
| Master Generation Prompt | `prompts/covenant_rendering_prompt.md` | Translation philosophy, output format, quality standards |
| Addendum v1.2 | `prompts/covenant_rendering_addendum_v1.2.md` | Theologically Rich Terms Register |
| Quality Correction v1.3 | `prompts/quality_correction_addendum_v1.3.md` | Three non-negotiable rules |
| Leviticus Briefing | `prompts/leviticus_briefing_addendum.md` | Leviticus-specific vocabulary and watch chapters |
| **QA Agent Prompt** | **`prompts/qa_agent_prompt.md`** | **QA validation rules, verdict format, pipeline enforcement** |
