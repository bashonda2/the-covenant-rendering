# The Covenant Rendering — Quality Contract

*What must be true for output to be correct?*

**Owner:** Aaron Blonquist
**Created:** 2026-02-27
**Last updated:** 2026-03-28
**Version:** 2.0

---

## System Reference

| Document | File | Question It Answers |
|---|---|---|
| Source of Truth | `TCR_source_of_truth.md` | What are we building? What's the current status? |
| Data Reference | `TCR_data_reference.md` | What data exists? What are the schemas and terms? |
| **Quality Contract** | **`TCR_quality_contract.md`** | **What must be true for output to be correct?** |
| Operational Playbook | `TCR_operational_playbook.md` | How do we generate, deploy, and operate? |

---

## 1. Three Non-Negotiable Rules

These rules were established during the Exodus generation process after QA identified systemic issues in early chapters. They are permanent and apply to all future generation:

**Rule 1: No KJV pass-through.** Every rendering must be independently translated from the Hebrew sense. The `rendering` field must never be a copy or near-copy of the `text_kjv` field. The only permitted exception is name-only verses (e.g., "Reuben, Simeon, Levi, and Judah") where any translation produces identical text.

**Rule 2: No boilerplate translator notes.** Every `translator_notes` entry must be specific to its verse — explaining what is happening in *that verse*, what Hebrew features are present, what translation decisions were made, and what the reader should know. Generic notes like "The narrative advances the confrontation between divine promise and imperial power" are prohibited.

**Rule 3: Consistent modernization.** No archaic pronouns (thou, thee, thy, ye), no archaic verb forms (hast, hath, goest, takest, shalt), no archaic vocabulary (unto, behold used reflexively, "to wit," wherefore) in the `rendering` field. Clean, modern English throughout.

---

## 2. Validation Checks (automated)

- JSON parses without errors
- Verse count matches expected chapter length
- All required fields present on every verse
- Verse numbering is sequential (1, 2, 3...)
- `rendering` does not match `text_kjv` verbatim
- `translator_notes` does not contain known boilerplate strings
- `expanded_rendering` is present on all targeted register-term verses
- `key_terms` entries have all required sub-fields (`hebrew`, `transliteration`, `rendered_as`, `semantic_range`, `note`)
- `meta.book` and `meta.chapter` match the filename
- Qere/Ketiv notation in `text_hebrew` follows WLC convention: Ketiv in square brackets `[...]`, Qere in parentheses `(...)`, Ketiv appearing first

---

## 3. Two-Agent Pipeline

All chapter generation follows a two-agent pipeline. No chapter may be committed, pushed, or marked as complete unless it has passed both stages:

1. **Generation Agent** produces the chapter JSON from Hebrew source text using the full prompt stack (master prompt + addendum v1.2 + correction v1.3 + book-specific briefing if available).
2. **QA Agent** validates the chapter against all automated and quality checks defined in `prompts/qa_agent_prompt.md`. The QA Agent must be a separate AI context from the generation agent — it cannot QA its own output.
3. **Only chapters that receive a PASS verdict from the QA Agent may be committed to the repository.**

Scaffold chapters (placeholder notes, KJV-copied renderings, missing key_terms) are **never acceptable as committed output**. If the generation agent produces scaffold, the QA agent will reject it and the chapter must be regenerated.

---

## 4. Scaffold Policy

Scaffold chapters are never acceptable as committed output. Any scaffold chapter already in the repository must be remediated through the two-agent pipeline before the book is considered complete.

Scaffold remediation status (all complete):

| Book | Scaffold Chapters | Remediated | Remaining |
|---|---|---|---|
| Exodus | 9 (ch 28-31, 35-39) | **9 (all — complete)** | **0** |
| Leviticus | 24 (ch 1-15, 18, 20-27) | **24 (all — complete)** | **0** |
| Numbers | 36 (all) | **36 (all — complete)** | **0** |
| Deuteronomy | 34 (all) | **34 (all — complete)** | **0** |
| **Total** | **103** | **103** | **0** |

**Remediation priority order** (retained for future reference):

**Tier 1 — Watch chapters (regenerate first):**
- Exodus: 28, 29, 30, 31
- Leviticus: 1, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14, 23, 25, 26
- Numbers: 6, 14, 22, 23, 24, 27
- Deuteronomy: 5, 6, 18, 28, 30, 32, 34

**Tier 2 — Remaining scaffold chapters (regenerate after Tier 1 complete):**
All other scaffold chapters in book order.

---

## 5. Resolved Issues

