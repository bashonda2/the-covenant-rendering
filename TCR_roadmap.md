# The Covenant Rendering — Strategic Roadmap

**Status:** Active working document. Companion to `TCR_source_of_truth.md`.
**Owner:** Aaron Blonquist.
**Last revised:** 2026-05-11 (initial — v1.0).

> *Previous roadmap (March 2026, completed April 2026) preserved as `TCR_roadmap_archive_2026-04-08.md`. This document supersedes it with the post-completion strategic direction.*

---

## 1. Vision

The Covenant Rendering aims to become **the single most comprehensive, scholarly, open-source biblical-text corpus in existence** — the resource that every biblical scholar treats as required sourcing.

This is a defensible ambition. The pre-Nicene and rabbinic source texts that scholars actually consult are scattered across paid databases (Logos, Accordance), public-domain HTML dumps with no interconnection (sacred-texts.com, earlychristianwritings.com, Schaff's Ante-Nicene Fathers on CCEL), and print-only critical editions (Loeb, Sources Chrétiennes). **No existing online resource integrates them.** None has verse-level cross-tradition linking. None has AI search across the whole corpus. None is open under CC-BY-4.0.

TCR can be the first because:

1. It already has the foundation — Bible with manuscript and interpretive traditions, verse-level tradition cards, cross-reference linkification, AI search, ⌘K navigation, open structured data.
2. AI generation makes the rendering bottleneck tractable. What previously required teams of scholars and decades can be paced across months by a small operation with rigorous quality controls.
3. The CC-BY-4.0 licensing makes it usable in ways the commercial alternatives are not.

This document codifies the multi-pillar plan to get there.

---

## 2. Current State (May 2026)

| Component | State |
|---|---|
| Canonical Bible | 66 books, 1,189 chapters, 31,169 verses — translated from WLC + SBLGNT |
| Deuterocanonical | 7 books / 137 chapters — Jerome's Vulgate Latin + English |
| Pre-Nicaea Canon | 1 Enoch (108 ch), Jubilees (50 ch) |
| Dead Sea Scrolls | Per-chapter Isaiah, Deuteronomy, 1-2 Samuel, Psalms + 22 fragment-summary books |
| Septuagint | Per-chapter Isaiah/Psalms/Proverbs/Job/Jeremiah/Daniel/Esther/Exodus/1 Samuel + per-book variant files for 30 other OT books |
| Samaritan Pentateuch | 5 books, 160 variants |
| Targumim | 1,001 entries (Onkelos 393 + Jonathan 608) — Pre-Nicene Tier S complete |
| Latin Vulgate | 838 renderings across all 66 books |
| Joseph Smith Translation | Book of Moses, JS-Matthew, Appendix, 428 footnotes |
| AI search | 2,794 tradition entries indexed; 93 books / 2,167 chapters |
| UX | Command Palette (⌘K), inline tradition cards, linkified cross-refs + hover preview, canon filter |

**Total page count on site: ~2,500.**

---

## 3. Three Strategic Pillars

The path from "rich Bible site" to "comprehensive scholarly corpus" runs through three coordinated pillars:

| Pillar | Goal | Estimated scope |
|---|---|---|
| **I. Comprehensive Pre-Nicene Corpus** | Add all major pre-Nicene Jewish + Christian + heterodox texts | ~4,000 new chapters / 12-18 months |
| **II. Verse-as-Center Architecture** | Every verse is a portal to every resource that touches it | UX rework; ~1 month |
| **III. Doctrinal Index** | Document every major doctrine, when it was formulated, by whom, with primary-source citations | ~200 doctrine entries / 6-9 months |

Each pillar is independent but they reinforce each other. The corpus expansion gives the verse pages more to surface; the verse-page architecture makes the corpus navigable; the doctrinal index makes the whole library a usable scholarly tool rather than just a text dump.

---

# Pillar I — Comprehensive Pre-Nicene Corpus

## 4. Corpus Phase Plan

Each phase is a contained workstream with its own milestone deliverable. The phases are independent but sequenced for compound value (each phase builds on the cross-linkage of prior phases).

### Phase A — Pre-Nicene Tier S Corroboration

**Strategic value:** Sharpens the pre-Nicene Tier S argument already in TCR (Targumic Memra theology). Demonstrates that *Jewish* mediator-doctrine predates *Christian* Logos-Christology by decades. The single most distinctive content addition.

**Scope:** ~350 chapters / 6-8 weeks

| Text | Date | Chapters | Significance |
|---|---|---|---|
| **Philo of Alexandria — Logos selections** | ~20 BCE – 50 CE | ~50 entries from key treatises (On the Confusion of Tongues, On the Migration of Abraham, On the Cherubim, Allegorical Interpretation, Life of Moses, On Dreams, Questions on Genesis/Exodus) | Pre-Christian Jewish Logos doctrine. "Second God," "Eldest Son," "First-Born Word," "Image of God." Direct conceptual ground for John 1. |
| **Justin Martyr — *Dialogue with Trypho*** | ~155 | 142 chapters | Earliest extended Christian-Jewish dialogue. Justin uses Targumic-style messianic exegesis. Calls Christ "another God and Lord" — pre-Nicene subordinationism that Nicaea would later anathematize. |
| **Justin Martyr — First Apology** | ~155 | 68 chapters | Earliest Christian self-defense to imperial Rome. Logos as universal seed (logos spermatikos). |
| **Justin Martyr — Second Apology** | ~155 | 15 chapters | Follow-up apology. |
| **Odes of Solomon** | ~100 | 42 odes | Earliest Christian hymnbook. Christ speaks in first person; pre-Nicene worship language. Found at Nag Hammadi + Syriac MSS. |
| **1 Clement** | ~95-96 | 65 chapters | Earliest Christian text outside the NT. Bishop of Rome to Corinth. Already presupposes ecclesiastical hierarchy + apostolic succession. |
| **Didache** | ~50-150 | 16 chapters | Earliest church manual. Baptismal liturgy, Eucharistic prayer, Two Ways ethics. Pre-dates most NT Pauline letters in some scholars' estimation. |
| **Ignatius of Antioch — 7 letters** | ~107 | 7 letters | Earliest high Christology outside NT. Calls Jesus "our God" (Eph 18:2). Martyred ~110. |
| **Letter to Diognetus** | ~150-200 | 12 chapters | Apologetic letter; "soul of the world" metaphor for Christians; subordinationist Christology. |
| **Letter of Aristeas** | ~150-100 BCE | 322 verses (no chapter structure — sectioned in critical eds.) | Jewish Hellenistic account of LXX translation. Establishes the legend; theologically significant for Jewish-Greek interface. |
| **4 Ezra (2 Esdras 3-14)** | ~100 | 12 chapters | Late-1st-century Jewish apocalypse. Messiah reigns 400 years and dies. Cosmically different Christology from Nicene. Already in Orthodox canon. |
| **2 Baruch (Syriac Apocalypse)** | ~100 | 87 chapters | Companion apocalypse to 4 Ezra. Heavenly Jerusalem; eschatological scenarios. |

**Phase A milestone:** *TCR becomes the only online source with Philo's Logos passages cross-linked to John 1, Targum Onkelos Memra entries, and the Vulgate.* This is a quotable result.

---

### Phase B — Pre-Nicene Christian Corpus (Ante-Nicene Fathers)

**Strategic value:** The complete pre-Nicene Christian theological corpus. Required reading for any patristic scholarship. Existing Schaff edition (Ante-Nicene Fathers, 10 vols, 1885 — public domain) is the de-facto reference but is in archaic English and not cross-linked. TCR modernizes + cross-links.

**Scope:** ~800 chapters / 10-12 weeks

| Text | Date | Significance |
|---|---|---|
| **Irenaeus — *Against Heresies*** | ~180 | 5 books. Foundational anti-Gnostic. Recapitulation theology. First catalog of NT canon. |
| **Irenaeus — *Demonstration of the Apostolic Preaching*** | ~190 | Survives in Armenian. Catechetical summary of early-Catholic faith. |
| **Tertullian — *Apologeticum*** | ~197 | Defense of Christians against Roman accusations. |
| **Tertullian — *Against Praxeas*** | ~213 | First Latin treatise on the Trinity. Coined *trinitas*, *persona*, *substantia*. Held Father > Son (subordinationism). |
| **Tertullian — *On the Resurrection of the Flesh*** | ~210 | Bodily resurrection doctrine. |
| **Tertullian — *On Baptism*** | ~200 | Earliest extant treatise on baptism. |
| **Tertullian — *On Prescription Against Heretics*** | ~200 | Apostolic-succession argumentation. |
| **Tertullian — *On the Soul*** | ~210 | Traducianism (souls inherited). |
| **Tertullian — *Against Marcion*** | ~207 | 5 books vs Marcion. Defends OT-NT unity. |
| **Clement of Alexandria — *Stromata*** | ~200 | 8 books. Christianity-as-true-philosophy. |
| **Clement of Alexandria — *Paedagogus*** | ~198 | 3 books. Christ as moral instructor. |
| **Clement of Alexandria — *Protrepticus*** | ~195 | Exhortation to Greeks to become Christian. |
| **Origen — *On First Principles (De Principiis)*** | ~225 | 4 books. First systematic Christian theology. Eternal generation; subordinationism; apokatastasis. |
| **Origen — *Against Celsus*** | ~248 | 8 books. Major anti-pagan apology. |
| **Hippolytus — *Refutation of All Heresies*** | ~225 | 10 books. Roman bishop; cataloged Gnostic systems. |
| **Hippolytus — *Apostolic Tradition*** | ~215 | Liturgical/ecclesiastical order. Foundational for Roman Rite. |
| **Cyprian — Selected letters** | ~250 | Bishop of Carthage. Donatist precursor controversies. |
| **Cyprian — *On the Unity of the Catholic Church*** | ~251 | Episcopal-monarchical ecclesiology. |
| **Novatian — *On the Trinity*** | ~250 | First Latin Trinitarian treatise. Subordinationist. |
| **Athenagoras — *Plea for Christians*** | ~177 | Apology to Marcus Aurelius. Trinitarian language. |
| **Athenagoras — *On the Resurrection*** | ~178 | Bodily resurrection. |
| **Theophilus of Antioch — *To Autolycus*** | ~180 | First documented use of "Trinity" (triados). |
| **Tatian — *Address to the Greeks*** | ~170 | Anti-Greek philosophical polemic. |
| **Tatian — *Diatessaron*** | ~170 | Earliest gospel harmony. Used liturgically until ~5th c. in Syriac East. |
| **Melito of Sardis — *Peri Pascha*** | ~170 | Easter homily. Earliest evidence of anti-Judaism in Christian liturgy. |
| **Aristides — *Apology*** | ~125 | Earliest extant Christian apology. |
| **Minucius Felix — *Octavius*** | ~200 | Latin dialogue defending Christianity. |
| **Lactantius — *Divine Institutes*** | ~310 | 7 books. Last major pre-Nicene Latin theology. |
| **Shepherd of Hermas** | ~140 | Apocalyptic vision-text. Widely read; in Codex Sinaiticus. |
| **Epistle of Barnabas** | ~70-132 | Anti-Jewish allegorical reading of OT. |
| **2 Clement** | ~140-160 | Earliest extant Christian sermon. |
| **Martyrdom of Polycarp** | ~155 | Earliest detailed martyrdom account. |
| **Polycarp — Letter to the Philippians** | ~110-140 | Bishop of Smyrna. Pastoral letter. |
| **Papias fragments** | ~110 | Earliest comments on gospel composition. |
| **Hermias — *Mockery of the Pagan Philosophers*** | ~200 | Anti-pagan satire. |
| **Gregory Thaumaturgus — Selected works** | ~250 | "Wonder-worker" of Neocaesarea. |
| **Methodius of Olympus — *Symposium*** | ~290 | On virginity; anti-Origenist subordinationism. |

**Phase B milestone:** *TCR contains the complete Ante-Nicene Fathers corpus in modern English with verse-level cross-references to canonical Scripture.*

---

### Phase C — Jewish Hellenistic & Pseudepigrapha

**Strategic value:** Second Temple Jewish literature — the textual world Jesus and the apostles inhabited. Most of this corpus has no canonical status but is essential context for NT.

**Scope:** ~700 chapters / 10-12 weeks

| Text | Date | Significance |
|---|---|---|
| **Philo of Alexandria — full corpus** | ~20 BCE – 50 CE | ~40 treatises. Allegorical biblical interpretation; Logos theology; Hellenistic Jewish synthesis. |
| **Josephus — *The Jewish War*** | ~75 | 7 books. First-century eyewitness to the destruction of Jerusalem. |
| **Josephus — *Antiquities of the Jews*** | ~93 | 20 books. Comprehensive Jewish history. Contains *Testimonium Flavianum* (Jesus reference) and James-brother-of-Jesus reference. |
| **Josephus — *Against Apion*** | ~95 | Defense of Judaism. |
| **Josephus — *Life*** | ~95 | Autobiography. |
| **Testaments of the Twelve Patriarchs** | ~100 BCE – 100 CE | Pre-Christian + Christian-interpolated. Each patriarch addresses his sons. |
| **Testament of Moses (Assumption of Moses)** | ~30 CE | Cited Jude 9. |
| **Testament of Abraham** | ~100 CE | Heavenly journey narrative. |
| **Testament of Job** | ~100 BCE – 100 CE | Hellenistic Job narrative. |
| **Testament of Solomon** | ~100-300 CE | Demonology. |
| **2 Enoch (Slavonic Apocalypse)** | ~100 | Heavenly cosmology; Melchizedek tradition. |
| **3 Enoch (Hebrew Apocalypse)** | ~5th-6th c. but preserves earlier traditions | Metatron as "lesser YHWH." Direct evidence of Two-Powers theology condemned in b. Sanhedrin 38b. |
| **Apocalypse of Abraham** | ~100 | Heavenly throne vision; angelic mediator. |
| **Apocalypse of Adam** | ~100-300 | Sethian tradition; redeemer figure. |
| **Joseph and Aseneth** | ~100 BCE – 100 CE | Conversion narrative; Eucharistic-like meal language. |
| **Sibylline Oracles** | ~150 BCE – 700 CE | Jewish + Christian compositions imitating pagan oracles. |
| **Pseudo-Phocylides** | ~100 BCE – 100 CE | Hellenistic Jewish ethics in verse. |
| **Lives of the Prophets** | ~1st c. | Biographical traditions about OT prophets. |
| **Pseudo-Philo — *Biblical Antiquities* (LAB)** | ~70 | Rewritten Bible from Adam to David. |
| **3 Maccabees** | ~50 BCE | Already in Orthodox canon. |
| **4 Maccabees** | ~30-100 CE | Already in Orthodox canon. Stoic-Jewish philosophy of martyrdom. |
| **Prayer of Manasseh** | ~100 BCE – 100 CE | Already in Orthodox canon. Penitential prayer. |
| **1 Esdras** | ~150 BCE | Already in Orthodox canon. Greek alternative to Ezra-Nehemiah. |

**Phase C milestone:** *TCR contains the complete Second Temple Jewish literary corpus in modern English with cross-references to the canonical Bible and the Christian pre-Nicene texts in Phases A-B.*

---

### Phase D — NT Apocrypha & Nag Hammadi

**Strategic value:** The "Christianity that didn't win" — non-canonical Christian texts that shaped popular devotion, were read in early churches, and document the diversity that Nicaea and subsequent councils narrowed.

**Scope:** ~300 chapters / 6-8 weeks

| Text | Date | Significance |
|---|---|---|
| **Gospel of Thomas** | ~50-150 | Nag Hammadi. 114 sayings. Pre-canonical or parallel sayings tradition. |
| **Gospel of Peter** | ~150 | Docetic. Resurrection narrative with talking cross. |
| **Gospel of Mary** | ~150-200 | Mary Magdalene as foremost disciple. Gnostic. |
| **Gospel of Philip** | ~250 | Nag Hammadi. Valentinian. Bridal-chamber sacrament. |
| **Gospel of Truth** | ~150 | Nag Hammadi. Valentinian meditation on the Word. |
| **Gospel of Judas** | ~150-200 | Recovered 2006. Judas as Jesus's true disciple. |
| **Gospel of the Hebrews** | ~100-150 | Fragments. Jewish-Christian. |
| **Gospel of the Egyptians** | ~100-200 | Fragments. Sethian Gnostic. |
| **Gospel of the Ebionites** | ~150 | Fragments. Adoptionist Jewish-Christian. |
| **Infancy Gospel of Thomas** | ~150-200 | Childhood miracles of Jesus. |
| **Protoevangelium of James** | ~150 | Mary's life and Jesus's birth. Foundational for Marian devotion. |
| **Acts of John** | ~150-200 | Apocryphal acts. |
| **Acts of Paul (with Thecla)** | ~160-200 | Female apostolic-figure narrative. |
| **Acts of Peter** | ~150-200 | Includes Quo vadis legend. |
| **Acts of Thomas** | ~200-225 | Mission to India. Hymn of the Pearl. |
| **Acts of Andrew** | ~150-200 | Apocryphal acts. |
| **Apocalypse of Peter** | ~135 | Earliest detailed Christian vision of heaven/hell. |
| **Apocalypse of Paul** | ~250-400 | Heavenly journey; Dante precursor. |
| **Ascension of Isaiah** | ~100 | Christian apocalypse with descent Christology. |
| **5 Ezra / 6 Ezra** | ~150-200 | Christian additions to 4 Ezra. |
| **Epistle of the Apostles** | ~150 | Post-resurrection discourse against Gnostics. |
| **3 Corinthians** | ~150 | Apocryphal Pauline letter. |
| **Apocryphon of John** | ~150-200 | Nag Hammadi. Sethian creation myth. |
| **Tripartite Tractate** | ~200 | Nag Hammadi. Valentinian systematic theology. |
| **Sophia of Jesus Christ** | ~150 | Nag Hammadi. Post-resurrection revelation discourse. |
| **Pistis Sophia** | ~250 | Late Gnostic. Sophia mythology. |
| **On the Origin of the World** | ~250-300 | Nag Hammadi. Cosmogony. |
| **Trimorphic Protennoia** | ~200 | Nag Hammadi. Triple-form first thought. |
| **Three Steles of Seth** | ~250-300 | Nag Hammadi. Sethian. |
| **Apocalypse of Adam** | ~100-300 | Nag Hammadi. Pre-Christian Sethian. |

**Phase D milestone:** *TCR is the most comprehensive English-language modern-rendered NT apocrypha and Nag Hammadi corpus, with each text cross-referenced to canonical NT readings.*

---

### Phase E — Targumim Expansion

**Strategic value:** Deepens the Jewish interpretive tradition already in TCR. Pseudo-Jonathan and Neofiti are richer, more midrashic, and more theologically explicit than Onkelos.

**Scope:** ~200 chapters / 4-6 weeks

| Text | Date | Significance |
|---|---|---|
| **Targum Pseudo-Jonathan** | ~7th-8th c. but with earlier traditions | Expansive paraphrase Pentateuch. Most midrashically rich. |
| **Targum Neofiti** | ~1st-4th c. | Palestinian Pentateuch Targum. Discovered 1956. |
| **Fragmentary Targumim** | Various | Cairo Geniza fragments, Vatican MS, Paris MS. |
| **Targum Psalms** | ~4th-5th c. | Davidic-messianic readings. |
| **Targum Job** | Various | Christian-era. |
| **Targum Proverbs** | ~3rd-5th c. | Wisdom theology. |
| **Targum Megilloth** | Various | Song of Songs, Ruth, Lamentations, Ecclesiastes, Esther. |
| **Targum Chronicles** | Various | Late, expansive. |
| **11QtgJob** | ~50 BCE | Oldest extant Aramaic Targum. Already documented in DSS fragments. |

**Phase E milestone:** *Complete Targumic corpus — every available Targum tradition surfaced and cross-linked.*

---

### Phase F — Rabbinic Foundations

**Strategic value:** Foundational Jewish exegetical literature. The midrashic and halakhic tradition that runs parallel to Christian patristics. Provides Jewish reception-history of biblical texts.

**Scope:** ~400 chapters / 8-10 weeks

| Text | Date | Significance |
|---|---|---|
| **Mishnah** (selected tractates) | ~200 | 63 tractates. Foundational rabbinic law. Tractates Sanhedrin, Avodah Zarah, Pesachim, Berakhot, Avot most NT-relevant. |
| **Tosefta** (parallel tractates) | ~250 | Parallel to Mishnah; additional traditions. |
| **Mekhilta of R. Ishmael** | ~250 | Tannaitic midrash on Exodus. |
| **Sifra (Torat Kohanim)** | ~250 | Tannaitic midrash on Leviticus. |
| **Sifre Numbers** | ~250 | Tannaitic midrash. |
| **Sifre Deuteronomy** | ~250 | Tannaitic midrash. |
| **Genesis Rabbah** | ~400 | Amoraic midrash on Genesis. |
| **Exodus Rabbah** | ~10th c. but with earlier material | Midrash. |
| **Pirkei de-Rabbi Eliezer** | ~8th-9th c. | Pseudo-Tannaitic narrative midrash. |
| **Pesikta de-Rav Kahana** | ~5th c. | Festival-cycle midrash. |
| **Tanchuma-Yelammedenu** | ~4th-5th c. | Midrash collection. |
| **Avot de-Rabbi Natan** | ~700-900 | Aggadic expansion of Pirkei Avot. |
| **Talmud selections** | ~400-600 | Specific passages of NT relevance (e.g., Sanhedrin 38b on Two Powers, Sanhedrin 43a on Jesus, Avodah Zarah passages on Christianity, Berakhot on prayer). |

**Phase F milestone:** *Rabbinic foundations surfaced with the Christian-readable NT-relevance arguments documented at each entry.*

---

### Phase G — Syriac Christian Corpus

**Strategic value:** Eastern Christian witness independent of Greek and Latin traditions. The Peshitta is the Syriac Bible — its variants are significant.

**Scope:** ~200 chapters / 4-6 weeks

| Text | Date | Significance |
|---|---|---|
| **Peshitta** (NT variants) | ~2nd-4th c. | Syriac Bible. Old Syriac variants in Sinaiticus + Curetonianus. |
| **Diatessaron** (Syriac/Arabic recension) | ~170 | Gospel harmony. |
| **Aphrahat — *Demonstrations*** | ~340 | Earliest Syriac Christian theology. |
| **Ephrem the Syrian — Selected works** | ~350-373 | Hymns, biblical commentaries. Post-Nicene but foundational for Syriac tradition. |
| **Acts of Thomas** (Syriac version) | ~200 | See Phase D. |
| **Odes of Solomon** (Syriac MSS) | ~100 | See Phase A. |
| **Bardaisan fragments** | ~150-200 | Early Syriac Gnostic. |

**Phase G milestone:** *Eastern Christian textual witness documented — TCR includes the Syriac tradition's specific NT readings and its earliest theological voices.*

---

### Phase H — Patristic Biblical Commentaries (post-Nicene, foundational)

**Strategic value:** The major commentaries that became formative for Christian biblical interpretation. Post-Nicene but the standard medieval interpretive frame.

**Scope:** ~600 chapters / 12-15 weeks

| Author | Works | Date |
|---|---|---|
| **John Chrysostom** | Homilies on Genesis, Psalms, Matthew, John, Acts, Romans, Hebrews | ~390-407 |
| **Augustine** | On Genesis, On the Psalms, Tractates on John, City of God (selections), Confessions (selections), On the Trinity | ~395-430 |
| **Jerome** | Commentaries on Isaiah, Jeremiah, Ezekiel, Daniel, Minor Prophets, Matthew | ~390-410 |
| **Ambrose of Milan** | Hexameron, On the Christian Faith, On the Holy Spirit | ~380-395 |
| **Athanasius** | Festal Letters (esp. 39 — canon), On the Incarnation, Against the Arians | ~330-373 |
| **Basil of Caesarea** | Hexameron, On the Holy Spirit | ~370-379 |
| **Gregory of Nazianzus** | Theological Orations | ~380 |
| **Gregory of Nyssa** | On the Making of Man, On the Soul and the Resurrection | ~380 |
| **Cyril of Alexandria** | Commentaries on John, Luke, Isaiah; On the Unity of Christ | ~410-440 |
| **Cyril of Jerusalem** | Catechetical Lectures | ~350 |

**Phase H milestone:** *The major patristic biblical commentaries are surfaced and cross-linked to the verses they exposit. A reader on Genesis 1 can see how Augustine, Chrysostom, Basil, Origen each read the verse.*

---

## 5. Phase Sequencing

Phases run in approximately the order A → B → C → D → E → F → G → H, but with overlap possible where authoring resources permit:

- Phases A-D are **pre-Nicene corpus** — the strict scope of the user's original ambition. Estimated 9-12 months at sustained pace.
- Phases E-F are **Jewish corpus expansion** — Targumim deepening + rabbinic foundations. Independent track. Estimated 3-4 months.
- Phases G-H are **Eastern + post-Nicene patristic** — completing the picture. Estimated 4-5 months.

**Estimated full-corpus completion: 18-24 months at current pacing.**

---

# Pillar II — Verse-as-Center Architecture

## 6. The Usability Problem

As the corpus grows, a single verse will have:

- 1 modern English rendering
- Hebrew or Greek source text + KJV reference
- Translator notes (already linkified)
- Key terms (already shown)
- Tradition cards (DSS, LXX, Targum, Vulgate, Samaritan, JST, etc.) — already shown inline
- Cross-references (linkified text in notes; hover preview already works)
- **NEW: Patristic citations** — every Father who quoted this verse, with their context
- **NEW: Liturgical use** — where the verse appears in Eastern/Western liturgy
- **NEW: Doctrinal use** — what doctrines were built on this verse (links to Pillar III)
- **NEW: Apocryphal echoes** — every apocryphal text that quotes or echoes this verse
- **NEW: Rabbinic citations** — Mishnah/Tosefta/Midrash references
- **NEW: Manuscript variants beyond major traditions** — minor readings, conjectural emendations
- **NEW: Greek/Hebrew morphological parse** — verb tense/voice/mood for original-language students
- **NEW: Concordance** — every other occurrence of key terms in the canon

A chapter page can't surface all of this for every verse without becoming unreadable. We need a **layered information architecture**.

## 7. Architecture Design

### Layer 1: Reading view (chapter page) — keep as-is

The current chapter page is the **reading experience**. It surfaces:
- The verse rendering + source text + KJV
- Translator notes + key terms (collapsed in `<details>`)
- Inline tradition cards (already lazy-loaded on heavy chapters)

This stays. It's clean, fast, and the primary use case.

### Layer 2: Verse deep-dive page (`/[book]/[chapter]/[verse]`) — major rework

The existing verse permalink page (e.g., `/genesis/1/1`) becomes the **comprehensive verse-detail page**. Everything about that verse, organized into sections:

```
┌─────────────────────────────────────────────────────┐
│ GENESIS 1:1 — bereshit bara elohim                  │
│ ─────────────────────────────────────────────────── │
│ HEBREW SOURCE  | KJV  | TCR RENDERING               │
├─────────────────────────────────────────────────────┤
│ ▸ MANUSCRIPT WITNESSES (DSS, LXX, Samaritan)        │
│ ▸ INTERPRETIVE TRADITIONS (Targum, Vulgate, JST)    │
│ ▸ APOCRYPHAL & PRE-NICENE ECHOES (Philo, Justin..)  │
│ ▸ PATRISTIC CITATIONS (Augustine, Chrysostom, ...)  │
│ ▸ RABBINIC RECEPTION (Genesis Rabbah, Talmud, ...)  │
│ ▸ DOCTRINAL USE (creatio ex nihilo, imago Dei, ...) │
│ ▸ LITURGICAL USE (Easter Vigil readings, ...)       │
│ ▸ CROSS-REFERENCES (John 1:1, Heb 1:2, ...)         │
│ ▸ ORIGINAL-LANGUAGE PARSE (morphology + lexicon)    │
│ ▸ TRANSLATOR NOTES (current chapter-level content)  │
│ ▸ KEY TERMS                                         │
└─────────────────────────────────────────────────────┘
```

Each section is independently expandable. Lazy-loaded where heavy.

### Layer 3: Per-tradition deep-dive (existing) — `/dss-isaiah/53`, `/lxx-isaiah/53`, etc.

These already exist. Stay as the dedicated comparison views.

### Architecture changes required

1. **New per-verse data API** — `/data/verse/{book}/{ch}/{v}.json` returning a unified document with all related resources (tradition entries, patristic citations, doctrinal links, etc.) for one verse. Built at compile time.
2. **Verse deep-dive page rewrite** — replace existing `/[book]/[chapter]/[verse].astro` with the comprehensive layout above.
3. **Inline "Deep dive" link** on each verse in chapter pages — replaces the current verse-permalink copy button with a "View everything about this verse →" link to the deep page.
4. **Patristic-citation index** — new data structure mapping Bible references to patristic citations. Generated from Phase B authoring.
5. **Doctrinal-link index** — new data structure mapping doctrines to scriptural foundations. Generated from Pillar III work.
6. **Concordance integration** — existing concordance.json already has terms; needs cross-linking with verse pages.

### Architectural milestone

**Verse deep-dive shipped before Phase C completes** so the new corpus authored in Phases A-B is immediately surfaced on verse pages. Target: deep-dive UX ships after Phase A completes (~8-10 weeks from now).

---

# Pillar III — Doctrinal Index

## 8. Vision

A comprehensive, scholarly, cross-referenced catalog of every major Christian doctrine, documenting:

1. **What the doctrine is** — clear definition.
2. **Scriptural foundation** — verses cited in support, with TCR links.
3. **Historical formulation** — when it was first articulated, by whom, in what document.
4. **Conciliar/dogmatic decisions** — councils, papal definitions, confessions of faith.
5. **Contested positions** — every major dissenting view with primary-source citations.
6. **Modern denominational positions** — Catholic, Orthodox, Lutheran, Reformed, Anabaptist, Anglican, Methodist, Pentecostal, etc.
7. **Change-tracking** — where doctrine evolved (e.g., slavery, usury, religious liberty, women's ordination, contraception).

**Bias policy: every claim is sourced or explicitly called out as contested.** Where multiple positions are defensible, each is presented in its strongest form with primary-source citations. TCR does not adjudicate; it documents.

## 9. Doctrine Taxonomy

A doctrine entry is a JSON record at `src/data/doctrines/{slug}.json` with structured fields. The full taxonomy is organized into thirteen domains:

### IX.1 — Theology Proper (the doctrine of God)
- Divine simplicity
- Divine attributes (omniscience, omnipotence, omnipresence, immutability, impassibility, aseity, eternity, holiness, justice, love)
- God's relationship to time (timelessness vs everlastingness)
- God's relationship to creation (creator-creation distinction)
- Divine action (concursus, primary/secondary causes)
- Divine providence
- Divine concurrence and freedom of creatures
- Open theism (modern dissent)
- Process theology (modern dissent)
- Theodicy (problem of evil)
- Knowledge of God (natural theology vs revelation)
- Names of God (YHWH, Elohim, Adonai, etc.)

### IX.2 — Trinitarian Doctrine
- The Trinity (formal: Constantinople 381; informal earlier)
- Persons and essence (Cappadocian formulation)
- Eternal generation of the Son
- Eternal procession of the Spirit
- Filioque (Western addition; Eastern rejection; 1054 schism)
- Coinherence / perichoresis
- The economic Trinity vs the immanent Trinity
- Subordinationism (pre-Nicene; condemned)
- Modalism / Sabellianism (condemned)
- Tritheism (condemned)
- Arianism (Council of Nicaea 325)
- Semi-Arianism (homoiousios vs homoousios)
- Social Trinitarianism (modern)

### IX.3 — Christology
- Deity of Christ (homoousios — Nicaea 325)
- Humanity of Christ
- The hypostatic union (Chalcedon 451)
- The two natures (without confusion, change, division, separation)
- The two wills (Third Constantinople 681; against monothelitism)
- The communicatio idiomatum
- Pre-existence
- Kenosis / self-emptying (Phil 2)
- Sinlessness
- Virgin birth
- Bodily resurrection
- Ascension
- Second coming (parousia)
- Christ's three offices (prophet/priest/king — munus triplex)
- Christ's descent into hell (descensus ad inferos)
- Adoptionism (condemned)
- Docetism (condemned)
- Nestorianism (condemned Ephesus 431)
- Monophysitism (condemned Chalcedon 451)
- Monothelitism (condemned Third Constantinople 681)
- Apollinarianism (condemned)

### IX.4 — Pneumatology (the Holy Spirit)
- Personhood of the Spirit
- Deity of the Spirit (Constantinople 381)
- Procession (Eastern: from Father only; Western: filioque)
- Indwelling of the Spirit
- Sealing of the Spirit
- Baptism in / with the Spirit
- Gifts of the Spirit (charismata)
- Fruit of the Spirit
- Sanctification by the Spirit
- Inspiration of Scripture by the Spirit
- Cessationism vs continuationism

### IX.5 — Soteriology
- Atonement theories: Christus Victor, Recapitulation (Irenaeus), Ransom (Origen), Satisfaction (Anselm 1098), Penal Substitution (Reformers), Moral Influence (Abelard), Governmental (Grotius)
- Original sin (Augustine ~412; Trent 1547)
- Pelagianism (condemned Carthage 418)
- Semi-Pelagianism (condemned Orange 529)
- Total depravity (Reformed)
- Election (Catholic vs Reformed vs Arminian formulations)
- Predestination (single vs double)
- Reprobation
- Effectual calling
- Regeneration
- Conversion (faith + repentance)
- Justification (forensic vs ontological — Reformation hinge)
- Imputed vs infused righteousness
- Faith and works (James-Paul tension)
- Sola fide (Reformation)
- Sola gratia
- Sanctification (progressive vs definitive)
- Perseverance of the saints
- Apostasy (possible vs impossible)
- Theosis / deification (Eastern emphasis)
- Universalism / apokatastasis (Origen; debated)
- Annihilationism
- Limited vs unlimited atonement
- The order of salvation (ordo salutis)

### IX.6 — Ecclesiology
- The Church as one / holy / catholic / apostolic (Nicene Creed)
- Visible vs invisible Church
- The Mystical Body of Christ
- Apostolic succession
- Petrine primacy / papal infallibility (Vatican I 1870)
- Conciliarism
- Episcopal vs presbyterian vs congregational vs Quaker polity
- Ordination (sacrament vs commission)
- Women's ordination (denominational positions)
- The threefold ministry (bishop/priest/deacon)
- Magisterium
- Sensus fidelium
- Marks of the Church
- The Church and the state (Erastianism, theocracy, separationism)
- Ecumenism

### IX.7 — Sacramentology
- Number of sacraments (7 in Catholic/Orthodox; 2 in most Protestant)
- Sacrament vs ordinance
- Baptism: efficacy, mode (immersion/pouring/sprinkling), subjects (infant vs believer's)
- Baptismal regeneration
- Eucharist:
  - Transubstantiation (Lateran IV 1215; Trent 1551)
  - Consubstantiation (Luther)
  - Memorialism (Zwingli)
  - Spiritual / pneumatic presence (Calvin)
  - Eastern Orthodox mystery
  - Open vs closed communion
- Confirmation
- Holy orders
- Marriage as sacrament (vs covenant)
- Penance / reconciliation / confession
- Anointing of the sick / extreme unction
- Sacramentals

### IX.8 — Hamartiology
- Sin's origin
- Original sin
- Concupiscence
- Mortal vs venial sin (Catholic)
- Total depravity (Reformed)
- Transmission (federal vs realist vs mediate imputation)
- Personal sin
- Sins of commission vs omission
- Seven deadly sins (medieval)
- Sin against the Holy Spirit
- The unpardonable sin
- Demons / Satan / fallen angels
- The fall of Adam (literal vs theological)

### IX.9 — Bibliology
- Inspiration (verbal vs plenary vs dynamic)
- Inerrancy (Hodge/Warfield 1881; Chicago Statement 1978)
- Infallibility
- The canon: OT formation, NT formation, deuterocanonical disputes
- Apocrypha (Catholic vs Protestant lists)
- Sufficiency of Scripture
- Perspicuity of Scripture (Reformation)
- Authority of Scripture vs tradition (sola scriptura vs prima scriptura)
- Versification and chapter divisions
- Translation philosophy (formal vs dynamic equivalence)

### IX.10 — Eschatology
- Death
- The intermediate state
- Heaven
- Hell (eternal conscious torment vs annihilationism vs universalism)
- Purgatory (Catholic; rejected Reformation)
- Limbo (medieval; never definitive)
- Resurrection of the dead (general)
- Particular judgment
- General judgment
- The millennium (premillennial / postmillennial / amillennial)
- Tribulation
- Rapture (dispensational; 19th c. innovation)
- Antichrist
- Beatific vision
- New heavens and new earth
- Apokatastasis
- The communion of saints

### IX.11 — Mariology
- Mary as Theotokos (Ephesus 431)
- Perpetual virginity (Lateran 649)
- Immaculate Conception (Pius IX 1854)
- Assumption of Mary (Pius XII 1950)
- Mary as Mediatrix / Co-Redemptrix (debated, not officially defined)
- Marian devotions and apparitions
- Protestant rejections

### IX.12 — Moral / Practical Theology
- Natural law
- Conscience
- Cardinal virtues (prudence, justice, fortitude, temperance)
- Theological virtues (faith, hope, charity)
- Beatitudes
- Just war doctrine
- Pacifism
- Capital punishment (changing Catholic position)
- Slavery (changing — Christian abolition)
- Usury (changing — Lateran 1215 → modern banking acceptance)
- Religious liberty (Dignitatis Humanae 1965)
- Sexual ethics
- Marriage (divorce, polygamy, same-sex)
- Contraception (Humanae Vitae 1968)
- Abortion
- Euthanasia / end-of-life ethics
- Wealth and poverty (theology of)
- Stewardship of creation
- Just labor and economic ethics

### IX.13 — Angelology / Demonology
- Existence and nature of angels
- The angelic hierarchy (Pseudo-Dionysius)
- Guardian angels
- Fallen angels / demons
- Satan
- Demonic possession and exorcism
- The veneration of saints
- Intercession of saints
- Beatification and canonization

---

**Estimated total doctrinal entries: ~200**, organized into the 13 domains above. Each entry is roughly 1,000-2,000 words with primary-source citations and TCR scripture links.

## 10. Doctrine Entry Schema

Each doctrine is a JSON file with this structure:

```json
{
  "slug": "original-sin",
  "name": "Original Sin",
  "domain": "hamartiology",
  "definition": "...",
  "scriptural_foundations": [
    {
      "reference": "Genesis 3:1-19",
      "url": "/genesis/3",
      "note": "The fall narrative — Adam and Eve's disobedience."
    },
    {
      "reference": "Romans 5:12-21",
      "url": "/romans/5#v12",
      "note": "Paul's locus classicus on imputed Adamic guilt and Christ's federal headship."
    }
  ],
  "historical_formulation": [
    {
      "date": "~412 CE",
      "figure": "Augustine of Hippo",
      "source": "De peccatorum meritis et remissione",
      "summary": "Augustine's mature doctrine of inherited guilt..."
    },
    {
      "date": "418 CE",
      "council": "Council of Carthage",
      "canon": "Canon 2",
      "summary": "Condemnation of Pelagianism..."
    }
  ],
  "conciliar_definitions": [
    {"council": "Trent Session V", "date": "1546", "summary": "..."}
  ],
  "contested_positions": [
    {"position": "Pelagianism", "advocates": ["Pelagius", "Celestius"], "source": "...", "argument": "...", "status": "condemned 418 Carthage"},
    {"position": "Semi-Pelagianism", "advocates": ["John Cassian"], "source": "...", "argument": "...", "status": "condemned 529 Orange"},
    {"position": "Eastern Orthodox ancestral-sin view", "argument": "Inheritance of mortality and corruption but not guilt", "source": "Maximus the Confessor..."},
    {"position": "Federal (Reformed) imputation", "advocates": ["Calvin", "Hodge"], "source": "...", "argument": "..."},
    {"position": "Mediate imputation", "advocates": ["Placeus"], "source": "..."}
  ],
  "denominational_positions": {
    "catholic": "Defined Trent 1547; CCC §§385-421...",
    "orthodox": "Ancestral sin; not Augustinian guilt-transmission...",
    "lutheran": "Concord Formula Article 1; total depravity...",
    "reformed": "Westminster Confession VI; federal imputation...",
    "anabaptist": "Reject Augustinian transmission; age-of-accountability...",
    "anglican": "39 Articles IX; mixed Catholic-Reformed inheritance...",
    "methodist": "Articles of Religion VII; prevenient grace overcomes...",
    "pentecostal": "Various — generally Wesleyan or Reformed substrate..."
  },
  "change_tracking": [
    {
      "date": "Pre-Augustine",
      "summary": "Eastern fathers (Irenaeus, Athanasius, Cappadocians) emphasized inherited mortality + corruption but not personal guilt of Adam's descendants."
    },
    {
      "date": "412 CE — Augustine",
      "summary": "Doctrine sharpens to include inherited guilt (massa damnata)..."
    },
    {
      "date": "1546 — Trent",
      "summary": "Roman dogmatic definition..."
    }
  ],
  "modern_disputes": [
    {"point": "Whether evolutionary biology requires reformulation", "positions": ["Federal headship without literal Adam", "Literal Adam required", "Etiological reading"]},
    {"point": "Whether 'original sin' applies pre-Christ"}
  ],
  "primary_sources": [
    {"title": "De peccatorum meritis et remissione", "author": "Augustine", "date": "412", "url": "/augustine/de-peccatorum-meritis"},
    {"title": "Council of Carthage 418, Canons", "url": "/conciliar/carthage-418"},
    {"title": "Council of Orange 529, Canons", "url": "/conciliar/orange-529"},
    {"title": "Trent Session V Decree on Original Sin", "url": "/conciliar/trent-session-v"}
  ],
  "see_also": ["pelagianism", "predestination", "imputation", "depravity", "concupiscence"],
  "last_revised": "2026-01-15"
}
```

## 11. Doctrinal Page Structure

`/doctrine` — landing page listing all 13 domains.

`/doctrine/{domain}` — domain page (e.g., `/doctrine/soteriology`) listing all doctrines in that domain.

`/doctrine/{slug}` — individual doctrine page (e.g., `/doctrine/original-sin`) with the structured content above.

Each chapter page surfaces a **"Doctrines built on this verse"** card under verses that anchor major doctrines (driven by the `scriptural_foundations` index reverse-mapped to verses).

## 12. Bias Policy

For every doctrine entry:

1. **State each position in its strongest form.** Not as straw-man, not with opposing terminology, but as its advocates would state it.
2. **Cite primary sources for every claim.** Augustine's actual words for Augustinian original sin; Pelagius's actual fragments for Pelagianism (where extant); Council decrees verbatim.
3. **Identify the editor.** Each entry includes provenance metadata (`prompt_version`, `last_revised`, etc.) so readers can trace the rendering's methodology.
4. **Explicit "this is contested" labeling.** When TCR cannot adjudicate, the page says so. Examples: limbo (medieval, never definitive), women's ordination (denominational positions), the historicity of Adam (modern scientific-theological dispute).
5. **No editorial preference for one denomination's outcome.** TCR documents Catholic, Orthodox, and Protestant positions with equal rigor. Where one tradition holds a position uniquely (e.g., Mormon teaching on baptism for the dead), it gets its own section, not dismissal.

This is the editorial differentiator. Every other doctrine reference is biased — Wikipedia leans secular/Protestant, the *Catholic Encyclopedia* leans Catholic, *Theopedia* leans Reformed. TCR is the first to commit to scholarly-neutral source-cited doctrinal coverage with the AI generation that makes it actually feasible.

---

## 13. Source-Edition Citation Policy

For all newly-authored content in Phases A-H and for doctrinal entries, TCR commits to source-edition citation:

| Source corpus | Critical edition |
|---|---|
| Philo | Loeb Classical Library (Colson, Whitaker, Marcus); Cohn-Wendland (German critical) |
| Josephus | Loeb (Thackeray, Marcus, Wikgren, Feldman); Niese (German critical) |
| Pseudepigrapha | Charlesworth, *Old Testament Pseudepigrapha* (2 vols, 1983-85); Sparks, *Apocryphal Old Testament* |
| Ante-Nicene Fathers | Schaff, *Ante-Nicene Fathers* (10 vols); Sources Chrétiennes (where available) |
| NT Apocrypha | Hennecke-Schneemelcher / Elliott, *Apocryphal New Testament*; Ehrman, *Lost Scriptures* |
| Nag Hammadi | Robinson, *Nag Hammadi Library in English*; Meyer, *Nag Hammadi Scriptures* |
| Targumim | Sperber, *The Bible in Aramaic*; McNamara *Aramaic Bible* series |
| Rabbinic | Neusner translations (Mishnah, Tosefta, Talmud Yerushalmi); Schottenstein (Bavli); Soncino |
| Patristic commentaries | NPNF (Schaff); Fathers of the Church series (CUA Press); Ancient Christian Commentary on Scripture (IVP) |
| Conciliar | Tanner, *Decrees of the Ecumenical Councils*; Denzinger, *Enchiridion Symbolorum* |

Every TCR entry cites the critical edition it works from. This is what raises the bar from "AI-generated text" to "scholarly resource."

---

## 14. Quality Standards (extending existing TCR standards)

1. **Source-edition citation** (above).
2. **Translator notes** explain the lexical/translational decisions — not narrative commentary.
3. **Theological-history notes** (for tradition entries) cite the receiving theologians and contexts by name.
4. **Cross-references** are verified — every link points to a real page.
5. **Self-audit before user review** — TCR memory feedback: Claude must audit output against quality standard before asking user to review.
6. **No bias** — for doctrinal entries, every contested position presented in its strongest form.
7. **Reading level** — target 11th-12th grade for patristic and scholarly material (raised from 9th-10th grade canonical Bible target).

---

## 15. Pacing & Milestones

This is a 12-18 month program. Working session-by-session, expected pace:

| Quarter | Phase | Milestone |
|---|---|---|
| 2026 Q2 (May-Jun) | Phase A start (Philo, Justin, Odes, 1 Clement, Didache) | First pre-Nicene Tier S corroboration entries live |
| 2026 Q3 (Jul-Sep) | Phase A complete; Phase B start | Phase A milestone document published; Pillar II verse-page deep-dive ships |
| 2026 Q4 (Oct-Dec) | Phase B continues (Irenaeus, Tertullian, Origen, Clement Alex.) | First half of Ante-Nicene Fathers indexed |
| 2027 Q1 (Jan-Mar) | Phase B complete; Phase C start (Philo full, Josephus) | Complete pre-Nicene Christian corpus published |
| 2027 Q2 (Apr-Jun) | Phase C complete; Phase D start (NT Apocrypha + Nag Hammadi) | Complete Jewish Hellenistic corpus published |
| 2027 Q3 (Jul-Sep) | Phase D complete; Phase E start (Targumim expansion) | Apocryphal corpus published |
| 2027 Q4 (Oct-Dec) | Phase E complete; Phase F start (Rabbinic) | Complete Targumic corpus published |
| 2028 Q1-Q2 | Phases F-G complete | Eastern + rabbinic foundations |
| 2028 Q3-Q4 | Phase H (patristic commentaries) | Comprehensive corpus complete |

**Pillar III (Doctrinal Index) runs in parallel** to corpus expansion. Aim: ~5 doctrine entries per week sustainable pace once the schema and structure are established. Initial 50 entries (the most-foundational) within 3 months; remaining ~150 entries paced across the rest of the program.

**Pillar II (verse-page architecture)** is a contained engineering effort. Estimated 3-4 weeks of focused work; targeted for after Phase A completes so the new corpus is immediately surfaced.

---

## 16. Strategic Decisions (Locked 2026-05-11)

All eight architectural questions resolved by user directive on 2026-05-11.

1. **Routing model for new books — DECISION: Each text as its own book.** Slugs like `/justin-dialogue`, `/1-clement`, `/didache`, `/philo-conf` (Confusion of Tongues), `/philo-migr` (Migration of Abraham), `/4-ezra`, `/2-baruch`, etc. Each gets its own BookInfo entry in the registry, its own canon-filter inclusion, its own `/books` listing, its own PDF, its own AI-search inclusion. Makes scholarly citations cleaner.
2. **Canon-filter implications — DECISION: Yes, add new categories.** The `/books` canon filter expands to include: Protestant, Catholic, Orthodox, Ethiopian, **Pre-Nicene Christian corpus** (new), **Jewish Hellenistic** (new), **Pseudepigrapha** (new), **NT Apocrypha & Nag Hammadi** (new), **Rabbinic foundations** (new), **Syriac corpus** (new), **Patristic biblical commentaries** (new), **All**.
3. **Doctrinal section URL prefix — DECISION: `/doctrines/` (plural).**
4. **PDF generation — DECISION: Yes, extend to pre-Nicene corpus.** Each new book gets a PDF generated at the same point its data ships. Per-phase milestone PDFs (e.g., "Phase A milestone — Pre-Nicene Tier S corroboration corpus, single PDF") also generated. PDF generation runs as part of the standard deploy pipeline.
5. **AI search scope — DECISION: Yes, include all new corpora.** Each new book added to `CANONICAL_BOOKS` or `EXTENDED_BOOKS` in `tcr-search-api/server.js`, plus tradition aliases for searchable keywords ("Philo," "Justin," "1 Clement," "Trypho," "Logos doctrine," etc.). Search index will grow to ~10,000-15,000 tradition entries by completion of Phases A-H.
6. **Public semantic versioning — DECISION: Yes, adopt 3-part SemVer.** Current state versioned as **TCR v1.0.0** (released 2026-05-11). Phase A completion = v1.1.0. Each subsequent phase = minor bump. Major bumps reserved for architectural reorganizations (e.g., Pillar II verse-page rework = v2.0.0). Each version tagged in git for stable citation. SoT versioning (v5.x) continues as internal documentation versioning, separate from the public TCR semantic version.
7. **Citation export — DECISION: BibTeX + RIS + Chicago plain text.** Every verse page (`/[book]/[chapter]/[verse]`) and every doctrine page (`/doctrines/{slug}`) gets a "Cite this" button that emits three formats: BibTeX (academic LaTeX standard), RIS (Zotero/EndNote/Mendeley/JSTOR cross-tool standard), and Chicago plain text (default humanities and theology citation style). Each citation includes URL + access date. Implementation as a small Astro component using page metadata. Targeted for shipping alongside Pillar II verse-page rework.
8. **Sequencing — DECISION: Pillar I Phase A start + Pillar III scaffolding in parallel; Pillar II after Phase A.** Concretely: begin Philo Logos selections + 1 Clement + Didache + Ignatius authoring immediately; in parallel, scaffold the `/doctrines/` section with the schema and first 5-10 pilot entries (Trinity, Christology, Original Sin, Justification, Eucharist). Pillar II verse-page deep-dive ships after Phase A so it has the new corpus to surface.

---

## 17. Phase A Kickoff — Architectural Prerequisites

Before authoring begins, the following architectural changes are needed to support "each text as its own book" routing.

### 17.1 BookInfo schema extension

Current schema has `testament: 'old' | 'new'`. Pre-Nicene Jewish + Christian texts don't fit. Extension needed:

```ts
type Testament = 'old' | 'new' | 'extra-canonical';

type Section =
  // existing
  | 'pentateuch' | 'historical' | 'wisdom' | 'major-prophets' | 'minor-prophets'
  | 'gospels' | 'pauline' | 'general-epistles' | 'apocalypse'
  | 'deuterocanonical' | 'orthodox-additions' | 'pre-nicaea-canon'
  | 'dead-sea-scrolls'
  // NEW for Phase A onward
  | 'jewish-hellenistic'        // Philo, Josephus, Aristeas, Pseudo-Philo
  | 'pseudepigrapha'             // 2-3 Enoch, Testaments, Apocalypses, 4 Ezra, 2 Baruch
  | 'apostolic-fathers'          // 1 Clement, 2 Clement, Ignatius, Polycarp, Hermas, Didache, Barnabas, Diognetus
  | 'apologists'                 // Justin, Tatian, Athenagoras, Theophilus, Aristides, Melito
  | 'ante-nicene-fathers'        // Irenaeus, Tertullian, Clement Alex., Origen, Hippolytus, Cyprian, Novatian, etc.
  | 'nt-apocrypha'               // Gospel of Thomas, Acts of Paul, Apocalypses, etc.
  | 'nag-hammadi'                // The Coptic Gnostic library
  | 'targumim'                   // Pseudo-Jonathan, Neofiti, fragmentary, Writings
  | 'rabbinic'                   // Mishnah, Tosefta, Mekhilta, Sifra, Sifre, Midrash Rabbah
  | 'syriac-corpus'              // Peshitta, Diatessaron, Aphrahat, Ephrem
  | 'patristic-commentaries';    // Augustine, Chrysostom, Jerome, Ambrose, Athanasius, Basil, Gregories, Cyrils
```

### 17.2 Canon array expansion

Current canons: `'protestant' | 'catholic' | 'orthodox' | 'ethiopian'`. Add filterable categories:

```ts
type Canon =
  | 'protestant' | 'catholic' | 'orthodox' | 'ethiopian'  // existing — actual canons
  | 'pre-nicene-christian'                                 // filter category
  | 'jewish-hellenistic'                                   // filter category
  | 'pseudepigrapha'                                       // filter category
  | 'nt-apocrypha'                                         // filter category
  | 'nag-hammadi'                                          // filter category
  | 'rabbinic'                                             // filter category
  | 'syriac'                                               // filter category
  | 'patristic-commentaries';                              // filter category
```

The `/books` page canon filter UI adds buttons for each new category.

### 17.3 Slug conventions

Each book gets a unique slug. Conventions:

- **Philo treatises** — `philo-{abbrev}` (e.g., `philo-conf` = On the Confusion of Tongues, `philo-migr` = On the Migration of Abraham). Use the standard Loeb/Goodenough abbreviations.
- **Justin Martyr** — `justin-dialogue`, `justin-first-apology`, `justin-second-apology`.
- **Apostolic Fathers** — `1-clement`, `2-clement`, `didache`, `barnabas`, `diognetus`, `shepherd-of-hermas`, `martyrdom-of-polycarp`, `polycarp-philippians`.
- **Ignatius's 7 letters** — `ignatius-ephesians`, `ignatius-magnesians`, `ignatius-trallians`, `ignatius-romans`, `ignatius-philadelphians`, `ignatius-smyrnaeans`, `ignatius-polycarp`.
- **Pseudepigrapha** — `4-ezra`, `2-baruch`, `3-baruch`, `2-enoch`, `3-enoch`, `testaments-of-twelve-patriarchs`, `testament-of-moses`, `apocalypse-of-abraham`, `joseph-and-aseneth`, `sibylline-oracles`, `pseudo-philo-lab`.
- **NT Apocrypha** — `gospel-of-thomas`, `gospel-of-peter`, `gospel-of-mary`, `protoevangelium-of-james`, `acts-of-paul`, `apocalypse-of-peter`, `ascension-of-isaiah`.
- **Nag Hammadi** — `apocryphon-of-john`, `gospel-of-truth`, `tripartite-tractate`, `sophia-of-jesus-christ`, etc.

### 17.4 PDF generation pipeline extension

The existing PDF pipeline (`scripts/generate-pdf.*`) generates per-book PDFs from chapter JSON. Extension for pre-Nicene corpus:

- Each new book gets a PDF at the same time its data ships.
- Per-phase compendium PDFs (e.g., "Phase A — Pre-Nicene Tier S corroboration corpus, 12 texts").
- The `/download` page is updated to list PDFs by canon-filter category.

### 17.5 Citation-export component

A single reusable component `CitationExport.astro` that takes page metadata (book name, chapter, verse if present, doctrine slug if present, source-edition, access date) and emits three citations as a copy-clipboardable button group.

### 17.6 Semantic versioning system

Adopt **TCR v1.0.0** as the release tag of today's deployed state (2026-05-11). Each phase completion gets a minor bump. Each git tag annotated with the milestone. Version visible in footer.

---

## 18. Pillar III Pilot — First 10 Doctrines

The first 10 doctrine entries serve as the **schema validation** for the doctrinal-index methodology. They cover the most foundational and most-contested doctrines across the major denominational divides:

| # | Doctrine | Domain | Why first |
|---|---|---|---|
| 1 | **The Trinity** | trinitarian | The defining post-Nicene formulation. |
| 2 | **Deity of Christ (homoousios)** | christology | The Nicene Creed's hinge. |
| 3 | **Original sin** | hamartiology | Augustinian-Pelagian + Eastern-Western divide. |
| 4 | **Justification** | soteriology | Reformation hinge — sola fide vs Trent. |
| 5 | **The Eucharist** | sacramentology | Transubstantiation vs consubstantiation vs memorialism vs Calvinist real-presence vs Eastern mystery. |
| 6 | **Predestination** | soteriology | Catholic vs Reformed vs Arminian. |
| 7 | **Scripture (canon + authority)** | bibliology | Sola scriptura vs Scripture-and-tradition; canon disputes. |
| 8 | **Baptism** | sacramentology | Mode + subjects + efficacy. |
| 9 | **The Church (one/holy/catholic/apostolic)** | ecclesiology | Polity + apostolic succession + papal primacy. |
| 10 | **Resurrection of the dead + the intermediate state** | eschatology | Heaven/hell/purgatory/limbo + millennial views. |

These 10 entries lock the schema. Subsequent ~190 entries follow the same pattern.

---

## 19. Open log

| Date | Item |
|---|---|
| 2026-05-11 | Vision established (user directive). Three-pillar plan documented. Eight architectural decisions locked. Phase A authoring + Pillar III scaffolding sequenced in parallel. |


---

## 17. The Ambition, Restated

Done at scale, TCR becomes the resource where:

- A pastor planning a sermon on Genesis 1 sees not just the Hebrew, the modern English, and the KJV — but Targum Onkelos, Philo on the Logos, Justin Martyr's Two-Powers argument, Augustine on creation, Aquinas on creatio ex nihilo, and the doctrinal page on creation theology — all from one verse page.
- A scholar writing about pre-Nicene Christology cites TCR alongside Loeb and Sources Chrétiennes, because TCR's modern renderings + cross-references are easier to work with than archaic ANF and don't require institutional database access.
- A seminary student studying for an MDiv finds TCR is the only place where Catholic, Orthodox, and Reformed positions on (say) justification are documented side-by-side with primary-source citations, without editorial spin.
- An AI search engineer or theology-tools developer pulls TCR's open structured data (CC-BY-4.0) because it's the only comprehensive corpus they can legally embed.
- A controversial doctrinal question gets researched on TCR because every answer is sourced or explicitly called out as contested.

This document codifies the path. Phases A-H plus three coordinated pillars. **18-24 months.** **Required sourcing for biblical scholarship.**

---

## Change log

| Date | Version | Changes |
|---|---|---|
| 2026-05-11 | v1.0 | Initial roadmap document. Establishes three-pillar plan (Pre-Nicene Corpus, Verse-as-Center Architecture, Doctrinal Index). Defines Phases A-H, doctrinal taxonomy, source-citation policy, and 18-24 month milestone framework. Supersedes archived March-2026 roadmap. |
| 2026-05-11 | v1.1 | Eight architectural decisions locked by user directive. Routing: each text as its own book with dedicated slug. Canon filter expands to 12 categories. Doctrines path: `/doctrines/`. PDF generation extends to all new corpora. AI search indexes all new content. Public semantic versioning adopted (today = **TCR v1.0.0**). Citation export = BibTeX + RIS + Chicago plain text. Sequencing: Phase A authoring + Pillar III scaffolding in parallel; Pillar II after Phase A. Phase A Kickoff section (Section 17) added with BookInfo schema extension, canon-array expansion, slug conventions, PDF pipeline extension, citation-export component spec, semantic-versioning system. Section 18 added: Pillar III Pilot — first 10 doctrines list (Trinity, Deity of Christ, Original Sin, Justification, Eucharist, Predestination, Scripture, Baptism, The Church, Resurrection). |
