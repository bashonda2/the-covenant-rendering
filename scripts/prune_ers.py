#!/usr/bin/env python3
"""
Prune expanded_rendering fields that are narrative commentary rather than
Hebrew term analysis. Keeps ERs that reference specific Hebrew terms;
removes ERs that are verse-by-verse commentary.

Usage:
    python3 scripts/prune_ers.py 1-samuel/          # prune and write
    python3 scripts/prune_ers.py 1-samuel/ --dry-run # report only, no changes
"""

import json
import os
import re
import sys
from pathlib import Path


def is_term_focused(er_text: str) -> bool:
    """Return True if the ER is focused on a specific Hebrew term."""
    first_100 = er_text[:120]

    if re.search(r"Hebrew\b", first_100):
        return True

    if re.match(
        r"The (verb|noun|word|term|phrase|name|root|particle|adjective|"
        r"construction|formula|expression|title|idiom|image|imagery|"
        r"metaphor|prefix|suffix|infinitive|imperative|cognate|"
        r"designation|epithet|clause|command|declaration|oath|blessing)",
        er_text,
    ):
        return True

    if re.search(r"\(['\"]?[a-zāēīōūâêîôûḥṣṭ]", first_100):
        return True

    if re.search(r"[\u0590-\u05FF]", first_100):
        return True

    if re.match(r"(Literally|The literal|In Hebrew|The root\b)", er_text):
        return True

    return False


def prune_chapter(filepath: str, dry_run: bool = False) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = {"file": filepath, "total_ers": 0, "kept": 0, "removed": 0, "removed_verses": []}

    for v in data.get("verses", []):
        er = v.get("expanded_rendering", "")
        if not er:
            continue

        stats["total_ers"] += 1

        if is_term_focused(er):
            stats["kept"] += 1
        else:
            stats["removed"] += 1
            stats["removed_verses"].append(v.get("verse", "?"))
            if not dry_run:
                del v["expanded_rendering"]

    if not dry_run and stats["removed"] > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return stats


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/prune_ers.py <dir> [--dry-run]")
        sys.exit(1)

    target = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN (no files will be modified) ===\n")

    files = sorted(
        os.path.join(target, f)
        for f in os.listdir(target)
        if f.startswith("chapter-") and f.endswith(".json")
    )

    total_ers = 0
    total_kept = 0
    total_removed = 0

    for fpath in files:
        stats = prune_chapter(fpath, dry_run)
        total_ers += stats["total_ers"]
        total_kept += stats["kept"]
        total_removed += stats["removed"]

        ch = os.path.basename(fpath).replace("chapter-", "").replace(".json", "")
        if stats["removed"] > 0:
            print(
                f"Ch {ch}: {stats['total_ers']} ERs → kept {stats['kept']}, "
                f"removed {stats['removed']} (vv. {stats['removed_verses']})"
            )
        else:
            print(f"Ch {ch}: {stats['total_ers']} ERs → all kept")

    print(f"\nSUMMARY: {total_ers} total → {total_kept} kept, {total_removed} removed")
    pct = total_kept / total_ers * 100 if total_ers else 0
    print(f"New density will be {total_kept}/{812} verses ({total_kept/812*100:.0f}%)")


if __name__ == "__main__":
    main()