| Date | Issue | Resolution |
|---|---|---|
| 2026-02-27 | Genesis chapters missing `expanded_rendering` on 11 key covenant verses | Amendment pass applied: 11 expanded_renderings added + ch32 key_terms normalized. Verified by automated validation. |
| 2026-03-04 | Exodus ch2-10: renderings copying KJV verbatim | All 9 chapters regenerated with independent modern English renderings. Automated check confirms 0 KJV matches (except name-only lists). |
| 2026-03-04 | Exodus ch2-10: boilerplate translator notes | All 9 chapters regenerated with verse-specific notes. Automated check confirms 0 boilerplate instances. |
| 2026-03-04 | Exodus ch2-10: inconsistent archaisms in renderings | All 9 chapters regenerated with consistent modern English. No archaic forms remain. |
| 2026-03-04 | Exodus ch7-8: Hebrew/KJV verse-number offset | Hebrew versification (WLC) used as primary, with explicit KJV alignment mapping applied during generation. Chapter files follow Hebrew chapter structure. |
| 2026-03-04 | Exodus ch7: missing `expanded_rendering` for hardening (7:3) | Added: expanded_rendering explaining chazaq/qasheh as judicial confirmation of Pharaoh's existing rebellion. |
| 2026-03-04 | Exodus ch9: missing `expanded_rendering` for sovereignty (9:16) | Added: expanded_rendering explaining he'emadtikha as God positioning Pharaoh within divine purpose. |
| 2026-03-15 | Deuteronomy 28:30: qere/ketiv bracket convention incorrect in `text_hebrew` | Original fix on 2026-03-15 reversed bracket/parenthesis assignments from WLC standard. Corrected 2026-03-28 after verification against BibleHub WLC, BHS digital editions, and tanach.us. WLC convention is: Ketiv (written) in square brackets `[ישגלנה]`, Qere (read) in parentheses `(יִשְׁכָּבֶ֔נָּה)`, Ketiv first. QA Agent prompt check #18 also corrected to match. |

---

## 6. Lessons Learned

**Exodus ch2-10 regeneration (2026-03-04).** Early Exodus chapters revealed that without explicit anti-KJV-copying rules, the generation model defaults to KJV diction when producing renderings. Nearly half the verses in some chapters were verbatim KJV pass-through. The same generation run produced boilerplate translator notes (a single generic sentence reused across dozens of verses) and inconsistent modernization (archaic forms like "thou goest" appearing alongside modern English). The Quality Correction Addendum v1.3 was created to prevent these issues permanently. All nine affected chapters were regenerated from scratch with full verse-specific renderings and notes. The lesson: quality rules must be explicit in the prompt context, not merely implied by the translation philosophy. If a failure mode is possible, it must be explicitly prohibited.

**Deuteronomy 28:30 qere/ketiv bracket convention (2026-03-15, corrected 2026-03-28).** During remediation of Deuteronomy 28, the `text_hebrew` field for verse 30 had its qere/ketiv notation fixed — but the bracket/parenthesis assignments were themselves backwards from the actual WLC standard. The original fix (2026-03-15) documented the convention as "Ketiv in parentheses, Qere in brackets," which is the reverse of how BHS/WLC digital editions actually encode it. Verification against BibleHub's WLC display, tanach.us, and the BHS digital text for Deut 28:30 confirmed the correct WLC convention: **Ketiv (written manuscript text) in square brackets `[...]`, Qere (traditional reading) in parentheses `(...)`**, Ketiv first — i.e., `[ישגלנה] (יִשְׁכָּבֶ֔נָּה)`. All SOT references and QA check #18 corrected on 2026-03-28. The lesson: formatting conventions must be verified against the actual source text editions, not assumed. When documenting a convention, cite the specific source (BHS page, WLC digital edition) rather than relying on memory or secondary descriptions.

---

## 7. Standing Decisions

| Decision | Rationale |
|---|---|
| Hebrew versification is primary | The WLC verse numbering governs chapter files. KJV verse numbers may differ (especially in Psalms, Exodus 7-8, Joel, Malachi). The `text_kjv` field maps to the correct KJV verse regardless. |
| `expanded_rendering` placement after `rendering`, before `translator_notes` | Consistent field ordering across all chapters. |
| One `translator_notes` entry minimum per verse | Ensures no verse is left without contextual documentation. |
| `key_terms` only where theologically significant | Not every verse needs key_terms. Over-annotation dilutes the value of entries that appear. |
| Reading level targets 8th-10th grade | Comparable to ESV. Accessible but not simplified. |
| Qere/Ketiv notation: Ketiv `[...]` then Qere `(...)` | Follows WLC/BHS convention (verified against BibleHub WLC, tanach.us, BHS digital editions). Ketiv (written manuscript text) in square brackets appears first; Qere (traditional reading) in parentheses appears second. Example: `[ישגלנה] (יִשְׁכָּבֶ֔נָּה)` in Deut 28:30. |

---

*Version 2.0 — 2026-03-28*
