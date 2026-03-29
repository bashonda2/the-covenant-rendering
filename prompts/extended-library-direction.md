# The Covenant Rendering — Extended Library & Multi-Tradition Stacking

## Strategic Direction Update

**Date:** 2026-03-28
**Context:** This document establishes the strategic direction for TCR's Extended Library — the multi-tradition textual comparison feature that will make TCR unique among Bible platforms. Update the SOT, data models, and site architecture accordingly.

---

## 1. The Vision

TCR will not just render the Bible from the Masoretic Text. It will show how communities across 2,300 years have read the same passages — from the Dead Sea caves to the Restoration — side by side, for free, with documented translation decisions at every verse.

The organizing question for every tradition included is: **"How does this tradition read this passage?"**

This is not about declaring which text is "right." It is about surfacing the full conversation that the biblical text has generated across centuries, languages, and faith communities — and trusting the reader with the complexity.

---

## 2. Tradition Tiers

### Tier: Primary
**Label in UI:** "From the Hebrew"

| Tradition | Source Text | Date | Scope | License |
|---|---|---|---|---|
| **TCR (The Covenant Rendering)** | Westminster Leningrad Codex (WLC) | 10th c. CE manuscript; ancient text tradition | Full OT (and eventually NT from SBLGNT) | CC-BY-4.0 (our work) |

This is the base rendering — always present, always the default view.

---

### Tier: Manuscript Traditions
**Label in UI:** "Other manuscript traditions"

These are independent textual witnesses — actual manuscripts or manuscript families that preserve the biblical text in forms that differ from the Masoretic tradition. All are pre-Nicaea (325 CE) in origin.

| Tradition | Source Text | Date | Pre-Nicaea? | Scope | License | Priority |
|---|---|---|---|---|---|---|
| **Dead Sea Scrolls (DSS)** | DJD editions, Leon Levy Digital Library | 250 BCE – 70 CE | Yes | Fragmentary — Isaiah most complete (1QIsaiah-a covers all 66 chapters). Major fragments: Psalms (11QPsa), Deuteronomy, Samuel, Jeremiah, Daniel | Public domain (ancient texts; TCR rendering is original work) | **1 — Start here** |
| **Septuagint (LXX)** | Rahlfs' edition (standard critical text) | 3rd–2nd c. BCE | Yes | Full OT in Greek. Most significant divergences: Jeremiah (1/8 shorter), Daniel (additions: Susanna, Bel and Dragon), Esther (107 added verses), Psalms (Psalm 151 + numbering differences) | Public domain | **3** |
| **Samaritan Pentateuch** | Published critical editions | 4th c. BCE divergence | Yes | Genesis–Deuteronomy only. ~6,000 variant readings vs. MT. Theologically significant: 10th commandment designates Mt. Gerizim | Public domain | **5** |

---

### Tier: Pre-Nicaea Canon
**Label in UI:** "Books read before the councils"

These are books that were widely read by Second Temple Jewish communities and/or early Christians before the canon was formalized at Nicaea (325 CE) and subsequent councils. They were excluded from the Protestant and Catholic canons but preserved by other traditions (primarily Ethiopian Orthodox). Their inclusion demonstrates what early communities actually considered scripture.

| Tradition | Source Text | Date | Pre-Nicaea? | Scope | License | Priority |
|---|---|---|---|---|---|---|
| **1 Enoch** | Ge'ez text (R.H. Charles edition; Knibb edition) | 3rd–1st c. BCE | Yes | 108 chapters. Quoted in Jude 14-15. Found at Qumran (Aramaic fragments). Shaped early Christian angelology, demonology, eschatology. Canonical in Ethiopian Orthodox Church. | Public domain (ancient text; scholarly editions' apparatus may vary) | **2** |
| **Jubilees** | Ge'ez text (R.H. Charles edition; VanderKam edition) | 2nd c. BCE | Yes | 50 chapters. Retells Genesis–Exodus with emphasis on solar calendar and covenant chronology. Multiple copies found at Qumran. Canonical in Ethiopian Orthodox Church. | Public domain | **6** |

**Why these matter:** 1 Enoch and Jubilees were not fringe texts. They were mainstream in Second Temple Judaism — multiple copies at Qumran, quoted or alluded to in the New Testament, influential on early Christian theology. Their exclusion from later canons was a historical decision, not a reflection of their original status. Including them lets readers see what the biblical world actually looked like before institutional standardization.

---

