# -*- coding: utf-8 -*-
"""Sweep all chapter files for placeholder key_terms entries."""
import json, os

results = []
for book in sorted(os.listdir('.')):
    if not os.path.isdir(book) or book.startswith('.') or book in ['scripts', 'prompts', 'texts', 'node_modules', 'dist', 'public']:
        continue
    for fname in sorted(os.listdir(book)):
        if not fname.startswith('chapter-') or not fname.endswith('.json'):
            continue
        fpath = os.path.join(book, fname)
        with open(fpath) as f:
            data = json.load(f)
        for v in data.get('verses', []):
            for kt in v.get('key_terms', []):
                ra = kt.get('rendered_as', '')
                note = kt.get('note', '')
                sr = kt.get('semantic_range', '')
                hit = False
                reasons = []
                if 'see rendering' in ra.lower() or 'see note' in ra.lower() or 'see hebrew' in ra.lower():
                    hit = True
                    reasons.append('rendered_as placeholder')
                if 'see translator' in note.lower() or note == 'See translator notes for context.':
                    hit = True
                    reasons.append('note placeholder')
                if 'see note' in sr.lower():
                    hit = True
                    reasons.append('semantic_range placeholder')
                if hit:
                    results.append({
                        'file': fpath,
                        'verse': v.get('verse'),
                        'hebrew': kt.get('hebrew', ''),
                        'translit': kt.get('transliteration', ''),
                        'rendered_as': ra,
                        'note_preview': note[:100],
                        'reasons': reasons
                    })

print(f"Found {len(results)} placeholder key_terms entries:\n")
for r in results:
    print(f"  {r['file']} v{r['verse']}: {r['translit']}")
    print(f"    rendered_as: {r['rendered_as']}")
    print(f"    note: {r['note_preview']}")
    print(f"    issues: {', '.join(r['reasons'])}")
    print()
