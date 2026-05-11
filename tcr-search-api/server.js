import express from 'express';
import cors from 'cors';
import Anthropic from '@anthropic-ai/sdk';
import { readFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_ROOT = process.env.DATA_ROOT || join(__dirname, '..');
const PORT = process.env.PORT || 3847;

// ── Rate limiter (in-memory, per IP) ──────────────────────────────────────

const rateLimitMap = new Map();
const RATE_LIMIT = 10;
const RATE_WINDOW_MS = 60_000;

function checkRateLimit(ip) {
  const now = Date.now();
  let entry = rateLimitMap.get(ip);
  if (!entry || now - entry.windowStart > RATE_WINDOW_MS) {
    entry = { windowStart: now, count: 0 };
    rateLimitMap.set(ip, entry);
  }
  entry.count++;
  return entry.count <= RATE_LIMIT;
}

// Clean up stale entries every 5 minutes
setInterval(() => {
  const now = Date.now();
  for (const [ip, entry] of rateLimitMap) {
    if (now - entry.windowStart > RATE_WINDOW_MS * 2) rateLimitMap.delete(ip);
  }
}, 300_000);

// ── Book metadata ─────────────────────────────────────────────────────────

const CANONICAL_BOOKS = [
  // OT
  'genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy',
  'joshua', 'judges', 'ruth', '1-samuel', '2-samuel',
  '1-kings', '2-kings', '1-chronicles', '2-chronicles',
  'ezra', 'nehemiah', 'esther', 'job', 'psalms', 'proverbs',
  'ecclesiastes', 'song-of-solomon', 'isaiah', 'jeremiah',
  'lamentations', 'ezekiel', 'daniel', 'hosea', 'joel', 'amos',
  'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah',
  'haggai', 'zechariah', 'malachi',
  // NT
  'matthew', 'mark', 'luke', 'john', 'acts',
  'romans', '1-corinthians', '2-corinthians', 'galatians',
  'ephesians', 'philippians', 'colossians',
  '1-thessalonians', '2-thessalonians',
  '1-timothy', '2-timothy', 'titus', 'philemon',
  'hebrews', 'james', '1-peter', '2-peter',
  '1-john', '2-john', '3-john', 'jude', 'revelation',
  // Deuterocanonical (Vulgate Latin + English rendering, 137 chapters)
  'tobit', 'judith', 'wisdom-of-solomon', 'sirach',
  'baruch', '1-maccabees', '2-maccabees',
];

const EXTENDED_BOOKS = [
  // DSS — per-chapter dedicated sites
  'dss-isaiah', 'dss-deuteronomy', 'dss-1-samuel', 'dss-2-samuel', 'dss-psalms',
  // LXX — per-chapter dedicated sites
  'lxx-daniel', 'lxx-esther', 'lxx-jeremiah',
  'lxx-isaiah', 'lxx-psalms', 'lxx-proverbs', 'lxx-job',
  // Interpretive traditions
  'targum-onkelos', 'targum-jonathan', 'jst', 'samaritan-pentateuch', 'vulgate',
  // Pre-Nicaea canon
  '1-enoch', 'jubilees',
];

const ALL_BOOKS = [...CANONICAL_BOOKS, ...EXTENDED_BOOKS];

function slugToName(slug) {
  return slug
    .split('-')
    .map(w => {
      if (/^\d+$/.test(w)) return w;
      if (w === 'lxx') return 'LXX';
      if (w === 'dss') return 'DSS';
      if (w === 'jst') return 'JST';
      return w.charAt(0).toUpperCase() + w.slice(1);
    })
    .join(' ');
}

// ── Load condensed index at startup ───────────────────────────────────────

console.log('Loading TCR data index...');

const bookIndex = {};  // slug -> { name, chapters: [{ chapter, summary, keyTerms, connections }] }
let concordanceData = null;
let crossrefData = null;

function loadBookIndex(slug) {
  const bookDir = join(DATA_ROOT, slug);
  if (!existsSync(bookDir)) return null;

  const files = readdirSync(bookDir)
    .filter(f => f.startsWith('chapter-') && f.endsWith('.json'))
    .sort();

  const chapters = [];
  for (const file of files) {
    try {
      const raw = JSON.parse(readFileSync(join(bookDir, file), 'utf-8'));
      const chNum = raw.meta?.chapter || parseInt(file.replace('chapter-', '').replace('.json', ''));

      const keyTermsList = [];
      const expandedRenderings = [];
      // Variant notes from tradition data (DSS / LXX / etc.). These contain the
      // scholarly content (marquee variant labels, NT cross-refs, manuscript designations)
      // that queries actually target.
      const variantNotesIndex = [];
      for (const v of (raw.verses || [])) {
        for (const kt of (v.key_terms || [])) {
          keyTermsList.push(kt.transliteration + ' -> ' + kt.rendered_as);
        }
        if (v.expanded_rendering) {
          expandedRenderings.push(`v${v.verse}: ${v.expanded_rendering}`);
        }
        // Tradition-data files use variant_notes arrays. Index them, capped per-verse to
        // keep the in-memory blob bounded.
        if (Array.isArray(v.variant_notes)) {
          for (const note of v.variant_notes.slice(0, 3)) {
            if (typeof note === 'string' && note.length > 30) {
              variantNotesIndex.push(`v${v.verse}: ${note.slice(0, 400)}`);
            }
          }
        }
      }

      chapters.push({
        chapter: chNum,
        summary: raw.preamble?.summary || '',
        remarkable: raw.preamble?.remarkable || '',
        friction: raw.preamble?.friction || '',
        connections: raw.preamble?.connections || '',
        notableVariants: raw.preamble?.notable_variants || '',
        structuralNotes: raw.preamble?.structural_notes || '',
        manuscripts: raw.preamble?.manuscripts || '',
        keyTerms: [...new Set(keyTermsList)].slice(0, 30),
        expandedRenderings: expandedRenderings.slice(0, 10),
        variantNotes: variantNotesIndex.slice(0, 20),
        verseCount: raw.verses?.length || 0,
      });
    } catch (e) {
      // skip malformed files
    }
  }

  return {
    name: slugToName(slug),
    slug,
    chapterCount: chapters.length,
    chapters,
  };
}

// Per-book tradition data (renderings/variants/footnotes/passages arrays) for traditions
// that aren't per-chapter files: targum-onkelos, targum-jonathan, vulgate, samaritan-pentateuch,
// jst, dss-fragments. Each entry becomes a search-indexable record keyed by reference.
const traditionEntries = [];  // { slug, reference, title, body, url }

function loadPerBookTradition(traditionSlug, fileGlob, dataKey) {
  const dir = join(DATA_ROOT, traditionSlug);
  if (!existsSync(dir)) return 0;
  const files = readdirSync(dir).filter(f => f.endsWith('.json'));
  let count = 0;
  for (const file of files) {
    try {
      const raw = JSON.parse(readFileSync(join(dir, file), 'utf-8'));
      const entries = raw[dataKey] || raw.variants || raw.renderings || raw.footnotes || raw.passages || [];
      const bookSlug = file.replace('.json', '');
      for (const e of entries) {
        const ref = e.reference || '';
        // Build a compact searchable body: rendering + notes (truncated)
        const parts = [];
        if (e.targum_rendering) parts.push(e.targum_rendering);
        if (e.vulgate_rendering) parts.push(e.vulgate_rendering);
        if (e.sp_rendering) parts.push(e.sp_rendering);
        if (e.dss_rendering) parts.push(e.dss_rendering);
        if (e.change_summary) parts.push(e.change_summary);
        if (e.theological_legacy) parts.push(e.theological_legacy);
        if (Array.isArray(e.notes)) parts.push(e.notes.slice(0, 2).join(' '));
        const body = parts.join(' ').slice(0, 600);
        if (!body) continue;
        traditionEntries.push({
          slug: traditionSlug,
          bookSlug,
          reference: ref,
          body: body.toLowerCase(),
          // Display title used when surfacing in context
          title: `${slugToName(traditionSlug)} :: ${ref}`,
          // Best-effort URL: tradition-page anchor
          url: traditionSlug === 'dss-fragments'
              ? `/dss-fragments#book-${bookSlug}`
              : `/${traditionSlug}/${bookSlug}`,
          significance: e.significance || null,
          category: e.category || null,
        });
        count++;
      }
    } catch (e) { /* skip */ }
  }
  return count;
}

// Load per-book tradition data for non-per-chapter traditions.
const traditionLoadCount =
  loadPerBookTradition('targum-onkelos', null, 'renderings') +
  loadPerBookTradition('targum-jonathan', null, 'renderings') +
  loadPerBookTradition('vulgate', null, 'renderings') +
  loadPerBookTradition('samaritan-pentateuch', null, 'variants') +
  loadPerBookTradition('jst', null, 'footnotes') +
  loadPerBookTradition('dss-fragments', null, 'variants');
console.log(`  Tradition entries indexed: ${traditionLoadCount}`);

for (const slug of ALL_BOOKS) {
  const idx = loadBookIndex(slug);
  if (idx) bookIndex[slug] = idx;
}

// Load concordance
const concordancePath = join(DATA_ROOT, 'scripts', 'concordance.json');
if (existsSync(concordancePath)) {
  try {
    concordanceData = JSON.parse(readFileSync(concordancePath, 'utf-8'));
    console.log(`  Concordance loaded: ${concordanceData.terms?.length || 0} terms`);
  } catch (e) {
    console.warn('  Failed to load concordance:', e.message);
  }
}

// Load cross-references
const crossrefPath = join(DATA_ROOT, 'scripts', 'crossref_db.json');
if (existsSync(crossrefPath)) {
  try {
    crossrefData = JSON.parse(readFileSync(crossrefPath, 'utf-8'));
    console.log(`  Cross-references loaded: ${crossrefData.cross_references?.length || 0} entries`);
  } catch (e) {
    console.warn('  Failed to load cross-references:', e.message);
  }
}

const loadedBookCount = Object.keys(bookIndex).length;
const totalChapters = Object.values(bookIndex).reduce((s, b) => s + b.chapterCount, 0);
console.log(`  Index ready: ${loadedBookCount} books, ${totalChapters} chapters`);

// ── Query relevance matching ──────────────────────────────────────────────

function scoreChapterRelevance(query, bookSlug, chapterInfo, bookNameMatch) {
  const q = query.toLowerCase();
  const words = q.split(/\s+/).filter(w => w.length > 2);
  let score = 0;

  const bookName = slugToName(bookSlug).toLowerCase();

  // Exact book name match
  if (q.includes(bookName)) score += 20;
  if (q.includes(bookSlug)) score += 20;

  // Partial book name match (e.g., "enoch" matches "1 enoch", "psalms" matches "psalms")
  const bookWords = bookName.split(/\s+/);
  for (const bw of bookWords) {
    if (bw.length > 2 && q.includes(bw)) score += 15;
  }
  const slugWords = bookSlug.split('-');
  for (const sw of slugWords) {
    if (sw.length > 2 && q.includes(sw)) score += 15;
  }

  // Boost from book-level match detection
  if (bookNameMatch) score += 10;

  // Check for chapter number reference (e.g., "genesis 1" or "genesis chapter 3")
  const chapterRegex = new RegExp(`(?:${bookSlug}|${bookName})\\s+(?:chapter\\s+)?(\\d+)`, 'i');
  const chMatch = q.match(chapterRegex);
  if (chMatch && parseInt(chMatch[1]) === chapterInfo.chapter) score += 50;

  // Check for verse reference (e.g., "genesis 1:1")
  const verseRegex = new RegExp(`(?:${bookSlug}|${bookName})\\s+(\\d+):(\\d+)`, 'i');
  const vMatch = q.match(verseRegex);
  if (vMatch && parseInt(vMatch[1]) === chapterInfo.chapter) score += 60;

  const textBlob = [
    chapterInfo.summary,
    chapterInfo.remarkable,
    chapterInfo.friction,
    chapterInfo.connections,
    chapterInfo.notableVariants,
    chapterInfo.structuralNotes,
    chapterInfo.manuscripts,
    ...chapterInfo.keyTerms,
    ...chapterInfo.expandedRenderings,
    ...(chapterInfo.variantNotes || []),
  ].join(' ').toLowerCase();

  for (const w of words) {
    if (textBlob.includes(w)) score += 3;
  }

  return score;
}

// Tradition-name aliases. A query mentioning these terms boosts the corresponding tradition slugs.
const TRADITION_ALIASES = {
  // Each alias-word maps to a list of slug prefixes that should be boosted
  'septuagint':       ['lxx-'],
  'lxx':              ['lxx-'],
  'targum':           ['targum-'],
  'targumic':         ['targum-'],
  'onkelos':          ['targum-onkelos'],
  'jonathan':         ['targum-jonathan'],
  'aramaic':          ['targum-'],
  'memra':            ['targum-onkelos'],
  'shekinah':         ['targum-'],
  'vulgate':          ['vulgate'],
  'jerome':           ['vulgate'],
  'dead sea':         ['dss-'],
  'qumran':           ['dss-'],
  'scroll':           ['dss-'],
  'samaritan':        ['samaritan-pentateuch'],
  'jst':              ['jst'],
  'joseph smith':     ['jst'],
  'hebrew bible':     [],  // generic — no boost
  // Deuterocanonical / apocrypha — these are now full Bible books on the site
  // (slug each), so we boost the book slug directly rather than a prefix.
  'apocrypha':        ['tobit', 'judith', 'wisdom-of-solomon', 'sirach', 'baruch', '1-maccabees', '2-maccabees'],
  'apocryphal':       ['tobit', 'judith', 'wisdom-of-solomon', 'sirach', 'baruch', '1-maccabees', '2-maccabees'],
  'deuterocanonical': ['tobit', 'judith', 'wisdom-of-solomon', 'sirach', 'baruch', '1-maccabees', '2-maccabees'],
  'deuterocanon':     ['tobit', 'judith', 'wisdom-of-solomon', 'sirach', 'baruch', '1-maccabees', '2-maccabees'],
  'tobit':            ['tobit'],
  'judith':           ['judith'],
  'wisdom of solomon':['wisdom-of-solomon'],
  'ben sira':         ['sirach'],
  'ecclesiasticus':   ['sirach'],
  'sirach':           ['sirach'],
  'baruch':           ['baruch'],
  'maccabees':        ['1-maccabees', '2-maccabees'],
  'maccabean':        ['1-maccabees', '2-maccabees'],
  'hanukkah':         ['1-maccabees', '2-maccabees'],
};

function detectTraditionPrefixes(query) {
  const q = query.toLowerCase();
  const matched = new Set();
  for (const [alias, prefixes] of Object.entries(TRADITION_ALIASES)) {
    if (q.includes(alias)) {
      for (const p of prefixes) matched.add(p);
    }
  }
  return matched;
}

function findRelevantTraditionEntries(query, maxEntries = 20) {
  const q = query.toLowerCase();
  const words = q.split(/\s+/).filter(w => w.length > 2);
  const tradPrefixes = detectTraditionPrefixes(query);
  const scored = [];
  for (const entry of traditionEntries) {
    let score = 0;
    // Boost for tradition-name match
    for (const p of tradPrefixes) {
      if (entry.slug.startsWith(p)) { score += 8; break; }
    }
    // Boost for reference match
    const refLower = (entry.reference || '').toLowerCase();
    if (refLower && q.includes(refLower)) score += 25;
    // Per-word body matches
    for (const w of words) {
      if (entry.body.includes(w)) score += 2;
    }
    // Significance / category boost
    if (entry.significance === 'theological') score += 1;
    if (score >= 6) {
      scored.push({ ...entry, score });
    }
  }
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, maxEntries);
}

