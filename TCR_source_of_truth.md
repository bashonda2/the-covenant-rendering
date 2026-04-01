# The Covenant Rendering — Source of Truth

*What are we building, and what's the current status?*

**Owner:** Aaron Blonquist
**Created:** 2026-02-27
**Last updated:** 2026-04-01
**Version:** 3.5

---

## System Reference

| Document | File | Question It Answers |
|---|---|---|
| **Source of Truth** | **`TCR_source_of_truth.md`** | **What are we building? What's the current status?** |
| Data Reference | `TCR_data_reference.md` | What data exists? What are the schemas and terms? |
| Quality Contract | `TCR_quality_contract.md` | What must be true for output to be correct? |
| Operational Playbook | `TCR_operational_playbook.md` | How do we generate, deploy, and operate? |
| Full Roadmap | `TCR_roadmap.md` | What's the plan from now to project completion? |

### Governing Prompt Documents

| Document | Path | Purpose |
|---|---|---|
| Master Generation Prompt | [`prompts/covenant_rendering_prompt.md`](prompts/covenant_rendering_prompt.md) | Translation philosophy, output format, consistency rules, quality standards |
| Addendum v1.2 | [`prompts/covenant_rendering_addendum_v1.2.md`](prompts/covenant_rendering_addendum_v1.2.md) | Theologically Rich Terms Register, expanded_rendering rules, term definitions |
| Quality Correction Addendum v1.3 | [`prompts/quality-correction-addendum-v1.3.md`](prompts/quality-correction-addendum-v1.3.md) | Three non-negotiable quality rules: no KJV pass-through, no boilerplate notes, consistent modernization |
| QA Agent Prompt | [`prompts/qa_agent_prompt.md`](prompts/qa_agent_prompt.md) | QA validation rules, verdict format, two-agent pipeline enforcement |
| Leviticus Briefing | [`prompts/leviticus-briefing-addendum.md`](prompts/leviticus-briefing-addendum.md) | Leviticus-specific vocabulary, offerings, purity, watch chapters, tone guidance |
| Joshua Briefing | [`prompts/joshua-briefing-addendum.md`](prompts/joshua-briefing-addendum.md) | Joshua-specific vocabulary, conquest/cherem, land allotment, watch chapters, tone guidance |
| Judges Briefing | [`prompts/judges-briefing-addendum.md`](prompts/judges-briefing-addendum.md) | Judges-specific vocabulary, shofet/moshia, cyclical pattern, Song of Deborah, Samson, epilogue, tone guidance |
| Extended Library Direction | [`prompts/extended-library-direction.md`](prompts/extended-library-direction.md) | Multi-tradition stacking strategy, tier structure (manuscript/pre-Nicaea/interpretive), priority order, data model expansion, JST copyright research |
| Chapter Preamble Spec | [`prompts/chapter-preamble-specification.md`](prompts/chapter-preamble-specification.md) | Preamble format (summary, remarkable, friction, connections), tone, placement, generation instructions |
| Multi-Agent Consistency Rules | [`prompts/multi-agent-consistency-rules.md`](prompts/multi-agent-consistency-rules.md) | Locked Term Register (18 terms with single authorized renderings), expanded_rendering density rules (5-20%), key_terms schema enforcement, cross-chapter consistency checks. Addresses multi-agent generation drift. |
| Isaiah Briefing | [`prompts/isaiah-briefing-addendum.md`](prompts/isaiah-briefing-addendum.md) | Isaiah-specific vocabulary (Qedosh Yisra'el, eved YHWH, go'el as Redeemer, netser/choter/shoresh), structural guide (First/Second/Third Isaiah), sensitive-passage handling (almah 7:14, Suffering Servant 52:13-53:12, Cyrus as mashiach 45:1), prophetic formulas, poetry rendering rules |
| Jeremiah Briefing | [`prompts/jeremiah-briefing-addendum.md`](prompts/jeremiah-briefing-addendum.md) | Jeremiah-specific vocabulary (shuv dual meaning, berit chadashah, navi sheqer, shalom shalom), mixed genre handling (poetry/prose), emotional intensity preservation, New Covenant (31:31-34) sensitive-passage protocol, pittitani (20:7) confrontational rendering requirement, prophetic formulas, watch chapters |

