#!/usr/bin/env python3
"""
Build a cross-reference database from TCR Cross-Reference notes in translator_notes.
Scans all chapter files and extracts structured cross-reference connections.
"""

import json
import os
import re
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANONICAL_BOOKS = [
    'genesis','exodus','leviticus','numbers','deuteronomy',
    'joshua','judges','ruth','1-samuel','2-samuel','1-kings','2-kings',
    '1-chronicles','2-chronicles','ezra','nehemiah','esther','job',
    'psalms','proverbs','ecclesiastes','song-of-songs','isaiah','jeremiah',
    'lamentations','ezekiel','daniel','hosea','joel','amos','obadiah',
    'jonah','micah','nahum','habakkuk','zephaniah','haggai','zechariah','malachi',
    'matthew','mark','luke','john','acts','romans',
    '1-corinthians','2-corinthians','galatians','ephesians','philippians',
    'colossians','1-thessalonians','2-thessalonians','1-timothy','2-timothy',
    'titus','philemon','hebrews','james','1-peter','2-peter',
    '1-john','2-john','3-john','jude','revelation'
]

# Map display names to directory names
BOOK_NAME_MAP = {}
for b in CANONICAL_BOOKS:
    # "1-samuel" -> "1 samuel", "song-of-songs" -> "song of songs", etc.
    BOOK_NAME_MAP[b.replace('-', ' ')] = b
    BOOK_NAME_MAP[b] = b

# Additional name mappings
EXTRA_NAMES = {
    'gen': 'genesis', 'genesis': 'genesis',
    'exod': 'exodus', 'exodus': 'exodus', 'ex': 'exodus',
    'lev': 'leviticus', 'leviticus': 'leviticus',
    'num': 'numbers', 'numbers': 'numbers',
    'deut': 'deuteronomy', 'deuteronomy': 'deuteronomy',
    'josh': 'joshua', 'joshua': 'joshua',
    'judg': 'judges', 'judges': 'judges',
    'ruth': 'ruth',
    '1 sam': '1-samuel', '1 samuel': '1-samuel', 'i samuel': '1-samuel', '1sam': '1-samuel',
    '2 sam': '2-samuel', '2 samuel': '2-samuel', 'ii samuel': '2-samuel', '2sam': '2-samuel',
    '1 kings': '1-kings', 'i kings': '1-kings', '1 kgs': '1-kings', '1kings': '1-kings',
    '2 kings': '2-kings', 'ii kings': '2-kings', '2 kgs': '2-kings', '2kings': '2-kings',
    '1 chron': '1-chronicles', '1 chronicles': '1-chronicles', 'i chronicles': '1-chronicles',
    '2 chron': '2-chronicles', '2 chronicles': '2-chronicles', 'ii chronicles': '2-chronicles',
    'ezra': 'ezra', 'neh': 'nehemiah', 'nehemiah': 'nehemiah',
    'esth': 'esther', 'esther': 'esther',
    'job': 'job',
    'ps': 'psalms', 'psalm': 'psalms', 'psalms': 'psalms', 'psa': 'psalms',
    'prov': 'proverbs', 'proverbs': 'proverbs',
    'eccl': 'ecclesiastes', 'ecclesiastes': 'ecclesiastes', 'eccles': 'ecclesiastes',
    'song': 'song-of-songs', 'song of songs': 'song-of-songs', 'song of solomon': 'song-of-songs',
    'isa': 'isaiah', 'isaiah': 'isaiah',
    'jer': 'jeremiah', 'jeremiah': 'jeremiah',
    'lam': 'lamentations', 'lamentations': 'lamentations',
    'ezek': 'ezekiel', 'ezekiel': 'ezekiel',
    'dan': 'daniel', 'daniel': 'daniel',
    'hos': 'hosea', 'hosea': 'hosea',
    'joel': 'joel',
    'amos': 'amos',
    'obad': 'obadiah', 'obadiah': 'obadiah',
    'jonah': 'jonah', 'jon': 'jonah',
    'mic': 'micah', 'micah': 'micah',
    'nah': 'nahum', 'nahum': 'nahum',
    'hab': 'habakkuk', 'habakkuk': 'habakkuk',
    'zeph': 'zephaniah', 'zephaniah': 'zephaniah',
    'hag': 'haggai', 'haggai': 'haggai',
    'zech': 'zechariah', 'zechariah': 'zechariah',
    'mal': 'malachi', 'malachi': 'malachi',
    'matt': 'matthew', 'matthew': 'matthew', 'mat': 'matthew',
    'mark': 'mark', 'mk': 'mark',
    'luke': 'luke', 'lk': 'luke',
    'john': 'john', 'jn': 'john',
    'acts': 'acts',
    'rom': 'romans', 'romans': 'romans',
    '1 cor': '1-corinthians', '1 corinthians': '1-corinthians',
    '2 cor': '2-corinthians', '2 corinthians': '2-corinthians',
    'gal': 'galatians', 'galatians': 'galatians',
    'eph': 'ephesians', 'ephesians': 'ephesians',
    'phil': 'philippians', 'philippians': 'philippians',
    'col': 'colossians', 'colossians': 'colossians',
    '1 thess': '1-thessalonians', '1 thessalonians': '1-thessalonians',
    '2 thess': '2-thessalonians', '2 thessalonians': '2-thessalonians',
    '1 tim': '1-timothy', '1 timothy': '1-timothy',
    '2 tim': '2-timothy', '2 timothy': '2-timothy',
    'titus': 'titus', 'tit': 'titus',
    'philem': 'philemon', 'philemon': 'philemon', 'phlm': 'philemon',
    'heb': 'hebrews', 'hebrews': 'hebrews',
    'jas': 'james', 'james': 'james',
    '1 pet': '1-peter', '1 peter': '1-peter',
    '2 pet': '2-peter', '2 peter': '2-peter',
    '1 john': '1-john', '1 jn': '1-john',
    '2 john': '2-john', '2 jn': '2-john',
    '3 john': '3-john', '3 jn': '3-john',
    'jude': 'jude',
    'rev': 'revelation', 'revelation': 'revelation',
}