// Detect which books a query is likely about
function detectMatchedBooks(query) {
  const q = query.toLowerCase();
  const matched = new Set();
  for (const slug of ALL_BOOKS) {
    const name = slugToName(slug).toLowerCase();
    if (q.includes(name) || q.includes(slug)) {
      matched.add(slug);
      continue;
    }
    // Partial match: e.g., "enoch" -> "1-enoch", "samuel" -> "1-samuel", "2-samuel"
    const nameWords = name.split(/\s+/).filter(w => w.length > 2);
    const slugWords = slug.split('-').filter(w => w.length > 2);
    for (const w of [...nameWords, ...slugWords]) {
      if (q.includes(w)) { matched.add(slug); break; }
    }
  }
  return matched;
}

function findRelevantChapters(query, maxChapters = 15) {
  const matchedBooks = detectMatchedBooks(query);
  const tradPrefixes = detectTraditionPrefixes(query);
  const scored = [];
  for (const [slug, book] of Object.entries(bookIndex)) {
    const bookMatch = matchedBooks.has(slug);
    // Boost: tradition-name in query boosts matching per-chapter tradition corpora
    // (e.g., "Septuagint Isaiah" → boost lxx-isaiah's chapters).
    let traditionBoost = 0;
    for (const p of tradPrefixes) {
      if (slug.startsWith(p)) { traditionBoost = 15; break; }
    }
    for (const ch of book.chapters) {
      const score = scoreChapterRelevance(query, slug, ch, bookMatch) + traditionBoost;
      if (score > 0) {
        scored.push({ slug, chapter: ch.chapter, score });
      }
    }
  }
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, maxChapters);
}