---

## Current State

- **Status:** Jeremiah complete — 797/1,189 chapters (67.0%), 20,249 verses across 24 books, all passing automated QA. Second prophetic book done. Crossed 67%.
- **Quality:** All 797 chapters pass QA. Jeremiah generated with briefing addendum, all 52 chapters passing automated QA. 1,364 verses, 1.9 MB structured data. Key passages: New Covenant (31:31-34), pittitani (20:7), call narrative (1:5), Temple Sermon (7:4), letter to exiles (29:11), fall of Jerusalem (39, 52).
- **Website:** thecovenantrendering.com live — 691 pages across 22 books. Isaiah and Jeremiah not yet deployed.
- **Documentation:** SOT v3.5.
- **Repos:** Data repo and site repo current.
- **Next:** Remaining Prophets — Lamentations (5), Ezekiel (48), Daniel (12), plus 12 Minor Prophets (67 chapters). 132 chapters to complete the Old Testament.

---

## 1. Vision and Core Commitments

The Covenant Rendering is a complete, modern English rendering of the Bible — Old Testament and New Testament — translated directly from the original Hebrew and Greek source texts, with fully documented translation decisions at every verse, released as open-source structured data.

Beyond the standard Bible, TCR will surface how communities across 2,300 years have read the same passages — from the Dead Sea caves to the Restoration — side by side, for free, with documented translation decisions at every verse. The organizing question for every tradition included is: **"How does this tradition read this passage?"** This is not about declaring which text is "right." It is about trusting the reader with the full conversation that the biblical text has generated across centuries, languages, and faith communities.

### Three audiences, served equally

1. **General readers** — clean, modern English scripture without losing theological depth.
2. **Bible students and scholars** — transparent, documented translation decisions visible at every verse.
3. **Developers and builders** — structured, machine-readable Bible data free of licensing restrictions.

### Core commitments

