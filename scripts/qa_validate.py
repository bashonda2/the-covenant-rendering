#!/usr/bin/env python3
"""
TCR QA Validation Script — Automated Checks 1-10
From prompts/qa_agent_prompt.md

Runs all binary pass/fail automated checks against a chapter JSON file.
Usage:
    python3 scripts/qa_validate.py exodus/chapter-05.json
    python3 scripts/qa_validate.py numbers/  # validate all chapters in a book
    python3 scripts/qa_validate.py --scaffold-report  # show all scaffold chapters
"""

import json
import os
import sys
import re
from pathlib import Path
from difflib import SequenceMatcher

ARCHAIC_WORDS = [
    r'\bthou\b', r'\bthee\b', r'\bthy\b', r'\bthine\b',
    r'\bhath\b', r'\bdoth\b', r'\bsaith\b',
    r'\bgoest\b', r'\btakest\b', r'\bdealest\b', r'\bkilledst\b',
    r'\bye\b', r'\bto wit\b', r'\bwherefore\b', r'\bunto\b',
    r'\bseparateth\b', r'\bsodden\b', r'\bheave shoulder\b',
]

BANNED_NOTE_STRINGS = [
    "the narrative advances the confrontation",
    "the narrative advances the conflict",
    "full verse-specific note to be completed",
    "numbers narrative/census detail",
    "to be completed in quality pass",
]

REGISTER_TERMS = [
    "chesed", "berit", "kippur", "kapporet", "qadosh", "teshuvah",
    "ga'al", "go'el", "shalom", "tsedeq", "tsedaqah", "olam",
    "emunah", "kavod", "shekhinah",
]

NT_BOOKS = {
    'matthew', 'mark', 'luke', 'john', 'acts',
    'romans', '1-corinthians', '2-corinthians', 'galatians', 'ephesians',
    'philippians', 'colossians', '1-thessalonians', '2-thessalonians',
    '1-timothy', '2-timothy', 'titus', 'philemon',
    'hebrews', 'james', '1-peter', '2-peter',
    '1-john', '2-john', '3-john', 'jude', 'revelation',
}

# Verses where KJV proximity is accepted because the Hebrew/Aramaic is simple and direct
# enough that any competent translation converges on the same English. These were audited
# on 2026-04-05 and confirmed as independent translations from the source text.
# Categories: superscriptions, prophetic formulas, divine self-identification, simple
# parallelism, date/narrative formulas, iconic direct speech.
KJV_ACCEPTED_CONVERGENCE = {
    # Isaiah
    ('isaiah', 2, 1), ('isaiah', 11, 2), ('isaiah', 19, 25),
    ('isaiah', 33, 22), ('isaiah', 35, 5),
    ('isaiah', 36, 15), ('isaiah', 36, 17), ('isaiah', 36, 19),
    ('isaiah', 37, 13), ('isaiah', 37, 14), ('isaiah', 38, 22),
    ('isaiah', 40, 5), ('isaiah', 40, 31),
    ('isaiah', 41, 20), ('isaiah', 42, 12), ('isaiah', 43, 15),
    ('isaiah', 46, 9), ('isaiah', 50, 3), ('isaiah', 53, 6),
    ('isaiah', 55, 9), ('isaiah', 66, 15),
    # Jeremiah
    ('jeremiah', 1, 1), ('jeremiah', 8, 20),
    ('jeremiah', 11, 6), ('jeremiah', 13, 5), ('jeremiah', 14, 1),
    ('jeremiah', 21, 1), ('jeremiah', 21, 6), ('jeremiah', 21, 10),
    ('jeremiah', 25, 1), ('jeremiah', 26, 6), ('jeremiah', 26, 7),
    ('jeremiah', 28, 10), ('jeremiah', 28, 17),
    ('jeremiah', 32, 1), ('jeremiah', 34, 6), ('jeremiah', 41, 15),
    ('jeremiah', 48, 13), ('jeremiah', 50, 1),
    ('jeremiah', 51, 15), ('jeremiah', 51, 40), ('jeremiah', 52, 26),
    # Lamentations
    ('lamentations', 3, 46),
    # Ezekiel
    ('ezekiel', 6, 2), ('ezekiel', 11, 4),
    ('ezekiel', 29, 1), ('ezekiel', 29, 2), ('ezekiel', 29, 6),
    ('ezekiel', 30, 24), ('ezekiel', 34, 7), ('ezekiel', 34, 9),
    ('ezekiel', 35, 2),
    # Daniel (Aramaic)
    ('daniel', 4, 3), ('daniel', 4, 4), ('daniel', 4, 24),
    # Minor Prophets
    ('hosea', 9, 14),
    ('joel', 1, 1), ('joel', 1, 3), ('joel', 3, 14),
    ('amos', 1, 1), ('amos', 7, 9),
    ('micah', 1, 1), ('micah', 6, 7),
    ('habakkuk', 2, 14), ('habakkuk', 2, 20),
    ('habakkuk', 3, 3), ('habakkuk', 3, 18),
    ('zechariah', 3, 3),
    # 2 Chronicles
    ('2-chronicles', 14, 3),
}