function findRelevantConcordanceTerms(query) {
  if (!concordanceData?.terms) return [];
  const q = query.toLowerCase();
  return concordanceData.terms.filter(t => {
    return q.includes(t.term) ||
      q.includes(t.default_rendering?.toLowerCase() || '');
  });
}

function findRelevantCrossRefs(query, relevantChapters, matchedBooks) {
  if (!crossrefData?.cross_references) return [];
  const q = query.toLowerCase();
  const qWords = q.split(/\s+/).filter(w => w.length > 3);
  const chapSet = new Set(relevantChapters.map(c => `${c.slug}:${c.chapter}`));
  const bookSet = matchedBooks || new Set();

  const results = [];
  const seen = new Set();

  for (const ref of crossrefData.cross_references) {
    const key = `${ref.from_book}:${ref.from_chapter}:${ref.from_verse}->${ref.to_book}:${ref.to_chapter}:${ref.to_verse}`;
    if (seen.has(key)) continue;

    let matched = false;
    // Match by chapter
    if (chapSet.has(`${ref.from_book}:${ref.from_chapter}`) ||
        chapSet.has(`${ref.to_book}:${ref.to_chapter}`)) matched = true;
    // Match by book
    if (bookSet.has(ref.from_book) || bookSet.has(ref.to_book)) matched = true;
    // Match by keyword in note
    if (!matched && ref.note) {
      const noteLower = ref.note.toLowerCase();
      for (const w of qWords) {
        if (noteLower.includes(w)) { matched = true; break; }
      }
    }

    if (matched) {
      seen.add(key);
      results.push(ref);
    }
  }
  return results.slice(0, 80);
}