### Tier: Interpretive Traditions
**Label in UI:** "How traditions read this passage"

These are not independent manuscript witnesses but interpretive renderings — translations, paraphrases, or revisions that show how specific faith communities understood the biblical text. They are included as evidence of reading traditions, not as source texts.

| Tradition | Source Text | Date | Pre-Nicaea? | Scope | License | Priority |
|---|---|---|---|---|---|---|
| **Targumim** | Targum Onkelos (Torah), Targum Jonathan (Prophets) | 1st c. BCE – 5th c. CE (earliest layers pre-Nicaea) | Earliest layers yes | Torah + Prophets. Aramaic interpretive paraphrases used in synagogue worship. Show rabbinic interpretation of difficult passages. | Public domain | **7** |
| **Joseph Smith Translation (JST)** | LDS edition (Pearl of Great Price: Book of Moses, JS-Matthew; JST footnotes/appendix in LDS Bible) | 1830s CE | No | Selective — modifies specific passages, not the entire Bible. Major sections: Genesis 1-24 (Book of Moses), Matthew 24 (JS-Matthew), plus scattered verse revisions throughout OT and NT. | Need to verify LDS Church copyright status on JST text. Pearl of Great Price text may be usable; JST footnotes/appendix may have restrictions. **Research required before implementation.** | **4** |

**Critical note on JST:** The JST is categorically different from every other tradition in this list. It is not a translation from original languages — it is a revelatory revision of the KJV English text. This must be clearly communicated in the UI. The framing "How this tradition reads this passage" is accurate and defensible. Placing it alongside the Targumim (which are also interpretive, not strictly translational) creates a natural, honest category.

**JST copyright research needed:** Before implementing JST content, verify:
- Is the Pearl of Great Price text (Book of Moses, JS-Matthew) freely usable, or does Intellectual Reserve hold copyright?
- Are the JST footnotes/appendix in the LDS Bible under copyright?
- The Community of Christ "Inspired Version" is a separate publication and is NOT to be used — only the LDS-recognized JST text.

---

## 3. Implementation Priority

| Priority | Tradition | Why First | Estimated Scope |
|---|---|---|---|
| **1** | Dead Sea Scrolls (Isaiah) | Highest academic impact. 1QIsaiah-a covers all 66 chapters. Most variant readings. Pre-Nicaea by 300+ years. | 66 chapters of Isaiah with variant annotations |
| **2** | 1 Enoch | "The book that was in the Bible." Quoted in NT. Pre-Nicaea. No one else offers this in a comparative framework. | 108 chapters (standalone book, not stacked against MT) |
| **3** | Septuagint | The early church's Bible. Essential for NT cross-references. | Start with Jeremiah, Daniel, Esther (highest divergence) |
| **4** | JST | Core audience value. Fits naturally in interpretive tier. | Genesis 1-24 (Moses), Matthew 24, selected verse revisions |
| **5** | Samaritan Pentateuch | Oldest independent Pentateuch witness. Manageable scope (Gen-Deut only). | 5 books, variant annotations only |
| **6** | Jubilees | Completes the Ethiopian pre-Nicaea pair with 1 Enoch. DSS attestation. | 50 chapters (standalone) |
| **7** | Targumim | Rounds out the interpretive tier. Aramaic reading tradition. | Torah + Prophets, selective key passages |

---

## 4. Data Model Updates

### 4.1 The `alternateEditions` field (already in BookInfo)

The existing `alternateEditions` field on the BookInfo data model should be expanded to support the tier structure:

```javascript
alternateEditions: [
  {
    id: "dss-1qisaiah-a",
    name: "Dead Sea Scrolls (1QIsaiah-a)",
    tier: "manuscript",        // "manuscript" | "pre-nicaea-canon" | "interpretive"
    uiLabel: "Other manuscript traditions",
    sourceText: "1QIsaiah-a (Qumran Cave 1)",
    date: "150-100 BCE",
    preNicaea: true,
    scope: "full",             // "full" | "partial" | "fragments"
    description: "The Great Isaiah Scroll — the oldest complete manuscript of any biblical book.",
    license: "public-domain"
  }
]
```

### 4.2 Stacking UI Concept

On a chapter page, the reader sees the TCR rendering by default. A toggle or tab bar allows switching to or comparing with other traditions:

```
┌─────────────────────────────────────────────────┐
│ Isaiah 40:3                                      │
│                                                   │
│ [TCR ▼] [DSS] [LXX] [Targum]                    │
│                                                   │
│ "A voice calls out: In the wilderness,           │
│  prepare the way of the LORD..."                 │
│                                                   │
│ ┌─ DSS Variant ──────────────────────────────┐   │
│ │ 1QIsaiah-a reads identically here.         │   │
│ │ No significant variant at this verse.      │   │
│ └────────────────────────────────────────────┘   │
│                                                   │
│ ┌─ LXX Reading ──────────────────────────────┐   │
│ │ "A voice of one crying in the wilderness:  │   │
│ │  Prepare the way of the Lord..."           │   │
│ │ Note: The LXX punctuation differs — the    │   │
│ │ voice is "in the wilderness," not the      │   │
│ │ preparation. Matthew 3:3 follows the LXX.  │   │
│ └────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### 4.3 Variant Verse Schema

For manuscript traditions that stack against the base TCR text, each variant verse needs:

```json
{
  "verse": 3,
  "tradition": "dss-1qisaiah-a",
  "has_variant": true,
  "variant_rendering": "The DSS reading here...",
  "variant_notes": ["Explanation of how and why this differs from the MT"],
  "significance": "minor" | "moderate" | "major" | "theological",
  "manuscript_reference": "1QIsaiah-a, col. XXXIII, line 3"
}
```

For standalone books (1 Enoch, Jubilees), use the standard TCR verse schema — they don't stack against anything, they stand alone.

---

## 5. Site Architecture Updates

### 5.1 Books Page (`/books`)

The Library page should organize traditions visually:

- **Standard Bible** (66 books) — current implementation
- **Extended Library** — grouped by tier:
  - Manuscript Traditions (DSS, LXX, Samaritan Pentateuch)
  - Pre-Nicaea Canon (1 Enoch, Jubilees)
  - Interpretive Traditions (Targumim, JST)

### 5.2 Canon Filter

A future UI control on `/books` that lets users filter by canonical tradition:

- Protestant (66 books)
- Catholic (73 books — adds Deuterocanonical)
- Orthodox (78+ books — adds Orthodox additions)
- Ethiopian (81+ books — adds 1 Enoch, Jubilees, etc.)
- All traditions (everything)

### 5.3 Chapter Pages

When a chapter has alternate editions available, show a tradition selector. Default to TCR. Allow side-by-side comparison or toggle view.

---

## 6. What NOT to Do

1. **Do not present the JST as a manuscript tradition.** It is an interpretive/revelatory revision of the KJV English text. The UI must make this clear through tier labeling.
2. **Do not use any copyrighted modern English translation** (ESV, NIV, NASB, NLT, etc.) for comparison. TCR renderings from each source text are original work.
3. **Do not use the Community of Christ "Inspired Version"** for JST content. Only the LDS-recognized JST text.
4. **Do not rush the Extended Library at the expense of the base rendering.** The standard 66-book Bible from the WLC/SBLGNT is the foundation. Extended traditions are built on top of a completed base, not instead of it.
5. **Do not harmonize traditions.** When texts disagree, show both readings. The point is comparison, not resolution.

---

## 7. SOT Updates Required

Update the Source of Truth with:
- This document referenced in the governing documents table
- The tier structure added to the Extended Library section of the roadmap
- Priority order for tradition implementation
- JST copyright research flagged as a blocking item for Priority 4
- Pre-Nicaea framing language added to the project description

---

## 8. Generation Implications

Each new tradition will require its own generation prompt adapted from the master prompt:
- **DSS:** Source text changes from WLC to specific scroll editions. Variant annotation format needed.
- **LXX:** Source language changes from Hebrew to Greek. Requires Greek competency in the prompt.
- **1 Enoch / Jubilees:** Source language is Ge'ez (Ethiopic). Rendered from scholarly English translations of the Ge'ez (Charles, Knibb, VanderKam) with full disclosure.
- **Targumim:** Source language is Aramaic. Rendered from the Aramaic with interpretive-tradition framing.
- **JST:** Source is English (KJV-based). The rendering IS the JST text itself — the value is in the stacking comparison and the notes explaining what Joseph Smith changed and why.
- **Samaritan Pentateuch:** Source is Samaritan Hebrew script. Rendered from critical editions with variant annotations against the MT.

**Do not begin generating Extended Library content until the base 66-book rendering is substantially complete** (at minimum through the Prophets). The foundation must be solid before the additions.

---

*"Every tradition that shaped how people read the Bible — from the Dead Sea caves to the Restoration — in one place, side by side, for free."*
