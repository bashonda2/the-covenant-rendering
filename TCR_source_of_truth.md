# The Covenant Rendering — Source of Truth

*What are we building, and what's the current status?*

**Owner:** Aaron Blonquist
**Created:** 2026-02-27
**Last updated:** 2026-03-28
**Version:** 2.3

---

## System Reference

| Document | File | Question It Answers |
|---|---|---|
| **Source of Truth** | **`TCR_source_of_truth.md`** | **What are we building? What's the current status?** |
| Data Reference | `TCR_data_reference.md` | What data exists? What are the schemas and terms? |
| Quality Contract | `TCR_quality_contract.md` | What must be true for output to be correct? |
| Operational Playbook | `TCR_operational_playbook.md` | How do we generate, deploy, and operate? |

### Governing Prompt Documents

| Document | Path | Purpose |
|---|---|---|
| Master Generation Prompt | [`prompts/covenant_rendering_prompt.md`](prompts/covenant_rendering_prompt.md) | Translation philosophy, output format, consistency rules, quality standards |
| Addendum v1.2 | [`prompts/covenant_rendering_addendum_v1.2.md`](prompts/covenant_rendering_addendum_v1.2.md) | Theologically Rich Terms Register, expanded_rendering rules, term definitions |
| Quality Correction Addendum v1.3 | [`prompts/quality-correction-addendum-v1.3.md`](prompts/quality-correction-addendum-v1.3.md) | Three non-negotiable quality rules: no KJV pass-through, no boilerplate notes, consistent modernization |
| QA Agent Prompt | [`prompts/qa_agent_prompt.md`](prompts/qa_agent_prompt.md) | QA validation rules, verdict format, two-agent pipeline enforcement |
| Leviticus Briefing | [`prompts/leviticus-briefing-addendum.md`](prompts/leviticus-briefing-addendum.md) | Leviticus-specific vocabulary, offerings, purity, watch chapters, tone guidance |
| Joshua Briefing | [`prompts/joshua-briefing-addendum.md`](prompts/joshua-briefing-addendum.md) | Joshua-specific vocabulary, conquest/cherem, land allotment, watch chapters, tone guidance |

---

## Current State

- **Status:** Pentateuch + Joshua complete — 211/1,189 chapters (17.7%), 6,508 verses, all passing automated QA.
- **Quality:** All 103 scaffold chapters remediated via two-agent pipeline. Joshua 24/24 chapters passed QA (zero KJV pass-through, zero boilerplate, zero archaisms, key_terms schema validated). 0 QA failures across all books.
- **Website:** thecovenantrendering.com live — 220 pages across 6 books (Pentateuch + Joshua). Full Bible architecture deployed: 86 books registered (66 standard + 20 Extended Library), section-grouped mega-menu, `/books` Library page, data-driven home/about pages. Multi-source manuscript comparison model (`alternateEditions`) in place for future scholarly stacking feature.
- **Documentation:** SOT restructured to 4-document architecture (2026-03-28).
- **Repos:** Data repo and site repo current, both pushed.
- **Next:** Begin Judges (21 chapters, 618 verses).

---

## 1. Vision and Core Commitments

The Covenant Rendering is a complete, modern English rendering of the Bible — Old Testament and New Testament — translated directly from the original Hebrew and Greek source texts. It is the first AI-generated Bible rendering with fully documented translation decisions at every verse, released as open-source structured data.

### Three audiences, served equally

1. **General readers** — clean, modern English scripture without losing theological depth.
2. **Bible students and scholars** — transparent, documented translation decisions visible at every verse.
3. **Developers and builders** — structured, machine-readable Bible data free of licensing restrictions.

### Core commitments

- **Ecumenical.** Not affiliated with any denomination, church, or religious organization.
- **Transparent.** Every translation decision is documented. Nothing is hidden.
- **Open source.** CC-BY-4.0. Anyone can use, share, adapt, and build upon it.
- **AI-generated with full disclosure.** Produced by Claude (Anthropic). Generation prompts included in the repository.

### Two-Layer Architecture