function loadFullChapter(slug, chapterNum) {
  const padded = String(chapterNum).padStart(2, '0');
  const filePath = join(DATA_ROOT, slug, `chapter-${padded}.json`);
  if (!existsSync(filePath)) return null;
  try {
    return JSON.parse(readFileSync(filePath, 'utf-8'));
  } catch {
    return null;
  }
}

// ── Query classification ──────────────────────────────────────────────────

function classifyQuery(query) {
  const q = query.toLowerCase();

  // Specific: contains a verse reference like "genesis 1:1" or "isaiah 53:11"
  const verseRefPattern = /(?:[\w-]+)\s+\d+:\d+/i;
  // Chapter reference like "genesis 1" or "psalm 23"
  const chapterRefPattern = /(?:genesis|exodus|leviticus|numbers|deuteronomy|joshua|judges|ruth|samuel|kings|chronicles|ezra|nehemiah|esther|job|psalms?|proverbs|ecclesiastes|song|isaiah|jeremiah|lamentations|ezekiel|daniel|hosea|joel|amos|obadiah|jonah|micah|nahum|habakkuk|zephaniah|haggai|zechariah|malachi|matthew|mark|luke|john|acts|romans|corinthians|galatians|ephesians|philippians|colossians|thessalonians|timothy|titus|philemon|hebrews|james|peter|jude|revelation|enoch|jubilees)\s+\d+/i;

  if (verseRefPattern.test(q)) return 'specific';
  if (chapterRefPattern.test(q)) return 'specific';

  const matchedBooks = detectMatchedBooks(q);
  if (matchedBooks.size > 0) return 'book-level';

  return 'topical';
}

