#!/usr/bin/env python3
"""
Build a concordance of theologically significant terms across all 66 canonical books.
Scans key_terms arrays and expanded_rendering fields in every chapter JSON file.
"""

import json
import os
import re
from collections import defaultdict
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

# Terms to track.  Keys: transliteration patterns (case-insensitive).
# Values: dict with language, default_rendering.
HEBREW_TERMS = {
    'chesed':       {'language': 'hebrew', 'default_rendering': 'faithful love',
                     'patterns': [r'\bchesed\b', r'\bḥesed\b']},
    'berit':        {'language': 'hebrew', 'default_rendering': 'covenant',
                     'patterns': [r'\bberit\b', r'\bb[eə]rit\b', r'\bbrit\b']},
    'kavod':        {'language': 'hebrew', 'default_rendering': 'glory',
                     'patterns': [r'\bkavod\b', r'\bkabod\b']},
    'shalom':       {'language': 'hebrew', 'default_rendering': 'peace',
                     'patterns': [r'\bshalom\b']},
    'tsedeq':       {'language': 'hebrew', 'default_rendering': 'righteousness',
                     'patterns': [r'\btsedeq\b', r'\btsedaqah\b', r'\btzedek\b',
                                  r'\btsedek\b', r'\btsedaqah\b', r'\btsedaq\b']},
    'emunah':       {'language': 'hebrew', 'default_rendering': 'faithfulness',
                     'patterns': [r'\bemunah\b', r'\b[ʾ]?emunah\b']},
    'qadosh':       {'language': 'hebrew', 'default_rendering': 'holy',
                     'patterns': [r'\bqadosh\b', r'\bqodesh\b', r'\bqados\b', r'\bqadesh\b']},
    'go\'el':       {'language': 'hebrew', 'default_rendering': 'kinsman-redeemer',
                     'patterns': [r'\bgo[ʾ\']?el\b', r'\bgoel\b']},
    'mashiach':     {'language': 'hebrew', 'default_rendering': 'anointed one',
                     'patterns': [r'\bmashiach\b', r'\bmashiakh\b', r'\bmeshiach\b']},
    'torah':        {'language': 'hebrew', 'default_rendering': 'instruction / the Law',
                     'patterns': [r'\btorah\b']},
    'ruach':        {'language': 'hebrew', 'default_rendering': 'spirit / wind / breath',
                     'patterns': [r'\bruach\b', r'\bruaḥ\b']},
    'navi':         {'language': 'hebrew', 'default_rendering': 'prophet',
                     'patterns': [r'\bnavi\b', r'\bnabi\b']},
    'cherem':       {'language': 'hebrew', 'default_rendering': 'devoted to destruction',
                     'patterns': [r'\bcherem\b', r'\bḥerem\b']},
    'olam':         {'language': 'hebrew', 'default_rendering': 'forever / eternal',
                     'patterns': [r'\bolam\b', r'\b[ʿ]?olam\b']},
}

GREEK_TERMS = {
    'pistis':       {'language': 'greek', 'default_rendering': 'faith',
                     'patterns': [r'\bpistis\b', r'\bπίστ']},
    'charis':       {'language': 'greek', 'default_rendering': 'grace',
                     'patterns': [r'\bcharis\b', r'\bχάρι']},
    'dikaiosynē':   {'language': 'greek', 'default_rendering': 'righteousness',
                     'patterns': [r'\bdikaiosyn[eē]\b', r'\bδικαιοσύν']},
    'agapē':        {'language': 'greek', 'default_rendering': 'love',
                     'patterns': [r'\bagap[eē]\b', r'\bἀγάπ']},
    'logos':        {'language': 'greek', 'default_rendering': 'word',
                     'patterns': [r'\blogos\b', r'\bλόγο']},
    'pneuma':       {'language': 'greek', 'default_rendering': 'spirit',
                     'patterns': [r'\bpneuma\b', r'\bπνεῦμα']},
    'ekklēsia':     {'language': 'greek', 'default_rendering': 'church / assembly',
                     'patterns': [r'\bekklesia\b', r'\bekklēsia\b', r'\bἐκκλησί']},
    'euangelion':   {'language': 'greek', 'default_rendering': 'gospel / good news',
                     'patterns': [r'\beuangelion\b', r'\bεὐαγγέλι']},
    'sōtēria':      {'language': 'greek', 'default_rendering': 'salvation',
                     'patterns': [r'\bs[oō]t[eē]ria\b', r'\bσωτηρί']},
    'basileia':     {'language': 'greek', 'default_rendering': 'kingdom',
                     'patterns': [r'\bbasileia\b', r'\bβασιλεί']},
    'koinōnia':     {'language': 'greek', 'default_rendering': 'fellowship / communion',
                     'patterns': [r'\bkoin[oō]nia\b', r'\bκοινωνί']},
    'parousia':     {'language': 'greek', 'default_rendering': 'coming / arrival / presence',
                     'patterns': [r'\bparousia\b', r'\bπαρουσί']},
    'Christos':     {'language': 'greek', 'default_rendering': 'Christ / Anointed One',
                     'patterns': [r'\bChristos\b', r'\bchristos\b', r'\bΧριστό']},
    'kyrios':       {'language': 'greek', 'default_rendering': 'Lord',
                     'patterns': [r'\bkyrios\b', r'\bκύριο']},
}

