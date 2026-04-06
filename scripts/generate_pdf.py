#!/usr/bin/env python3
"""
Generate print-ready PDFs from The Covenant Rendering JSON chapter data.

Uses fpdf2 (pure Python PDF library).

Usage:
    python3 generate_pdf.py                  # Generate everything
    python3 generate_pdf.py --book ruth      # Generate one book PDF
    python3 generate_pdf.py --test           # Generate Ruth only (test mode)
    python3 generate_pdf.py --books-only     # Per-book PDFs only
    python3 generate_pdf.py --full-only      # Full Bible PDF only
    python3 generate_pdf.py --testaments-only  # OT + NT PDFs only
"""

import json
import os
import sys
import argparse
from pathlib import Path
from fpdf import FPDF

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "pdf"
PDF_DIR.mkdir(exist_ok=True)

# Page dimensions (US Letter in mm: 215.9 x 279.4)
PAGE_W = 215.9
PAGE_H = 279.4
MARGIN = 25.4  # 1 inch = 25.4mm
CONTENT_W = PAGE_W - 2 * MARGIN  # usable width

# Font paths
FONT_DIR = "/System/Library/Fonts/Supplemental"
GEORGIA = f"{FONT_DIR}/Georgia.ttf"
GEORGIA_BOLD = f"{FONT_DIR}/Georgia Bold.ttf"
GEORGIA_ITALIC = f"{FONT_DIR}/Georgia Italic.ttf"
GEORGIA_BOLD_ITALIC = f"{FONT_DIR}/Georgia Bold Italic.ttf"

HELVETICA_DIR = "/System/Library/Fonts"
# We'll use Helvetica Neue if available, otherwise built-in Helvetica

# Canonical book order
CANON = [
    ("genesis", "Genesis", "OT"),
    ("exodus", "Exodus", "OT"),
    ("leviticus", "Leviticus", "OT"),
    ("numbers", "Numbers", "OT"),
    ("deuteronomy", "Deuteronomy", "OT"),
    ("joshua", "Joshua", "OT"),
    ("judges", "Judges", "OT"),
    ("ruth", "Ruth", "OT"),
    ("1-samuel", "1 Samuel", "OT"),
    ("2-samuel", "2 Samuel", "OT"),
    ("1-kings", "1 Kings", "OT"),
    ("2-kings", "2 Kings", "OT"),
    ("1-chronicles", "1 Chronicles", "OT"),
    ("2-chronicles", "2 Chronicles", "OT"),
    ("ezra", "Ezra", "OT"),
    ("nehemiah", "Nehemiah", "OT"),
    ("esther", "Esther", "OT"),
    ("job", "Job", "OT"),
    ("psalms", "Psalms", "OT"),
    ("proverbs", "Proverbs", "OT"),
    ("ecclesiastes", "Ecclesiastes", "OT"),
    ("song-of-songs", "Song of Songs", "OT"),
    ("isaiah", "Isaiah", "OT"),
    ("jeremiah", "Jeremiah", "OT"),
    ("lamentations", "Lamentations", "OT"),
    ("ezekiel", "Ezekiel", "OT"),
    ("daniel", "Daniel", "OT"),
    ("hosea", "Hosea", "OT"),
    ("joel", "Joel", "OT"),
    ("amos", "Amos", "OT"),
    ("obadiah", "Obadiah", "OT"),
    ("jonah", "Jonah", "OT"),
    ("micah", "Micah", "OT"),
    ("nahum", "Nahum", "OT"),
    ("habakkuk", "Habakkuk", "OT"),
    ("zephaniah", "Zephaniah", "OT"),
    ("haggai", "Haggai", "OT"),
    ("zechariah", "Zechariah", "OT"),
    ("malachi", "Malachi", "OT"),
    ("matthew", "Matthew", "NT"),
    ("mark", "Mark", "NT"),
    ("luke", "Luke", "NT"),
    ("john", "John", "NT"),
    ("acts", "Acts", "NT"),
    ("romans", "Romans", "NT"),
    ("1-corinthians", "1 Corinthians", "NT"),
    ("2-corinthians", "2 Corinthians", "NT"),
    ("galatians", "Galatians", "NT"),
    ("ephesians", "Ephesians", "NT"),
    ("philippians", "Philippians", "NT"),
    ("colossians", "Colossians", "NT"),
    ("1-thessalonians", "1 Thessalonians", "NT"),
    ("2-thessalonians", "2 Thessalonians", "NT"),
    ("1-timothy", "1 Timothy", "NT"),
    ("2-timothy", "2 Timothy", "NT"),
    ("titus", "Titus", "NT"),
    ("philemon", "Philemon", "NT"),
    ("hebrews", "Hebrews", "NT"),
    ("james", "James", "NT"),
    ("1-peter", "1 Peter", "NT"),
    ("2-peter", "2 Peter", "NT"),
    ("1-john", "1 John", "NT"),
    ("2-john", "2 John", "NT"),
    ("3-john", "3 John", "NT"),
    ("jude", "Jude", "NT"),
    ("revelation", "Revelation", "NT"),
]

