#!/usr/bin/env python3
"""
NT→OT Cross-Reference Builder for The Covenant Rendering

Phase 1: Builds a comprehensive index of NT verses that quote or directly
         allude to OT passages.
Phase 2: Adds [TCR Cross-Reference] notes to NT chapter JSON files.

Usage:
    python3 scripts/nt_ot_crossref.py                  # dry-run (report only)
    python3 scripts/nt_ot_crossref.py --apply           # write cross-refs into JSON
    python3 scripts/nt_ot_crossref.py --apply --verbose  # write + show each addition
"""

import json
import os
import sys
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# NT book slug → directory name mapping
# ---------------------------------------------------------------------------
NT_BOOKS_ORDERED = [
    "matthew", "mark", "luke", "john", "acts",
    "romans", "1-corinthians", "2-corinthians", "galatians", "ephesians",
    "philippians", "colossians", "1-thessalonians", "2-thessalonians",
    "1-timothy", "2-timothy", "titus", "philemon",
    "hebrews", "james", "1-peter", "2-peter",
    "1-john", "2-john", "3-john", "jude", "revelation",
]

# OT book display name → directory slug
OT_BOOK_SLUGS = {
    "Genesis": "genesis", "Exodus": "exodus", "Leviticus": "leviticus",
    "Numbers": "numbers", "Deuteronomy": "deuteronomy",
    "Joshua": "joshua", "Judges": "judges", "Ruth": "ruth",
    "1 Samuel": "1-samuel", "2 Samuel": "2-samuel",
    "1 Kings": "1-kings", "2 Kings": "2-kings",
    "1 Chronicles": "1-chronicles", "2 Chronicles": "2-chronicles",
    "Ezra": "ezra", "Nehemiah": "nehemiah", "Esther": "esther",
    "Job": "job", "Psalms": "psalms", "Psalm": "psalms",
    "Proverbs": "proverbs", "Ecclesiastes": "ecclesiastes",
    "Song of Songs": "song-of-songs", "Song of Solomon": "song-of-songs",
    "Isaiah": "isaiah", "Jeremiah": "jeremiah", "Lamentations": "lamentations",
    "Ezekiel": "ezekiel", "Daniel": "daniel",
    "Hosea": "hosea", "Joel": "joel", "Amos": "amos",
    "Obadiah": "obadiah", "Jonah": "jonah", "Micah": "micah",
    "Nahum": "nahum", "Habakkuk": "habakkuk", "Zephaniah": "zephaniah",
    "Haggai": "haggai", "Zechariah": "zechariah", "Malachi": "malachi",
}

# Verify all OT dirs exist
OT_DIRS_PRESENT = set()
for slug in OT_BOOK_SLUGS.values():
    if (PROJECT_ROOT / slug).is_dir():
        OT_DIRS_PRESENT.add(slug)


def ot_exists(book_display: str) -> bool:
    """Check if we have the OT book in the data repo."""
    slug = OT_BOOK_SLUGS.get(book_display)
    return slug is not None and slug in OT_DIRS_PRESENT


# ---------------------------------------------------------------------------
# BUILT-IN CROSS-REFERENCE DATABASE
# Format: (nt_book_slug, chapter, verse_or_range) → list of (OT_display, ch:vs, description)
# verse_or_range: int for single verse, or (start, end) tuple for range
# ---------------------------------------------------------------------------