- **Ecumenical.** Not affiliated with any denomination, church, or religious organization.
- **Transparent.** Every translation decision is documented. Nothing is hidden.
- **Open source.** CC-BY-4.0. Anyone can use, share, adapt, and build upon it.
- **Reproducible.** Generation prompts and methodology included in the repository.

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
| **Judges** | 21/21 | 618 | Complete | All chapters passed QA. Watch chapters (1, 2, 3, 4-5, 6-8, 9, 11, 13-16, 19, 20-21) received detailed attention. 64 key_terms, 13 expanded_renderings. Song of Deborah rendered as poetry. Post-QA: 26 schema violations fixed across 8 chapters (ch 9-10: bare-string key_terms; ch 13-16: wrong field names; ch 17, 21: object-format expanded_rendering). |
| **Ruth** | 4/4 | 85 | Complete | All chapters passed QA. 23 key_terms, 10 expanded_renderings. Full preambles. Go'el theology (ch 2-4), chesed (ch 1, 2, 3), davaq (ch 1). Genealogy to David (ch 4). |
| **1 Samuel** | 31/31 | 812 | Complete | All chapters passed QA. Hannah's Song rendered as poetry (ch 2). Key theological coverage: mashiach/anointing (ch 10, 16), cherem (ch 15), mashiach YHWH (ch 24, 26), Endor necromancy (ch 28). Post-QA remediation: nagid standardized to "leader" (was prince/ruler/leader across 4 verses), chesed standardized to "faithful love" (was loyal kindness/faithful love across 3 verses), sarnei standardized to "tyrants" (was rulers in ch 5). 151 narrative-commentary expanded_renderings pruned (336→185, density 41%→23%). |
| **2 Samuel** | 24/24 | 695 | Complete | All chapters passed QA after remediation. Davidic covenant (ch 7), David-Bathsheba (ch 11-12), Absalom rebellion (ch 13-19), David's psalm (ch 22, poetry), last words (ch 23, poetry). 227 ERs pruned (363→136, 17% density). chesed standardized across 5 chapters. Song of the Bow (ch 1) rendered as poetry. |
| **1 Kings** | 22/22 | 816 | Complete | All chapters passed QA. Temple construction and dedication (ch 5-8), Solomon's wisdom and fall (ch 3, 10-11), kingdom divided (ch 12), Elijah cycle (ch 17-19), Mount Carmel (ch 18), still small voice (ch 19), Naboth's vineyard (ch 21). 14 KJV-proximate regnal formulas rewritten. Post-audit remediation: regnal death formula standardized to "slept with his fathers" (was "rested with his ancestors" in ch 11, "lay down with his ancestors" in ch 2), succession formula standardized to "reigned in his place" (was "became king" in ch 11, 22), qodesh ha-qodashim standardized to "Holy of Holies" (was "Most Holy Place" in ch 7, 8). |
| **2 Kings** | 25/25 | 719 | Complete | All chapters passed QA. Elijah ascension (ch 2), Naaman (ch 5), Jehu's revolution (ch 9-10), Fall of Samaria with theological explanation (ch 17), Hezekiah-Sennacherib crisis (ch 18-19), Josiah's reforms and Passover (ch 22-23), Fall of Jerusalem (ch 25). End of Deuteronomistic History. Regnal formulas consistent. |
| **1 Chronicles** | 29/29 | 942 | Complete | All chapters passed QA. Genealogies (ch 1-9) with Prayer of Jabez (4:10). Chronicler's David narrative (ch 10-22). Davidic covenant (ch 17, ha-satan in ch 21). Temple personnel (ch 23-27). David's prayer and Solomon's anointing (ch 28-29). |
| **2 Chronicles** | 36/36 | 822 | Complete | All chapters passed QA. Temple dedication and 7:14 (ch 5-7), kingdom from Judah's perspective (ch 10-28), Hezekiah's revival (ch 29-32), Manasseh's repentance unique to Chronicles (ch 33), Josiah's Passover (ch 35), Cyrus decree — last words of the Hebrew Bible (ch 36). |
| **Ezra** | 10/10 | 280 | Complete | All chapters passed QA. Aramaic sections (4:8-6:18, 7:12-26) preserved with language-shift notes. Return from exile, Temple rebuilt, intermarriage crisis. |
| **Nehemiah** | 13/13 | 406 | Complete | All chapters passed QA. Wall rebuilt (ch 3-6), Torah reading (ch 8), Levites' great prayer (ch 9), covenant renewal (ch 10), Nehemiah's reforms (ch 13). |
| **Esther** | 10/10 | 167 | Complete | All chapters passed QA. No divine name injected. Providence unnamed throughout. "For such a time as this" (4:14), Purim established (ch 9). |
| **Job** | 42/42 | 1,070 | Complete | All chapters passed QA. Prose prologue/epilogue (ch 1-2, 42:7-17), poetry throughout. Ha-satan as role not name (ch 1-2). Wisdom Poem (ch 28). "I know my Redeemer lives" (19:25-27). God from the whirlwind (ch 38-41). Behemoth and Leviathan. nacham translation problem in 42:6 addressed. |
| **Psalms** | 150/150 | 2,461 | Complete | All chapters passed QA. Five books (I-V). All poetry with line breaks. Psalm 119 (176v acrostic, 8 torah-words). Key psalms: 1 (Torah), 2 (Messianic), 22 (Forsaken), 23 (Shepherd), 51 (Penitential), 89 (Davidic covenant), 110 (Melchizedek), 119 (Torah meditation), 136 (Great Hallel), 150 (Final Halleluyah). |
| **Proverbs** | 31/31 | 915 | Complete | All chapters passed QA. Woman Wisdom (ch 1, 8-9), Solomonic collections (ch 10-22, 25-29), Words of the Wise (ch 22-24), Agur (ch 30), eshet chayil acrostic (ch 31:10-31). |
| **Ecclesiastes** | 12/12 | 222 | Complete | All chapters passed QA. hevel rendered as "vapor" throughout (not "vanity"). Time poem (3:1-8), aging allegory (12:1-7). qohelet retained as Hebrew title. |
| **Song of Solomon** | 8/8 | 117 | Complete | All chapters passed QA. Love poetry rendered without allegorizing. Three wasf descriptions. "Love is as strong as death" (8:6-7) with shalhevet-yah. Hebrew versification for ch 7. |
| **Isaiah** | 66/66 | 1,292 | Complete | All chapters passed QA. Briefing addendum created. Three sections: First Isaiah (1-39, Assyrian crisis), Second Isaiah (40-55, exile comfort), Third Isaiah (56-66, restoration). almah as "young woman" (7:14) with full tradition notes. Four Servant Songs (42:1-4, 49:1-6, 50:4-9, 52:13-53:12) — both Jewish and Christian readings presented without privilege. Cyrus as mashiach (45:1). "the Holy One of Israel" always in full. go'el as "Redeemer" (capitalized) for God throughout. 95% poetry with line breaks. |
| **Jeremiah** | 52/52 | 1,364 | Complete | All chapters passed QA. Briefing addendum created. Call narrative (ch 1), Temple Sermon (ch 7), confessions (11-12, 15, 17-18, 20), potter and clay (ch 18), Righteous Branch (ch 23), letter to exiles with 29:11 (ch 29), NEW COVENANT berit chadashah (31:31-34) with both Jewish and Christian readings presented, field purchase during siege (ch 32), scroll burned (ch 36), cistern rescue (ch 38), fall of Jerusalem (ch 39, 52). pittitani (20:7) rendered as "You deceived me" without softening. Oracles against nations (ch 46-51). Historical appendix (ch 52). shuv rendered context-dependently for return/apostasy. All prophetic formulas locked. |
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