Every verse exists in two layers: a **Reading Layer** (`rendering` field — clean modern English, no Hebrew, no jargon) and a **Study Layer** (`text_hebrew`, `text_kjv`, `translator_notes`, `key_terms`, `expanded_rendering` — optional depth for those who want it). A Bible app can show just the rendering; a study tool can surface the full apparatus; a developer can query any field.

---

## 2. Translation Philosophy

The full translation philosophy is documented in [`prompts/covenant_rendering_prompt.md`](prompts/covenant_rendering_prompt.md). The core principles are:

1. **Translate from the Hebrew, not from the KJV.** The KJV is a reference for readers, not a source text. The rendering must be independently produced from the Hebrew.

2. **Formal equivalence with clarity.** Word-for-word as the baseline, but natural English takes priority over wooden literalism.

3. **Preserve ambiguity when it exists in the source.** If the Hebrew is genuinely ambiguous, do not resolve it — render it ambiguously and document the options.

4. **Modernize vocabulary, not theology.** Replace archaic English with modern equivalents without changing theological meaning.

5. **Preserve key theological terms consistently.** LORD for YHWH, God for Elohim, covenant for berit, etc. Full consistency table in the master prompt.

6. **Render Hebrew idioms meaningfully.** Translate the meaning, not the surface grammar. Document the original idiom in translator notes.

7. **Render poetry as poetry.** Preserve parallelism, line breaks, and the rhythm of Hebrew verse. Do not flatten poetry into prose.

8. **Document everything.** Every significant translation decision is explained in the notes. Honest about ambiguity: "The Hebrew here is uncertain" is a valid note.

---

## 3. Progress Tracker

| Book | Chapters | Verses | Status | QA Status |
|---|---|---|---|---|
| **Genesis** | 50/50 | 1,534 | Complete | Passed. Amendment pass complete. |
| **Exodus** | 40/40 | 1,213 | Complete | All chapters passed QA. Watch chapters (12, 20, 24, 32, 33, 34, 40) received A/A+ grades. |
| **Leviticus** | 27/27 | 859 | Complete | Watch chapters (16, 17, 19) quality-passed. All chapters remediated. |
| **Numbers** | 36/36 | 1,288 | Complete | All chapters remediated. Verse offsets handled in ch16-17, 29-30. |
| **Deuteronomy** | 34/34 | 956 | Complete | All chapters remediated. Verse offsets handled in ch5, 12-13, 22-23, 28-29. |
| **Joshua** | 24/24 | 658 | Complete | All chapters passed QA. Watch chapters (1, 2, 5, 6, 7, 10, 13-21, 23, 24) received detailed attention. |
| Judges | 0/21 | 0/618 | Not started | — |
| Ruth | 0/4 | 0/85 | Not started | — |
| 1 Samuel | 0/31 | 0/810 | Not started | — |
| 2 Samuel | 0/24 | 0/695 | Not started | — |
| 1 Kings | 0/22 | 0/816 | Not started | — |
| 2 Kings | 0/25 | 0/719 | Not started | — |
| 1 Chronicles | 0/29 | 0/942 | Not started | — |
| 2 Chronicles | 0/36 | 0/822 | Not started | — |
| Ezra | 0/10 | 0/280 | Not started | — |
| Nehemiah | 0/13 | 0/406 | Not started | — |
| Esther | 0/10 | 0/167 | Not started | — |
| Job | 0/42 | 0/1,070 | Not started | — |
| Psalms | 0/150 | 0/2,461 | Not started | — |
| Proverbs | 0/31 | 0/915 | Not started | — |
| Ecclesiastes | 0/12 | 0/222 | Not started | — |
| Song of Solomon | 0/8 | 0/117 | Not started | — |
| Isaiah | 0/66 | 0/1,292 | Not started | — |
| Jeremiah | 0/52 | 0/1,364 | Not started | — |
| Lamentations | 0/5 | 0/154 | Not started | — |
| Ezekiel | 0/48 | 0/1,273 | Not started | — |
| Daniel | 0/12 | 0/357 | Not started | — |
| Hosea | 0/14 | 0/197 | Not started | — |
| Joel | 0/3 | 0/73 | Not started | — |
| Amos | 0/9 | 0/146 | Not started | — |
| Obadiah | 0/1 | 0/21 | Not started | — |
| Jonah | 0/4 | 0/48 | Not started | — |
| Micah | 0/7 | 0/105 | Not started | — |
| Nahum | 0/3 | 0/47 | Not started | — |
| Habakkuk | 0/3 | 0/56 | Not started | — |
| Zephaniah | 0/3 | 0/53 | Not started | — |
| Haggai | 0/2 | 0/38 | Not started | — |
| Zechariah | 0/14 | 0/211 | Not started | — |
| Malachi | 0/4 | 0/55 | Not started | — |
| Matthew | 0/28 | 0/1,071 | Not started | — |
| Mark | 0/16 | 0/678 | Not started | — |
| Luke | 0/24 | 0/1,151 | Not started | — |
| John | 0/21 | 0/879 | Not started | — |
| Acts | 0/28 | 0/1,007 | Not started | — |
| Romans | 0/16 | 0/433 | Not started | — |
| 1 Corinthians | 0/16 | 0/437 | Not started | — |
| 2 Corinthians | 0/13 | 0/257 | Not started | — |
| Galatians | 0/6 | 0/149 | Not started | — |
| Ephesians | 0/6 | 0/155 | Not started | — |
| Philippians | 0/4 | 0/104 | Not started | — |
| Colossians | 0/4 | 0/95 | Not started | — |
| 1 Thessalonians | 0/5 | 0/89 | Not started | — |
| 2 Thessalonians | 0/3 | 0/47 | Not started | — |
| 1 Timothy | 0/6 | 0/113 | Not started | — |
| 2 Timothy | 0/4 | 0/83 | Not started | — |
| Titus | 0/3 | 0/46 | Not started | — |
| Philemon | 0/1 | 0/25 | Not started | — |
| Hebrews | 0/13 | 0/303 | Not started | — |
| James | 0/5 | 0/108 | Not started | — |
| 1 Peter | 0/5 | 0/105 | Not started | — |
| 2 Peter | 0/3 | 0/61 | Not started | — |
| 1 John | 0/5 | 0/105 | Not started | — |
| 2 John | 0/1 | 0/13 | Not started | — |
| 3 John | 0/1 | 0/15 | Not started | — |
| Jude | 0/1 | 0/25 | Not started | — |
| Revelation | 0/22 | 0/404 | Not started | — |