POETRY_BOOKS = {
    "psalms", "proverbs", "ecclesiastes", "song-of-songs",
    "job", "lamentations",
}

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_chapter(book_folder, chapter_num):
    path = BASE_DIR / book_folder / f"chapter-{chapter_num:02d}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def count_chapters(book_folder):
    book_dir = BASE_DIR / book_folder
    if not book_dir.exists():
        return 0
    return len(list(book_dir.glob("chapter-*.json")))


# ---------------------------------------------------------------------------
# Custom PDF class with headers/footers
# ---------------------------------------------------------------------------

class TCRPDF(FPDF):

    def __init__(self):
        super().__init__(format="letter")
        self.current_book = ""
        self.show_header = True
        self._suppress_header = False
        self._register_fonts()

    def _register_fonts(self):
        """Register Georgia TTF fonts."""
        self.add_font("Georgia", "", GEORGIA)
        self.add_font("Georgia", "B", GEORGIA_BOLD)
        self.add_font("Georgia", "I", GEORGIA_ITALIC)
        self.add_font("Georgia", "BI", GEORGIA_BOLD_ITALIC)

    def header(self):
        if self._suppress_header or self.page_no() <= 1:
            return
        self.set_font("Helvetica", "", 7)
        self.set_text_color(150, 150, 150)

        if self.page_no() % 2 == 0:
            # Left (even) page: book name
            self.set_y(10)
            self.set_x(MARGIN)
            self.cell(CONTENT_W, 4, self.current_book.upper(), align="L")
        else:
            # Right (odd) page: TCR
            self.set_y(10)
            self.set_x(MARGIN)
            self.cell(CONTENT_W, 4, "THE COVENANT RENDERING", align="R")

        self.set_text_color(0, 0, 0)
        self.set_y(MARGIN)

    def footer(self):
        self.set_y(-20)
        self.set_font("Georgia", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, str(self.page_no()), align="C")
        self.set_text_color(0, 0, 0)

    def _new_page_no_header(self):
        """Add a page that suppresses the running header."""
        self._suppress_header = True
        self.add_page()
        self._suppress_header = False


# ---------------------------------------------------------------------------
# Rendering functions
# ---------------------------------------------------------------------------

