#!/usr/bin/env python3
"""Audit all 22 completed books for ER density and preamble completeness."""

import json
import os
import glob

BASE = "/Users/aaronblonquist/The Covenant Rendering"

BOOKS = [
    "genesis", "exodus", "leviticus", "numbers", "deuteronomy",
    "joshua", "judges", "ruth",
    "1-samuel", "2-samuel", "1-kings", "2-kings",
    "1-chronicles", "2-chronicles",
    "ezra", "nehemiah", "esther",
    "job", "psalms", "proverbs", "ecclesiastes", "song-of-songs"
]

PREAMBLE_FIELDS = ["summary", "remarkable", "friction", "connections"]

def audit():
    print("=" * 90)
    print("AUDIT 1: EXPANDED RENDERING DENSITY")
    print("=" * 90)
    print(f"{'Book':<20} {'Chapters':>8} {'Verses':>8} {'w/ ER':>8} {'Density':>8}  Flag")
    print("-" * 90)

    total_all_verses = 0
    total_all_er = 0
    flagged_books = []

    for book in BOOKS:
        book_dir = os.path.join(BASE, book)
        if not os.path.isdir(book_dir):
            print(f"  WARNING: Directory not found: {book_dir}")
            continue

        files = sorted(glob.glob(os.path.join(book_dir, "chapter-*.json")))
        book_verses = 0
        book_er = 0
        chapter_count = len(files)

        for f in files:
            try:
                with open(f) as fh:
                    data = json.load(fh)
                verses = data.get("verses", [])
                book_verses += len(verses)
                for v in verses:
                    if "expanded_rendering" in v and v["expanded_rendering"]:
                        book_er += 1
            except Exception as e:
                print(f"  ERROR reading {f}: {e}")

        if book_verses > 0:
            density = (book_er / book_verses) * 100
        else:
            density = 0.0

        flag = ""
        if density > 20:
            flag = "*** OVER 20% ***"
            flagged_books.append((book, density, "OVER"))
        elif density < 5:
            flag = "*** UNDER 5% ***"
            flagged_books.append((book, density, "UNDER"))

        print(f"{book:<20} {chapter_count:>8} {book_verses:>8} {book_er:>8} {density:>7.1f}%  {flag}")
        total_all_verses += book_verses
        total_all_er += book_er

    print("-" * 90)
    overall = (total_all_er / total_all_verses * 100) if total_all_verses else 0
    print(f"{'TOTAL':<20} {'':>8} {total_all_verses:>8} {total_all_er:>8} {overall:>7.1f}%")
    print()

    if flagged_books:
        print("FLAGGED BOOKS:")
        for b, d, direction in flagged_books:
            print(f"  {b}: {d:.1f}% ({direction})")
    else:
        print("All books within 5-20% target range.")

    print()
    print("=" * 90)
    print("AUDIT 2: PREAMBLE COMPLETENESS")
    print("=" * 90)

    missing_preamble = []
    incomplete_preamble = []
    empty_field_preamble = []
    total_chapters = 0
    chapters_with_preamble = 0

    for book in BOOKS:
        book_dir = os.path.join(BASE, book)
        if not os.path.isdir(book_dir):
            continue

        files = sorted(glob.glob(os.path.join(book_dir, "chapter-*.json")))

        for f in files:
            chapter_name = f"{book}/{os.path.basename(f)}"
            total_chapters += 1
            try:
                with open(f) as fh:
                    data = json.load(fh)

                preamble = data.get("preamble")
                if preamble is None:
                    missing_preamble.append(chapter_name)
                    continue

                chapters_with_preamble += 1

                # Check for missing fields
                missing_fields = []
                empty_fields = []
                for field in PREAMBLE_FIELDS:
                    if field not in preamble:
                        missing_fields.append(field)
                    elif isinstance(preamble[field], str) and preamble[field].strip() == "":
                        empty_fields.append(field)

                if missing_fields:
                    incomplete_preamble.append((chapter_name, missing_fields))
                if empty_fields:
                    empty_field_preamble.append((chapter_name, empty_fields))

            except Exception as e:
                print(f"  ERROR reading {f}: {e}")

    print(f"\nTotal chapters scanned: {total_chapters}")
    print(f"Chapters WITH preamble: {chapters_with_preamble}")
    print(f"Chapters MISSING preamble: {len(missing_preamble)}")
    print()

    if missing_preamble:
        print(f"--- Chapters missing preamble entirely ({len(missing_preamble)}) ---")
        # Group by book
        from collections import defaultdict
        by_book = defaultdict(list)
        for ch in missing_preamble:
            parts = ch.split("/")
            by_book[parts[0]].append(parts[1])
        for b in BOOKS:
            if b in by_book:
                chs = by_book[b]
                print(f"  {b} ({len(chs)} chapters): {', '.join(sorted(chs))}")
        print()

    if incomplete_preamble:
        print(f"--- Chapters with incomplete preamble (missing fields) ({len(incomplete_preamble)}) ---")
        for ch, fields in incomplete_preamble:
            print(f"  {ch}: missing [{', '.join(fields)}]")
        print()

    if empty_field_preamble:
        print(f"--- Chapters with empty preamble fields ({len(empty_field_preamble)}) ---")
        for ch, fields in empty_field_preamble:
            print(f"  {ch}: empty [{', '.join(fields)}]")
        print()

    if not missing_preamble and not incomplete_preamble and not empty_field_preamble:
        print("All chapters have complete preambles with all 4 required fields populated.")

if __name__ == "__main__":
    audit()