// ── Build context for Claude ──────────────────────────────────────────────

function buildContext(query) {
  const matchedBooks = detectMatchedBooks(query);
  const queryType = classifyQuery(query);
  const relevantChapters = findRelevantChapters(query);
  const concordanceTerms = findRelevantConcordanceTerms(query);
  const crossRefs = findRelevantCrossRefs(query, relevantChapters, matchedBooks);

  const parts = [];

  // Determine which chapters get Tier 3 (full scholarly data)
  const tier3Set = new Set();
  if (queryType === 'specific') {
    for (const rc of relevantChapters.slice(0, 5)) {
      if (rc.score >= 40) tier3Set.add(`${rc.slug}:${rc.chapter}`);
    }
  }
  // Always Tier 3 for the single highest-scoring chapter
  if (relevantChapters.length > 0) {
    const top = relevantChapters[0];
    tier3Set.add(`${top.slug}:${top.chapter}`);
  }

  // ── SECTION 1: Book-level overviews (all matched books, from in-memory index) ──

  if (matchedBooks.size > 0) {
    parts.push('=== MATCHED BOOKS OVERVIEW ===\n');
    for (const slug of matchedBooks) {
      const book = bookIndex[slug];
      if (!book) continue;
      parts.push(`**${book.name}** (${book.slug}): ${book.chapterCount} chapters`);
      for (const ch of book.chapters) {
        const line = [`  Ch ${ch.chapter}`];
        if (ch.summary) line.push(`: ${ch.summary}`);
        if (ch.connections) line.push(` [Connections: ${ch.connections}]`);
        parts.push(line.join(''));
      }
      parts.push('');
    }
  }

  // ── SECTION 2: Tiered chapter data ──

  if (relevantChapters.length > 0) {
    parts.push('=== RELEVANT CHAPTER DATA ===\n');

    for (const { slug, chapter, score } of relevantChapters) {
      const bookName = slugToName(slug);
      const chKey = `${slug}:${chapter}`;
      const isTier3 = tier3Set.has(chKey);

      // Tier 3: Full scholarly data (source text, KJV, rendering, notes, key terms)
      if (isTier3) {
        const data = loadFullChapter(slug, chapter);
        if (!data) continue;

        parts.push(`--- ${bookName} Chapter ${chapter} [FULL DATA] ---`);
        if (data.preamble) {
          parts.push(`Summary: ${data.preamble.summary}`);
          if (data.preamble.remarkable) parts.push(`Notable: ${data.preamble.remarkable}`);
          if (data.preamble.friction) parts.push(`Translation friction: ${data.preamble.friction}`);
          if (data.preamble.connections) parts.push(`Connections: ${data.preamble.connections}`);
        }
        parts.push('');
        for (const v of data.verses) {
          const ref = `${bookName} ${chapter}:${v.verse}`;
          parts.push(`[${ref}]`);
          if (v.text_hebrew) parts.push(`  Hebrew: ${v.text_hebrew}`);
          if (v.text_greek) parts.push(`  Greek: ${v.text_greek}`);
          parts.push(`  TCR: ${v.rendering}`);
          parts.push(`  KJV: ${v.text_kjv}`);
          if (v.expanded_rendering) parts.push(`  Expanded: ${v.expanded_rendering}`);
          if (v.translator_notes?.length) {
            parts.push(`  Notes: ${v.translator_notes.join(' | ')}`);
          }
          for (const kt of (v.key_terms || [])) {
            parts.push(`  Term: ${kt.hebrew || kt.greek || ''} (${kt.transliteration}) -> "${kt.rendered_as}" [${kt.semantic_range}] — ${kt.note}`);
          }
        }
        parts.push('');
        continue;
      }

      // Tier 2: Renderings + notes (no source text, no KJV, no key_terms objects)
      const data = loadFullChapter(slug, chapter);
      if (!data) continue;

      parts.push(`--- ${bookName} Chapter ${chapter} ---`);
      if (data.preamble) {
        parts.push(`Summary: ${data.preamble.summary}`);
        if (data.preamble.remarkable) parts.push(`Notable: ${data.preamble.remarkable}`);
        if (data.preamble.friction) parts.push(`Translation friction: ${data.preamble.friction}`);
        if (data.preamble.connections) parts.push(`Connections: ${data.preamble.connections}`);
      }
      parts.push('');
      for (const v of data.verses) {
        const ref = `${bookName} ${chapter}:${v.verse}`;
        const line = [`[${ref}] ${v.rendering}`];
        if (v.expanded_rendering) line.push(`  Expanded: ${v.expanded_rendering}`);
        if (v.translator_notes?.length) {
          line.push(`  Notes: ${v.translator_notes.join(' | ')}`);
        }
        parts.push(line.join('\n'));
      }
      parts.push('');
    }
  }

  // ── SECTION 3: Concordance data ──

  if (concordanceTerms.length > 0) {
    parts.push('=== CONCORDANCE DATA ===\n');
    for (const term of concordanceTerms) {
      parts.push(`Term: ${term.term} (${term.language})`);
      parts.push(`Default rendering: ${term.default_rendering}`);
      for (const o of (term.occurrences || [])) {
        parts.push(`  ${slugToName(o.book)} ch.${o.chapter} (${o.count}x) — key verses: ${(o.key_verses || []).join(', ')}`);
      }
      parts.push('');
    }
  }

  // ── SECTION 4: Cross-references ──

  if (crossRefs.length > 0) {
    parts.push('=== CROSS-REFERENCES ===\n');
    for (const ref of crossRefs) {
      parts.push(`${slugToName(ref.from_book)} ${ref.from_chapter}:${ref.from_verse} -> ${slugToName(ref.to_book)} ${ref.to_chapter}:${ref.to_verse} (${ref.type}) — ${ref.note || ''}`);
    }
    parts.push('');
  }

  // ── SECTION 4b: Tradition entries (Targumim, Vulgate, Samaritan, JST, DSS-fragments) ──
  // These are per-book renderings/variants that aren't surfaced via the per-chapter index.
  // They're the scholarly content most users searching for "what does the Targum say about X"
  // are actually targeting.

  const tradEntries = findRelevantTraditionEntries(query, 20);
  if (tradEntries.length > 0) {
    parts.push('=== TRADITION-ENTRY MATCHES ===\n');
    parts.push('(Renderings/variants from Targumim, Vulgate, Samaritan Pentateuch, JST,');
    parts.push(' and DSS-fragment summaries that match the query. Cite these directly when relevant.)');
    parts.push('');
    for (const e of tradEntries) {
      parts.push(`[${e.title}]${e.significance ? ' ('+e.significance+')' : ''}`);
      parts.push(`  ${e.body.slice(0, 350)}`);
      parts.push(`  Page: ${e.url}`);
      parts.push('');
    }
  }

  // ── SECTION 5: Fallback overview ──

  if (relevantChapters.length === 0 && matchedBooks.size === 0) {
    parts.push('=== AVAILABLE BOOKS OVERVIEW ===\n');
    parts.push('Canonical books (66):');
    for (const slug of CANONICAL_BOOKS) {
      const b = bookIndex[slug];
      if (b) parts.push(`  ${b.name}: ${b.chapterCount} chapters`);
    }
    parts.push('\nExtended Library traditions:');
    for (const slug of EXTENDED_BOOKS) {
      const b = bookIndex[slug];
      if (b) parts.push(`  ${b.name}: ${b.chapterCount} chapters`);
    }
    parts.push('');
  }

  // ── URL reference guide ──

  parts.push('=== URL FORMAT GUIDE ===');
  parts.push('Canonical books: /[slug]/[chapter] e.g. /genesis/1');
  parts.push('Verse anchors: /[slug]/[chapter]#v[verse] e.g. /genesis/1#v1');
  parts.push('Deuterocanonical books (full Bible books — Vulgate Latin + English):');
  parts.push('  /tobit/[ch] (14 ch), /judith/[ch] (16 ch), /wisdom-of-solomon/[ch] (19 ch)');
  parts.push('  /sirach/[ch] (51 ch), /baruch/[ch] (6 ch)');
  parts.push('  /1-maccabees/[ch] (16 ch), /2-maccabees/[ch] (15 ch)');
  parts.push('Per-chapter manuscript-tradition pages (use for direct comparisons):');
  parts.push('  /dss-isaiah/[ch]      — Dead Sea Scrolls Isaiah (1QIsaᵃ); 66 chapters');
  parts.push('  /dss-deuteronomy/[ch] — DSS Deuteronomy (incl. 32:8 sons of God, 32:43 → Heb 1:6)');
  parts.push('  /dss-1-samuel/[ch]    — DSS 1 Samuel (incl. Nahash paragraph at 11:1)');
  parts.push('  /dss-2-samuel/[ch]    — DSS 2 Samuel (incl. Solomon\'s gold shields at 8:7)');
  parts.push('  /dss-psalms/[ch]      — DSS Psalter (11QPsᵃ; incl. Ps 22:16, Ps 145 nun-line, Pss 151A/151B)');
  parts.push('  /dss-fragments        — 22 books with smaller DSS attestation (anchored sections)');
  parts.push('  /lxx-isaiah/[ch]      — Septuagint Isaiah; 66 chapters');
  parts.push('  /lxx-psalms/[ch]      — Septuagint Psalter; 150 chapters');
  parts.push('  /lxx-proverbs/[ch]    — Septuagint Proverbs; 31 chapters');
  parts.push('  /lxx-job/[ch]         — Septuagint Job; 42 chapters');
  parts.push('  /lxx-jeremiah/[ch]    — Septuagint Jeremiah (shorter text); 52 chapters');
  parts.push('  /lxx-daniel/[ch]      — Septuagint/Theodotion Daniel');
  parts.push('  /lxx-esther/[ch]      — Greek Esther with additions');
  parts.push('Per-book interpretive tradition pages: /vulgate/[book] (all 66 books, 808 renderings),');
  parts.push('  /targum/[book] (Onkelos + Jonathan, 1,001 renderings), /samaritan-pentateuch/[book], /jst');
  parts.push('Free-standing tradition books: /1-enoch/[ch], /jubilees/[ch]');
  parts.push('Tradition landing pages: /jst, /vulgate, /targum, /samaritan-pentateuch');
  parts.push('Tradition-page verse anchors: /lxx-isaiah/53#v11 and similar.');
  parts.push('Book slugs: ' + ALL_BOOKS.join(', '));
  parts.push('');

  return parts.join('\n');
}