def add_title_page(pdf):
    """Title page for the full Bible."""
    pdf._new_page_no_header()
    pdf.set_y(100)
    pdf.set_font("Helvetica", "", 26)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 12, "The Covenant Rendering", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Georgia", "I", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "A Modern English Bible from the Hebrew and Greek", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(40)
    pdf.set_font("Georgia", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Translated by Aaron Blonquist", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)


def add_copyright_page(pdf):
    """Copyright / license page."""
    pdf._new_page_no_header()
    pdf.set_y(130)
    pdf.set_font("Georgia", "B", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "The Covenant Rendering", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Georgia", "", 8)
    lines = [
        "A Modern English Bible from the Hebrew and Greek",
        "Translated by Aaron Blonquist",
        "",
        "Copyright 2026 Aaron Blonquist.",
        "Licensed under the Creative Commons Attribution 4.0",
        "International License (CC-BY-4.0).",
        "",
        "You are free to share, copy, and redistribute this material in any",
        "medium or format, and to adapt, remix, transform, and build upon it",
        "for any purpose, even commercially, under the following terms:",
        "",
        "Attribution -- You must give appropriate credit to Aaron Blonquist",
        "as translator, provide a link to the license, and indicate if changes",
        "were made.",
        "",
        "License: https://creativecommons.org/licenses/by/4.0/",
        "",
        "Old Testament source text: Westminster Leningrad Codex (WLC)",
        "New Testament source text: Nestle-Aland / UBS Greek New Testament",
    ]
    for line in lines:
        if line == "":
            pdf.ln(3)
        else:
            pdf.cell(0, 4.2, line, align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)


def add_introduction(pdf):
    """Introduction page."""
    pdf._new_page_no_header()
    pdf.set_font("Helvetica", "", 15)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Introduction", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Georgia", "", 10)
    pdf.set_text_color(30, 30, 30)

    paras = [
        "The Covenant Rendering is a fresh English translation of the Bible produced directly from the Hebrew and Greek source texts. It aims to bring the meaning, weight, and texture of the original languages into clear, modern English without sacrificing the literary power of the ancient texts. Where older translations sometimes obscure meaning behind archaic phrasing, and where modern paraphrases sometimes flatten the richness of the original, this rendering seeks the middle ground: faithful to the source, readable in English, and honest about the choices a translator must make.",
        "Every translation is an interpretation. The Covenant Rendering does not pretend otherwise. Where a Hebrew or Greek word carries a range of meaning that no single English word can capture, the translator notes explain what was chosen and why. Where the ancient text is genuinely ambiguous, the ambiguity is preserved rather than silently resolved. The goal is not to replace other translations but to offer a rendering that takes the reader as close to the original as English allows, then trusts them to think.",
        "This is the Reading Layer: clean English text with verse numbers, chapter preambles for context, and translator notes for those who want to go deeper. The Hebrew, Greek, and comparative apparatus exist in the full digital edition. Here, the text breathes on its own.",
    ]
    for para in paras:
        pdf.multi_cell(CONTENT_W, 5.5, para, align="J")
        pdf.ln(3)

    pdf.set_text_color(0, 0, 0)


def add_toc(pdf, books_list):
    """Table of contents. books_list: [(display_name, testament), ...]"""
    pdf._new_page_no_header()
    pdf.set_font("Helvetica", "", 15)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Table of Contents", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    current_testament = None
    for name, testament in books_list:
        # Check if we need a new page
        if pdf.get_y() > PAGE_H - 35:
            pdf.add_page()
            pdf.ln(5)

        if testament != current_testament:
            current_testament = testament
            label = "Old Testament" if testament == "OT" else "New Testament"
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 6, label.upper(), align="L", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

        pdf.set_font("Georgia", "", 9.5)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 5.2, name, align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)


def add_testament_divider(pdf, name):
    """Testament divider page."""
    pdf._new_page_no_header()
    pdf.set_y(110)
    pdf.set_font("Helvetica", "", 22)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 12, name, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)


def add_book_divider(pdf, book_name):
    """Book title/divider page."""
    pdf._new_page_no_header()
    pdf.current_book = book_name
    pdf.set_y(100)
    pdf.set_font("Helvetica", "", 24)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 12, book_name, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)


def is_poetry(rendering, book_folder):
    """Detect poetry by line breaks in rendering."""
    return "\n" in rendering


def ensure_space(pdf, needed_mm):
    """Add a new page if there isn't enough vertical space."""
    if pdf.get_y() + needed_mm > PAGE_H - 30:
        pdf.add_page()
        return True
    return False