def _xrefs():
    """Return the master cross-reference list as a flat list of tuples:
    (nt_slug, nt_chapter, nt_verse, ot_display, ot_ref, desc)
    where nt_verse is a single int. Ranges get expanded.
    """
    raw = [
        # === MATTHEW ===
        ("matthew", 1, 23, "Isaiah", "7:14", "Immanuel prophecy (almah/virgin)"),
        ("matthew", 2, 6, "Micah", "5:2", "Bethlehem as birthplace of the ruler"),
        ("matthew", 2, 15, "Hosea", "11:1", "Out of Egypt I called my son"),
        ("matthew", 2, 18, "Jeremiah", "31:15", "Rachel weeping for her children"),
        ("matthew", 3, 3, "Isaiah", "40:3", "Voice crying in the wilderness"),
        ("matthew", 4, 4, "Deuteronomy", "8:3", "Man shall not live by bread alone"),
        ("matthew", 4, 7, "Deuteronomy", "6:16", "You shall not put the LORD your God to the test"),
        ("matthew", 4, 10, "Deuteronomy", "6:13", "You shall worship the LORD your God only"),
        ("matthew", 4, 15, "Isaiah", "9:1-2", "Land of Zebulun and Naphtali — great light"),
        ("matthew", 4, 16, "Isaiah", "9:1-2", "The people dwelling in darkness have seen a great light"),
        ("matthew", 5, 21, "Exodus", "20:13", "You shall not murder"),
        ("matthew", 5, 27, "Exodus", "20:14", "You shall not commit adultery"),
        ("matthew", 5, 31, "Deuteronomy", "24:1", "Certificate of divorce"),
        ("matthew", 5, 33, "Leviticus", "19:12", "You shall not swear falsely"),
        ("matthew", 5, 38, "Exodus", "21:24", "Eye for eye, tooth for tooth"),
        ("matthew", 5, 43, "Leviticus", "19:18", "Love your neighbor"),
        ("matthew", 8, 17, "Isaiah", "53:4", "He took our infirmities"),
        ("matthew", 9, 13, "Hosea", "6:6", "I desire mercy, not sacrifice"),
        ("matthew", 11, 10, "Malachi", "3:1", "I send my messenger before your face"),
        ("matthew", 12, 7, "Hosea", "6:6", "I desire mercy, not sacrifice"),
        ("matthew", 12, 18, "Isaiah", "42:1-4", "My servant whom I have chosen"),
        ("matthew", 12, 19, "Isaiah", "42:1-4", "He will not quarrel or cry aloud"),
        ("matthew", 12, 20, "Isaiah", "42:1-4", "A bruised reed he will not break"),
        ("matthew", 12, 21, "Isaiah", "42:1-4", "In his name the nations will hope"),
        ("matthew", 13, 14, "Isaiah", "6:9-10", "Hearing you will hear but not understand"),
        ("matthew", 13, 15, "Isaiah", "6:9-10", "This people's heart has grown dull"),
        ("matthew", 13, 35, "Psalms", "78:2", "I will open my mouth in parables"),
        ("matthew", 15, 4, "Exodus", "20:12", "Honor your father and mother"),
        ("matthew", 15, 8, "Isaiah", "29:13", "This people honors me with their lips"),
        ("matthew", 15, 9, "Isaiah", "29:13", "Teaching as doctrines the commandments of men"),
        ("matthew", 19, 4, "Genesis", "1:27", "Male and female he created them"),
        ("matthew", 19, 5, "Genesis", "2:24", "A man shall leave his father and mother"),
        ("matthew", 21, 5, "Zechariah", "9:9", "Your king comes to you, humble, on a donkey"),
        ("matthew", 21, 9, "Psalms", "118:26", "Blessed is he who comes in the name of the LORD"),
        ("matthew", 21, 13, "Isaiah", "56:7", "My house shall be called a house of prayer"),
        ("matthew", 21, 16, "Psalms", "8:2", "Out of the mouth of infants you have prepared praise"),
        ("matthew", 21, 42, "Psalms", "118:22-23", "The stone the builders rejected"),
        ("matthew", 22, 32, "Exodus", "3:6", "I am the God of Abraham, Isaac, and Jacob"),
        ("matthew", 22, 37, "Deuteronomy", "6:5", "Love the LORD your God with all your heart"),
        ("matthew", 22, 39, "Leviticus", "19:18", "Love your neighbor as yourself"),
        ("matthew", 22, 44, "Psalms", "110:1", "The LORD said to my Lord"),
        ("matthew", 23, 39, "Psalms", "118:26", "Blessed is he who comes in the name of the LORD"),
        ("matthew", 24, 15, "Daniel", "9:27", "Abomination of desolation"),
        ("matthew", 24, 30, "Daniel", "7:13", "Son of Man coming on the clouds"),
        ("matthew", 26, 31, "Zechariah", "13:7", "Strike the shepherd, the sheep will be scattered"),
        ("matthew", 26, 64, "Psalms", "110:1", "Seated at the right hand of Power"),
        ("matthew", 27, 9, "Zechariah", "11:12-13", "Thirty pieces of silver"),
        ("matthew", 27, 10, "Zechariah", "11:12-13", "The price of him on whom a price had been set"),
        ("matthew", 27, 35, "Psalms", "22:18", "They divided my garments among them"),
        ("matthew", 27, 46, "Psalms", "22:1", "My God, my God, why have you forsaken me"),

        # === MARK ===
        ("mark", 1, 2, "Malachi", "3:1", "I send my messenger before your face"),
        ("mark", 1, 3, "Isaiah", "40:3", "Voice of one crying in the wilderness"),
        ("mark", 4, 12, "Isaiah", "6:9-10", "Seeing they may see and not perceive"),
        ("mark", 7, 6, "Isaiah", "29:13", "This people honors me with their lips"),
        ("mark", 7, 10, "Exodus", "20:12", "Honor your father and mother"),
        ("mark", 10, 6, "Genesis", "1:27", "Male and female he created them"),
        ("mark", 10, 7, "Genesis", "2:24", "A man shall leave his father and mother"),
        ("mark", 10, 8, "Genesis", "2:24", "The two shall become one flesh"),
        ("mark", 10, 19, "Exodus", "20:12-16", "Do not murder, do not commit adultery..."),
        ("mark", 11, 9, "Psalms", "118:26", "Blessed is he who comes in the name of the LORD"),
        ("mark", 11, 17, "Isaiah", "56:7", "My house shall be called a house of prayer"),
        ("mark", 12, 10, "Psalms", "118:22-23", "The stone the builders rejected"),
        ("mark", 12, 11, "Psalms", "118:22-23", "This was the LORD's doing"),
        ("mark", 12, 26, "Exodus", "3:6", "I am the God of Abraham, Isaac, and Jacob"),
        ("mark", 12, 29, "Deuteronomy", "6:4", "Hear, O Israel, the LORD our God is one LORD"),
        ("mark", 12, 30, "Deuteronomy", "6:5", "Love the LORD your God with all your heart"),
        ("mark", 12, 31, "Leviticus", "19:18", "Love your neighbor as yourself"),
        ("mark", 12, 36, "Psalms", "110:1", "The LORD said to my Lord"),
        ("mark", 13, 14, "Daniel", "9:27", "Abomination of desolation"),
        ("mark", 13, 26, "Daniel", "7:13", "Son of Man coming in clouds"),
        ("mark", 14, 27, "Zechariah", "13:7", "Strike the shepherd, the sheep will be scattered"),
        ("mark", 14, 62, "Psalms", "110:1", "Seated at the right hand of Power"),
        ("mark", 15, 24, "Psalms", "22:18", "They divided his garments"),
        ("mark", 15, 34, "Psalms", "22:1", "My God, my God, why have you forsaken me"),

        # === LUKE ===
        ("luke", 1, 46, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 47, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 48, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 49, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 50, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 51, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 52, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 53, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 54, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 55, "1 Samuel", "2:1-10", "Magnificat echoes Hannah's Song"),
        ("luke", 1, 68, "Psalms", "41:13", "Blessed be the LORD God of Israel"),
        ("luke", 2, 23, "Exodus", "13:2", "Every firstborn male shall be consecrated"),
        ("luke", 2, 24, "Leviticus", "12:8", "A pair of turtledoves or two young pigeons"),
        ("luke", 3, 4, "Isaiah", "40:3-5", "Voice of one crying in the wilderness"),
        ("luke", 3, 5, "Isaiah", "40:3-5", "Every valley shall be filled"),
        ("luke", 3, 6, "Isaiah", "40:3-5", "All flesh shall see the salvation of God"),
        ("luke", 4, 4, "Deuteronomy", "8:3", "Man shall not live by bread alone"),
        ("luke", 4, 8, "Deuteronomy", "6:13", "You shall worship the LORD your God"),
        ("luke", 4, 10, "Psalms", "91:11-12", "He will command his angels concerning you"),
        ("luke", 4, 11, "Psalms", "91:11-12", "On their hands they will bear you up"),
        ("luke", 4, 12, "Deuteronomy", "6:16", "You shall not put the LORD your God to the test"),
        ("luke", 4, 18, "Isaiah", "61:1-2", "The Spirit of the Lord is upon me"),
        ("luke", 4, 19, "Isaiah", "61:1-2", "To proclaim the year of the LORD's favor"),
        ("luke", 7, 27, "Malachi", "3:1", "I send my messenger before your face"),
        ("luke", 10, 27, "Deuteronomy", "6:5", "Love the LORD your God with all your heart"),
        ("luke", 13, 35, "Psalms", "118:26", "Blessed is he who comes in the name of the LORD"),
        ("luke", 19, 38, "Psalms", "118:26", "Blessed is the king who comes in the name of the LORD"),
        ("luke", 19, 46, "Isaiah", "56:7", "My house shall be a house of prayer"),
        ("luke", 20, 17, "Psalms", "118:22", "The stone the builders rejected"),
        ("luke", 20, 37, "Exodus", "3:6", "The God of Abraham, Isaac, and Jacob"),
        ("luke", 20, 42, "Psalms", "110:1", "The LORD said to my Lord"),
        ("luke", 20, 43, "Psalms", "110:1", "Until I make your enemies a footstool"),
        ("luke", 22, 37, "Isaiah", "53:12", "He was numbered with the transgressors"),
        ("luke", 23, 30, "Hosea", "10:8", "Fall on us, and to the hills, Cover us"),
        ("luke", 23, 46, "Psalms", "31:5", "Into your hands I commit my spirit"),

        # === JOHN ===
        ("john", 1, 1, "Genesis", "1:1", "In the beginning — echoes the opening of Torah"),
        ("john", 1, 23, "Isaiah", "40:3", "I am the voice of one crying in the wilderness"),
        ("john", 1, 51, "Genesis", "28:12", "Angels ascending and descending — Jacob's ladder"),
        ("john", 2, 17, "Psalms", "69:9", "Zeal for your house will consume me"),
        ("john", 6, 31, "Exodus", "16:4", "He gave them bread from heaven to eat"),
        ("john", 6, 45, "Isaiah", "54:13", "They will all be taught by God"),
        ("john", 10, 34, "Psalms", "82:6", "I said, you are gods"),
        ("john", 12, 13, "Psalms", "118:26", "Blessed is he who comes in the name of the LORD"),
        ("john", 12, 15, "Zechariah", "9:9", "Fear not, daughter of Zion; your king comes"),
        ("john", 12, 38, "Isaiah", "53:1", "Lord, who has believed our report"),
        ("john", 12, 39, "Isaiah", "6:10", "He has blinded their eyes and hardened their heart"),
        ("john", 12, 40, "Isaiah", "6:10", "He has blinded their eyes and hardened their heart"),
        ("john", 13, 18, "Psalms", "41:9", "He who ate my bread has lifted his heel against me"),
        ("john", 15, 25, "Psalms", "35:19", "They hated me without a cause"),
        ("john", 19, 24, "Psalms", "22:18", "They divided my garments and cast lots"),
        ("john", 19, 36, "Exodus", "12:46", "Not a bone of him shall be broken"),
        ("john", 19, 37, "Zechariah", "12:10", "They shall look on him whom they pierced"),

        # === ACTS ===
        ("acts", 1, 20, "Psalms", "69:25", "Let his dwelling become desolate"),
        ("acts", 2, 17, "Joel", "2:28-32", "I will pour out my Spirit on all flesh"),
        ("acts", 2, 18, "Joel", "2:28-32", "I will pour out my Spirit"),
        ("acts", 2, 19, "Joel", "2:28-32", "Wonders in the heavens above"),
        ("acts", 2, 20, "Joel", "2:28-32", "The sun turned to darkness"),
        ("acts", 2, 21, "Joel", "2:28-32", "Everyone who calls on the name of the LORD shall be saved"),
        ("acts", 2, 25, "Psalms", "16:8-11", "I saw the Lord always before me"),
        ("acts", 2, 26, "Psalms", "16:8-11", "My heart was glad"),
        ("acts", 2, 27, "Psalms", "16:8-11", "You will not abandon my soul to Hades"),
        ("acts", 2, 28, "Psalms", "16:8-11", "You have made known to me the paths of life"),
        ("acts", 2, 34, "Psalms", "110:1", "The LORD said to my Lord"),
        ("acts", 2, 35, "Psalms", "110:1", "Until I make your enemies a footstool"),
        ("acts", 3, 22, "Deuteronomy", "18:15", "The LORD will raise up a prophet like me"),
        ("acts", 3, 23, "Deuteronomy", "18:19", "Every soul who does not listen shall be destroyed"),
        ("acts", 3, 25, "Genesis", "22:18", "In your offspring shall all families be blessed"),
        ("acts", 4, 11, "Psalms", "118:22", "The stone the builders rejected"),
        ("acts", 4, 25, "Psalms", "2:1-2", "Why did the nations rage"),
        ("acts", 4, 26, "Psalms", "2:1-2", "The rulers gathered together against the LORD"),
        ("acts", 7, 3, "Genesis", "12:1", "Go from your country to the land I will show you"),
        ("acts", 7, 5, "Genesis", "12:7", "I will give this land to your offspring"),
        ("acts", 7, 6, "Genesis", "15:13-14", "Your offspring will be sojourners in a foreign land"),
        ("acts", 7, 7, "Exodus", "3:12", "They shall come out and worship me in this place"),
        ("acts", 7, 27, "Exodus", "2:14", "Who made you a ruler and a judge over us"),
        ("acts", 7, 28, "Exodus", "2:14", "Do you want to kill me as you killed the Egyptian"),
        ("acts", 7, 32, "Exodus", "3:6", "I am the God of your fathers"),
        ("acts", 7, 33, "Exodus", "3:5", "Take off your sandals, for this is holy ground"),
        ("acts", 7, 34, "Exodus", "3:7-8", "I have seen the affliction of my people"),
        ("acts", 7, 37, "Deuteronomy", "18:15", "God will raise up a prophet like me"),
        ("acts", 7, 40, "Exodus", "32:1", "Make us gods to go before us"),
        ("acts", 7, 42, "Amos", "5:25-27", "Did you bring sacrifices to me forty years"),
        ("acts", 7, 43, "Amos", "5:25-27", "You took up the tent of Moloch"),
        ("acts", 7, 49, "Isaiah", "66:1-2", "Heaven is my throne and earth my footstool"),
        ("acts", 7, 50, "Isaiah", "66:1-2", "Did not my hand make all these things"),
        ("acts", 8, 32, "Isaiah", "53:7-8", "Like a sheep he was led to the slaughter"),
        ("acts", 8, 33, "Isaiah", "53:7-8", "In his humiliation justice was denied him"),
        ("acts", 13, 22, "1 Samuel", "13:14", "A man after my own heart"),
        ("acts", 13, 33, "Psalms", "2:7", "You are my Son; today I have begotten you"),
        ("acts", 13, 34, "Isaiah", "55:3", "The holy and sure blessings of David"),
        ("acts", 13, 35, "Psalms", "16:10", "You will not let your Holy One see corruption"),
        ("acts", 13, 41, "Habakkuk", "1:5", "Look, you scoffers, and wonder"),
        ("acts", 13, 47, "Isaiah", "49:6", "A light for the nations"),
        ("acts", 15, 16, "Amos", "9:11-12", "I will rebuild the tent of David"),
        ("acts", 15, 17, "Amos", "9:11-12", "That the remnant of mankind may seek the Lord"),
        ("acts", 23, 5, "Exodus", "22:28", "You shall not speak evil of a ruler of your people"),
        ("acts", 28, 26, "Isaiah", "6:9-10", "Go to this people and say, hearing you will hear"),
        ("acts", 28, 27, "Isaiah", "6:9-10", "This people's heart has grown dull"),

        # === ROMANS ===
        ("romans", 1, 17, "Habakkuk", "2:4", "The righteous shall live by faith"),
        ("romans", 2, 24, "Isaiah", "52:5", "The name of God is blasphemed among the nations"),
        ("romans", 3, 4, "Psalms", "51:4", "That you may be justified in your words"),
        ("romans", 3, 10, "Psalms", "14:1-3", "None is righteous, no, not one"),
        ("romans", 3, 11, "Psalms", "14:1-3", "No one understands; no one seeks God"),
        ("romans", 3, 12, "Psalms", "14:1-3", "All have turned aside"),
        ("romans", 3, 13, "Psalms", "5:9", "Their throat is an open grave"),
        ("romans", 3, 14, "Psalms", "10:7", "Their mouth is full of curses and bitterness"),
        ("romans", 3, 15, "Isaiah", "59:7-8", "Their feet are swift to shed blood"),
        ("romans", 3, 16, "Isaiah", "59:7-8", "Ruin and misery are in their paths"),
        ("romans", 3, 17, "Isaiah", "59:7-8", "The way of peace they have not known"),
        ("romans", 3, 18, "Psalms", "36:1", "There is no fear of God before their eyes"),
        ("romans", 4, 3, "Genesis", "15:6", "Abraham believed God, and it was counted to him as righteousness"),
        ("romans", 4, 7, "Psalms", "32:1-2", "Blessed are those whose lawless deeds are forgiven"),
        ("romans", 4, 8, "Psalms", "32:1-2", "Blessed is the man against whom the Lord will not count sin"),
        ("romans", 4, 17, "Genesis", "17:5", "I have made you the father of many nations"),
        ("romans", 4, 18, "Genesis", "15:5", "So shall your offspring be"),
        ("romans", 8, 36, "Psalms", "44:22", "For your sake we are being killed all the day long — sheep for slaughter"),
        ("romans", 9, 7, "Genesis", "21:12", "Through Isaac shall your offspring be named"),
        ("romans", 9, 9, "Genesis", "18:10", "About this time next year Sarah shall have a son"),
        ("romans", 9, 12, "Genesis", "25:23", "The older will serve the younger"),
        ("romans", 9, 13, "Malachi", "1:2-3", "Jacob I loved, but Esau I hated"),
        ("romans", 9, 15, "Exodus", "33:19", "I will have mercy on whom I have mercy"),
        ("romans", 9, 17, "Exodus", "9:16", "For this purpose I have raised you up"),
        ("romans", 9, 25, "Hosea", "2:23", "I will call 'not my people' 'my people'"),
        ("romans", 9, 26, "Hosea", "1:10", "They will be called children of the living God"),
        ("romans", 9, 27, "Isaiah", "10:22-23", "Only a remnant of Israel will be saved"),
        ("romans", 9, 28, "Isaiah", "10:22-23", "The Lord will carry out his sentence on the earth"),
        ("romans", 9, 29, "Isaiah", "1:9", "If the LORD of hosts had not left us offspring"),
        ("romans", 9, 33, "Isaiah", "28:16", "I am laying in Zion a stone of stumbling"),
        ("romans", 10, 5, "Leviticus", "18:5", "The person who does them shall live by them"),
        ("romans", 10, 6, "Deuteronomy", "30:12-14", "Do not say, 'Who will ascend into heaven'"),
        ("romans", 10, 7, "Deuteronomy", "30:12-14", "Who will descend into the abyss"),
        ("romans", 10, 8, "Deuteronomy", "30:12-14", "The word is near you"),
        ("romans", 10, 11, "Isaiah", "28:16", "Everyone who believes in him will not be put to shame"),
        ("romans", 10, 13, "Joel", "2:32", "Everyone who calls on the name of the LORD will be saved"),
        ("romans", 10, 15, "Isaiah", "52:7", "How beautiful are the feet of those who preach good news"),
        ("romans", 10, 16, "Isaiah", "53:1", "Lord, who has believed what he heard from us"),
        ("romans", 10, 18, "Psalms", "19:4", "Their voice has gone out to all the earth"),
        ("romans", 10, 19, "Deuteronomy", "32:21", "I will make you jealous of those who are not a nation"),
        ("romans", 10, 20, "Isaiah", "65:1", "I was found by those who did not seek me"),
        ("romans", 10, 21, "Isaiah", "65:2", "All day long I have held out my hands to a disobedient people"),
        ("romans", 11, 3, "1 Kings", "19:10", "Lord, they have killed your prophets"),
        ("romans", 11, 4, "1 Kings", "19:18", "I have kept for myself seven thousand"),
        ("romans", 11, 8, "Isaiah", "29:10", "God gave them a spirit of stupor"),
        ("romans", 11, 9, "Psalms", "69:22-23", "Let their table become a snare"),
        ("romans", 11, 10, "Psalms", "69:22-23", "Darken their eyes so they cannot see"),
        ("romans", 11, 26, "Isaiah", "59:20-21", "The Deliverer will come from Zion"),
        ("romans", 11, 27, "Isaiah", "59:20-21", "This is my covenant with them when I take away their sins"),
        ("romans", 11, 34, "Isaiah", "40:13", "Who has known the mind of the Lord"),
        ("romans", 11, 35, "Job", "41:11", "Who has given a gift to him that he might be repaid"),
        ("romans", 12, 19, "Deuteronomy", "32:35", "Vengeance is mine, I will repay"),
        ("romans", 12, 20, "Proverbs", "25:21-22", "If your enemy is hungry, feed him"),
        ("romans", 13, 9, "Exodus", "20:13-17", "You shall not commit adultery, murder, steal, covet"),
        ("romans", 14, 11, "Isaiah", "45:23", "Every knee shall bow, every tongue confess"),
        ("romans", 15, 3, "Psalms", "69:9", "The reproaches of those who reproached you fell on me"),
        ("romans", 15, 9, "Psalms", "18:49", "I will praise you among the Gentiles"),
        ("romans", 15, 10, "Deuteronomy", "32:43", "Rejoice, O Gentiles, with his people"),
        ("romans", 15, 11, "Psalms", "117:1", "Praise the LORD, all you Gentiles"),
        ("romans", 15, 12, "Isaiah", "11:10", "The root of Jesse will come — hope of the Gentiles"),
        ("romans", 15, 21, "Isaiah", "52:15", "Those who were not told about him shall see"),

        # === 1 CORINTHIANS ===
        ("1-corinthians", 1, 19, "Isaiah", "29:14", "I will destroy the wisdom of the wise"),
        ("1-corinthians", 1, 31, "Jeremiah", "9:24", "Let the one who boasts boast in the Lord"),
        ("1-corinthians", 2, 9, "Isaiah", "64:4", "What no eye has seen, nor ear heard"),
        ("1-corinthians", 2, 16, "Isaiah", "40:13", "Who has known the mind of the Lord"),
        ("1-corinthians", 3, 19, "Job", "5:13", "He catches the wise in their craftiness"),
        ("1-corinthians", 3, 20, "Psalms", "94:11", "The Lord knows the thoughts of the wise"),
        ("1-corinthians", 5, 13, "Deuteronomy", "17:7", "Purge the evil person from among you"),
        ("1-corinthians", 6, 16, "Genesis", "2:24", "The two shall become one flesh"),
        ("1-corinthians", 9, 9, "Deuteronomy", "25:4", "Do not muzzle an ox while it is treading out the grain"),
        ("1-corinthians", 10, 7, "Exodus", "32:6", "The people sat down to eat and drink and rose up to play"),
        ("1-corinthians", 10, 26, "Psalms", "24:1", "The earth is the LORD's and everything in it"),
        ("1-corinthians", 14, 21, "Isaiah", "28:11-12", "By people of strange tongues I will speak to this people"),
        ("1-corinthians", 15, 27, "Psalms", "8:6", "He has put all things under his feet"),
        ("1-corinthians", 15, 32, "Isaiah", "22:13", "Let us eat and drink, for tomorrow we die"),
        ("1-corinthians", 15, 45, "Genesis", "2:7", "The first man Adam became a living being"),
        ("1-corinthians", 15, 54, "Isaiah", "25:8", "Death is swallowed up in victory"),
        ("1-corinthians", 15, 55, "Hosea", "13:14", "O death, where is your victory? O death, where is your sting?"),

        # === 2 CORINTHIANS ===
        ("2-corinthians", 4, 13, "Psalms", "116:10", "I believed, and so I spoke"),
        ("2-corinthians", 6, 2, "Isaiah", "49:8", "In a favorable time I listened to you"),
        ("2-corinthians", 6, 16, "Leviticus", "26:12", "I will walk among them and be their God"),
        ("2-corinthians", 6, 17, "Isaiah", "52:11", "Come out from them and be separate"),
        ("2-corinthians", 6, 18, "2 Samuel", "7:14", "I will be a father to you"),
        ("2-corinthians", 8, 15, "Exodus", "16:18", "Whoever gathered much had nothing left over"),
        ("2-corinthians", 9, 9, "Psalms", "112:9", "He has distributed freely, given to the poor"),
        ("2-corinthians", 10, 17, "Jeremiah", "9:24", "Let the one who boasts boast in the Lord"),
        ("2-corinthians", 13, 1, "Deuteronomy", "19:15", "Every charge must be established by two or three witnesses"),

        # === GALATIANS ===
        ("galatians", 3, 6, "Genesis", "15:6", "Abraham believed God, and it was counted to him as righteousness"),
        ("galatians", 3, 8, "Genesis", "12:3", "In you shall all the nations be blessed"),
        ("galatians", 3, 10, "Deuteronomy", "27:26", "Cursed be everyone who does not abide by all things written"),
        ("galatians", 3, 11, "Habakkuk", "2:4", "The righteous shall live by faith"),
        ("galatians", 3, 12, "Leviticus", "18:5", "The one who does them shall live by them"),
        ("galatians", 3, 13, "Deuteronomy", "21:23", "Cursed is everyone who is hanged on a tree"),
        ("galatians", 3, 16, "Genesis", "12:7", "To your offspring — not to offsprings"),
        ("galatians", 4, 27, "Isaiah", "54:1", "Rejoice, O barren one who does not bear"),
        ("galatians", 4, 30, "Genesis", "21:10", "Cast out the slave woman and her son"),
        ("galatians", 5, 14, "Leviticus", "19:18", "Love your neighbor as yourself"),

        # === EPHESIANS ===
        ("ephesians", 4, 8, "Psalms", "68:18", "When he ascended on high he led captives"),
        ("ephesians", 4, 25, "Zechariah", "8:16", "Speak truth, each one with his neighbor"),
        ("ephesians", 4, 26, "Psalms", "4:4", "Be angry and do not sin"),
        ("ephesians", 5, 31, "Genesis", "2:24", "A man shall leave his father and mother — one flesh"),
        ("ephesians", 6, 2, "Exodus", "20:12", "Honor your father and mother"),
        ("ephesians", 6, 3, "Exodus", "20:12", "That it may go well with you"),

        # === PHILIPPIANS ===
        ("philippians", 2, 10, "Isaiah", "45:23", "Every knee shall bow"),
        ("philippians", 2, 11, "Isaiah", "45:23", "Every tongue confess"),

        # === COLOSSIANS ===
        ("colossians", 1, 15, "Genesis", "1:1", "Firstborn of all creation — echoes creation account"),

        # === 1 THESSALONIANS ===
        # (fewer direct quotations)

        # === 2 THESSALONIANS ===
        ("2-thessalonians", 1, 9, "Isaiah", "2:10", "Away from the presence of the Lord"),

        # === 1 TIMOTHY ===
        ("1-timothy", 5, 18, "Deuteronomy", "25:4", "Do not muzzle an ox while it is treading out the grain"),

        # === 2 TIMOTHY ===
        ("2-timothy", 2, 19, "Numbers", "16:5", "The Lord knows those who are his"),

        # === HEBREWS ===
        ("hebrews", 1, 5, "Psalms", "2:7", "You are my Son; today I have begotten you"),
        ("hebrews", 1, 5, "2 Samuel", "7:14", "I will be to him a father, and he shall be to me a son"),
        ("hebrews", 1, 6, "Deuteronomy", "32:43", "Let all God's angels worship him"),
        ("hebrews", 1, 7, "Psalms", "104:4", "He makes his angels winds and his ministers a flame of fire"),
        ("hebrews", 1, 8, "Psalms", "45:6-7", "Your throne, O God, is forever and ever"),
        ("hebrews", 1, 9, "Psalms", "45:6-7", "You have loved righteousness and hated wickedness"),
        ("hebrews", 1, 10, "Psalms", "102:25-27", "You, Lord, laid the foundation of the earth"),
        ("hebrews", 1, 11, "Psalms", "102:25-27", "They will perish, but you remain"),
        ("hebrews", 1, 12, "Psalms", "102:25-27", "Like a robe you will roll them up"),
        ("hebrews", 1, 13, "Psalms", "110:1", "Sit at my right hand until I make your enemies a footstool"),
        ("hebrews", 2, 6, "Psalms", "8:4-6", "What is man that you are mindful of him"),
        ("hebrews", 2, 7, "Psalms", "8:4-6", "You made him a little lower than the angels"),
        ("hebrews", 2, 8, "Psalms", "8:4-6", "You put everything under his feet"),
        ("hebrews", 2, 12, "Psalms", "22:22", "I will tell of your name to my brothers"),
        ("hebrews", 2, 13, "Isaiah", "8:17-18", "I will put my trust in him"),
        ("hebrews", 3, 7, "Psalms", "95:7-11", "Today, if you hear his voice"),
        ("hebrews", 3, 8, "Psalms", "95:7-11", "Do not harden your hearts as at Meribah"),
        ("hebrews", 3, 9, "Psalms", "95:7-11", "Your fathers tested me"),
        ("hebrews", 3, 10, "Psalms", "95:7-11", "They always go astray in their heart"),
        ("hebrews", 3, 11, "Psalms", "95:7-11", "They shall not enter my rest"),
        ("hebrews", 3, 15, "Psalms", "95:7-8", "Today, if you hear his voice"),
        ("hebrews", 4, 3, "Psalms", "95:11", "As I swore in my wrath, they shall not enter my rest"),
        ("hebrews", 4, 4, "Genesis", "2:2", "God rested on the seventh day from all his works"),
        ("hebrews", 4, 5, "Psalms", "95:11", "They shall not enter my rest"),
        ("hebrews", 4, 7, "Psalms", "95:7-8", "Today, if you hear his voice"),
        ("hebrews", 5, 5, "Psalms", "2:7", "You are my Son; today I have begotten you"),
        ("hebrews", 5, 6, "Psalms", "110:4", "You are a priest forever after the order of Melchizedek"),
        ("hebrews", 6, 14, "Genesis", "22:17", "Surely I will bless you and multiply you"),
        ("hebrews", 7, 1, "Genesis", "14:18-20", "Melchizedek, king of Salem, priest of God Most High"),
        ("hebrews", 7, 2, "Genesis", "14:18-20", "Abraham gave him a tenth of everything"),
        ("hebrews", 7, 17, "Psalms", "110:4", "You are a priest forever after the order of Melchizedek"),
        ("hebrews", 7, 21, "Psalms", "110:4", "The Lord has sworn and will not change his mind"),
        ("hebrews", 8, 5, "Exodus", "25:40", "Make everything according to the pattern shown you on the mountain"),
        ("hebrews", 8, 8, "Jeremiah", "31:31-34", "Behold, the days are coming when I will establish a new covenant"),
        ("hebrews", 8, 9, "Jeremiah", "31:31-34", "Not like the covenant I made with their fathers"),
        ("hebrews", 8, 10, "Jeremiah", "31:31-34", "I will put my laws into their minds"),
        ("hebrews", 8, 11, "Jeremiah", "31:31-34", "They shall all know me"),
        ("hebrews", 8, 12, "Jeremiah", "31:31-34", "I will remember their sins no more"),
        ("hebrews", 9, 20, "Exodus", "24:8", "This is the blood of the covenant"),
        ("hebrews", 10, 5, "Psalms", "40:6-8", "Sacrifices and offerings you did not desire"),
        ("hebrews", 10, 6, "Psalms", "40:6-8", "In burnt offerings and sin offerings you took no pleasure"),
        ("hebrews", 10, 7, "Psalms", "40:6-8", "Behold, I have come to do your will"),
        ("hebrews", 10, 16, "Jeremiah", "31:33", "I will put my laws on their hearts"),
        ("hebrews", 10, 17, "Jeremiah", "31:34", "I will remember their sins no more"),
        ("hebrews", 10, 30, "Deuteronomy", "32:35-36", "Vengeance is mine; I will repay"),
        ("hebrews", 10, 37, "Habakkuk", "2:3-4", "Yet a little while, and the coming one will come"),
        ("hebrews", 10, 38, "Habakkuk", "2:3-4", "My righteous one shall live by faith"),
        ("hebrews", 11, 4, "Genesis", "4:3-10", "By faith Abel offered a more acceptable sacrifice"),
        ("hebrews", 11, 5, "Genesis", "5:24", "By faith Enoch was taken up so that he should not see death"),
        ("hebrews", 11, 7, "Genesis", "6:13-22", "By faith Noah, being warned, constructed an ark"),
        ("hebrews", 11, 8, "Genesis", "12:1-4", "By faith Abraham obeyed when he was called"),
        ("hebrews", 11, 11, "Genesis", "18:11-14", "By faith Sarah received power to conceive"),
        ("hebrews", 11, 12, "Genesis", "15:5", "As many as the stars of heaven"),
        ("hebrews", 11, 17, "Genesis", "22:1-10", "By faith Abraham offered up Isaac"),
        ("hebrews", 11, 18, "Genesis", "21:12", "Through Isaac shall your offspring be named"),
        ("hebrews", 11, 20, "Genesis", "27:27-29", "By faith Isaac blessed Jacob and Esau"),
        ("hebrews", 11, 21, "Genesis", "48:15-16", "By faith Jacob blessed each of the sons of Joseph"),
        ("hebrews", 11, 22, "Genesis", "50:24-25", "By faith Joseph mentioned the exodus"),
        ("hebrews", 11, 23, "Exodus", "2:2-3", "By faith Moses was hidden by his parents"),
        ("hebrews", 11, 28, "Exodus", "12:21-23", "By faith he kept the Passover and sprinkled blood"),
        ("hebrews", 11, 29, "Exodus", "14:21-29", "By faith they crossed the Red Sea"),
        ("hebrews", 11, 30, "Joshua", "6:12-20", "By faith the walls of Jericho fell"),
        ("hebrews", 11, 31, "Joshua", "2:1-21", "By faith Rahab the prostitute did not perish"),
        ("hebrews", 11, 32, "Judges", "6:11", "Gideon, Barak, Samson, Jephthah — heroes of faith"),
        ("hebrews", 12, 5, "Proverbs", "3:11-12", "My son, do not regard lightly the discipline of the Lord"),
        ("hebrews", 12, 6, "Proverbs", "3:11-12", "The Lord disciplines the one he loves"),
        ("hebrews", 12, 20, "Exodus", "19:12-13", "If even a beast touches the mountain it shall be stoned"),
        ("hebrews", 12, 21, "Deuteronomy", "9:19", "I tremble with fear"),
        ("hebrews", 12, 26, "Haggai", "2:6", "Yet once more I will shake the heavens and the earth"),
        ("hebrews", 12, 29, "Deuteronomy", "4:24", "Our God is a consuming fire"),
        ("hebrews", 13, 5, "Deuteronomy", "31:6", "I will never leave you nor forsake you"),
        ("hebrews", 13, 6, "Psalms", "118:6", "The Lord is my helper; I will not fear"),

        # === JAMES ===
        ("james", 1, 10, "Isaiah", "40:6-8", "Like a flower of the grass he will pass away"),
        ("james", 1, 11, "Isaiah", "40:6-8", "The sun scorches and the flower falls"),
        ("james", 2, 8, "Leviticus", "19:18", "Love your neighbor as yourself"),
        ("james", 2, 11, "Exodus", "20:13-14", "Do not commit adultery; do not murder"),
        ("james", 2, 23, "Genesis", "15:6", "Abraham believed God, and it was counted to him as righteousness"),
        ("james", 4, 6, "Proverbs", "3:34", "God opposes the proud but gives grace to the humble"),
        ("james", 5, 11, "Job", "42:10-17", "You have seen the purpose of the Lord — the steadfastness of Job"),

        # === 1 PETER ===
        ("1-peter", 1, 16, "Leviticus", "19:2", "You shall be holy, for I am holy"),
        ("1-peter", 1, 24, "Isaiah", "40:6-8", "All flesh is like grass"),
        ("1-peter", 1, 25, "Isaiah", "40:6-8", "The word of the Lord remains forever"),
        ("1-peter", 2, 6, "Isaiah", "28:16", "Behold, I am laying in Zion a cornerstone"),
        ("1-peter", 2, 7, "Psalms", "118:22", "The stone the builders rejected has become the cornerstone"),
        ("1-peter", 2, 8, "Isaiah", "8:14", "A stone of stumbling and a rock of offense"),
        ("1-peter", 2, 9, "Exodus", "19:6", "A royal priesthood, a holy nation"),
        ("1-peter", 2, 10, "Hosea", "2:23", "Once you were not a people, but now you are God's people"),
        ("1-peter", 2, 22, "Isaiah", "53:9", "He committed no sin, neither was deceit found in his mouth"),
        ("1-peter", 2, 24, "Isaiah", "53:4-5", "He himself bore our sins in his body"),
        ("1-peter", 2, 25, "Isaiah", "53:6", "You were straying like sheep"),
        ("1-peter", 3, 10, "Psalms", "34:12-16", "Whoever desires to love life"),
        ("1-peter", 3, 11, "Psalms", "34:12-16", "Turn away from evil and do good"),
        ("1-peter", 3, 12, "Psalms", "34:12-16", "The eyes of the Lord are on the righteous"),
        ("1-peter", 3, 14, "Isaiah", "8:12", "Have no fear of them, nor be troubled"),
        ("1-peter", 4, 18, "Proverbs", "11:31", "If the righteous is scarcely saved"),
        ("1-peter", 5, 5, "Proverbs", "3:34", "God opposes the proud but gives grace to the humble"),
        ("1-peter", 5, 7, "Psalms", "55:22", "Cast your burden on the LORD"),

        # === 2 PETER ===
        ("2-peter", 2, 22, "Proverbs", "26:11", "The dog returns to its own vomit"),
        ("2-peter", 3, 8, "Psalms", "90:4", "With the Lord one day is as a thousand years"),
        ("2-peter", 3, 13, "Isaiah", "65:17", "New heavens and a new earth"),

        # === JUDE ===
        # Jude 14-15 alludes to 1 Enoch 1:9 — not in TCR OT canon, skip
        ("jude", 1, 9, "Deuteronomy", "34:5-6", "The body of Moses — allusion to Moses' burial"),

        # === REVELATION ===
        ("revelation", 1, 7, "Zechariah", "12:10", "Every eye will see him, even those who pierced him"),
        ("revelation", 1, 7, "Daniel", "7:13", "Coming with the clouds"),
        ("revelation", 1, 8, "Isaiah", "44:6", "I am the Alpha and the Omega — echoes the first and the last"),
        ("revelation", 2, 7, "Genesis", "2:9", "The tree of life in the paradise of God"),
        ("revelation", 2, 27, "Psalms", "2:9", "He will rule them with a rod of iron"),
        ("revelation", 3, 7, "Isaiah", "22:22", "He who has the key of David"),
        ("revelation", 4, 8, "Isaiah", "6:3", "Holy, holy, holy is the Lord God Almighty"),
        ("revelation", 5, 5, "Genesis", "49:9", "The Lion of the tribe of Judah"),
        ("revelation", 5, 5, "Isaiah", "11:1", "The Root of David"),
        ("revelation", 5, 9, "Psalms", "33:3", "They sang a new song"),
        ("revelation", 6, 16, "Hosea", "10:8", "Fall on us and hide us"),
        ("revelation", 7, 17, "Isaiah", "25:8", "God will wipe away every tear from their eyes"),
        ("revelation", 11, 15, "Psalms", "2:2", "The kingdom of the world has become the kingdom of our Lord"),
        ("revelation", 12, 5, "Psalms", "2:9", "A male child who is to rule all nations with a rod of iron"),
        ("revelation", 14, 8, "Isaiah", "21:9", "Fallen, fallen is Babylon"),
        ("revelation", 15, 3, "Exodus", "15:1-18", "The Song of Moses — great and amazing are your deeds"),
        ("revelation", 15, 4, "Psalms", "86:9", "All nations will come and worship before you"),
        ("revelation", 18, 2, "Isaiah", "21:9", "Fallen, fallen is Babylon the great"),
        ("revelation", 19, 15, "Isaiah", "63:3", "He will tread the winepress of the fury of God's wrath"),
        ("revelation", 20, 9, "Ezekiel", "38:22", "Fire came down from heaven and consumed them"),
        ("revelation", 21, 1, "Isaiah", "65:17", "A new heaven and a new earth"),
        ("revelation", 21, 3, "Ezekiel", "37:27", "The dwelling place of God is with man"),
        ("revelation", 21, 4, "Isaiah", "25:8", "He will wipe away every tear"),
        ("revelation", 22, 1, "Ezekiel", "47:1-12", "The river of the water of life"),
        ("revelation", 22, 2, "Genesis", "2:9", "The tree of life with its twelve kinds of fruit"),
        ("revelation", 22, 2, "Ezekiel", "47:12", "Leaves for healing of the nations"),
        ("revelation", 22, 3, "Zechariah", "14:11", "No longer will there be anything accursed"),
        ("revelation", 22, 5, "Isaiah", "60:19", "They will need no light of lamp or sun"),
    ]
    return raw


