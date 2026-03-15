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
    verse_nums = [v.get('verse') for v in verses]
    expected_nums = list(range(1, verse_count + 1))
    if verse_nums == expected_nums:
        results['checks']['verse_numbering'] = 'PASS'
    else:
        results['checks']['verse_numbering'] = 'FAIL'
        gaps = set(expected_nums) - set(verse_nums)
        dupes = [n for n in verse_nums if verse_nums.count(n) > 1]
        if gaps:
            results['issues'].append(f'Missing verses: {sorted(gaps)}')
        if dupes:
            results['issues'].append(f'Duplicate verses: {sorted(set(dupes))}')
        results['passed'] = False

    # Check 4: Required fields present
    required_fields = ['verse', 'text_hebrew', 'text_kjv', 'rendering', 'translator_notes', 'reading_level']
    missing_fields = []
    for v in verses:
        vnum = v.get('verse', '?')
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
    for v in verses:
        rendering = v.get('rendering', '')
        kjv = v.get('text_kjv', '')
        if not rendering or not kjv:
            continue
        sim = similarity(rendering, kjv)
        if sim > 0.92 and not is_name_only_list(rendering):
            kjv_matches.append(f'v{v.get("verse", "?")}: {sim:.0%} match')
    if kjv_matches:
        results['checks']['no_kjv_passthrough'] = f'FAIL ({len(kjv_matches)}/{verse_count})'
        results['issues'].extend(kjv_matches[:10])
        results['passed'] = False
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

    # Check 9: key_terms sub-fields complete
    kt_required = ['hebrew', 'transliteration', 'rendered_as', 'semantic_range', 'note']
    kt_issues = []
    for v in verses:
        for kt in v.get('key_terms', []):
            for field in kt_required:
                if field not in kt or not kt[field]:
                    kt_issues.append(f'v{v.get("verse", "?")}: key_term missing {field}')
    if kt_issues:
        results['checks']['key_terms_complete'] = f'FAIL ({len(kt_issues)} issues)'
        results['issues'].extend(kt_issues[:10])
        results['passed'] = False
    else:
        results['checks']['key_terms_complete'] = 'PASS'

    # Check 10: expanded_rendering placement
    er_issues = []
    for v in verses:
        if 'expanded_rendering' in v:
            keys = list(v.keys())
            r_idx = keys.index('rendering') if 'rendering' in keys else -1
            er_idx = keys.index('expanded_rendering')
            tn_idx = keys.index('translator_notes') if 'translator_notes' in keys else len(keys)
            if r_idx >= 0 and er_idx < r_idx:
                er_issues.append(f'v{v.get("verse", "?")}: expanded_rendering before rendering')
            if er_idx > tn_idx:
                er_issues.append(f'v{v.get("verse", "?")}: expanded_rendering after translator_notes')
    if er_issues:
        results['checks']['er_placement'] = f'FAIL ({len(er_issues)} issues)'
        results['issues'].extend(er_issues)
        results['passed'] = False
    else:
        results['checks']['er_placement'] = 'PASS'

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