def add_preamble(pdf, preamble):
    """Render chapter preamble."""
    if not preamble:
        return

    sections = [
        ("summary", "Summary"),
        ("remarkable", "What Makes This Remarkable"),
        ("friction", "Translation Friction"),
        ("connections", "Connections"),
    ]

    has_content = False
    for key, label in sections:
        val = preamble.get(key, "")
        if val:
            has_content = True
            break

    if not has_content:
        return

    # Draw left border line (we'll track start y)
    start_y = pdf.get_y()
    indent = 5  # left indent for preamble text

    for key, label in sections:
        val = preamble.get(key, "")
        if not val:
            continue

        # Strip tradition comparison sections for print
        for splitter in ["\n\n**Tradition comparisons:**", "\n\n**Tradition comparison"]:
            if splitter in val:
                val = val.split(splitter)[0].strip()

        ensure_space(pdf, 15)

        # Label
        pdf.set_x(MARGIN + indent)
        pdf.set_font("Helvetica", "B", 6.5)
        pdf.set_text_color(140, 140, 140)
        label_w = pdf.get_string_width(label + ":  ")
        pdf.cell(label_w, 4, label + ":", new_x="END", new_y="TOP")

        # Text
        pdf.set_font("Georgia", "I", 8)
        pdf.set_text_color(100, 100, 100)
        remaining_w = CONTENT_W - indent - label_w
        # Use multi_cell for wrapping but handle the first line alongside the label
        x_after_label = pdf.get_x()
        y_before = pdf.get_y()

        # Write first portion inline, then wrap
        pdf.set_x(x_after_label)
        pdf.multi_cell(remaining_w, 4, val, align="L")

        pdf.ln(1.5)

    # Draw decorative left border
    end_y = pdf.get_y()
    if end_y > start_y:
        pdf.set_draw_color(210, 210, 210)
        pdf.set_line_width(0.5)
        pdf.line(MARGIN + 2, start_y, MARGIN + 2, end_y - 1)
        pdf.set_draw_color(0, 0, 0)

    pdf.ln(3)
    pdf.set_text_color(0, 0, 0)


def add_verses(pdf, verses, book_folder):
    """Render verses in paragraph style with superscript verse numbers."""
    pdf.set_font("Georgia", "", 10)
    pdf.set_text_color(26, 26, 26)

    # Group verses into paragraph blocks
    # Poetry verses get their own block; prose verses are grouped together
    blocks = []  # list of (type, content) where type is 'prose' or 'poetry'
    current_prose = []

    for v in verses:
        text = v.get("rendering", "")
        if not text:
            continue
        vnum = v.get("verse", "")

        if is_poetry(text, book_folder):
            if current_prose:
                blocks.append(("prose", current_prose))
                current_prose = []
            blocks.append(("poetry", [(vnum, text)]))
        else:
            current_prose.append((vnum, text))

    if current_prose:
        blocks.append(("prose", current_prose))

    for block_type, block_verses in blocks:
        if block_type == "prose":
            _render_prose_block(pdf, block_verses)
        else:
            _render_poetry_block(pdf, block_verses, book_folder)


def _render_prose_block(pdf, verse_list):
    """Render prose verses as a paragraph with superscript verse numbers."""
    ensure_space(pdf, 10)

    # Build fragments for write() - mixing fonts for superscript verse numbers
    for i, (vnum, text) in enumerate(verse_list):
        # Verse number (superscript-like: smaller, raised)
        pdf.set_font("Georgia", "B", 6.5)
        pdf.set_text_color(140, 140, 140)
        pdf.write(5, str(vnum))

        # Verse text
        pdf.set_font("Georgia", "", 10)
        pdf.set_text_color(26, 26, 26)
        suffix = " " if i < len(verse_list) - 1 else ""
        pdf.write(5, text + suffix)

    pdf.ln(5.5)


def _render_poetry_block(pdf, verse_list, book_folder):
    """Render poetry verses preserving line breaks."""
    ensure_space(pdf, 12)

    indent_base = 10  # mm indent for poetry

    for vnum, text in verse_list:
        lines = text.split("\n")
        for j, line in enumerate(lines):
            stripped = line.lstrip()
            extra_indent = len(line) - len(stripped)
            total_indent = indent_base + (extra_indent * 2)

            ensure_space(pdf, 5)

            pdf.set_x(MARGIN + total_indent)

            if j == 0:
                # First line: add verse number
                pdf.set_font("Georgia", "B", 6.5)
                pdf.set_text_color(140, 140, 140)
                pdf.write(4.5, str(vnum))
                pdf.set_font("Georgia", "", 10)
                pdf.set_text_color(26, 26, 26)
                pdf.write(4.5, stripped)
                pdf.ln(4.8)
            else:
                pdf.set_font("Georgia", "", 10)
                pdf.set_text_color(26, 26, 26)
                if stripped:
                    pdf.cell(CONTENT_W - total_indent, 4.8, stripped,
                             new_x="LMARGIN", new_y="NEXT")
                else:
                    pdf.ln(2)

    pdf.ln(3)