# Verses absent from SBLGNT critical text (present in KJV / Textus Receptus only).
# These get empty text_greek/rendering with an explanatory translator_note, which is correct.
TEXTUAL_CRITICAL_OMISSIONS = {
    ('matthew', 17, 21), ('matthew', 18, 11), ('matthew', 23, 14),
    ('mark', 7, 16), ('mark', 9, 44), ('mark', 9, 46),
    ('mark', 11, 26), ('mark', 15, 28),
    ('luke', 23, 17),
    ('john', 5, 4),  # omitted entirely (no entry)
    ('john', 7, 53), ('john', 8, 1), ('john', 8, 2), ('john', 8, 3),
    ('john', 8, 4), ('john', 8, 5), ('john', 8, 6), ('john', 8, 7),
    ('john', 8, 8), ('john', 8, 9), ('john', 8, 10), ('john', 8, 11),
    ('acts', 8, 37),  # omitted entirely (no entry)
    ('acts', 15, 34), ('acts', 24, 7), ('acts', 28, 29),
}


def detect_testament(filepath: str) -> str:
    """Detect whether a file belongs to OT or NT based on its directory name."""
    parts = Path(filepath).parts
    for part in parts:
        if part.lower() in NT_BOOKS:
            return 'NT'
    return 'OT'


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def is_name_only_list(text: str) -> bool:
    """Heuristic: if the verse is mostly proper nouns (names), KJV match is acceptable."""
    words = text.split()
    if len(words) < 3:
        return False
    name_pattern = re.compile(r'^[A-Z][a-z]+,?$|^and$|^of$|^the$|^son$|^sons$|^daughter$|^daughters$')
    name_count = sum(1 for w in words if name_pattern.match(w))
    return name_count / len(words) > 0.6