**Total Bible:** 1,189 chapters. 31,102 verses. 797/1,189 chapters complete (67.0%). Pentateuch, Historical Books, Wisdom Literature, Isaiah, and Jeremiah complete.

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
- **Judges complete** — 21 chapters, 618 verses, all passing automated QA (second historical book) — on site
- All 103 scaffold chapters remediated via two-agent pipeline
- thecovenantrendering.com launched — 242 pages live (7 books)
- **Full Bible architecture deployed** — 86 books registered (66 standard + 20 Extended Library), expanded `BookInfo` data model with testament/section/tier/order/canons/sourceText/status/alternateEditions, section-grouped mega-menu navigation, `/books` Library page with progress tracking, data-driven home and about pages
- **Multi-source manuscript comparison model** — `alternateEditions` field on key books (Genesis, Isaiah, Psalms, Daniel, Esther, Jeremiah) ready for scholarly stacking feature
- **Extended Library direction established** — Multi-tradition stacking strategy with 3 tiers (manuscript traditions, pre-Nicaea canon, interpretive traditions), 7-priority implementation order, expanded `AlternateEdition` data model
- SSL, Nginx, deploy pipeline operational
- tcr-site GitHub repo created and pushed
- EVM integration live (verse toggle feature)
- SOT restructured to 4-document architecture (2026-03-28)

### Near-term
- **Ruth** (4 chapters, 85 verses) — quick win, go'el (kinsman-redeemer) theology
- Continue historical books (1-2 Samuel through Esther)
- EveryVerseMatters.com integration — TCR as the house translation for EVM, the primary downstream consumer of this rendering

### Medium-term
- Historical books (1-2 Samuel through Esther)
- Psalms (major poetry — parallelism handling is critical)
- Wisdom literature (Job, Proverbs, Ecclesiastes, Song of Solomon)
- Prophets (chesed, teshuvah, shalom, kavod territory)

### Long-term
- New Testament (source text shifts from WLC to SBLGNT)
- Greek Theologically Rich Terms Register (parallel to Hebrew register)
- Complete standard Bible (66 books)

### Extended Library & Multi-Tradition Stacking (after base Bible substantially complete)

Full strategy: [`prompts/extended-library-direction.md`](prompts/extended-library-direction.md)

**Tradition tiers:**