def add_translator_notes(pdf, verses):
    """Render translator notes as endnotes for the chapter."""
    notes = []
    for v in verses:
        vnum = v.get("verse", "")
        for note in v.get("translator_notes", []):
            notes.append((vnum, note))

    if not notes:
        return

    ensure_space(pdf, 15)

    # Separator line
    pdf.set_draw_color(210, 210, 210)
    pdf.set_line_width(0.3)
    y = pdf.get_y()
    pdf.line(MARGIN, y, MARGIN + 50, y)
    pdf.set_draw_color(0, 0, 0)
    pdf.ln(3)

    # Header
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(140, 140, 140)
    pdf.cell(CONTENT_W, 4, "TRANSLATOR NOTES", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    for vnum, note in notes:
        ensure_space(pdf, 8)

        # Verse reference
        pdf.set_font("Georgia", "B", 7.5)
        pdf.set_text_color(100, 100, 100)
        ref_w = pdf.get_string_width(str(vnum) + ". ")
        pdf.cell(ref_w, 3.8, str(vnum) + ".", new_x="END", new_y="TOP")

        # Note text
        pdf.set_font("Georgia", "", 7.5)
        pdf.set_text_color(100, 100, 100)
        x = pdf.get_x()
        pdf.multi_cell(CONTENT_W - (x - MARGIN), 3.8, note, align="L")
        pdf.ln(1.5)

    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def add_chapter(pdf, data, book_folder, book_name):
    """Render a complete chapter."""
    chapter_num = data.get("meta", {}).get("chapter", "")
    preamble = data.get("preamble", {})
    verses = data.get("verses", [])

    # Ensure we start with some space (but not necessarily a new page for every chapter)
    if pdf.get_y() > PAGE_H - 80:
        pdf.add_page()

    # Large chapter number
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 28)
    pdf.set_text_color(60, 60, 60)
    ch_str = str(chapter_num)
    ch_w = pdf.get_string_width(ch_str)
    ch_y = pdf.get_y()
    pdf.cell(ch_w + 4, 12, ch_str, new_x="END", new_y="TOP")
    pdf.set_text_color(0, 0, 0)

    # Reserve space beside chapter number for first preamble line
    text_start_x = MARGIN + ch_w + 6
    pdf.set_xy(text_start_x, ch_y + 2)

    # Move past the chapter number area
    pdf.set_xy(MARGIN, ch_y + 14)

    # Preamble
    add_preamble(pdf, preamble)

    # Verses
    add_verses(pdf, verses, book_folder)

    # Translator notes
    add_translator_notes(pdf, verses)


def add_book(pdf, book_folder, book_name, include_divider=True):
    """Render an entire book."""
    if include_divider:
        add_book_divider(pdf, book_name)

    num_chapters = count_chapters(book_folder)
    for ch in range(1, num_chapters + 1):
        data = load_chapter(book_folder, ch)
        if data:
            add_chapter(pdf, data, book_folder, book_name)


# ---------------------------------------------------------------------------
# PDF generation entry points
# ---------------------------------------------------------------------------

def generate_book_pdf(book_folder, book_name):
    """Generate a single book PDF."""
    pdf = TCRPDF()
    pdf.set_auto_page_break(auto=True, margin=28)
    pdf.current_book = book_name

    add_book(pdf, book_folder, book_name, include_divider=True)

    output = PDF_DIR / f"{book_folder}.pdf"
    pdf.output(str(output))
    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"  {output.name:45s} {size_mb:7.2f} MB")