ALL_TERMS = {}
ALL_TERMS.update(HEBREW_TERMS)
ALL_TERMS.update(GREEK_TERMS)


def match_key_term(kt, term_name, term_info):
    """Check if a key_terms entry matches a concordance term."""
    translit = kt.get('transliteration', '').lower()
    for pat in term_info['patterns']:
        if re.search(pat, translit, re.IGNORECASE):
            return True
    # Also check the hebrew/greek field text and note field
    for field in ['hebrew', 'greek', 'note']:
        text = kt.get(field, '')
        if text:
            for pat in term_info['patterns']:
                if re.search(pat, text, re.IGNORECASE):
                    return True
    return False


def scan_expanded_rendering(text, term_name, term_info):
    """Check if an expanded_rendering mentions the term."""
    for pat in term_info['patterns']:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def build_concordance():
    # Structure: term_name -> book -> chapter -> set of verses
    data = {t: defaultdict(lambda: defaultdict(set)) for t in ALL_TERMS}

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

                # Check key_terms
                for kt in verse.get('key_terms', []):
                    for term_name, term_info in ALL_TERMS.items():
                        if match_key_term(kt, term_name, term_info):
                            data[term_name][book][chap_num].add(verse_num)

                # Check expanded_rendering
                er = verse.get('expanded_rendering', '')
                if er:
                    for term_name, term_info in ALL_TERMS.items():
                        if scan_expanded_rendering(er, term_name, term_info):
                            data[term_name][book][chap_num].add(verse_num)

                # Also check translator_notes for transliteration mentions
                for note in verse.get('translator_notes', []):
                    if isinstance(note, str):
                        for term_name, term_info in ALL_TERMS.items():
                            for pat in term_info['patterns']:
                                if re.search(pat, note, re.IGNORECASE):
                                    data[term_name][book][chap_num].add(verse_num)
                                    break

    # Build output
    terms_out = []
    for term_name, term_info in ALL_TERMS.items():
        occurrences = []
        total = 0
        for book in CANONICAL_BOOKS:
            if book in data[term_name]:
                for chap in sorted(data[term_name][book].keys()):
                    verses = sorted(data[term_name][book][chap])
                    count = len(verses)
                    total += count
                    occurrences.append({
                        'book': book,
                        'chapter': chap,
                        'count': count,
                        'key_verses': verses
                    })
        if occurrences or total == 0:
            terms_out.append({
                'term': term_name,
                'language': term_info['language'],
                'default_rendering': term_info['default_rendering'],
                'occurrences': occurrences,
                'total_occurrences': total
            })

    result = {
        'generated': str(date.today()),
        'terms': sorted(terms_out, key=lambda x: (-x['total_occurrences'], x['term']))
    }

    out_path = os.path.join(BASE, 'scripts', 'concordance.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Concordance written to {out_path}")
    print(f"Total terms: {len(terms_out)}")
    for t in result['terms']:
        books_count = len(set(o['book'] for o in t['occurrences']))
        print(f"  {t['term']:20s}  {t['total_occurrences']:5d} occurrences across {books_count:3d} books")


if __name__ == '__main__':
    build_concordance()
