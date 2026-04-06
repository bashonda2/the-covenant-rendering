# The Covenant Rendering — Operational Playbook

*How do we generate, deploy, and operate?*

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
| Quality Contract | `TCR_quality_contract.md` | What must be true for output to be correct? |
| **Operational Playbook** | **`TCR_operational_playbook.md`** | **How do we generate, deploy, and operate?** |

---

## 1. Generation Pipeline

1. **Generate chapters sequentially** within each book, in batches of 3-5 chapters.
2. **Validate each batch automatically:** JSON integrity, verse counts, field presence, KJV-duplication detection, boilerplate-note detection.
3. **Send each batch for QA review** before proceeding to the next batch.
4. **Fix issues identified in QA** before generating more chapters. Do not accumulate debt.
5. **Commit AND push to GitHub.** Every commit must be followed by `git push`. Local-only commits are not considered published. The data repo lives at `github.com:bashonda2/the-covenant-rendering.git` — always push to `origin main` after committing.
6. **Log QA results and fixes** in `TCR_quality_contract.md` (Resolved Issues section).

---

## 2. Commit Message Format

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

## 3. Website — thecovenantrendering.com

### 3.1 Overview

The Covenant Rendering has a live public website at **https://thecovenantrendering.com**. It is a statically generated Astro site that renders all translation data (Hebrew, rendering, KJV, translator notes, key terms) into a browsable, mobile-friendly web interface. The site is the public face of the project — the place readers and developers encounter TCR.

The website source code lives at `~/TCR` and is a separate repo from the translation data.

### 3.2 Tech Stack

| Component | Choice | Notes |
|---|---|---|
| Framework | Astro 5 (static output) | All pages generated at build time from JSON data. No server-side rendering, no database, no API. |
| CSS | Tailwind CSS v4 | Via `@tailwindcss/vite` plugin |
| Verse font | Cormorant Garamond | Google Fonts — serif, scholarly feel |
| UI font | Inter | Google Fonts — clean sans-serif for navigation, labels, metadata |
| Hebrew font | Noto Serif Hebrew | Google Fonts — full RTL support, vowel pointing renders correctly |
| Accent color | Deep teal `#1e6b5a` | Distinct from EVM's gold/parchment palette |
| Background | Warm cream `#fafaf8` | |

### 3.3 Repositories

| Repo | URL | Local Path | Contents |
|---|---|---|---|
| Translation data | https://github.com/bashonda2/the-covenant-rendering | `~/The Covenant Rendering/` | JSON chapter files, prompts, SOT documents |
| Website source | https://github.com/bashonda2/tcr-site | `~/TCR/` | Astro site, components, styles, build-time data copies |

These are separate repos. The data repo is the canonical source for translation JSON. The site repo contains build-time copies of the data (in `src/data/`) plus all site-specific code.

### 3.4 Infrastructure

| Property | Value |
|---|---|
| Domain | thecovenantrendering.com |
| VPS | *(IP removed from public docs)* |
| SSH | *(credentials removed from public docs)* |
| Web server | Nginx 1.24.0 (Ubuntu) |
| Web root | `/var/www/tcr/` |
| Nginx config | `/etc/nginx/sites-available/thecovenantrendering.com` |
| SSL | Let's Encrypt via certbot. Auto-renews. |
| Contact email | contact@thecovenantrendering.com → forwards to aaronblonquist@hotmail.com |
| Email forwarding | Namecheap built-in email forwarding (MX records point to Namecheap forwarding servers) |
| DNS management | Namecheap |

**Email separation from EVM:** TCR uses `contact@thecovenantrendering.com` (Namecheap forwarding → Hotmail). EVM uses `contact@everyversematters.com` (ImprovMX → Gmail). Separate domain emails and separate inboxes preserve TCR's scholarly/interfaith positioning — visitors to TCR do not see an LDS-specific connection through shared contact info.

### 3.5 Site Structure — Live Pages

| Route | Source File | Purpose |
|---|---|---|
| `/` | `src/pages/index.astro` | Homepage: hero, Genesis 1:1–2 live example with key term callouts (bara, tohu vavohu), problem/solution pitch, design principles, current status panel |
| `/{book}` | `src/pages/[book]/index.astro` | Chapter grid — dynamic route serves all books (Genesis, Exodus, Leviticus, Numbers, Deuteronomy) with verse counts and first-verse previews |
| `/{book}/[n]` | `src/pages/[book]/[chapter].astro` | Verse-by-verse chapter display with collapsible "Notes & Key Terms" panel per verse — dynamic route serves all book/chapter combinations |
| `/about` | `src/pages/about.astro` | Translation philosophy, source texts, AI disclosure, CC-BY-4.0 license details, book status roadmap |

