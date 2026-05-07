# The Covenant Rendering — Source of Truth

*What are we building, and what's the current status?*

**Owner:** Aaron Blonquist
**Created:** 2026-02-27
**Last updated:** 2026-04-20
**Version:** 5.5

---

## System Reference

| Document | File | Question It Answers |
|---|---|---|
| **Source of Truth** | **`TCR_source_of_truth.md`** | **What are we building? What's the current status?** |
| Data Reference | `TCR_data_reference.md` | What data exists? What are the schemas and terms? |
| Quality Contract | `TCR_quality_contract.md` | What must be true for output to be correct? |
| Operational Playbook | `TCR_operational_playbook.md` | How do we generate, deploy, and operate? |
| Auditor Source of Truth | `TCR_auditor_source_of_truth.md` | How do I audit this project? (standalone, self-contained) |
| Full Roadmap | `TCR_roadmap.md` | What's the plan from now to project completion? |
| Tradition Expansion Roadmap | `TCR_tradition_expansion_roadmap.md` | Full plan for comprehensive verse-level tradition stacking |

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
| Ezekiel Briefing | [`prompts/ezekiel-briefing-addendum.md`](prompts/ezekiel-briefing-addendum.md) | Ezekiel-specific vocabulary (kavod YHWH, merkavah, chayot, ofannim, ben adam, Adonai YHWH), visionary language preservation, "This is what the Lord GOD says" formula (distinct from other prophets), sensitive passages (ch 16/23 unsanitized, ch 37 dual reading, 44:9 foreigners tension), Temple measurement conventions, generation plan |

---

## Current State