# Merge
BOOK_NAME_MAP.update(EXTRA_NAMES)


def normalize_book_name(name):
    """Try to resolve a book name to a canonical directory name."""
    name = name.strip().lower()
    # Direct lookup
    if name in BOOK_NAME_MAP:
        return BOOK_NAME_MAP[name]
    # Try removing trailing 's'
    if name.rstrip('s') in BOOK_NAME_MAP:
        return BOOK_NAME_MAP[name.rstrip('s')]
    return None


def classify_reference_type(note_text):
    """Determine reference type from the note content."""
    lower = note_text.lower()
    if 'quot' in lower:
        return 'quotation'
    if 'allud' in lower or 'allu' in lower:
        return 'allusion'
    if 'echo' in lower:
        return 'echo'
    if 'reference' in lower or 'refer' in lower:
        return 'reference'
    if 'fulfill' in lower or 'fulfi' in lower:
        return 'fulfillment'
    if 'parallel' in lower:
        return 'parallel'
    return 'reference'


# Regex to find Bible references like "Genesis 38", "Isaiah 7:14", "2 Samuel 7:12-14",
# "Numbers 1:7", "Psalm 110:1", etc.
BOOK_PATTERN = (
    r'(?:1|2|3|I|II|III)?\s*'
    r'(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|'
    r'Joshua|Judges|Ruth|Samuel|Kings|Chronicles|'
    r'Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs|'
    r'Ecclesiastes|Song\s+of\s+(?:Songs|Solomon)|'
    r'Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|'
    r'Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|'
    r'Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|'
    r'Matthew|Mark|Luke|John|Acts|Romans|'
    r'Corinthians|Galatians|Ephesians|Philippians|'
    r'Colossians|Thessalonians|Timothy|Titus|'
    r'Philemon|Hebrews|James|Peter|Jude|Revelation)'
)

REF_PATTERN = re.compile(
    r'(' + BOOK_PATTERN + r')\s+(\d+)(?::(\d+))?(?:\s*[-–]\s*(\d+)(?::(\d+))?)?',
    re.IGNORECASE
)


def extract_references(note_text):
    """Extract all Bible references from a note string."""
    refs = []
    for m in REF_PATTERN.finditer(note_text):
        book_str = m.group(1).strip()
        chapter = int(m.group(2))
        verse = int(m.group(3)) if m.group(3) else None

        book_dir = normalize_book_name(book_str)
        if book_dir:
            refs.append({
                'book': book_dir,
                'chapter': chapter,
                'verse': verse
            })
    return refs


def build_crossrefs():
    cross_references = []

    for book in CANONICAL_BOOKS:
        book_dir = os.path.join(BASE, book)
        if not os.path.isdir(book_dir):
            continue

        chapter_files = sorted(
            f for f in os.listdir(book_dir)
            if f.startswith('chapter-') and f.endswith('.json')
        )

        for cf in chapter_files:
            chap_num = int(cf.replace('chapter-', '').replace('.json', ''))
            filepath = os.path.join(book_dir, cf)

            try:
                with open(filepath, 'r', encoding='utf-8') as fh:
                    chapter_data = json.load(fh)
            except (json.JSONDecodeError, IOError):
                continue

            for verse in chapter_data.get('verses', []):
                verse_num = verse.get('verse', 0)

                for note in verse.get('translator_notes', []):
                    if not isinstance(note, str):
                        continue
                    if '[TCR Cross-Reference]' not in note:
                        continue

                    ref_type = classify_reference_type(note)
                    refs = extract_references(note)

                    # Create a brief summary from the note
                    # Strip the tag and trim
                    summary = note.replace('[TCR Cross-Reference]', '').strip()
                    # Truncate if very long
                    if len(summary) > 200:
                        summary = summary[:197] + '...'

                    for ref in refs:
                        cross_references.append({
                            'from_book': book,
                            'from_chapter': chap_num,
                            'from_verse': verse_num,
                            'to_book': ref['book'],
                            'to_chapter': ref['chapter'],
                            'to_verse': ref['verse'],
                            'type': ref_type,
                            'note': summary
                        })

    result = {
        'generated': str(date.today()),
        'cross_references': cross_references
    }

    out_path = os.path.join(BASE, 'scripts', 'crossref_db.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Cross-reference database written to {out_path}")
    print(f"Total cross-references: {len(cross_references)}")

    # Stats
    from_books = set(cr['from_book'] for cr in cross_references)
    to_books = set(cr['to_book'] for cr in cross_references)
    types = {}
    for cr in cross_references:
        types[cr['type']] = types.get(cr['type'], 0) + 1

    print(f"Source books: {len(from_books)}")
    print(f"Target books: {len(to_books)}")
    print("By type:")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t:20s}: {c}")


if __name__ == '__main__':
    build_crossrefs()