| Tier | UI Label | Traditions | Pre-Nicaea? |
|---|---|---|---|
| Primary | "From the Hebrew" | TCR (WLC) — always present, always default | N/A |
| Manuscript Traditions | "Other manuscript traditions" | Dead Sea Scrolls, Septuagint (LXX), Samaritan Pentateuch | Yes (all pre-325 CE) |
| Pre-Nicaea Canon | "Books read before the councils" | 1 Enoch, Jubilees | Yes |
| Interpretive Traditions | "How traditions read this passage" | Targumim, Joseph Smith Translation (JST), Latin Vulgate | Partial |

**Implementation priority:**

| Priority | Tradition | Why First | Blocking? |
|---|---|---|---|
| 1 | Dead Sea Scrolls (Isaiah) | Highest academic impact. 1QIsaiah-a covers all 66 chapters. | — |
| 2 | 1 Enoch | Quoted in NT. Pre-Nicaea. No one else offers this comparatively. | — |
| 3 | Septuagint | The early church's Bible. Essential for NT cross-references. | — |
| 4 | JST | Core audience value. Fits in interpretive tier. | **JST copyright research required.** Verify Intellectual Reserve status on Pearl of Great Price text and JST footnotes/appendix before implementation. Do NOT use Community of Christ "Inspired Version." |
| 5 | Samaritan Pentateuch | Oldest independent Pentateuch witness. | — |
| 6 | Jubilees | Completes Pre-Nicaea pair with 1 Enoch. DSS attestation. | — |
| 7 | Targumim | Rounds out interpretive tier. Aramaic reading tradition. | — |
| 8 | Latin Vulgate | The Bible of Western Christianity for 1,000+ years. Jerome translated OT from Hebrew. | Introduces Latin as new source language. |

- Multi-source version tabs on chapter pages (scholarly stacking UI)
- Canon filter UI on `/books` page (Protestant / Catholic / Orthodox / Ethiopian / All)
- DSS fragment viewer for partial-chapter rendering

### Chapter Preambles (two-pass approach)

Full specification: [`prompts/chapter-preamble-specification.md`](prompts/chapter-preamble-specification.md)

Every chapter receives a translator's introduction with four sections: summary, what makes it remarkable, translation friction, and connections to other Scripture. Generated in two passes:

**First pass:** Generated as part of the per-book workflow immediately after chapters pass QA. Uses available translator notes, key terms, and connections to books that exist at that time.

**Second pass (after Phase 4):** Enrichment sweep updating friction and connections sections with specific references to variant readings from stacked traditions and cross-references to later books.

Infrastructure is in place: `Preamble` type in data model, optional `preamble` field on `Chapter` interface, collapsible UI on chapter pages.