**Total Bible:** 1,189 chapters. 31,102 verses. 211/1,189 chapters complete (17.7%). Pentateuch + Joshua complete.

---

## 4. Future Roadmap

### Completed

- Genesis translated (50 chapters, 1,534 verses) — on site
- Exodus translated (40 chapters, 1,213 verses) — on site
- Leviticus translated (27 chapters, 859 verses) — on site
- Numbers translated (36 chapters, 1,288 verses) — on site
- Deuteronomy translated (34 chapters, 956 verses) — on site
- **Full Pentateuch complete** — 187 chapters, 5,850 verses, all passing automated QA
- **Joshua complete** — 24 chapters, 658 verses, all passing automated QA (first historical book) — on site
- All 103 scaffold chapters remediated via two-agent pipeline
- thecovenantrendering.com launched — 220 pages live (6 books)
- **Full Bible architecture deployed** — 86 books registered (66 standard + 20 Extended Library), expanded `BookInfo` data model with testament/section/tier/order/canons/sourceText/status/alternateEditions, section-grouped mega-menu navigation, `/books` Library page with progress tracking, data-driven home and about pages
- **Multi-source manuscript comparison model** — `alternateEditions` field on key books (Genesis, Isaiah, Psalms, Daniel, Esther, Jeremiah) ready for scholarly stacking feature
- SSL, Nginx, deploy pipeline operational
- tcr-site GitHub repo created and pushed
- EVM integration live (verse toggle feature)
- SOT restructured to 4-document architecture (2026-03-28)

### Near-term
- **Judges** (21 chapters, 618 verses) — second historical book
- Continue historical books (Ruth through Esther)
- EveryVerseMatters.com integration — TCR as the house translation for EVM, the primary downstream consumer of this rendering