// ── Anthropic client ──────────────────────────────────────────────────────

const anthropic = new Anthropic();

const SYSTEM_PROMPT = `You are the search assistant for The Covenant Rendering (TCR), a scholarly open-source Bible translation. The TCR translates all 66 canonical books from the Westminster Leningrad Codex (Old Testament) and SBL Greek New Testament (New Testament), and serves the 7 deuterocanonical books (Tobit, Judith, Wisdom of Solomon, Sirach, Baruch, 1 Maccabees, 2 Maccabees) in Jerome's Vulgate Latin with English rendering. The Extended Library also includes manuscript and interpretive traditions: Dead Sea Scrolls (DSS), Septuagint (LXX), Targumim (1,001 entries from Onkelos & Jonathan), Latin Vulgate (808 entries across all 66 books), Joseph Smith Translation (JST), Samaritan Pentateuch, 1 Enoch, and Jubilees.

Rules:
- Answer questions using ONLY the TCR data provided in the context. Do not use outside knowledge about Bible content.
- Be THOROUGH. This is an academic project — cite every relevant reference in the data, not just a selection. If the data contains 20 relevant passages, cite all 20.
- Every claim must cite a specific verse or tradition. Format citations as markdown links: [Genesis 1:1](/genesis/1#v1), [DSS Isaiah 53:4](/dss-isaiah/53#v4), [Psalm 23:1](/psalms/23#v1).
- For book slugs with numbers, use the format: [1 Samuel 3:10](/1-samuel/3#v10).
- For deuterocanonical books, link directly like [Tobit 3:11](/tobit/3#v11), [Sirach 24:8](/sirach/24#v8), [1 Maccabees 4:36](/1-maccabees/4#v36), [Wisdom of Solomon 7:26](/wisdom-of-solomon/7#v26). These books are now full Bible books on the site.
- When a question concerns a manuscript tradition (Septuagint, Dead Sea Scrolls, Vulgate, Targumim, Samaritan, JST), and a per-chapter tradition page exists for that book (see URL FORMAT GUIDE), include a direct link to that page so the reader can browse the variant comparison alongside the base text. E.g., for an Isaiah 53 LXX question: link both [Isaiah 53:11](/isaiah/53#v11) AND [Septuagint Isaiah 53](/lxx-isaiah/53).
- Be scholarly in tone. Organize responses logically — by book, by theme, or by tradition as appropriate.
- When discussing translation decisions, reference the translator notes and key terms from the data.
- If the data provided doesn't contain enough information to answer fully, say so clearly and suggest which books or chapters might be relevant.
- Do not invent or assume verse content that isn't in the provided data.
- Use the MATCHED BOOKS OVERVIEW section to identify all relevant chapters, not just the ones with full verse data.
- Use paragraph form for explanations, not excessive bullet points.`;

