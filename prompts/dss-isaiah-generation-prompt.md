# DSS Isaiah Generation Prompt — 1QIsaiah-a (The Great Isaiah Scroll)

## Purpose

Generate variant-annotation data for every chapter of Isaiah comparing the Dead Sea Scrolls text (1QIsaiah-a, "The Great Isaiah Scroll") against the Masoretic Text (WLC) that TCR's base rendering uses.

This is NOT a standalone translation. It is a scholarly apparatus that documents where and how the oldest complete manuscript of Isaiah differs from the medieval Masoretic tradition — and what those differences mean.

## Source Text

**1QIsaiah-a** — The Great Isaiah Scroll, discovered in Qumran Cave 1 in 1947. Dated paleographically to approximately 125 BCE. The oldest complete manuscript of any biblical book. Now housed in the Shrine of the Book, Israel Museum, Jerusalem.

The scroll contains all 66 chapters of Isaiah on 17 sheets of parchment, in 54 columns. It preserves a text approximately 1,000 years older than the Leningrad Codex (1008 CE).

## Reference Materials

- The Digital Dead Sea Scrolls (Israel Museum): digitized high-resolution images
- DJD (Discoveries in the Judaean Desert) critical editions
- Eugene Ulrich, "The Biblical Qumran Scrolls"
- Martin Abegg, Peter Flint, Eugene Ulrich, "The Dead Sea Scrolls Bible" (DSSB)
- Emanuel Tov, "Textual Criticism of the Hebrew Bible"

## Output Schema

Each chapter produces a JSON file following this schema:

```json
{
  "meta": {
    "project": "The Covenant Rendering",
    "version": "1.0.0",
    "book": "Isaiah",
    "chapter": 7,
    "tradition": "dss-1qisaiah-a",
    "tradition_label": "Dead Sea Scrolls (1QIsaᵃ)",
    "source_text": "1QIsaiah-a (Qumran Cave 1)",
    "base_text": "Westminster Leningrad Codex (WLC)",
    "date": "c. 125 BCE",
    "manuscript_location": "Shrine of the Book, Israel Museum, Jerusalem",
    "generated_at": "2026-04-05T00:00:00Z",
    "prompt_version": "1.0",
    "license": "CC-BY-4.0"
  },
  "preamble": {
    "summary": "Overview of this chapter's DSS variants — how many, how significant, what patterns.",
    "notable_variants": "The most theologically or textually significant variants in this chapter.",
    "scroll_condition": "Physical condition of this section of the scroll (legible, damaged, lacunae).",
    "column_reference": "Which columns of 1QIsaiah-a contain this chapter."
  },
  "verses": [
    {
      "verse": 1,
      "has_variant": false,
      "manuscript_reference": "1QIsaᵃ col. VI, line 1",
      "variant_notes": ["No significant variant. The scroll reads identically to the MT here."]
    },
    {
      "verse": 14,
      "has_variant": true,
      "significance": "major",
      "mt_reading": "הָעַלְמָה",
      "dss_reading": "העלמה",
      "variant_rendering": "the young woman",
      "mt_rendering": "the young woman",
      "variant_notes": [
        "1QIsaiah-a spells the word without the mater lectionis (he) but the word is identical: almah, 'young woman.' The scroll does NOT read betulah ('virgin'). This is significant because it confirms that the pre-Christian Hebrew text of Isaiah 7:14 read almah, supporting the TCR rendering of 'young woman' rather than 'virgin.'",
        "The definite article ha- ('the') is present in both MT and 1QIsaiah-a, suggesting a specific young woman known to Ahaz — not an abstract future figure."
      ],
      "manuscript_reference": "1QIsaᵃ col. VI, line 14"
    }
  ]
}
```

## Significance Levels

- **`none`** — No variant (scroll matches MT). Still document the verse with `has_variant: false`.
- **`minor`** — Orthographic differences only (plene vs. defective spelling, matres lectionis). No impact on meaning.
- **`moderate`** — Different word form, preposition, conjunction, or suffix that slightly affects translation but not theology.
- **`major`** — Different word, phrase, or reading that produces a meaningfully different translation.
- **`theological`** — Variant that directly affects a theologically significant passage (Messianic prophecy, divine name, covenant language, etc.).

## What to Document

For EVERY verse in each chapter, produce an entry. Even verses with no variant get an entry with `has_variant: false` — this confirms the comparison was made and the texts agree.

For verses WITH variants:
1. **`mt_reading`** — The Hebrew text from the WLC (Masoretic) for the relevant word/phrase
2. **`dss_reading`** — The Hebrew text from 1QIsaiah-a for the same word/phrase
3. **`variant_rendering`** — How the DSS reading would be rendered in English
4. **`mt_rendering`** — How the MT reading is rendered in the base TCR text
5. **`variant_notes`** — Scholarly explanation of the difference, its likely cause (scribal error, different Vorlage, theological emendation, orthographic convention), and its significance
6. **`manuscript_reference`** — Column and line reference in 1QIsaiah-a

## Key Variant Categories in 1QIsaiah-a

1. **Orthographic**: 1QIsaiah-a uses fuller (plene) spelling far more than MT. Most variants are this type. Document but mark as `minor`.

2. **Morphological**: Different verb forms, suffixes, or grammatical constructions. Often `moderate`.

3. **Lexical**: Different words entirely. These are the significant variants. Mark as `major` or `theological`.

4. **Plus/Minus**: Text present in one but absent in the other. Mark as `major`.

5. **Word order**: Different sequence of the same words. Usually `moderate`.

## Notable Passages to Handle with Care

- **Isaiah 7:14** — almah reading (see above)
- **Isaiah 9:6** — Throne names and their DSS forms
- **Isaiah 11:1-10** — Messianic branch prophecy
- **Isaiah 14:12** — Helel ben Shachar (Lucifer passage)
- **Isaiah 40:3** — "Voice crying in the wilderness" (quoted in all four Gospels)
- **Isaiah 42:1-4** — First Servant Song
- **Isaiah 52:13-53:12** — Fourth Servant Song / Suffering Servant (the most theologically sensitive passage — every variant matters)
- **Isaiah 61:1** — "Spirit of the Lord GOD is upon me" (quoted by Jesus in Luke 4:18)

## File Naming

Output files go in a `dss-isaiah/` directory:
```
dss-isaiah/chapter-01.json
dss-isaiah/chapter-02.json
...
dss-isaiah/chapter-66.json
```

## Quality Standards

1. Every verse in the chapter must have an entry — no gaps.
2. Variant notes must be substantive and scholarly, not boilerplate.
3. When the scroll is damaged or illegible at a verse, document this: `"scroll_condition": "partially illegible"` and note what can and cannot be read.
4. Do not invent variants. If the texts agree, say so. If you are uncertain about a reading, say so.
5. Column references should be as accurate as possible based on the standard column numbering of 1QIsaiah-a (54 columns).
6. Cross-reference the base TCR Isaiah rendering where relevant — the reader can look at both side by side.

## Tone

Scholarly but accessible. Write for an educated general reader, not just for textual critics. Explain what the variant means and why it matters — or why it doesn't.