### Medium-term
- Historical books (Judges through Esther)
- Psalms (major poetry — parallelism handling is critical)
- Wisdom literature (Job, Proverbs, Ecclesiastes, Song of Solomon)
- Prophets (chesed, teshuvah, shalom, kavod territory)

### Long-term
- New Testament (source text shifts from WLC to SBLGNT)
- Greek Theologically Rich Terms Register (parallel to Hebrew register)
- Complete standard Bible (66 books)
- Extended Library: Deuterocanonical/Apocrypha, Orthodox additions, Ethiopian canon, Dead Sea Scrolls
- Multi-source version tabs on chapter pages (scholarly stacking UI)
- Canon filter UI on `/books` page (Protestant / Catholic / Orthodox / Ethiopian / All)
- DSS fragment viewer for partial-chapter rendering

### Tooling (as needed)
- Automated validation scripts for batch QA
- Concordance generation across completed books
- Cross-reference database
- Site search (Pagefind or equivalent — warranted with 6 books / 220 pages)
- Individual verse permalinks (`/genesis/1/1`) for SEO and sharing
- PDF/print generation pipeline
- Search across all texts

---

## 5. Project Information

| Field | Value |
|---|---|
| **Project name** | The Covenant Rendering |
| **Creator** | Aaron Blonquist |
| **Contact (public)** | contact@thecovenantrendering.com |
| **Contact (personal)** | aaronblonquist@gmail.com |
| **License** | CC-BY-4.0 |
| **AI model** | Claude (Anthropic) |
| **Source text (OT)** | Westminster Leningrad Codex (WLC) |
| **Source text (NT)** | SBL Greek New Testament (SBLGNT) |
| **Reference text** | King James Version (KJV) |
| **Prompt version** | 1.3 |
| **Data repo** | https://github.com/bashonda2/the-covenant-rendering (`~/The Covenant Rendering/`) |
| **Website repo** | https://github.com/bashonda2/tcr-site (`~/TCR/`) |
| **Live site** | https://thecovenantrendering.com |
| **VPS** | 209.74.80.143 (`ssh root@209.74.80.143`) |
| **Web root** | `/var/www/tcr/` |

### Attribution

When using The Covenant Rendering, credit:

> The Covenant Rendering by Aaron Blonquist. Licensed under CC-BY-4.0.

---

## 6. Change Log

| Date | Changes |
|---|---|
| 2026-03-29 | **Full Bible architecture deployed:** Expanded BookInfo data model (86 books registered: 66 standard + 20 Extended Library). Section-grouped mega-menu navigation. New `/books` Library page with progress bar. Home page and about page now data-driven from BOOKS registry. Joshua deployed to site (24 chapters, 220 total pages). Multi-source `alternateEditions` model in place for future scholarly stacking. Site committed and pushed to GitHub. |
| 2026-03-28 | **Joshua complete:** 24/24 chapters, 658 verses, all passing automated QA. First historical book. Watch chapters (1, 2, 5, 6, 7, 10, 13-21, 23, 24) received detailed attention. key_terms schema validated across all chapters. SOT and README updated. |
| 2026-03-28 | Joshua kickoff: briefing addendum created (`prompts/joshua-briefing-addendum.md`), `joshua/` directory created, SOT updated. First historical book. |
| 2026-03-28 | SOT restructured from 1 document (783 lines) to 4-document architecture per SOT Style Guide best practices. Qere/Ketiv bracket convention corrected to match WLC/BHS standard in Deut 28:30, QA prompt, and all SOT references. |
| 2026-03-15 | All 103 scaffold chapters remediated. Full Pentateuch passes automated QA: 187/187 chapters. Website updated with dynamic routes and Books dropdown nav. |
| 2026-03-04 | Exodus ch2-10 regenerated with v1.3 quality rules. Quality Correction Addendum created. |
| 2026-02-27 | Project created. Genesis complete. SOT established. |

---

*"The heavens declare the glory of God, and the sky above proclaims the work of his hands." — Psalm 19:1*

---

*Version 2.3 — 2026-03-29*