**Current page count:** 194 (1 homepage + 1 about + 5 book indexes + 187 chapter pages)

### 3.6 Key Components

| Component | File | Purpose |
|---|---|---|
| Layout | `src/layouts/Layout.astro` | Base HTML, Google Fonts loading, nav bar with Books dropdown (all 5 Pentateuch books) + mobile hamburger, dynamic footer, SEO meta/OG tags |
| VerseCard | `src/components/VerseCard.astro` | Single verse display: Hebrew (RTL), rendering, KJV, collapsible notes/key terms panel. Accepts `bookName` prop. |
| Data utility | `src/data/tcr.ts` | `BOOKS` registry, `loadChapter(book, n)`, `getAllChapterNums(book)`, `getBook(slug)`, TypeScript interfaces |

### 3.7 The BOOKS Registry (`src/data/tcr.ts`)

When adding a new book to the website, the first code change is adding an entry to the `BOOKS` array:

```typescript
export const BOOKS: BookInfo[] = [
  { slug: 'genesis', name: 'Genesis', hebrewName: 'בְּרֵאשִׁית', transliteration: 'Bereshit', meaning: 'In the beginning', chapters: 50 },
  { slug: 'exodus', name: 'Exodus', hebrewName: 'שְׁמוֹת', transliteration: 'Shemot', meaning: 'Names', chapters: 40 },
  { slug: 'leviticus', name: 'Leviticus', hebrewName: 'וַיִּקְרָא', transliteration: 'Vayiqra', meaning: 'And He called', chapters: 27 },
  { slug: 'numbers', name: 'Numbers', hebrewName: 'בְּמִדְבַּר', transliteration: 'Bemidbar', meaning: 'In the wilderness', chapters: 36 },
  { slug: 'deuteronomy', name: 'Deuteronomy', hebrewName: 'דְּבָרִים', transliteration: 'Devarim', meaning: 'Words', chapters: 34 },
];
```

All data loading functions (`loadChapter`, `getAllChapterNums`, `getBookVerseCount`) take a `book` slug parameter and reference this registry.

### 3.8 How to Add a New Book to the Website

The site uses dynamic routes (`src/pages/[book]/`) that automatically generate pages for any book registered in the `BOOKS` array. Adding a new book requires only **two code changes** — no new page files, no navigation updates, no footer changes.

**Step 1: Copy data to the site.**
```bash
cp -r "/Users/aaronblonquist/The Covenant Rendering/{book}/" ~/TCR/src/data/{book}/
```

**Step 2: Register the book in `src/data/tcr.ts`.** Add a new entry to the `BOOKS` array with the book's slug, name, Hebrew name, transliteration, meaning, and chapter count. The dynamic routes, nav dropdown, footer, and homepage status panel all render from this array — no other file changes needed for the book to appear.

**Step 3 (optional): Update the about page.** In `src/pages/about.astro`, change the book's status from `'planned'` to `'complete'` in the roadmap table if applicable.

**Step 4: Build, commit, deploy.**
```bash
cd ~/TCR
npm run build          # Verify all pages generate
git add -A && git commit -m "feat: add {Book}" && git push
./deploy.sh            # Build + rsync to VPS
```

**Step 5: Verify live.** Confirm the new pages load at `https://thecovenantrendering.com/{book}` and `https://thecovenantrendering.com/{book}/1`.

### 3.9 Deployment

```bash
# From ~/TCR — builds and deploys in one command:
./deploy.sh

# What deploy.sh does:
# 1. npm run build  (generates static HTML from JSON data)
# 2. rsync -avz --delete dist/ <user>@<vps-ip>:/var/www/tcr/
```

Build time: ~0.8s for 194 pages. Rsync only transfers changed files. Zero downtime.

### 3.10 Local Development

```bash
cd ~/TCR
npm run dev     # starts dev server at http://localhost:4321
npm run build   # builds to dist/
```

### 3.11 Design Rules

- **Text contrast minimum:** `text-stone-600` for any readable content. `text-stone-400` is reserved for decorative separators and fine print only.
- **KJV text:** `text-base` (16px) minimum — not `text-sm`. Italic serif (Cormorant Garamond) to visually distinguish from TCR rendering.
- **Hebrew text:** RTL, Noto Serif Hebrew, `text-hebrew` class with `direction: rtl; unicode-bidi: bidi-override; line-height: 2;`
- **Accent color:** Deep teal `#1e6b5a` throughout. NOT gold/parchment (that's EVM's palette).

---

*Version 2.0 — 2026-03-28*