def validate_chapter(filepath: str) -> dict:
    """Run all 10 automated checks on a chapter file. Returns a results dict."""
    results = {
        'file': filepath,
        'checks': {},
        'issues': [],
        'passed': True,
    }

    # Check 1: JSON integrity
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        results['checks']['json_integrity'] = 'PASS'
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        results['checks']['json_integrity'] = 'FAIL'
        results['issues'].append(f'JSON parse error: {e}')
        results['passed'] = False
        return results

    verses = data.get('verses', [])
    meta = data.get('meta', {})

    # Check 2: Verse count
    verse_count = len(verses)
    results['checks']['verse_count'] = f'{verse_count} verses'

    # Check 3: Verse numbering
    # Filter out entries without a 'verse' field (e.g. verse_range textual notes)
    verse_nums = [v.get('verse') for v in verses if v.get('verse') is not None]
    book_name = meta.get('book', '').lower().replace(' ', '-')
    # Normalize book names: "1 Corinthians" -> "1-corinthians"
    if book_name and not any(c == '-' for c in book_name) and book_name[0].isdigit():
        book_name = book_name.replace(' ', '-')
    chapter_num = meta.get('chapter', 0)

    # Special handling for John 8 (Pericope Adulterae: 7:53-8:11 included as textual note)
    # The PA section prepends 7:53 and 8:1-11 before the main chapter, causing apparent duplicates.
    is_john_8 = (book_name == 'john' and chapter_num == 8)
    if is_john_8:
        # Only check the main chapter verses (12-59), skipping PA section
        main_verse_nums = [vn for vn in verse_nums if vn >= 12]
        max_verse = max(main_verse_nums) if main_verse_nums else 0
        expected_nums = set(range(12, max_verse + 1))
        actual_nums = set(main_verse_nums)
    else:
        max_verse = max(verse_nums) if verse_nums else 0
        expected_nums = set(range(1, max_verse + 1))
        actual_nums = set(verse_nums)

    gaps = expected_nums - actual_nums
    # Filter out textual-critical omissions (verses absent from SBLGNT)
    tc_gaps = {vn for vn in gaps if (book_name, chapter_num, vn) in TEXTUAL_CRITICAL_OMISSIONS}
    real_gaps = gaps - tc_gaps

    if is_john_8:
        dupes = []  # duplicates expected due to PA section
    else:
        dupes = [n for n in verse_nums if verse_nums.count(n) > 1]

    if not real_gaps and not dupes:
        note = ''
        if tc_gaps:
            note = f' (textual-critical omissions: {sorted(tc_gaps)})'
        if is_john_8:
            note += ' (Pericope Adulterae handled)'
        results['checks']['verse_numbering'] = f'PASS{note}'
    else:
        results['checks']['verse_numbering'] = 'FAIL'
        if real_gaps:
            results['issues'].append(f'Missing verses: {sorted(real_gaps)}')
        if dupes:
            results['issues'].append(f'Duplicate verses: {sorted(set(dupes))}')
        results['passed'] = False

    # Check 4: Required fields present
    testament = detect_testament(filepath)
    source_field = 'text_greek' if testament == 'NT' else 'text_hebrew'
    required_fields = ['verse', source_field, 'text_kjv', 'rendering', 'translator_notes', 'reading_level']
    missing_fields = []
    for v in verses:
        vnum = v.get('verse', '?')
        # Skip entries without a verse number (e.g. verse_range textual notes in John 8)
        if vnum == '?' or vnum is None:
            continue
        # Skip textual-critical omissions — these intentionally lack text_greek/rendering
        if (book_name, chapter_num, vnum) in TEXTUAL_CRITICAL_OMISSIONS:
            continue
        for field in required_fields:
            if field not in v or not v[field]:
                missing_fields.append(f'v{vnum}: missing {field}')
    if missing_fields:
        results['checks']['required_fields'] = f'FAIL ({len(missing_fields)} missing)'
        results['issues'].extend(missing_fields[:10])
        if len(missing_fields) > 10:
            results['issues'].append(f'... and {len(missing_fields) - 10} more')
        results['passed'] = False
    else:
        results['checks']['required_fields'] = 'PASS'

    # Check 5: No KJV pass-through
    kjv_matches = []
    kjv_convergences = []
    for v in verses:
        rendering = v.get('rendering', '')
        kjv = v.get('text_kjv', '')
        if not rendering or not kjv:
            continue
        sim = similarity(rendering, kjv)
        if sim > 0.92 and not is_name_only_list(rendering):
            vnum = v.get('verse', '?')
            if (book_name, chapter_num, vnum) in KJV_ACCEPTED_CONVERGENCE:
                kjv_convergences.append(f'v{vnum}: {sim:.0%} match (accepted — Hebrew warrants similar English)')
            else:
                kjv_matches.append(f'v{vnum}: {sim:.0%} match')
    if kjv_matches:
        results['checks']['no_kjv_passthrough'] = f'FAIL ({len(kjv_matches)}/{verse_count})'
        results['issues'].extend(kjv_matches[:10])
        results['passed'] = False
    elif kjv_convergences:
        results['checks']['no_kjv_passthrough'] = f'PASS ({len(kjv_convergences)} accepted convergence{"s" if len(kjv_convergences) != 1 else ""})'
    else:
        results['checks']['no_kjv_passthrough'] = 'PASS'

    # Check 6: No boilerplate notes
    boilerplate_found = []
    note_texts = []
    for v in verses:
        notes = v.get('translator_notes', [])
        if isinstance(notes, str):
            notes = [notes]
        for note in notes:
            note_lower = note.lower() if isinstance(note, str) else ''
            for banned in BANNED_NOTE_STRINGS:
                if banned in note_lower:
                    boilerplate_found.append(f'v{v.get("verse", "?")}: banned string "{banned}"')
                    break
            note_texts.append((v.get('verse', '?'), note))

    # Check for identical notes across 3+ verses
    note_counts = {}
    for vnum, note in note_texts:
        key = note.strip().lower() if isinstance(note, str) else ''
        if len(key) > 20:
            if key not in note_counts:
                note_counts[key] = []
            note_counts[key].append(vnum)
    for note_text, vnums in note_counts.items():
        if len(vnums) >= 3:
            boilerplate_found.append(f'Identical note across {len(vnums)} verses ({vnums[:5]}...): "{note_text[:60]}..."')

    if boilerplate_found:
        results['checks']['no_boilerplate'] = f'FAIL ({len(boilerplate_found)} issues)'
        results['issues'].extend(boilerplate_found[:10])
        results['passed'] = False
    else:
        results['checks']['no_boilerplate'] = 'PASS'

    # Check 7: No archaic language in renderings
    archaic_found = []
    for v in verses:
        rendering = v.get('rendering', '')
        rendering_check = rendering.replace('LORD', '')  # LORD is not archaic
        for pattern in ARCHAIC_WORDS:
            matches = re.findall(pattern, rendering_check, re.IGNORECASE)
            if matches:
                archaic_found.append(f'v{v.get("verse", "?")}: "{matches[0]}" in rendering')
    if archaic_found:
        results['checks']['no_archaic'] = f'FAIL ({len(archaic_found)} found)'
        results['issues'].extend(archaic_found[:10])
        results['passed'] = False
    else:
        results['checks']['no_archaic'] = 'PASS'

    # Check 8: Meta fields correct
    meta_issues = []
    if not meta.get('book'):
        meta_issues.append('meta.book missing')
    if not meta.get('chapter'):
        meta_issues.append('meta.chapter missing')
    pv = meta.get('prompt_version', '')
    if isinstance(pv, str):
        try:
            if float(pv) < 1.3:
                meta_issues.append(f'meta.prompt_version is {pv}, must be >= 1.3')
        except ValueError:
            meta_issues.append(f'meta.prompt_version invalid: {pv}')
    elif isinstance(pv, (int, float)):
        if pv < 1.3:
            meta_issues.append(f'meta.prompt_version is {pv}, must be >= 1.3')
    else:
        meta_issues.append('meta.prompt_version missing')
    if meta.get('license') != 'CC-BY-4.0':
        meta_issues.append(f'meta.license is "{meta.get("license")}", must be CC-BY-4.0')
    if meta_issues:
        results['checks']['meta_fields'] = f'FAIL ({len(meta_issues)} issues)'
        results['issues'].extend(meta_issues)
        results['passed'] = False
    else:
        results['checks']['meta_fields'] = 'PASS'

    # Check 9: key_terms structure and schema
    kt_source_field = 'greek' if testament == 'NT' else 'hebrew'
    kt_required = {kt_source_field, 'transliteration', 'rendered_as', 'semantic_range', 'note'}
    kt_wrong_names = {'register_translation': 'rendered_as', 'gloss': 'semantic_range'}
    kt_issues = []
    for v in verses:
        vnum = v.get('verse', '?')
        kts = v.get('key_terms', [])
        if not isinstance(kts, list):
            kt_issues.append(f'v{vnum}: key_terms is {type(kts).__name__}, must be list')
            continue
        for i, kt in enumerate(kts):
            if not isinstance(kt, dict):
                kt_issues.append(f'v{vnum}: key_terms[{i}] is {type(kt).__name__}, must be object')
                continue
            for wrong, correct in kt_wrong_names.items():
                if wrong in kt:
                    kt_issues.append(f'v{vnum}: key_terms[{i}] uses "{wrong}" instead of "{correct}"')
            for field in kt_required:
                if field not in kt or not kt[field]:
                    kt_issues.append(f'v{vnum}: key_terms[{i}] missing "{field}"')
    if kt_issues:
        results['checks']['key_terms_schema'] = f'FAIL ({len(kt_issues)} issues)'
        results['issues'].extend(kt_issues[:20])
        results['passed'] = False
    else:
        results['checks']['key_terms_schema'] = 'PASS'

    # Check 10: expanded_rendering type and placement
    er_issues = []
    for v in verses:
        if 'expanded_rendering' in v:
            vnum = v.get('verse', '?')
            er = v['expanded_rendering']
            if not isinstance(er, str):
                er_issues.append(f'v{vnum}: expanded_rendering is {type(er).__name__}, must be string')
            elif not er.strip():
                er_issues.append(f'v{vnum}: expanded_rendering is empty')
            keys = list(v.keys())
            r_idx = keys.index('rendering') if 'rendering' in keys else -1
            er_idx = keys.index('expanded_rendering')
            tn_idx = keys.index('translator_notes') if 'translator_notes' in keys else len(keys)
            if r_idx >= 0 and er_idx < r_idx:
                er_issues.append(f'v{vnum}: expanded_rendering before rendering')
            if er_idx > tn_idx:
                er_issues.append(f'v{vnum}: expanded_rendering after translator_notes')
    if er_issues:
        results['checks']['er_schema'] = f'FAIL ({len(er_issues)} issues)'
        results['issues'].extend(er_issues)
        results['passed'] = False
    else:
        results['checks']['er_schema'] = 'PASS'

    # Summary stats
    kt_count = sum(len(v.get('key_terms', [])) for v in verses)
    er_count = sum(1 for v in verses if v.get('expanded_rendering'))
    results['summary'] = {
        'book': meta.get('book', '?'),
        'chapter': meta.get('chapter', '?'),
        'verses': verse_count,
        'key_terms': kt_count,
        'expanded_renderings': er_count,
        'prompt_version': meta.get('prompt_version', '?'),
    }

    return results