- **Status:** FULL BIBLE + EXTENDED LIBRARY COMPLETE — 66-book standard Bible (1,189 chapters, 31,169 verses) plus 7 Extended Library traditions all live.
- **Standard Bible:** OT (929 ch, 23,210 v from WLC) + NT (260 ch, 7,959 v from SBLGNT). **1,189/1,189 chapters pass automated QA.** 69 verses whitelisted as accepted convergence (KJV proximity where Hebrew/Greek only produces one natural rendering). Zero failures.
- **Extended Library (all deployed):**
  - DSS Isaiah (1QIsaᵃ): 66 ch, 590 variants vs MT
  - 1 Enoch: 108 ch, 1,054 verses (standalone from Ge'ez)
  - Jubilees: 50 ch, 1,245 verses (standalone from Ge'ez)
  - LXX Jeremiah: 52 ch variant comparison (shorter text, confirmed by 4QJerb)
  - LXX Daniel: 15 files (12 variant + Susanna, Prayer of Azariah, Bel and Dragon)
  - LXX Esther: 16 files (10 variant + 6 Additions A-F)
  - JST: Book of Moses (8 ch), JS-Matthew (55 v), Appendix (14 passages), Footnotes (428 entries across OT/NT — expanded from 111). All from official LDS Church publications.
  - Samaritan Pentateuch: 5 books, 156 significant variants (Gerizim theology, 10th commandment)
  - Targum Onkelos: 5 books, 176 renderings (Memra, anti-anthropomorphism, Messianic)
  - Targum Jonathan: 5 books, 153 renderings (Servant Songs reinterpreted, explicit Messianic readings)
  - Latin Vulgate: **66 per-book variant files (791 renderings)** covering every book of the Protestant canon, plus **7 deuterocanonical books** rendered in full from Jerome's Latin (Tobit 14 ch, Judith 16 ch, Wisdom 19 ch, Sirach 51 ch, Baruch 6 ch, 1 Maccabees 16 ch, 2 Maccabees 15 ch — 137 chapters total). 203 Vulgate files.
- **Website:** thecovenantrendering.com — 1,598 pages live.
- **AI Search:** `tcr-search-api` — Claude-powered "Ask the Text" on homepage. Tiered context strategy: indexed summaries for breadth, full scholarly data for specific passages. Queries concordance (28 terms), cross-references (2,328 refs), and all 77 book indexes.
- **Documentation:** SOT v5.5.
- **Repos:** Both current.
- **Active work:** Full Tradition Expansion — comprehensive verse-level stacking of all traditions across every Bible chapter. See `TCR_tradition_expansion_roadmap.md` for 10-phase plan.
- **Next:** Phase 3 (LXX expansion to full OT), Phase 4 (DSS beyond Isaiah), Phase 5 (Targumim comprehensive), then website generalization and AI search updates.

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
| **Lamentations** | 5/5 | 154 | Complete | All chapters passed QA. Acrostic poetry (ch 1-4), triple acrostic (ch 3). Eikhah opening. chesed/emunah hope passage (3:22-23). Unresolved ending (5:22) preserved. Jewish liturgical re-reading tradition documented. |
| **Ezekiel** | 48/48 | 1,273 | Complete | All chapters passed QA. Briefing addendum created. Throne-chariot merkavah vision (ch 1), Temple abominations and glory departure (ch 8-11), unfaithful wife allegory unsanitized (ch 16, 63 verses), Oholah/Oholibah unsanitized (ch 23), individual responsibility (ch 18), God as shepherd (ch 34), valley of dry bones (ch 37), Gog/Magog (ch 38-39), new Temple vision (ch 40-48), river from Temple (ch 47), YHWH Shammah (48:35). "This is what the Lord GOD says" formula (Adonai YHWH). |
| **Daniel** | 12/12 | 357 | Complete | All chapters passed QA. Bilingual: Hebrew (ch 1:1-2:4a, 8-12), Aramaic (ch 2:4b-7:28). Language transitions documented. Statue dream (ch 2), fiery furnace (ch 3), lions' den (ch 6), four beasts and Son of Man/bar enash (ch 7), 70 weeks/shavu'im (ch 9), resurrection (12:2). |
| **Hosea** | 14/14 | 197 | Complete | All chapters passed QA. Marriage metaphor. chesed not sacrifice (6:6). "When Israel was a child" (11:1). shuv as key verb throughout. |
| **Joel** | 3/3 | 73 | Complete | All chapters passed QA. Locust plague, Spirit on all flesh (2:28-29), Valley of Decision. English versification with Hebrew noted. |
| **Amos** | 9/9 | 146 | Complete | All chapters passed QA. Social justice. "For three... and for four" pattern. "Let justice roll down" (5:24). qayits/qets wordplay (8:1-2). Booth of David (9:11). |
| **Obadiah** | 1/1 | 21 | Complete | Passed QA. Shortest OT book. Oracle against Edom. |
| **Jonah** | 4/4 | 48 | Complete | All chapters passed QA. Narrative prose. Fish prayer as poetry (ch 2). God's compassion beyond Israel. |
| **Micah** | 7/7 | 105 | Complete | All chapters passed QA. "Act justly, love faithful love, walk humbly" (6:8). Bethlehem prophecy (5:2). mi-kha-El wordplay (7:18). |
| **Nahum** | 3/3 | 47 | Complete | All chapters passed QA. Fall of Nineveh. War poetry. Partial acrostic (ch 1). |
| **Habakkuk** | 3/3 | 56 | Complete | All chapters passed QA. "The righteous shall live by his emunah" (2:4). Theophany psalm (ch 3). "Though the fig tree does not bud" (3:17-18). |
| **Zephaniah** | 3/3 | 53 | Complete | All chapters passed QA. Dies irae tradition (1:14-18). "He will exult over you with singing" (3:17). |
| **Haggai** | 2/2 | 38 | Complete | All chapters passed QA. Rebuild the Temple. "Glory of the latter house" (2:9). Zerubbabel as signet ring (2:23). |
| **Zechariah** | 14/14 | 211 | Complete | All chapters passed QA. Eight night visions (ch 1-6). "Not by might nor by power" (4:6). King on a donkey (9:9). "They will look on me, the one they have pierced" (12:10). Living waters (14:8). Hebrew/English versification fixed for ch 1-2. |
| **Malachi** | 4/4 | 55 | Complete | All chapters passed QA. Last prophetic voice. Disputation style. Tithes (3:10). Sun of righteousness (4:2). Elijah before the great day (4:5). Hebrew versification noted. |
| **Matthew** | 28/28 | 1,071 | Complete | All chapters passed QA. Genealogy (ch 1), Sermon on the Mount (ch 5-7), parables (ch 13), Olivet Discourse (ch 24-25), Passion narrative (ch 26-28). Fulfillment quotations throughout. |
| **Mark** | 16/16 | 678 | Complete | All chapters passed QA. Messianic Secret, Passion narrative emphasis. Longer ending (16:9-20) included with textual note. |
| **Luke** | 24/24 | 1,151 | Complete | All chapters passed QA. Birth narrative (ch 1-2), parables unique to Luke (Good Samaritan ch 10, Prodigal Son ch 15), Emmaus road (ch 24). |
| **John** | 21/21 | 880 | Complete | All chapters passed QA. Prologue/Logos hymn (ch 1), seven signs, seven "I am" statements, Farewell Discourse (ch 13-17), Pericope Adulterae (7:53-8:11) included with textual-critical apparatus. |
| **Acts** | 28/28 | 1,006 | Complete | All chapters passed QA. Pentecost (ch 2), Stephen's speech (ch 7), Paul's conversion (ch 9), Jerusalem Council (ch 15), Paul's journeys and trials. Textual-critical omissions handled (8:37, 15:34, 24:7, 28:29). |
| **Romans** | 16/16 | 433 | Complete | All chapters passed QA. Justification by faith (ch 1-5), baptism into Christ (ch 6), Spirit and flesh (ch 8), Israel's destiny (ch 9-11), ethical exhortation (ch 12-15), Phoebe as diakonos (16:1), Junia as apostle (16:7), doxology with textual placement notes (16:25-27). |
| **1 Corinthians** | 16/16 | 437 | Complete | All chapters passed QA. Divisions (ch 1-4), Lord's Supper (ch 11), love chapter (ch 13), resurrection (ch 15), spiritual gifts (ch 12, 14). |
| **2 Corinthians** | 13/13 | 257 | Complete | All chapters passed QA. Ministry of reconciliation (ch 5), Paul's weakness/strength paradox (ch 12), "new creation" (5:17). |
| **Galatians** | 6/6 | 149 | Complete | All chapters passed QA. Justification by faith not law (ch 2-3), allegory of Hagar/Sarah (ch 4), fruit of the Spirit (ch 5). |
| **Ephesians** | 6/6 | 155 | Complete | All chapters passed QA. Cosmic christology (ch 1), saved by grace (2:8-9), household codes (ch 5-6), armor of God (6:10-18). |
| **Philippians** | 4/4 | 104 | Complete | All chapters passed QA. Christ Hymn/kenosis (2:5-11), "to live is Christ" (1:21), pressing forward (ch 3). |
| **Colossians** | 4/4 | 95 | Complete | All chapters passed QA. Colossian Hymn (1:15-20), fullness of deity (2:9), household codes (ch 3). |
| **1 Thessalonians** | 5/5 | 89 | Complete | All chapters passed QA. Parousia expectation (ch 4-5), "caught up in the clouds" (4:17). |
| **2 Thessalonians** | 3/3 | 47 | Complete | All chapters passed QA. Man of lawlessness (ch 2), restrainer theology. |
| **1 Timothy** | 6/6 | 113 | Complete | All chapters passed QA. Pastoral instruction, overseers/deacons (ch 3), "godliness with contentment" (6:6). |
| **2 Timothy** | 4/4 | 83 | Complete | All chapters passed QA. "All Scripture is God-breathed" (3:16), Paul's final charge (ch 4). |
| **Titus** | 3/3 | 46 | Complete | All chapters passed QA. Cretan ministry, "grace of God has appeared" (2:11). |
| **Philemon** | 1/1 | 25 | Complete | Passed QA. Onesimus appeal, slavery/brotherhood tension. |
| **Hebrews** | 13/13 | 303 | Complete | All chapters passed QA. Christ superior to angels (ch 1-2), Melchizedek priesthood (ch 7), new covenant (ch 8-9), faith hall of fame (ch 11). |
| **James** | 5/5 | 108 | Complete | All chapters passed QA. Faith and works (ch 2), tongue (ch 3), "submit to God" (4:7). |
| **1 Peter** | 5/5 | 105 | Complete | All chapters passed QA. Living hope (ch 1), "living stones" (2:4-5), suffering (ch 3-4). |
| **2 Peter** | 3/3 | 61 | Complete | All chapters passed QA. False teachers (ch 2), day of the Lord (ch 3). |
| **1 John** | 5/5 | 105 | Complete | All chapters passed QA. "God is light" (1:5), "God is love" (4:8), "test the spirits" (4:1). |
| **2 John** | 1/1 | 13 | Complete | Passed QA. Walking in truth, warning against false teachers. |
| **3 John** | 1/1 | 15 | Complete | Passed QA. Gaius commended, Diotrephes rebuked. |
| **Jude** | 1/1 | 25 | Complete | Passed QA. "Contend for the faith" (v. 3), 1 Enoch quotation (vv. 14-15), doxology. |
| **Revelation** | 22/22 | 405 | Complete | All chapters passed QA. Seven churches (ch 2-3), throne room (ch 4-5), seals/trumpets/bowls, Babylon's fall (ch 17-18), new Jerusalem (ch 21-22), "Come, Lord Jesus" (22:20). Genesis-Revelation ring structure (tree of life restored). |

**Total Bible:** 1,189 chapters. 31,169 verses. 1,189/1,189 chapters complete (100%). **FULL BIBLE COMPLETE.** Old Testament (39 books, 929 chapters, 23,210 verses) and New Testament (27 books, 260 chapters, 7,959 verses) rendered from original Hebrew and Greek.

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
- ~~Deploy NT to thecovenantrendering.com~~ — DONE (2026-04-05)
- ~~Deep QA audit across all 66 books~~ — DONE (2026-04-05, 1,189/1,189 pass, convergence whitelist)
### Medium-term
- ~~Greek Theologically Rich Terms Register~~ — DONE (42 locked terms, 8 categories, cross-testament links, locked NT formulas)
- ~~NT-specific briefing addendums~~ — DONE (Gospels, Romans, Hebrews, Revelation — 4 addendums)
- ~~Site search~~ — DONE (Pagefind, 1,609 pages indexed, 309K words, at `/search`)
- ~~AI-powered search~~ — DONE (Claude-powered "Ask the Text" on homepage. `tcr-search-api` with tiered context: Tier 1 indexed summaries for all matched chapters, Tier 2 renderings+notes for top 15, Tier 3 full scholarly data for specific verse references. Queries 77 books, concordance, cross-references.)
- ~~Individual verse permalinks~~ — DONE (`/genesis/1/1` → `/genesis/1#v1` with highlight)
- ~~Concordance~~ — DONE (28 terms, 3,187 occurrences, at `scripts/concordance.json`)
- ~~Cross-reference database~~ — DONE (2,328 cross-refs, at `scripts/crossref_db.json`)
- ~~Preamble enrichment pass~~ — DONE (415 chapters enriched with tradition comparison notes across 43 books)

### Long-term
- ~~Complete standard Bible~~ — DONE (66 books, 1,189 chapters, 31,169 verses)
- ~~Latin Vulgate~~ — DONE (9 books, 184 renderings, deployed at `/vulgate/`)
- ~~PDF/print generation pipeline~~ — DONE (69 PDFs: 66 per-book + OT + NT + full Bible. Download page at `/download`)

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

| Priority | Tradition | Status | Notes |
|---|---|---|---|
| 1 | Dead Sea Scrolls | **DONE** | **Isaiah** 66 ch / 590 variants at `/dss-isaiah/`; **Deuteronomy** 34 ch at `/dss-deuteronomy/` (incl. 32:8 "sons of God", 32:43 → Heb 1:6); **1 Samuel** 31 ch at `/dss-1-samuel/` (incl. the Nahash paragraph at 11:1); **2 Samuel** 24 ch at `/dss-2-samuel/` (incl. Solomon's gold shields at 8:7); **Psalms** 151 ch at `/dss-psalms/` (incl. Ps 22:16 "they have pierced", Ps 145:13 nun-line, Pss 151A/151B); plus **22 fragment-summary books** at `/dss-fragments/` covering Genesis, Exodus, Leviticus, Numbers, Joshua (4QJoshᵃ altar relocation), Judges (4QJudgᵃ shorter Gideon prologue), Ruth, 1-2 Kings, 1-2 Chronicles, Ezra, Nehemiah, Esther (the only book NOT attested at Qumran), Job (11QtgJob — oldest Aramaic Targum), Proverbs, Ecclesiastes (4QQohᵃ paleographic dating), Song of Solomon, Lamentations, Ezekiel, Daniel (bilingual structure confirmed), the Twelve Minor Prophets (8HevXII gr kaige recension). **Comprehensive DSS coverage of the Hebrew Bible.** |
| 2 | 1 Enoch | **DONE** | 108 ch, 1,054 v, deployed at `/1-enoch/` |
| 3 | Septuagint (LXX, comprehensive OT coverage) | **DONE** | **9 per-chapter corpora** (Jeremiah 52ch, Daniel 15ch/537v/106var, Esther 10ch/166v/35var, Exodus 40ch/1,210v/156var, 1 Samuel 31ch/812v/68var, Isaiah 66ch/1,292v/58var, Psalms 150ch/2,536v/131var, Proverbs 31ch/915v/11var, Job 42ch/1,070v/11var) **+ ~30 per-book LXX files** (Pentateuch remainder, Joshua-Nehemiah historicals, Lamentations, Ezekiel, all 12 Minor Prophets, Ecclesiastes, Song of Songs). Routing wired in `getStackedTraditions` for Isaiah, Psalms, Proverbs, Job. |
| 4 | JST | **DONE** | 3 layers (Moses 8 ch, JS-Matt, Appendix 14, Footnotes **428** — 97 OT + 331 NT, expanded from the legacy 111). All from official LDS Church publications. Deployed at `/jst/` |
| 5 | Samaritan Pentateuch | **DONE** | 5 books, 156 variants, deployed at `/samaritan-pentateuch/` |
| 6 | Jubilees | **DONE** | 50 ch, 1,245 v, deployed at `/jubilees/` |
| 7 | Targumim | **DONE** | Onkelos 176 + Jonathan 153 renderings, deployed at `/targum/` |
| 8 | Latin Vulgate | **DONE** | 9 books, 184 renderings (Jerome's key choices), deployed at `/vulgate/` |

### Remaining Extended Library UI
- ~~Multi-source version tabs on chapter pages~~ — DONE (inline stacked tradition cards under each verse via `TraditionStack.astro`; data-driven via `TRADITION_REGISTRY` in `tcr.ts`).
- ~~Canon filter UI on `/books` page (Protestant / Catholic / Orthodox / Ethiopian / All)~~ — DONE (live filter with `aria-pressed`, focus-visible, sr-only live region announcing canon changes; URL-persisted via `?canon=`).
- ~~DSS fragment viewer for partial-chapter rendering~~ — DONE (the dedicated DSS pages render attestation entries directly for fragmentary coverage; `/dss-fragments/` provides per-book summary pages for books with smaller attestation).
- ~~Phase 4 DSS expansion to Psalms (11QPsᵃ) and Samuel (4QSamᵃ)~~ — DONE.

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
- AI search API (`tcr-search-api/server.js`) — Claude-powered semantic search across all 77 books. Express server on port 3847 with tiered context strategy (indexed summaries / renderings+notes / full scholarly data), query classification (specific/book-level/topical), concordance and cross-reference integration, rate limiting (10/min per IP). Deployed at `/api/search` via nginx proxy on the VPS.

---

## 5. Project Information

| Field | Value |
|---|---|
| **Project name** | The Covenant Rendering |
| **Creator** | Aaron Blonquist |
| **Contact (public)** | contact@thecovenantrendering.com |
| **Contact (personal)** | *(removed from public SOT)* |
| **License** | CC-BY-4.0 |
| **Methodology** | Prompts and generation workflow in `prompts/` directory |
| **Source text (OT)** | Westminster Leningrad Codex (WLC) |
| **Source text (NT)** | SBL Greek New Testament (SBLGNT) |
| **Reference text** | King James Version (KJV) |
| **Prompt version** | 1.3 |
| **Data repo** | https://github.com/bashonda2/the-covenant-rendering (`~/The Covenant Rendering/`) |
| **Website repo** | https://github.com/bashonda2/tcr-site (`~/TCR/`) |
| **Search API** | `tcr-search-api/` in data repo, deployed at `/opt/tcr-search-api/` on VPS, managed by PM2 as `tcr-search` |
| **Live site** | https://thecovenantrendering.com |
| **VPS** | *(removed from public SOT)* |
| **Web root** | `/var/www/tcr/` |

### Attribution

When using The Covenant Rendering, credit:

> The Covenant Rendering by Aaron Blonquist. Licensed under CC-BY-4.0.

---

## 6. Change Log

| Date | Changes |
|---|---|
| 2026-05-04 | **DSS FRAGMENT SUMMARIES (22 BOOKS) — PHASE 4 COMPLETE.** 22 per-book summary files at `/dss-fragments/` documenting Qumran attestation for biblical books with smaller DSS coverage: Genesis, Exodus, Leviticus, Numbers, Joshua, Judges, Ruth, 1-2 Kings, 1-2 Chronicles, Ezra, Nehemiah, Esther, Job, Proverbs, Ecclesiastes, Song of Solomon, Lamentations, Ezekiel, Daniel, the Twelve Minor Prophets. Marquee findings: **4QpaleoExodᵐ** (pre-Samaritan harmonizing edition — Samaritan-style expansions in mainstream Jewish scribal tradition before the sect's emergence); **4QJoshᵃ** (Joshua 8:30-35 altar narrative relocated to immediately after the Jordan crossing — a major structural variant with Samaritan parallels); **4QJudgᵃ** (shorter Gideon prologue omitting the prophet's rebuke speech at Judg 6:7-10 — possibly the original literary form); **11QtgJob** (the oldest extant Aramaic Targum of any biblical book, Job 17-42, c. 50 CE — predates rabbinic Targum tradition by centuries); **4QQohᵃ** (paleographic dating c. 175-150 BCE, settling Qohelet's terminus ante quem); **8HevXII gr** (kaige recension of the Greek Twelve, an early Hebrew-conforming revision of the Old Greek predating Aquila and Theodotion); **Daniel** bilingual Hebrew/Aramaic structure confirmed as original; **Esther** documented as the only book of the Hebrew Bible NOT attested at Qumran. Total: 7 documented variants across the 22 books (plus the absence-of-Esther entry). Single landing page with anchored sections (book-genesis, book-job, book-esther, etc.); each book includes manuscripts list, scroll description, notable variants, and per-variant detail where applicable. **PHASE 4 IS NOW COMPLETE**: Isaiah (per-chapter), Deuteronomy (per-chapter), 1 Samuel (per-chapter), 2 Samuel (per-chapter), Psalms (151 chapters), and 22 fragment-summary books — comprehensive DSS coverage of the Hebrew Bible. Live spot-checks at /dss-fragments/: 13× "4QpaleoExodᵐ", 12× "4QJoshᵃ", 11× "11QtgJob", 9× "kaige recension", 1× "not attested at Qumran" (Esther). Commits: tcr-site `3827cc2`, the-covenant-rendering `c48dc0a`. SOT v5.11. |
| 2026-05-04 | **DSS PSALMS (11QPsᵃ + 4QPss FAMILY) — PHASE 4 THIRD BATCH.** 151 chapter files (Pss 1–150 + apocryphal Ps 151) covering the roughly forty Qumran Psalms manuscripts — the most extensively attested biblical book at Qumran. Headline witness: **11QPsᵃ** (the Great Psalms Scroll, c. 30–50 CE) presents an alternative ordering of Pss 91–150 with four apocryphal compositions intermingled (Plea for Deliverance, Apostrophe to Zion, Hymn to the Creator, David's Compositions colophon claiming David authored 4,050 songs). Marquee variants: **Ps 22:16** "they have pierced" (5/6HevPs כָּארוּ) vs MT "like a lion" (כָּאֲרִי) — single-letter difference (yod vs waw); confirms LXX/Vulgate; the Hebrew-text basis of the traditional crucifixion reading. **Ps 145:13** restoration of the missing nun-line in the alphabetic acrostic ("the LORD is faithful in all his words and gracious in all his deeds") — confirms LXX, settles MT haplography case. **Ps 151** Hebrew Vorlage at 11QPsᵃ in two compositions (151A David's youth and anointing; 151B Goliath battle); proved LXX Ps 151 is not a late Greek composition but translated from Hebrew. Wiring: new `/dss-psalms/` page set with 151 chapter routes (1–99 zero-padded, 100–151 unpadded — already supported by `loadVariantChapter`); TRADITION_REGISTRY entry at priority 10; BOOKS-registry `psalms-dss` flipped to 'complete'; resolver auto-routes via the generic `-dss` suffix rule. Live spot-checks: `/dss-psalms/22` renders the marquee 9× ("they have pierced") + 8× ("like a lion") comparison; `/dss-psalms/145` renders the nun-line restoration; `/dss-psalms/151` renders the apocryphal Davidic autobiography. Commits: tcr-site `696a4eb`, the-covenant-rendering `0d8c4c7`. SOT v5.10. |
| 2026-05-04 | **DSS SAMUEL (4QSamᵃ) — PHASE 4 SECOND BATCH.** 55 per-chapter files (31 1 Samuel + 24 2 Samuel) covering 4QSamᵃ, among the oldest biblical Qumran scrolls (c. 250 BCE) and the most important DSS biblical witness after 1QIsaᵃ. 35 attestation entries, 9 documented variants (2 theological). Marquee readings: **1 Sam 11:1 — the Nahash paragraph** (four-sentence pericope explaining Nahash's right-eye gouging policy, absent from MT *and* LXX, known to Josephus, restored at NRSV 10:27b — the single most-discussed DSS-against-MT-and-LXX reading in the OT); 1 Sam 1:11, 22 (Hannah's Nazirite vow, restored at NRSV); 1 Sam 17 (David & Goliath: 4QSamᵃ supports the longer MT-type form against the LXX shorter form); 2 Sam 7:23 (Davidic-covenant divine-plural verb form preserved against the Chronicles parallel singular); 2 Sam 8:7 (Solomon's-gold-shields → Pharaoh-Shishak cross-reference matching LXX); 2 Sam 24:1 (YHWH-as-inciter form preserved against the post-exilic 1 Chr 21:1 Satan-as-inciter rewriting). Wiring: new `/dss-1-samuel/` (31 chapters) and `/dss-2-samuel/` (24 chapters) page sets modeled on `/dss-deuteronomy/`; two TRADITION_REGISTRY entries; BOOKS-registry alternateEditions added to both Samuel entries; books.astro DSS resolver generalized from per-slug map to `-dss` suffix rule. Live spot-checks: `/1-samuel/11` inline stack now surfaces the DSS amber card; `/dss-1-samuel/11` renders the full Nahash paragraph (23× "Nahash", 8× "right eye", 8× "gouge"). Commits: tcr-site `f53c160`, the-covenant-rendering `d13af75`. SOT v5.9. |
| 2026-05-04 | **WCAG 2.2 AA A11Y SWEEP + PERF PRELOAD + SEARCH-API TRADITION AWARENESS + DSS DEUTERONOMY (PHASE 4 FIRST BATCH).** Four-track session: (1) **Accessibility:** site-wide WCAG 2.2 AA pass — skip-to-main-content link in Layout (focus-visible only), 70+ `aria-hidden="true"` on decorative SVGs across 18 page templates, `aria-expanded` + `aria-controls` + post-toggle focus management on mobile menu and Books mega-menu, sr-only `role="status"` live region for verse-permalink "copied" feedback, `<label class="sr-only">` + `role="search"` + `aria-live` results region on AISearch, `focus-visible:ring` on all interactive elements (was hover-only or invisible), heading hierarchy fix (h3→h2 inside Translator's Introduction `<details>`), 15 instances of low-contrast `text-stone-300` lifted to `text-stone-500` (now ≥4.5:1), footer GitHub-link hover lifted from stone-300 (~1.5:1) to teal-600, download-page book grid → semantic `<ul><li>`. Live spot-checks: 70 aria-hidden, 37 focus-visible rings, skip link present on every page. Commit: tcr-site `1ce70d1`. (2) **Performance:** added `<link rel="preload" as="style">` for the Google Fonts CSS request (alongside existing preconnect) — estimated 100–200 ms LCP improvement on body-text-heavy chapter pages. Lighthouse audit identified two larger projects (font self-hosting/subsetting, Psalm 119 lazy-render of 176 tradition stacks) deferred to a future pass. (3) **AI search:** tcr-search-api URL-format guide expanded to enumerate every per-chapter tradition page (lxx-isaiah/psalms/proverbs/job, lxx-jeremiah/daniel/esther, dss-isaiah, dss-deuteronomy, plus tradition landing pages); system prompt now instructs Claude to link the relevant tradition page alongside canonical citations on tradition queries. Live test "Septuagint Psalter Psalm 22" now returns `/lxx-psalms/22` in citations (previously missing). Commit: the-covenant-rendering `7c3e5d9`. (4) **DSS Deuteronomy (Phase 4 first batch):** 34 per-chapter files (79 attestation entries, 4 documented theological/major variants) covering 4QDeut family + 1QDeut, 5QDeut, 11QDeut, 4QPhylacteries/Mezuzot, and 4QTestimonia. Marquee variants: Deut 5:12 *observe/remember* Sabbath harmonization (4QDeutⁿ), Deut 5:15 exodus+creation Sabbath rationales combined (4QDeutⁿ), **Deut 32:8 "sons of God"** at 4QDeutʲ (vs MT "sons of Israel") confirming LXX and recovering divine-council cosmology, **Deut 32:43 longer Song of Moses ending** at 4QDeutᵍ matching LXX with "let all the angels of God worship him" — Hebrew Vorlage of Hebrews 1:6. Wiring: new `/dss-deuteronomy/` index + 34 [chapter] routes (modeled on /dss-isaiah), tradition-registry entry at priority 10, BOOKS-registry `deuteronomy-dss` flipped to `'complete'`, books.astro DSS resolver extended for the new slug. Live: `/deuteronomy/32` inline stack now surfaces DSS amber cards alongside Targum/Vulgate; `/dss-deuteronomy/32` renders the marquee variants with full mt_reading/dss_reading comparison. Commits: tcr-site `4b77abf`, the-covenant-rendering `2226de8`. SOT v5.8. |
| 2026-04-28 | **FRONTEND USABILITY AUDIT FIXES — DEPLOYED.** Post-Phase-3 frontend audit surfaced and fixed: (1) **Missing tradition pages** (BLOCKER): created `/lxx-isaiah/` (66 ch), `/lxx-psalms/` (150 ch), `/lxx-proverbs/` (31 ch), `/lxx-job/` (42 ch) index + per-chapter routes (289 chapter pages total) modeled on `/lxx-jeremiah/`, each with MT vs LXX side-by-side comparison, significance badges (theological/major/moderate/minor), notable_variants/structural_notes preamble panels, and back-links to the TCR base rendering. (2) **BOOKS registry stale** (MAJOR): flipped `psalms-lxx` and `isaiah-lxx` from `'not-started'` to `'complete'`; added `alternateEditions` arrays to Job and Proverbs entries with proper LXX descriptions. (3) **books.astro resolver hardcoded** (MAJOR + NIT): replaced per-book hardcoded LXX route map with generic rule `slug → '/lxx-' + slug.replace(/-lxx$/, '')`; extracted DSS resolver for symmetry. (4) **Downloads page out of date**: only 6 of 66 per-book PDFs were downloadable; the other 60 were greyed-out placeholders. Copied all 66 individual PDFs from translation source repo to `public/pdf/`, aliased `song-of-songs.pdf` → `song-of-solomon.pdf` for slug compatibility, rewrote `download.astro` to iterate BOOKS by canonical section (Pentateuch / Historical / Wisdom / Major Prophets / Minor Prophets / Gospels / Acts / Pauline / General / Apocalypse), and replaced the stale "Popular books are linked below" copy with a live "X of 66 books complete" count from the registry. Build: 1,903 Pagefind-indexed pages (up from ~1,609), 312 MB rsynced. All 200 OK on smoke tests for new routes and previously-greyed PDFs (`/pdf/isaiah.pdf`, `/pdf/jeremiah.pdf`, `/pdf/song-of-solomon.pdf`). Commit: tcr-site `491d2b9`. |
| 2026-04-28 | **TRADITION EXPANSION PHASE 3 COMPLETE — LXX comprehensive OT coverage; DEPLOYED.** Septuagint expanded from 3 books (Jeremiah, Daniel, Esther) to comprehensive coverage. **Phase 3a–3h delivered**: 3a Genesis LXX (per-book, 20 renderings); 3b Pentateuch remainder Leviticus 15 / Numbers 12 / Deuteronomy 15 (per-book); 3c Exodus (per-chapter, 40ch/1,210v/156var); 3d Historical books Joshua 10 / Judges 8 / Ruth 6 / 2 Samuel 8 / 1 Kings 8 / 2 Kings 7 / 1 Chr 4 / 2 Chr 4 / Ezra 4 / Nehemiah 4 (per-book); 3e 1 Samuel (per-chapter, 31ch/812v/68var — David & Goliath shorter LXX form); 3f Wisdom: Psalms (per-chapter, 150ch/2,536v/131var — LXX numbering offset documented), Proverbs (per-chapter, 31ch/915v/11var), Job (per-chapter, 42ch/1,070v/11var — ~1/6 shorter than MT); 3g Isaiah (per-chapter, 66ch/1,292v/58var — full Christological/NT-citation documentation including Servant Songs, cornerstone trio, Acts 7/Mark 9:48 anchors); 3h remaining prophets per-book (Lamentations 4, Ezekiel 9, all 12 Minor Prophets ~32 entries) plus Ecclesiastes 3 and Song of Songs 3. Closeout: `getStackedTraditions()` extended to surface lxx-isaiah, lxx-psalms, lxx-proverbs, and lxx-job alongside existing tradition stacks; four new LXX directories mounted at `TCR/src/data/`. Schema follows established LXX pattern (mt_reading + lxx_reading in source-script, mt_rendering + variant_rendering, has_variant flag + significance level, NT-citation tracking in variant_notes). All chapter files JSON-validated. **Deployed**: tcr-site `28377c0` and the-covenant-rendering `83b5abe` pushed to GitHub; website built and rsynced to VPS (`/var/www/tcr/`); tcr-search-api server.js + 4 LXX corpora deployed to `/opt/tcr-search-api/` and `/opt/tcr-data/`; `pm2 restart tcr-search` — index expanded **77 books / 1,438 chapters → 81 books / 1,727 chapters** (+289 LXX chapters indexed). Stale 404 errors from prior model-ID iterations flushed; `claude-sonnet-4-6` confirmed healthy (HTTP 200 live test). SOT v5.6. |
| 2026-04-20 | **TRADITION EXPANSION PHASES 1-2 COMPLETE.** Phase 1 (JST): Footnotes expanded from 111 → 428 entries (97 OT + 331 NT), split into per-testament files (`jst-footnotes-ot.json`, `jst-footnotes-nt.json`). All 111 original entries preserved. JST appendix verified complete (14/14 passages). Phase 2 (Vulgate): Expanded from 9 books/184 renderings to **203 files**: 66 per-book variant-comparison files covering every Protestant-canon book (791 total renderings documenting Jerome's key Latin choices), plus 7 deuterocanonical books rendered in full from Latin (Tobit 14 ch, Judith 16 ch, Wisdom of Solomon 19 ch, Sirach 51 ch, Baruch 6 ch, 1 Maccabees 16 ch, 2 Maccabees 15 ch — 137 chapters, ~3,400 verses). Key renderings: ego sum qui sum, cornuta facies, vanitas vanitatum, iustus ex fide vivit, Verbum caro factum est, gratia plena, sacramentum magnum, dies irae, omnipotens sermo tuus. Audit findings fixed: 12 NT files renamed from underscores to hyphens (project convention), gospels.json split into individual matthew/mark/luke/john files, JST extended-verse-numbering note added. Full tradition expansion roadmap created (`TCR_tradition_expansion_roadmap.md`) — 10-phase plan for comprehensive verse-level stacking across all traditions. SOT v5.5. |
| 2026-04-11 | **AI SEARCH API BUILT AND DEPLOYED.** `tcr-search-api` created: Express server with Claude-powered "Ask the Text" semantic search on homepage. Three fixes applied: model name corrected (`claude-sonnet-4-6`), `DATA_ROOT` made configurable via env var, nginx timeout increased to 90s. Tiered context strategy implemented: Tier 1 (indexed summaries from in-memory startup index — all matched chapters, unlimited), Tier 2 (renderings + translator notes loaded from disk — top 15 chapters), Tier 3 (full scholarly data including Hebrew/Greek source text, KJV, key_terms — only for specific verse/chapter references). Query classification (specific/book-level/topical) routes queries to appropriate tier. Cross-reference search expanded to keyword matching in note text and book-slug matching. System prompt updated for thoroughness — all relevant references cited, not just a selection. `max_tokens` increased to 4096 for comprehensive answers. Deployed at `/opt/tcr-search-api/` on VPS, managed by PM2 as `tcr-search`, proxied via nginx at `/api/search`. SOT v5.4. |
| 2026-04-05 | **ROADMAP COMPLETE.** Preamble enrichment pass: 415 chapters across 43 books enriched with "Tradition comparisons" paragraphs linking to DSS, LXX, Samaritan, Targum, Vulgate, and JST data. PDF generation pipeline: 69 PDFs generated (66 per-book + OT 13MB + NT 4MB + full Bible 17MB). Download page deployed at /download with navigation link. All near-term, medium-term, and long-term roadmap items complete. SOT v5.3. |
| 2026-04-05 | **ROADMAP SUBSTANTIALLY COMPLETE.** Latin Vulgate generated (9 books, 184 renderings) and deployed at /vulgate/. Greek Theologically Rich Terms Register created (42 terms, locked NT formulas, cross-testament links). NT briefing addendums created for Gospels, Romans, Hebrews, Revelation. Pagefind site search deployed (1,609 pages indexed, 309K words). Individual verse permalinks implemented (/genesis/1/1 → scroll + highlight). Concordance built (28 terms, 3,187 occurrences). Cross-reference database built (2,328 refs). All 8/8 Extended Library priorities complete. Site: 35,076 pages (including verse permalinks). Only remaining items: preamble enrichment pass and PDF/print pipeline. SOT v5.2. |
| 2026-04-05 | **FULL AUDIT: 1,189/1,189 CHAPTERS PASS.** Auditor SOT v2.0 created and used for full-Bible validation. 2 fixes applied: Jonah 2:8 ER field ordering, Nahum 1:10 archaic "sodden" → "soaked". 69-verse convergence whitelist added to qa_validate.py — verses where KJV proximity is accepted because the Hebrew only produces one natural English rendering. Whitelist is categorized (superscriptions, prophetic formulas, divine self-identification, simple parallelism, date/narrative formulas, iconic direct speech) and documented in the script. New KJV-proximate verses not on the whitelist still trigger FAIL. Zero OT or NT chapters failing. |
| 2026-04-05 | **ALL EXTENDED LIBRARY TRADITIONS COMPLETE.** Final three traditions deployed: JST (3 layers — Book of Moses 8 ch/356 v, JS-Matthew 55 v, Appendix 14 passages, Footnotes 111 entries, all from official LDS Church publications with attribution), Samaritan Pentateuch (5 books, 156 variants including Gerizim 10th commandment and Deut 27:4), Targumim (Onkelos 176 renderings + Jonathan 153 renderings, covering Memra theology, anti-anthropomorphism, Messianic readings, Suffering Servant reinterpretation). Site now 1,598 pages with dedicated pages for each tradition. SOT v5.1. |
| 2026-04-05 | **JUBILEES COMPLETE.** Third Extended Library text. 50 chapters, 1,245 verses. "Little Genesis" — retells Genesis through Exodus 14 with 364-day solar calendar, jubilee chronology, and halakhic emphasis. Canonical in Ethiopian Orthodox, multiple Qumran copies. Key content: Angel of the Presence dictation (ch 1), Mastema as adversary (ch 10, 17-18, 48), circumcision as eternal covenant (ch 15), Dinah episode with Simeon/Levi praised (ch 30), Jacob's wars unique to Jubilees (ch 37-38), detailed Passover halakhah (ch 49). Deployed at /jubilees/. |
| 2026-04-05 | **LXX JEREMIAH, DANIEL, ESTHER COMPLETE.** Septuagint variant data for the three most divergent LXX books. LXX Jeremiah: 52 chapters, 187 variants — the shorter, older text confirmed by 4QJerb; ch 33:14-26 Messianic addition absent from LXX; Oracles Against Nations relocated after 25:13. LXX Daniel: 15 files (12 variant chapters + 3 additions: Susanna 64v, Prayer of Azariah 68v, Bel and Dragon 48v), 537 verses; OG Son of Man variant at 7:13. LXX Esther: 16 files (10 variant chapters + 6 Additions A-F), 271 verses; 107 added verses including prayers making God explicit where MT is silent. All deployed with dedicated pages. Site now 1,571 pages. |
| 2026-04-05 | **1 ENOCH COMPLETE.** Second Extended Library text. 108 chapters, 1,054 verses. The "book that was in the Bible" — canonical in Ethiopian Orthodox Church, quoted in Jude 14-15, found at Qumran. Five sections rendered: Book of Watchers (ch 1-36, Watcher angels, Azazel, throne vision, four compartments of the dead), Parables of Enoch (ch 37-71, Son of Man figure, pre-existence theology, Enoch identified as Son of Man in 71:14), Astronomical Book (ch 72-82, 364-day solar calendar), Dream Visions (ch 83-90, Animal Apocalypse), Epistle of Enoch (ch 91-108, Apocalypse of Weeks, woe oracles, birth of Noah). Source text: Ge'ez (R.H. Charles/Knibb editions). Cross-references to Jude, 2 Peter, Daniel 7, Ezekiel 1, Leviticus 16, Matthew 25. Site template updated for extended books (text_source/text_reference fields). Deployed at /1-enoch/. Site now 1,434 pages. |
| 2026-04-05 | **DSS ISAIAH (1QIsaᵃ) COMPLETE.** First Extended Library tradition generated. 66 chapters, 1,292 verses, 590 variants documented against the Masoretic Text (30 theological, 13 major). Variant-annotation schema created with significance levels (none/minor/moderate/major/theological). Column references, Hebrew readings from both MT and scroll, variant renderings, and scholarly notes for every verse. Key variants: Isaiah 7:14 almah confirmed (not betulah), Isaiah 53:11 "he shall see light" (yireh or) documented as theological, Isaiah 52:14 mashachti/mishchat ambiguity. Generation prompt created. DSS Isaiah pages deployed to site (67 new pages: index + 66 chapters) with variant comparison UI showing MT vs. scroll readings side-by-side. Site now 1,325 pages. |
| 2026-04-05 | **FULL BIBLE COMPLETE.** All 27 New Testament books generated from SBLGNT Greek: 260 chapters, 7,959 verses, all passing automated QA. Source text shifted from WLC to SBLGNT. Every verse includes text_greek, text_kjv, independent rendering, translator_notes, and reading_level. Greek key_terms with transliterations throughout. Full preambles on all 260 chapters. Romans 15-16 regenerated (had been empty files). Phoebe as diakonos (Rom 16:1), Junia as woman apostle (Rom 16:7), Pericope Adulterae (John 7:53-8:11) with full textual-critical apparatus. 16 textual-critical omissions handled (verses absent from SBLGNT but present in KJV/TR). QA script updated for NT support: text_greek/greek field recognition, TEXTUAL_CRITICAL_OMISSIONS set, John 8 Pericope Adulterae handling. 148 KJV-proximate NT verses remediated. 14 ER field-ordering issues fixed across 7 books. SOT v5.0. Full Bible: 66 books, 1,189 chapters, 31,169 verses. |
| 2026-04-04 | **OLD TESTAMENT COMPLETE.** Lamentations (5 ch, 154 v), Ezekiel (48 ch, 1,273 v), Daniel (12 ch, 357 v), and all 12 Minor Prophets (67 ch, 1,050 v) generated and passing QA. 132 chapters in a single session. Ezekiel briefing addendum created. Sensitive passages (Ezek 16, 23) rendered without sanitizing. Daniel's Hebrew/Aramaic bilingual structure documented. Zechariah versification corrected to English convention. 39 OT books, 929 chapters, 23,083 verses — all complete, all passing automated QA. SOT v4.0. |
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

*Version 5.11 — 2026-05-04*
