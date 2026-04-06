import express from 'express';
import cors from 'cors';
import Anthropic from '@anthropic-ai/sdk';
import { readFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_ROOT = join(__dirname, '..');
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
  'genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy',
  'joshua', 'judges', 'ruth', '1-samuel', '2-samuel',
  '1-kings', '2-kings', '1-chronicles', '2-chronicles',
  'ezra', 'nehemiah', 'esther', 'job', 'psalms', 'proverbs',
  'ecclesiastes', 'song-of-songs', 'isaiah', 'jeremiah',
  'lamentations', 'ezekiel', 'daniel', 'hosea', 'joel', 'amos',
  'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah',
  'haggai', 'zechariah', 'malachi',
  'matthew', 'mark', 'luke', 'john', 'acts',
  'romans', '1-corinthians', '2-corinthians', 'galatians',
  'ephesians', 'philippians', 'colossians',
  '1-thessalonians', '2-thessalonians',
  '1-timothy', '2-timothy', 'titus', 'philemon',
  'hebrews', 'james', '1-peter', '2-peter',
  '1-john', '2-john', '3-john', 'jude', 'revelation'
];

const EXTENDED_BOOKS = [
  'dss-isaiah', 'lxx-daniel', 'lxx-esther', 'lxx-jeremiah',
  'targum-onkelos', 'targum-jonathan', 'jst', 'samaritan-pentateuch',
  'vulgate', '1-enoch', 'jubilees'
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
      for (const v of (raw.verses || [])) {
        for (const kt of (v.key_terms || [])) {
          keyTermsList.push(kt.transliteration + ' -> ' + kt.rendered_as);
        }
        if (v.expanded_rendering) {
          expandedRenderings.push(`v${v.verse}: ${v.expanded_rendering}`);
        }
      }

      chapters.push({
        chapter: chNum,
        summary: raw.preamble?.summary || '',
        remarkable: raw.preamble?.remarkable || '',
        friction: raw.preamble?.friction || '',
        connections: raw.preamble?.connections || '',
        keyTerms: [...new Set(keyTermsList)].slice(0, 30),
        expandedRenderings: expandedRenderings.slice(0, 10),
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

function scoreChapterRelevance(query, bookSlug, chapterInfo) {
  const q = query.toLowerCase();
  const words = q.split(/\s+/).filter(w => w.length > 2);
  let score = 0;

  const bookName = slugToName(bookSlug).toLowerCase();
  if (q.includes(bookName)) score += 20;
  if (q.includes(bookSlug)) score += 20;

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
    ...chapterInfo.keyTerms,
    ...chapterInfo.expandedRenderings,
  ].join(' ').toLowerCase();

  for (const w of words) {
    if (textBlob.includes(w)) score += 3;
  }

  return score;
}

function findRelevantChapters(query, maxChapters = 10) {
  const scored = [];
  for (const [slug, book] of Object.entries(bookIndex)) {
    for (const ch of book.chapters) {
      const score = scoreChapterRelevance(query, slug, ch);
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

function findRelevantCrossRefs(query, relevantChapters) {
  if (!crossrefData?.cross_references) return [];
  const chapSet = new Set(relevantChapters.map(c => `${c.slug}:${c.chapter}`));
  return crossrefData.cross_references.filter(ref => {
    return chapSet.has(`${ref.from_book}:${ref.from_chapter}`) ||
      chapSet.has(`${ref.to_book}:${ref.to_chapter}`);
  }).slice(0, 30);
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

// ── Build context for Claude ──────────────────────────────────────────────

function buildContext(query) {
  const relevantChapters = findRelevantChapters(query);
  const concordanceTerms = findRelevantConcordanceTerms(query);
  const crossRefs = findRelevantCrossRefs(query, relevantChapters);

  const parts = [];

  // Full chapter data for the most relevant chapters
  if (relevantChapters.length > 0) {
    parts.push('=== RELEVANT CHAPTER DATA ===\n');
    for (const { slug, chapter } of relevantChapters) {
      const data = loadFullChapter(slug, chapter);
      if (!data) continue;
      const bookName = slugToName(slug);
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
    }
  }

  // Concordance terms
  if (concordanceTerms.length > 0) {
    parts.push('=== CONCORDANCE DATA ===\n');
    for (const term of concordanceTerms) {
      parts.push(`Term: ${term.term} (${term.language})`);
      parts.push(`Default rendering: ${term.default_rendering}`);
      const occ = (term.occurrences || []).slice(0, 20);
      for (const o of occ) {
        parts.push(`  ${slugToName(o.book)} ch.${o.chapter} (${o.count}x) — key verses: ${(o.key_verses || []).join(', ')}`);
      }
      parts.push('');
    }
  }

  // Cross-references
  if (crossRefs.length > 0) {
    parts.push('=== CROSS-REFERENCES ===\n');
    for (const ref of crossRefs) {
      parts.push(`${slugToName(ref.from_book)} ${ref.from_chapter}:${ref.from_verse} -> ${slugToName(ref.to_book)} ${ref.to_chapter}:${ref.to_verse} (${ref.type}) — ${ref.note || ''}`);
    }
    parts.push('');
  }

  // If no relevant chapters found, provide a summary of available books
  if (relevantChapters.length === 0) {
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

  // URL reference guide
  parts.push('=== URL FORMAT GUIDE ===');
  parts.push('Canonical books: /[slug]/[chapter] e.g. /genesis/1');
  parts.push('Verse anchors: /[slug]/[chapter]#v[verse] e.g. /genesis/1#v1');
  parts.push('Extended Library examples: /dss-isaiah/53, /targum-onkelos/genesis/1, /vulgate/genesis/1, /jst/genesis/1, /samaritan-pentateuch/genesis/1, /1-enoch/1, /jubilees/1');
  parts.push('');

  return parts.join('\n');
}

// ── Anthropic client ──────────────────────────────────────────────────────

const anthropic = new Anthropic();

const SYSTEM_PROMPT = `You are the search assistant for The Covenant Rendering (TCR), a scholarly open-source Bible translation. The TCR translates all 66 canonical books from the Westminster Leningrad Codex (Old Testament) and SBL Greek New Testament (New Testament), plus Extended Library traditions including Dead Sea Scrolls (DSS), Septuagint (LXX), Targumim, Joseph Smith Translation (JST), Samaritan Pentateuch, Vulgate, 1 Enoch, and Jubilees.

Rules:
- Answer questions using ONLY the TCR data provided in the context. Do not use outside knowledge about Bible content.
- Every claim must cite a specific verse or tradition. Format citations as markdown links: [Genesis 1:1](/genesis/1#v1), [DSS Isaiah 53:4](/dss-isaiah/53#v4), [Psalm 23:1](/psalms/23#v1).
- For book slugs with numbers, use the format: [1 Samuel 3:10](/1-samuel/3#v10).
- Be concise and scholarly in tone.
- When discussing translation decisions, reference the translator notes and key terms from the data.
- If the data provided doesn't contain enough information to answer, say so clearly and suggest which books or chapters might be relevant.
- Do not invent or assume verse content that isn't in the provided data.
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
      model: 'claude-sonnet-4-6-20250514',
      max_tokens: 2048,
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