// ── Express app ───────────────────────────────────────────────────────────

const app = express();
app.use(express.json({ limit: '1mb' }));
app.use(cors({
  origin: [
    'https://thecovenantrendering.com',
    'https://www.thecovenantrendering.com',
    /^http:\/\/localhost:\d+$/,
  ],
  methods: ['POST'],
}));

app.post('/api/search', async (req, res) => {
  const ip = req.headers['x-forwarded-for']?.split(',')[0]?.trim() || req.ip;

  if (!checkRateLimit(ip)) {
    return res.status(429).json({
      error: 'Rate limit exceeded. Please wait a moment before trying again.',
    });
  }

  const { query } = req.body;
  if (!query || typeof query !== 'string') {
    return res.status(400).json({ error: 'Missing or invalid "query" field.' });
  }
  if (query.length > 500) {
    return res.status(400).json({ error: 'Query too long (max 500 characters).' });
  }

  try {
    const context = buildContext(query);

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 4096,
      system: SYSTEM_PROMPT,
      messages: [{
        role: 'user',
        content: `Here is the relevant TCR data for this query:\n\n${context}\n\n---\n\nUser question: ${query}`,
      }],
    });

    const answerText = message.content
      .filter(b => b.type === 'text')
      .map(b => b.text)
      .join('\n');

    // Extract citations from the markdown links
    const citationRegex = /\[([^\]]+)\]\(\/([^)]+)\)/g;
    const citations = [];
    let match;
    while ((match = citationRegex.exec(answerText)) !== null) {
      const label = match[1];
      const url = '/' + match[2];
      const urlParts = url.split('#');
      const pathParts = urlParts[0].split('/').filter(Boolean);
      const verse = urlParts[1]?.replace('v', '') || null;

      // Try to parse book and chapter from the URL
      let book, chapter;
      if (pathParts.length >= 2) {
        book = pathParts.slice(0, -1).join('/');
        chapter = parseInt(pathParts[pathParts.length - 1]) || null;
      }

      citations.push({
        label,
        book: book || pathParts[0],
        chapter: chapter || null,
        verse: verse ? parseInt(verse) : null,
        url,
      });
    }

    return res.json({ answer: answerText, citations });
  } catch (err) {
    console.error('Search error:', err.message || err);
    return res.status(500).json({
      error: 'An error occurred while processing your question. Please try again.',
    });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    books: Object.keys(bookIndex).length,
    chapters: Object.values(bookIndex).reduce((s, b) => s + b.chapterCount, 0),
  });
});

app.listen(PORT, () => {
  console.log(`TCR Search API running on port ${PORT}`);
});
