# The Covenant Rendering

A modern English rendering of the Bible — Old Testament and New Testament — translated directly from the original Hebrew and Greek source texts. Open source. Fully documented. Free for everyone.

**Website:** [thecovenantrendering.com](https://thecovenantrendering.com)

## What This Is

The Covenant Rendering is a complete, modern English rendering of the Bible with fully documented translation decisions at every verse, released as open-source structured data under [CC-BY-4.0](LICENSE).

Beyond the standard 66-book Bible, TCR surfaces how communities across 2,300 years have read the same passages — from the Dead Sea caves to the Restoration — side by side, for free. The organizing question: **"How does this tradition read this passage?"**

- **Open source** — released under [CC-BY-4.0](LICENSE). Anyone can use, share, and build upon it.
- **Ecumenical** — not affiliated with any denomination.
- **Transparent** — every translation decision is documented in translator notes.
- **Reproducible** — generation prompts and methodology included in this repository.

## What's Here

### Standard Bible (66 books, 1,189 chapters, 31,169 verses)

| Testament | Books | Chapters | Source Text |
|-----------|-------|----------|-------------|
| Old Testament | 39 | 929 | Westminster Leningrad Codex (WLC) |
| New Testament | 27 | 260 | SBL Greek New Testament (SBLGNT) |

### Extended Library (10 traditions)

| Tradition | Type | Content | Directory |
|-----------|------|---------|-----------|
| Dead Sea Scrolls (1QIsaiah-a) | Manuscript comparison | 66 chapters, 590 variants vs MT | `dss-isaiah/` |
| 1 Enoch | Pre-Nicaea canon | 108 chapters, 1,054 verses | `1-enoch/` |
| Jubilees | Pre-Nicaea canon | 50 chapters, 1,245 verses | `jubilees/` |
| Septuagint Jeremiah | Manuscript comparison | 52 chapters (shorter, older text) | `lxx-jeremiah/` |
| Septuagint Daniel | Manuscript + additions | 15 files (Susanna, Prayer of Azariah, Bel and Dragon) | `lxx-daniel/` |
| Septuagint Esther | Manuscript + additions | 16 files (6 Additions, 107 added verses) | `lxx-esther/` |
| Joseph Smith Translation | Interpretive tradition | Book of Moses, JS-Matthew, Appendix, Footnotes | `jst/` |
| Samaritan Pentateuch | Manuscript comparison | 5 books, 156 significant variants | `samaritan-pentateuch/` |
| Targum Onkelos | Interpretive tradition | 5 books, 176 Aramaic renderings (Torah) | `targum-onkelos/` |
| Targum Jonathan | Interpretive tradition | 5 books, 153 Aramaic renderings (Prophets) | `targum-jonathan/` |
| Latin Vulgate | Western tradition | 9 books, 184 renderings (Jerome) | `vulgate/` |

## Data Format

Every chapter is a standalone JSON file. OT verses include Hebrew; NT verses include Greek.

### OT Verse Example (Genesis 1:1)

```json
{
  "verse": 1,
  "text_hebrew": "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃",
  "text_kjv": "In the beginning God created the heaven and the earth.",
  "rendering": "In the beginning, God created the heavens and the earth.",
  "translator_notes": ["..."],
  "key_terms": [
    {
      "hebrew": "בָּרָא",
      "transliteration": "bara",
      "rendered_as": "created",
      "semantic_range": "created, shaped, brought into being",
      "note": "This verb is used exclusively with God as its subject in the Hebrew Bible..."
    }
  ],
  "reading_level": "8th grade"
}
```

### NT Verse Example (Romans 8:1)

```json
{
  "verse": 1,
  "text_greek": "Οὐδὲν ἄρα νῦν κατάκριμα τοῖς ἐν Χριστῷ Ἰησοῦ.",
  "text_kjv": "There is therefore now no condemnation to them which are in Christ Jesus...",
  "rendering": "There is therefore now no condemnation for those who are in Christ Jesus.",
  "translator_notes": ["..."],
  "key_terms": [
    {
      "greek": "κατάκριμα",
      "transliteration": "katakrima",
      "rendered_as": "condemnation",
      "semantic_range": "condemnation, penalty, adverse verdict",
      "note": "..."
    }
  ],
  "reading_level": "7th grade"
}
```

## Directory Structure

```
The Covenant Rendering/
├── genesis/ through malachi/     # 39 OT books (chapter-01.json, etc.)
├── matthew/ through revelation/  # 27 NT books
├── dss-isaiah/                   # Dead Sea Scrolls variant data
├── 1-enoch/                      # 1 Enoch (108 chapters)
├── jubilees/                     # Jubilees (50 chapters)
├── lxx-jeremiah/                 # Septuagint Jeremiah variants
├── lxx-daniel/                   # Septuagint Daniel (variants + additions)
├── lxx-esther/                   # Septuagint Esther (variants + additions)
├── jst/                          # Joseph Smith Translation (3 layers)
├── samaritan-pentateuch/         # Samaritan Pentateuch variants
├── targum-onkelos/               # Targum Onkelos (Torah)
├── targum-jonathan/              # Targum Jonathan (Prophets)
├── vulgate/                      # Latin Vulgate (Jerome)
├── prompts/                      # Generation prompts and methodology
├── scripts/                      # QA validation, concordance, cross-references
├── pdf/                          # Downloadable PDFs
├── TCR_source_of_truth.md        # Project status and roadmap
├── TCR_quality_contract.md       # Quality standards
├── TCR_data_reference.md         # Data schemas and field rules
├── TCR_operational_playbook.md   # Generation and deployment procedures
└── TCR_auditor_source_of_truth.md # Audit methodology
```

## How It Was Made

The Covenant Rendering was generated using AI language models (Claude, by Anthropic) operating against the Hebrew and Greek source texts under carefully designed translation prompts.

Every chapter was produced through a two-stage pipeline: a generation agent translates from the source text following formal-equivalence principles, and a separate QA agent validates the output against 18 automated checks and 8 judgment-based quality standards. All 1,189 chapters pass automated validation.

The translation prompts, quality contract, validation scripts, and every chapter of structured data are in this repository. We believe transparency strengthens the work.

## Translation Philosophy

- **Translate from the Hebrew and Greek, not from the KJV.** The KJV is provided as a reference for readers, not as a source text.
- **Formal equivalence with clarity.** Word-for-word as the baseline, but natural English takes priority over wooden literalism.
- **Preserve ambiguity when it exists.** If the source text is genuinely ambiguous, the rendering preserves that ambiguity and documents the options.
- **Modernize vocabulary, not theology.** Archaic English is updated; theological meaning is not changed.
- **Document everything.** Every significant translation decision is explained in the notes.

## Building On This

The JSON structure is designed to be developer-friendly. You can use these files to:

- Build a Bible study app or website
- Generate formatted PDFs or print-ready documents
- Create verse-by-verse commentary platforms
- Power search tools that work across English, Hebrew, and Greek
- Build concordances or cross-reference databases
- Compare manuscript traditions programmatically

## License

This work is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

**Attribution:** "The Covenant Rendering, thecovenantrendering.com, CC-BY-4.0"

## Found an Error?

This project improves through feedback. If you find a rendering that misrepresents the Hebrew or Greek, a translator note that is inaccurate, or any other error — please [open an issue](https://github.com/bashonda2/the-covenant-rendering/issues) or email contact@thecovenantrendering.com.

## Contact

Aaron Blonquist — contact@thecovenantrendering.com

---

*"The heavens declare the glory of God, and the sky above proclaims the work of his hands." — Psalm 19:1*