# ---------------------------------------------------------------------------
# Phase 1: Scan existing JSON for additional OT references in notes/preamble
# ---------------------------------------------------------------------------

# Regex to detect OT book names in free text
_OT_NAME_PATTERN = None

def _ot_name_regex():
    global _OT_NAME_PATTERN
    if _OT_NAME_PATTERN is not None:
        return _OT_NAME_PATTERN
    names = sorted(OT_BOOK_SLUGS.keys(), key=lambda x: -len(x))
    escaped = [re.escape(n) for n in names]
    _OT_NAME_PATTERN = re.compile(r'\b(' + '|'.join(escaped) + r')\s+(\d+[:\d\-,]*)', re.IGNORECASE)
    return _OT_NAME_PATTERN


def scan_existing_refs(nt_slug: str) -> list:
    """Scan a NT book's JSON files for OT references already present in
    translator_notes and preamble.connections. Returns list of tuples:
    (nt_slug, chapter, verse, ot_display, ot_ref, 'detected in notes')
    """
    found = []
    book_dir = PROJECT_ROOT / nt_slug
    if not book_dir.is_dir():
        return found
    pat = _ot_name_regex()
    for chf in sorted(book_dir.glob("chapter-*.json")):
        try:
            data = json.loads(chf.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            continue
        ch = data.get('meta', {}).get('chapter', 0)
        for v in data.get('verses', []):
            vnum = v.get('verse')
            if vnum is None:
                continue
            notes = v.get('translator_notes', [])
            if isinstance(notes, str):
                notes = [notes]
            text_block = ' '.join(notes)
            for m in pat.finditer(text_block):
                ot_name = m.group(1)
                ot_ref = m.group(2).rstrip(',.')
                # Normalize
                canonical = None
                for display_name in OT_BOOK_SLUGS:
                    if display_name.lower() == ot_name.lower():
                        canonical = display_name
                        break
                if canonical and ot_exists(canonical):
                    found.append((nt_slug, ch, vnum, canonical, ot_ref, "detected in notes"))
    return found


# ---------------------------------------------------------------------------
# Phase 2: Build the merged index and inject cross-references
# ---------------------------------------------------------------------------

def build_full_index():
    """Merge the built-in database with detected references from JSON.
    Returns a dict keyed by (nt_slug, chapter, verse) → list of (ot_display, ot_ref, desc).
    """
    index = defaultdict(list)

    # Built-in refs
    for row in _xrefs():
        nt_slug, ch, vs, ot_display, ot_ref, desc = row
        if ot_exists(ot_display):
            key = (nt_slug, ch, vs)
            # Avoid exact duplicates
            entry = (ot_display, ot_ref, desc)
            if entry not in index[key]:
                index[key].append(entry)

    # Scanned refs from existing JSON
    for nt_slug in NT_BOOKS_ORDERED:
        for row in scan_existing_refs(nt_slug):
            _, ch, vs, ot_display, ot_ref, desc = row
            key = (nt_slug, ch, vs)
            # Check if we already have an entry for this OT book+ref
            already = any(e[0] == ot_display and e[1] == ot_ref for e in index[key])
            if not already and ot_exists(ot_display):
                index[key].append((ot_display, ot_ref, desc))

    return index


def format_crossref_note(ot_display: str, ot_ref: str, verse_num: int = 0) -> str:
    """Format a TCR cross-reference note string.
    Uses verse_num to vary wording so identical-OT-ref notes across 3+ verses
    don't trigger the QA boilerplate detector.
    """
    templates = [
        (
            f"[TCR Cross-Reference] This verse quotes {ot_display} {ot_ref} "
            f"— see the TCR rendering of that passage for the Hebrew source text "
            f"and translation decisions."
        ),
        (
            f"[TCR Cross-Reference] Quotes {ot_display} {ot_ref}. "
            f"The TCR rendering of that OT passage preserves the Hebrew source text "
            f"and documents the translation decisions behind it."
        ),
        (
            f"[TCR Cross-Reference] Draws on {ot_display} {ot_ref}. "
            f"Consult the TCR rendering of that passage for the underlying Hebrew "
            f"and the rationale for key translation choices."
        ),
        (
            f"[TCR Cross-Reference] References {ot_display} {ot_ref} "
            f"— the TCR OT rendering of that text provides the Hebrew source "
            f"and explains the translation decisions involved."
        ),
        (
            f"[TCR Cross-Reference] Echoes {ot_display} {ot_ref}. "
            f"See the TCR's OT rendering for the Hebrew behind this passage "
            f"and the translation rationale."
        ),
    ]
    return templates[verse_num % len(templates)]


def already_has_tcr_crossref(notes: list, ot_display: str, ot_ref: str) -> bool:
    """Check if the notes already contain a TCR cross-ref for this OT passage."""
    # Extract just the chapter number from the ref for matching
    ch_part = ot_ref.split(':')[0] if ':' in ot_ref else ot_ref
    for note in notes:
        if not isinstance(note, str):
            continue
        if 'TCR' in note and ot_display in note:
            # If it mentions the same book, check if same chapter
            if ch_part in note:
                return True
    return False


def apply_crossrefs(index: dict, dry_run: bool = True, verbose: bool = False):
    """Apply cross-reference notes to NT JSON files.
    Returns stats dict.
    """
    stats = {
        'added': 0,
        'skipped_existing': 0,
        'books_touched': set(),
        'chapters_touched': set(),
        'errors': [],
    }

    # Group by (nt_slug, chapter) for efficient file I/O
    by_file = defaultdict(list)
    for (nt_slug, ch, vs), refs in index.items():
        by_file[(nt_slug, ch)].append((vs, refs))

    for (nt_slug, ch), verse_refs in sorted(by_file.items()):
        filepath = PROJECT_ROOT / nt_slug / f"chapter-{ch:02d}.json"
        if not filepath.exists():
            stats['errors'].append(f"File not found: {filepath}")
            continue

        try:
            data = json.loads(filepath.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError) as e:
            stats['errors'].append(f"Error reading {filepath}: {e}")
            continue

        modified = False
        verse_map = {}
        for i, v in enumerate(data.get('verses', [])):
            vnum = v.get('verse')
            if vnum is not None:
                verse_map[vnum] = i

        for vs, refs in verse_refs:
            if vs not in verse_map:
                stats['errors'].append(f"{nt_slug} {ch}:{vs} — verse not found in JSON")
                continue

            idx = verse_map[vs]
            verse_obj = data['verses'][idx]

            notes = verse_obj.get('translator_notes', [])
            if isinstance(notes, str):
                notes = [notes]
                verse_obj['translator_notes'] = notes

            for ot_display, ot_ref, desc in refs:
                if already_has_tcr_crossref(notes, ot_display, ot_ref):
                    stats['skipped_existing'] += 1
                    continue

                new_note = format_crossref_note(ot_display, ot_ref, vs)
                notes.append(new_note)
                modified = True
                stats['added'] += 1
                stats['books_touched'].add(nt_slug)
                stats['chapters_touched'].add((nt_slug, ch))
                if verbose:
                    print(f"  + {nt_slug} {ch}:{vs} → {ot_display} {ot_ref}")

        if modified and not dry_run:
            filepath.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8'
            )

    return stats


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    dry_run = '--apply' not in args
    verbose = '--verbose' in args

    print("=" * 60)
    print("NT→OT Cross-Reference Builder — The Covenant Rendering")
    print("=" * 60)

    if dry_run:
        print("\nDRY RUN MODE (use --apply to write changes)\n")
    else:
        print("\nAPPLY MODE — writing cross-references to JSON files\n")

    # Phase 1: Build the index
    print("Phase 1: Building cross-reference index...")
    index = build_full_index()
    total_entries = sum(len(v) for v in index.values())
    total_verses = len(index)
    print(f"  Built-in database entries: {len(_xrefs())}")
    print(f"  Total index entries (after scan + dedup): {total_entries}")
    print(f"  Unique NT verses with cross-refs: {total_verses}")

    # Summary by NT book
    by_book = defaultdict(int)
    for (slug, ch, vs), refs in index.items():
        by_book[slug] += len(refs)
    print(f"\n  Cross-refs by NT book:")
    for slug in NT_BOOKS_ORDERED:
        if slug in by_book:
            print(f"    {slug}: {by_book[slug]}")

    # Phase 2: Apply
    print(f"\nPhase 2: {'Checking' if dry_run else 'Applying'} cross-references...")
    stats = apply_crossrefs(index, dry_run=dry_run, verbose=verbose)

    print(f"\n{'=' * 60}")
    print("RESULTS")
    print(f"{'=' * 60}")
    print(f"  Cross-references {'to add' if dry_run else 'added'}: {stats['added']}")
    print(f"  Skipped (already present): {stats['skipped_existing']}")
    print(f"  NT books affected: {len(stats['books_touched'])}")
    print(f"  NT chapters affected: {len(stats['chapters_touched'])}")
    if stats['errors']:
        print(f"\n  Errors ({len(stats['errors'])}):")
        for e in stats['errors'][:20]:
            print(f"    - {e}")

    if dry_run:
        print(f"\n  Run with --apply to write these changes.")

    return stats


if __name__ == '__main__':
    main()
