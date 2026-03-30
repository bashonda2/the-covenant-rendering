import json, os, sys, re
from pathlib import Path

BASE = Path("/Users/aaronblonquist/The Covenant Rendering")
BOOKS = ["1-chronicles", "2-chronicles", "ezra", "nehemiah", "esther", "job", "psalms"]

def is_narrative_commentary(er_text):
    """Heuristic: a term-focused ER references Hebrew terms/roots/transliterations.
    Narrative commentary discusses events/plot without anchoring to Hebrew vocab."""
    if not isinstance(er_text, str):
        return True, "NOT A STRING"
    
    hebrew_indicators = [
        r'[\u0590-\u05FF]',          # Hebrew Unicode chars
        r'\b[A-Z]?[a-z]*[āēīōūăĕĭŏŭâêîôûšḥṭṣ][a-z]*\b',  # transliteration chars
        r'\broot\b',
        r'\bHebrew\b',
        r'\bsemantic\b',
        r'\bcognate\b',
        r'\bverb\b',
        r'\bnoun\b',
        r'\badjective\b',
        r'\bparticiple\b',
        r'\binfinitive\b',
        r'\bqal\b',r'\bpiel\b',r'\bhiphil\b',r'\bhitpael\b',r'\bniphal\b',r'\bhophal\b',r'\bpual\b',
        r'\btransliterat',
        r'\blexical\b',
        r'\betymolog',
        r'\bword\b.*\bmeans?\b',
        r'\bterm\b',
        r'\blit\.\b',r'\bliterally\b',
    ]
    
    narrative_indicators = [
        r'\b(the story|the narrative|this event|what happens|plot)\b',
        r'\b(the scene|the episode|at this point in the story)\b',
    ]
    
    text_lower = er_text.lower()
    
    hebrew_score = 0
    for pat in hebrew_indicators:
        if re.search(pat, er_text, re.IGNORECASE):
            hebrew_score += 1
    
    narrative_score = 0
    for pat in narrative_indicators:
        if re.search(pat, text_lower):
            narrative_score += 1
    
    if hebrew_score >= 2:
        return False, None
    if hebrew_score == 0 and len(er_text) > 50:
        return True, "NO_HEBREW_TERMS"
    if narrative_score > 0 and hebrew_score < 2:
        return True, "NARRATIVE_PATTERN"
    return False, None

results = {}

for book in BOOKS:
    book_path = BASE / book
    if not book_path.exists():
        print(f"WARNING: {book} directory not found")
        continue
    
    chapters = sorted(book_path.glob("chapter-*.json"))
    book_data = {
        "total_verses": 0,
        "total_ers": 0,
        "chapters": {},
        "flagged_ers": [],
        "type_errors": [],
    }
    
    for ch_file in chapters:
        try:
            with open(ch_file) as f:
                data = json.load(f)
        except Exception as e:
            print(f"ERROR reading {ch_file}: {e}")
            continue
        
        ch_num = data.get("meta", {}).get("chapter", ch_file.stem)
        verses = data.get("verses", [])
        ch_verse_count = len(verses)
        ch_er_count = 0
        
        for v in verses:
            if "expanded_rendering" in v:
                er = v["expanded_rendering"]
                ch_er_count += 1
                
                # Check type
                if not isinstance(er, str):
                    book_data["type_errors"].append({
                        "chapter": ch_num,
                        "verse": v.get("verse"),
                        "type": type(er).__name__,
                    })
                
                # Check if narrative
                is_narr, reason = is_narrative_commentary(er)
                if is_narr:
                    preview = er if isinstance(er, str) else str(er)
                    preview = preview[:150] + "..." if len(preview) > 150 else preview
                    book_data["flagged_ers"].append({
                        "chapter": ch_num,
                        "verse": v.get("verse"),
                        "reason": reason,
                        "preview": preview,
                    })
        
        book_data["total_verses"] += ch_verse_count
        book_data["total_ers"] += ch_er_count
        book_data["chapters"][ch_num] = {
            "verses": ch_verse_count,
            "ers": ch_er_count,
            "density": round(ch_er_count / ch_verse_count * 100, 1) if ch_verse_count > 0 else 0,
        }
    
    book_data["density"] = round(book_data["total_ers"] / book_data["total_verses"] * 100, 1) if book_data["total_verses"] > 0 else 0
    results[book] = book_data

# === OUTPUT ===

print("=" * 90)
print("EXPANDED RENDERING ANALYSIS — SUMMARY TABLE")
print("=" * 90)
print(f"{'Book':<18} {'Verses':>8} {'ERs':>6} {'Density':>9} {'In Range':>10} {'Flagged':>9} {'Type Err':>10}")
print("-" * 90)

for book in BOOKS:
    if book not in results:
        continue
    d = results[book]
    in_range = "YES" if 5 <= d["density"] <= 20 else ("LOW" if d["density"] < 5 else "HIGH")
    print(f"{book:<18} {d['total_verses']:>8} {d['total_ers']:>6} {d['density']:>8}% {in_range:>10} {len(d['flagged_ers']):>9} {len(d['type_errors']):>10}")

total_v = sum(r["total_verses"] for r in results.values())
total_e = sum(r["total_ers"] for r in results.values())
total_d = round(total_e / total_v * 100, 1) if total_v > 0 else 0
total_f = sum(len(r["flagged_ers"]) for r in results.values())
total_t = sum(len(r["type_errors"]) for r in results.values())
print("-" * 90)
print(f"{'TOTAL':<18} {total_v:>8} {total_e:>6} {total_d:>8}% {'':>10} {total_f:>9} {total_t:>10}")

# High density books — chapter breakdown
print("\n")
for book in BOOKS:
    if book not in results:
        continue
    d = results[book]
    if d["density"] > 20:
        print("=" * 90)
        print(f"HIGH DENSITY BOOK: {book} ({d['density']}%) — Chapter Breakdown")
        print("=" * 90)
        print(f"  {'Chapter':<12} {'Verses':>8} {'ERs':>6} {'Density':>9}")
        print(f"  {'-'*40}")
        sorted_chs = sorted(d["chapters"].items(), key=lambda x: x[1]["density"], reverse=True)
        for ch, info in sorted_chs:
            marker = " <<<" if info["density"] > 25 else ""
            print(f"  Ch {ch:<8} {info['verses']:>8} {info['ers']:>6} {info['density']:>8}%{marker}")

# Flagged ERs
print("\n")
for book in BOOKS:
    if book not in results:
        continue
    d = results[book]
    if d["flagged_ers"]:
        print("=" * 90)
        print(f"FLAGGED ERs — {book} ({len(d['flagged_ers'])} flagged)")
        print("=" * 90)
        for f in d["flagged_ers"]:
            print(f"  Ch {f['chapter']}:{f['verse']} [{f['reason']}]")
            print(f"    \"{f['preview']}\"")
            print()

# Type errors
for book in BOOKS:
    if book not in results:
        continue
    d = results[book]
    if d["type_errors"]:
        print("=" * 90)
        print(f"TYPE ERRORS — {book}")
        print("=" * 90)
        for t in d["type_errors"]:
            print(f"  Ch {t['chapter']}:{t['verse']} — type is {t['type']} (should be string)")