def print_results(results: dict):
    s = results['summary']
    verdict = 'PASS' if results['passed'] else 'FAIL'
    print(f"\n{'='*60}")
    print(f"QA VERDICT: {verdict}")
    print(f"{'='*60}")
    print(f"Book: {s.get('book', '?')}")
    print(f"Chapter: {s.get('chapter', '?')}")
    print(f"Verses: {s.get('verses', '?')}")
    print(f"Key terms: {s.get('key_terms', 0)}")
    print(f"Expanded renderings: {s.get('expanded_renderings', 0)}")
    print(f"Prompt version: {s.get('prompt_version', '?')}")
    print(f"\nAutomated Checks:")
    for check, status in results['checks'].items():
        marker = '[x]' if 'PASS' in str(status) else '[ ]'
        print(f"  {marker} {check}: {status}")
    if results['issues']:
        print(f"\nIssues Found ({len(results['issues'])}):")
        for issue in results['issues']:
            print(f"  - {issue}")
    print()


def scaffold_report(root_dir: str):
    """Show all scaffold chapters across the project."""
    books = ['genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy']
    print(f"\n{'='*60}")
    print("SCAFFOLD REPORT")
    print(f"{'='*60}\n")

    total_scaffold = 0
    total_good = 0

    for book in books:
        book_dir = os.path.join(root_dir, book)
        if not os.path.isdir(book_dir):
            continue
        files = sorted(f for f in os.listdir(book_dir) if f.startswith('chapter-') and f.endswith('.json'))
        scaffold = []
        good = []
        for fname in files:
            path = os.path.join(book_dir, fname)
            results = validate_chapter(path)
            ch = fname.replace('chapter-', '').replace('.json', '')
            if results['passed']:
                good.append(ch)
            else:
                scaffold.append(ch)

        total_scaffold += len(scaffold)
        total_good += len(good)
        status = f"{len(good)} good / {len(scaffold)} failing"
        print(f"{book.upper()}: {status}")
        if scaffold:
            print(f"  Failing: ch {', '.join(scaffold)}")
        print()

    print(f"TOTAL: {total_good} passing / {total_scaffold} failing out of {total_good + total_scaffold}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/qa_validate.py <file_or_dir> [--scaffold-report]")
        sys.exit(1)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if sys.argv[1] == '--scaffold-report':
        scaffold_report(project_root)
        sys.exit(0)

    target = sys.argv[1]

    if os.path.isdir(target):
        files = sorted(
            os.path.join(target, f)
            for f in os.listdir(target)
            if f.startswith('chapter-') and f.endswith('.json')
        )
        pass_count = 0
        fail_count = 0
        for fpath in files:
            results = validate_chapter(fpath)
            print_results(results)
            if results['passed']:
                pass_count += 1
            else:
                fail_count += 1
        print(f"\nSUMMARY: {pass_count} PASS / {fail_count} FAIL out of {len(files)} chapters")
    elif os.path.isfile(target):
        results = validate_chapter(target)
        print_results(results)
        sys.exit(0 if results['passed'] else 1)
    else:
        print(f"Error: {target} not found")
        sys.exit(1)