def generate_testament_pdf(testament):
    """Generate OT or NT PDF."""
    label = "Old Testament" if testament == "OT" else "New Testament"
    filename = "old-testament.pdf" if testament == "OT" else "new-testament.pdf"

    books = [(f, n, t) for f, n, t in CANON if t == testament]
    toc_list = [(n, t) for _, n, t in books]

    pdf = TCRPDF()
    pdf.set_auto_page_break(auto=True, margin=28)

    add_title_page(pdf)
    add_copyright_page(pdf)
    add_introduction(pdf)
    add_toc(pdf, toc_list)
    add_testament_divider(pdf, label)

    for folder, name, _ in books:
        print(f"    {name}...", flush=True)
        add_book(pdf, folder, name)

    output = PDF_DIR / filename
    pdf.output(str(output))
    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"  {output.name:45s} {size_mb:7.2f} MB")


def generate_full_bible_pdf():
    """Generate the complete Bible PDF."""
    toc_list = [(n, t) for _, n, t in CANON]

    pdf = TCRPDF()
    pdf.set_auto_page_break(auto=True, margin=28)

    add_title_page(pdf)
    add_copyright_page(pdf)
    add_introduction(pdf)
    add_toc(pdf, toc_list)

    current_testament = None
    for folder, name, testament in CANON:
        if testament != current_testament:
            current_testament = testament
            t_label = "Old Testament" if testament == "OT" else "New Testament"
            add_testament_divider(pdf, t_label)
        print(f"    {name}...", flush=True)
        add_book(pdf, folder, name)

    output = PDF_DIR / "the-covenant-rendering-full.pdf"
    pdf.output(str(output))
    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"  {output.name:45s} {size_mb:7.2f} MB")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate TCR PDFs")
    parser.add_argument("--book", help="Generate PDF for a single book (folder name)")
    parser.add_argument("--test", action="store_true", help="Test mode: generate Ruth only")
    parser.add_argument("--books-only", action="store_true", help="Per-book PDFs only")
    parser.add_argument("--testaments-only", action="store_true", help="Testament PDFs only")
    parser.add_argument("--full-only", action="store_true", help="Full Bible PDF only")
    args = parser.parse_args()

    if args.test:
        print("=== Test mode: generating Ruth PDF ===")
        generate_book_pdf("ruth", "Ruth")
        print("\nDone! Check pdf/ruth.pdf")
        return

    if args.book:
        match = [(f, n) for f, n, _ in CANON if f == args.book]
        if not match:
            print(f"Unknown book: {args.book}")
            print("Available:", ", ".join(f for f, _, _ in CANON))
            sys.exit(1)
        folder, name = match[0]
        print(f"=== Generating {name} PDF ===")
        generate_book_pdf(folder, name)
        print("Done!")
        return

    if args.books_only:
        print("=== Generating per-book PDFs ===")
        for folder, name, _ in CANON:
            generate_book_pdf(folder, name)
        print(f"\nDone! {len(CANON)} book PDFs in pdf/")
        return

    if args.testaments_only:
        print("=== Generating testament PDFs ===")
        print("\n--- Old Testament ---")
        generate_testament_pdf("OT")
        print("\n--- New Testament ---")
        generate_testament_pdf("NT")
        print("\nDone!")
        return

    if args.full_only:
        print("=== Generating full Bible PDF ===")
        generate_full_bible_pdf()
        print("\nDone!")
        return

    # Default: generate everything
    print("=== Generating all TCR PDFs ===\n")

    print("--- Per-book PDFs ---")
    for folder, name, _ in CANON:
        generate_book_pdf(folder, name)

    print("\n--- Testament PDFs ---")
    print("\nOld Testament:")
    generate_testament_pdf("OT")
    print("\nNew Testament:")
    generate_testament_pdf("NT")

    print("\n--- Full Bible PDF ---")
    generate_full_bible_pdf()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_size = 0
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    for p in pdf_files:
        size = p.stat().st_size / (1024 * 1024)
        total_size += size
    print(f"  Total PDFs:  {len(pdf_files)}")
    print(f"  Total size:  {total_size:.1f} MB")
    print(f"  Output dir:  {PDF_DIR}")


if __name__ == "__main__":
    main()