### Tooling (as needed)
- Automated validation script (`scripts/qa_validate.py`) — 10 checks including JSON integrity, verse numbering, required fields, KJV pass-through detection, boilerplate detection, archaism detection, meta validation, key_terms schema validation (type checking, field name validation, required field presence), expanded_rendering type validation, and field placement
- ER pruning script (`scripts/prune_ers.py`) — Removes expanded_renderings that are narrative commentary rather than Hebrew term analysis. Uses heuristic: keeps ERs that reference Hebrew terms in the first ~120 chars; removes ERs starting with person names, narrative summary, or literary commentary. Supports `--dry-run` mode.
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
| **Methodology** | Prompts and generation workflow in `prompts/` directory |
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
| 2026-04-01 | **Jeremiah complete:** 52/52 chapters, 1,364 verses, all passing automated QA. 24th complete book. Second prophetic book. Briefing addendum created with vocabulary register (shuv, berit chadashah, navi sheqer, shalom shalom), mixed-genre handling, and sensitive-passage protocols. Key passages: call narrative with shaqed/shoqed wordplay (1:11-12), Temple Sermon with threefold mockery (7:4), confessions of Jeremiah (11:18-12:6, 15:10-21, 17:14-18, 18:18-23, 20:7-18), potter and clay (18:1-12), pittitani "You deceived me" rendered without softening (20:7), Righteous Branch tsemach tsaddiq (23:5-6), letter to exiles "plans for welfare and not disaster" (29:11), NEW COVENANT berit chadashah (31:31-34) — the only occurrence in the Hebrew Bible — with both Jewish (Torah renewed) and Christian (Hebrews 8:8-12) readings presented without privilege, field purchase during siege (32:6-15), scroll burned by Jehoiakim (36), cistern rescue by Ebed-Melech (38), fall of Jerusalem (39, 52), oracles against nations (46-51), Babylon oracle with scroll-sinking sign-act (51:59-64). Historical appendix (52) paralleling 2 Kings 25 with unique deportation numbers. 1.9 MB structured data. |
| 2026-03-31 | **Isaiah complete:** 66/66 chapters, 1,292 verses, all passing automated QA. 23rd complete book. First prophetic book. Largest prophetic book in the Bible. Briefing addendum created with term decisions, structural guide, and sensitive-passage handling. Three sections rendered: First Isaiah (1-39, Assyrian crisis), Second Isaiah (40-55, exile comfort with Servant Songs), Third Isaiah (56-66, restoration and new creation). Key passages: trisagion (6:3), almah as "young woman" (7:14) with full LXX/NT/tradition notes, four throne names (9:6), shoot from Jesse (11:1), death swallowed (25:8), resurrection (26:19), "comfort, comfort" (40:1), First Servant Song (42:1-4), Cyrus as mashiach (45:1), Fourth Servant Song (52:13-53:12) with both Jewish and Christian traditions presented, "come all who thirst" (55:1), "Spirit of the Lord upon me" (61:1), new heavens and earth (65:17). |
| 2026-03-31 | **Deep QA audit — all 22 books (679 chapters).** Term register consistency verified across all books: 1 locked-term violation fixed (sarnei "rulers" → "tyrants" in Judges 3:3), 7 legacy chesed renderings standardized ("steadfast love" → "faithful love"), 3 nagid renderings fixed ("ruler" → "leader" in 1 Chronicles), go'el capitalization corrected (Ps 19:15). 3 evil evaluation formula deviations corrected (1 Kgs 11:6, 2 Kgs 8:18, 8:27). 21 formal departure documentation notes added for contextual term variations. 232 preambles generated for Genesis through Judges (all pre-preamble books). AI attribution audit clean. ER density accepted as-is — Hebrew guides, not metrics. |
| 2026-03-30 | **Proverbs, Ecclesiastes, Song of Songs complete:** 51 chapters, 1,254 verses, all passing automated QA. 20th-22nd complete books. All Wisdom literature now done. Proverbs: Woman Wisdom speeches, eshet chayil acrostic. Ecclesiastes: hevel as "vapor", time poem, aging allegory. Song of Songs: love poetry preserved, shalhevet-yah in 8:6. Deployed to site (691 pages). |
| 2026-03-29 | **Cross-project remediation:** Joshua 16 pre-existing QA failures fixed (ER field ordering + KJV proximity in king list). Judges 11 pre-existing failures fixed. All 628 chapters now pass QA (628/628). Ezra ERs regenerated: 23 term-focused ERs added (8.2% density) after paraphrase purge. torah convention standardized project-wide: 33 instances of "Torah" transliteration replaced with "the Law" / "instruction" in rendering fields. Convention: torat Mosheh → "the Law of Moses", general torah → "instruction", sefer ha-torah → "the Book of the Law". |
| 2026-03-29 | **Psalms complete:** 150/150 chapters, 2,461 verses, all passing automated QA. 19th complete book. Largest book in the Bible. Five books (I-V), all poetry. Psalm 119 (176-verse acrostic). Deployed to site (640 pages). Crossed 50% of the Bible. |
| 2026-03-29 | **Full QA audit — all 19 books (Genesis through Psalms).** Automated QA: 583 PASS across 17 books; Joshua (5 FAIL) and Judges (11 FAIL) are pre-existing. Formula fixes applied: 1 succession (1 Chr 19:1), 3 prophetic messenger "Thus says" → "This is what the LORD says" (2 Chr 34:23-26), 1 "most holy place" → "Holy of Holies" (1 Chr 6:49), 1 grammar error (2 Chr 33:20). Ezra ERs purged: all 146 expanded_renderings were paraphrases, not term-focused — deleted entirely (52% → 0%). Psalms ERs pruned: 208 narrative-commentary ERs removed (934 → 726, 37% → 29%). Psalms density remains above 20% ceiling but all remaining ERs are genuinely term-focused Hebrew analysis. 2 Chr 33:20 KJV-proximity resolved by passive voice rewording. No model fields or AI attribution found in any new books. |
| 2026-03-29 | **Job complete:** 42/42 chapters, 1,070 verses, all passing automated QA. 18th complete book. First Wisdom book. Prose prologue/epilogue, poetry speeches throughout. Wisdom Poem (ch 28), God from the whirlwind (ch 38-41), nacham crux in 42:6. Deployed to site (490 pages). |
| 2026-03-29 | **Ezra, Nehemiah, Esther complete:** 33 chapters, 853 verses, all passing automated QA. 15th-17th complete books. All Historical Books now done (Genesis–Esther). Ezra: Aramaic sections preserved. Nehemiah: Levites' great prayer (ch 9). Esther: no divine name injected. Deployed to site (448 pages). |
| 2026-03-29 | **2 Chronicles complete:** 36/36 chapters, 822 verses, all passing automated QA. 14th complete book. Temple dedication with 7:14 (ch 7), Manasseh's repentance unique to Chronicles (ch 33), Cyrus decree closing the Hebrew Bible (ch 36). 17 KJV-proximate verses rewritten. Deployed to site (415 pages). All Historical Books now complete. |
| 2026-03-29 | **1 Chronicles complete:** 29/29 chapters, 942 verses, all passing automated QA. 13th complete book. Genealogies (ch 1-9), Chronicler's David narrative (ch 10-22), Temple personnel (ch 23-27), David's final prayer (ch 29). Deployed to site (379 pages). |
| 2026-03-29 | **2 Kings audit & remediation:** Post-generation audit found same formula inconsistencies as 1 Kings from parallel agents. Regnal death formula: 6 instances of "rested with his ancestors" (ch 8, 10, 16, 20, 21, 24) standardized to "slept with his fathers." Succession formula: 21 instances of "became king in his place" standardized to "reigned in his place" across 12 chapters. 1 instance of "succeeded him as king" (ch 1) also standardized. `model` field removed from meta in all 25 chapters (and retroactively from all 313 chapter files project-wide per Option B AI-attribution removal). 2 translator_notes/preamble formula references updated. All 25 chapters pass automated QA. ER density healthy at 5.8%, all term-focused. |
| 2026-03-29 | **AI attribution removed from reader-facing materials (Option B).** Removed "AI-generated" and "Claude (Anthropic)" references from README, SOT project description, SOT info table, generation prompts, and preamble specification tone guidance. Removed `model` field from meta in all 313 chapter JSON files project-wide. Internal process docs (QA agent prompt, quality contract, operational playbook) retain methodology references. The rendering speaks for itself; tooling provenance stays in the repo for transparency. |
| 2026-03-29 | **2 Kings complete:** 25/25 chapters, 719 verses, all passing automated QA. 12th complete book. Elijah ascension (ch 2), Naaman (ch 5), Jehu's revolution (ch 9-10), Fall of Samaria (ch 17), Hezekiah-Sennacherib (ch 18-19), Josiah's reforms (ch 22-23), Fall of Jerusalem and exile (ch 25). End of Deuteronomistic History. Deployed to site (350 pages). |
| 2026-03-29 | **1 Kings audit & remediation:** Post-generation audit found 3 formula inconsistencies from parallel agents. Regnal death formula: "rested with his ancestors" (ch 11) and "lay down with his ancestors" (ch 2) standardized to "slept with his fathers" (matching ch 14-16, 22). Succession formula: "became king in his place" (ch 11, 22) standardized to "reigned in his place" (matching ch 14-16). Temple term: qodesh ha-qodashim — "Most Holy Place" (ch 7, 8) standardized to "Holy of Holies" (matching ch 6). Multi-agent consistency rules updated with locked formulas for regnal, succession, prophetic messenger, and temple terms. Default Term Register relaxed from rigid lockdown to defaults-with-documented-variation, per project owner feedback that Hebrew semantic ranges must be honored. |
| 2026-03-29 | **1 Kings complete:** 22/22 chapters, 816 verses, all passing automated QA. 11th complete book. Temple dedication (ch 8) with full Name theology. Elijah cycle (ch 17-19) including Mount Carmel and qol demamah daqqah. Kingdom division (ch 12). 14 KJV-proximate regnal formulas rewritten. Deployed to site (325 pages). |
| 2026-03-29 | **2 Samuel complete:** 24/24 chapters, 695 verses, all passing automated QA. 10th complete book. Davidic covenant (ch 7), David-Bathsheba (ch 11-12), Absalom rebellion (ch 13-19). Post-generation remediation: 227 ERs pruned (363→136, 17% density), chesed standardized across 5 chapters, nagid→"leader" in ch 5, 3 KJV-proximate verses rewritten. Deployed to site (303 pages). |
| 2026-03-29 | **Multi-Agent Consistency Rules created & 1 Samuel/Ruth remediation:** Created `prompts/multi-agent-consistency-rules.md` — Locked Term Register (18 Hebrew terms with single authorized rendering), expanded_rendering density rules (5-20% target), key_terms schema enforcement, cross-chapter consistency protocol. Addresses root cause: parallel agents making independent rendering choices. Ruth: go'el standardized to "kinsman-redeemer" in ch 2-3 notes/ER. 1 Samuel: nagid→"leader" (4 verses), chesed→"faithful love" (3 verses), sarnei→"tyrants" (1 verse). 151 narrative-commentary ERs pruned from 1 Samuel (336→185, density 41%→23%) using `scripts/prune_ers.py`. ER pruning script added to tooling for future use. |
| 2026-03-29 | **Judges schema remediation & QA hardening:** Post-generation QA identified 26 schema violations across 8 Judges chapters in 3 patterns: bare-string key_terms (ch 9-10), wrong field names `register_translation`/`gloss` (ch 13-16), object-format expanded_rendering (ch 17, 21). All fixed and verified. QA script (`scripts/qa_validate.py`) enhanced with structural type checking: key_terms must be a list of dicts, each entry validated for correct field names, expanded_rendering must be a string. These checks now prevent all three violation patterns at generation time. |
| 2026-03-29 | **1 Samuel complete:** 31/31 chapters, 810 verses, all passing automated QA. 9th complete book. Hannah's Song rendered as poetry (ch 2). Full Saul-David narrative arc with theological depth on anointing, kingship, covenant loyalty, and divine rejection. Deployed to site (278 pages). |
| 2026-03-29 | **Ruth complete:** 4/4 chapters, 85 verses, all passing automated QA. 8th complete book. 23 key_terms, 10 expanded_renderings, full preambles on all chapters. Key theological coverage: chesed (1:8, 2:20, 3:10), go'el/kinsman-redeemer (2:20, 3:9-13, 4:1-14), davaq (1:14). Genealogy to David rendered with full theological notes. Deployed to site (247 pages). |
| 2026-03-29 | **Extended Library direction established:** Multi-tradition stacking strategy with 3 tiers (manuscript traditions, pre-Nicaea canon, interpretive traditions). 7-priority implementation order (DSS Isaiah → 1 Enoch → LXX → JST → Samaritan → Jubilees → Targumim). Expanded `AlternateEdition` data model with tier, date, scope, license, pre-Nicaea flag. JST copyright research flagged as blocking for Priority 4. Pre-Nicaea framing language added to project vision. |
| 2026-03-29 | **Judges complete:** 21/21 chapters, 618 verses, all passing automated QA. Second historical book. Watch chapters (1, 2, 3, 4-5, 6-8, 9, 11, 13-16, 19, 20-21) received detailed attention. 64 key_terms, 13 expanded_renderings. Song of Deborah rendered as poetry. Deployed to site. |
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

*Version 3.5 — 2026-04-01*
