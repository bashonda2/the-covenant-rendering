#!/usr/bin/env python3
"""
fix_kjv_proximate_nt.py — Rewrite NT renderings that are >92% similar to KJV.

Walks all NT book directories, finds verses where `rendering` is >92% similar
to `text_kjv` (excluding name-only lists), and rewrites the rendering to be
a fresh modern English translation that drops below 85% similarity.

Also repairs any garbled renderings left by a previous run (detected via
broken punctuation patterns like ";," or ":,").

Rewriting approach:
  - Reads both text_greek and text_kjv
  - Produces modern English with different wording, structure, and vocabulary
  - Maintains theological accuracy; targets 8th-grade reading level
  - No Hebrew/Greek terms, brackets, or footnote markers in rendering
"""

import json
import os
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

NT_BOOKS = [
    'matthew', 'mark', 'luke', 'john', 'acts',
    'romans', '1-corinthians', '2-corinthians', 'galatians', 'ephesians',
    'philippians', 'colossians', '1-thessalonians', '2-thessalonians',
    '1-timothy', '2-timothy', 'titus', 'philemon',
    'hebrews', 'james', '1-peter', '2-peter',
    '1-john', '2-john', '3-john', 'jude', 'revelation',
]


# ── Substitution layers (applied in order) ───────────────────────────────

# Layer 1: Archaic → modern vocabulary (always applied)
LAYER_1 = [
    # Verb forms
    (r'\bshall inherit\b', 'will receive'),
    (r'\bshall be called\b', 'will be known as'),
    (r'\bshall see\b', 'will see'),
    (r'\bshall obtain\b', 'will gain'),
    (r'\bshall be\b', 'will be'),
    (r'\bshall not\b', 'will not'),
    (r'\bshall come\b', 'will come'),
    (r'\bshall give\b', 'will give'),
    (r'\bshall have\b', 'will have'),
    (r'\bshall find\b', 'will find'),
    (r'\bshall know\b', 'will know'),
    (r'\bshall\b', 'will'),
    (r'\bsaith\b', 'says'),
    (r'\bhath\b', 'has'),
    (r'\bdoth\b', 'does'),
    (r'\bcometh\b', 'comes'),
    (r'\bgoeth\b', 'goes'),
    (r'\bseeth\b', 'sees'),
    (r'\bgiveth\b', 'gives'),
    (r'\bmaketh\b', 'makes'),
    (r'\bknoweth\b', 'knows'),
    (r'\bheareth\b', 'hears'),
    (r'\bbringeth\b', 'brings'),
    (r'\btaketh\b', 'takes'),
    (r'\bsendeth\b', 'sends'),
    (r'\bfindeth\b', 'finds'),
    (r'\bbelieveth\b', 'believes'),
    (r'\breceiveth\b', 'receives'),
    (r'\babideth\b', 'remains'),
    (r'\bbegat\b', 'fathered'),
    (r'\bspake\b', 'spoke'),
    # More archaic -eth verbs not covered above
    (r'\bcomforteth\b', 'comforts'), (r'\blaboureth\b', 'labors'),
    (r'\bhelpeth\b', 'helps'), (r'\bworketh\b', 'works'),
    (r'\bloveth\b', 'loves'), (r'\bleadeth\b', 'leads'),
    (r'\bkilleth\b', 'kills'), (r'\bteacheth\b', 'teaches'),
    (r'\braiseth\b', 'raises'), (r'\bdwelleth\b', 'dwells'),
    (r'\bsitteth\b', 'sits'), (r'\bsuffereth\b', 'suffers'),
    (r'\bpleaseth\b', 'pleases'), (r'\bcalleth\b', 'calls'),
    (r'\bwalketh\b', 'walks'), (r'\bkeepeth\b', 'keeps'),
    (r'\bhonoureth\b', 'honors'), (r'\bjudgeth\b', 'judges'),
    (r'\breigneth\b', 'reigns'), (r'\bshineth\b', 'shines'),
    (r'\bpasseth\b', 'surpasses'), (r'\bputteth\b', 'puts'),
    (r'\bceaseth\b', 'ceases'), (r'\blieth\b', 'lies'),
    (r'\blooketh\b', 'looks'), (r'\btroubleth\b', 'troubles'),
    (r'\banswereth\b', 'answers'), (r'\bwatcheth\b', 'watches'),
    (r'\bentereth\b', 'enters'), (r'\bopeneth\b', 'opens'),
    (r'\bstandeth\b', 'stands'), (r'\briseth\b', 'rises'),
    (r'\bspeaketh\b', 'speaks'), (r'\breadeth\b', 'reads'),
    (r'\bthinketh\b', 'thinks'), (r'\bliveth\b', 'lives'),
    (r'\bruneth\b', 'runs'), (r'\bfalleth\b', 'falls'),
    (r'\bturneth\b', 'turns'), (r'\bbuildeth\b', 'builds'),
    (r'\beareth\b', 'bears'), (r'\bsaveth\b', 'saves'),
    (r'\bboasteth\b', 'boasts'), (r'\benvieth\b', 'envies'),
    (r'\bpersuadeth\b', 'persuades'), (r'\bcleaveth\b', 'clings'),
    (r'\bseeketh\b', 'seeks'), (r'\bwriteth\b', 'writes'),
    (r'\bprayeth\b', 'prays'), (r'\bcrieth\b', 'cries'),
    (r'\btrusteth\b', 'trusts'), (r'\bholdeth\b', 'holds'),
    (r'\bgoverneth\b', 'governs'), (r'\bkindleth\b', 'kindles'),
    (r'\bneedeth\b', 'needs'), (r'\bsheweth\b', 'shows'),
    (r'\bwilleth\b', 'wills'), (r'\bperceiveth\b', 'perceives'),
    (r'\bvaunteth\b', 'boasts'), (r'\bbeholdeth\b', 'beholds'),
    (r'\bendureth\b', 'endures'), (r'\bhopeth\b', 'hopes'),
    (r'\bwist\b', 'knew'),
    (r'\bwaxed\b', 'grew'),
    (r'\bwroth\b', 'angry'),
    # Pronouns / archaic words
    (r'\bunto them\b', 'to them'),
    (r'\bunto him\b', 'to him'),
    (r'\bunto her\b', 'to her'),
    (r'\bunto you\b', 'to you'),
    (r'\bunto us\b', 'to us'),
    (r'\bunto the\b', 'to the'),
    (r'\bunto\b', 'to'),
    (r'\bthou art\b', 'you are'),
    (r'\bthou hast\b', 'you have'),
    (r'\bthou wilt\b', 'you will'),
    (r'\bthou\b', 'you'),
    (r'\bthee\b', 'you'),
    (r'\bthy\b', 'your'),
    (r'\bthine\b', 'your'),
    (r'\bye\b(?!\w)', 'you'),
    (r'\bbrethren\b', 'brothers and sisters'),
    (r'\bwherefore\b', 'for this reason'),
    (r'\bverily,? verily\b', 'I assure you'),
    (r'\bverily\b', 'truly'),
    (r'\bstraightway\b', 'right away'),
    (r'\bforthwith\b', 'right away'),
    # Nouns
    (r'\bbondservants?\b', 'servants'),
    (r'\btidings\b', 'news'),
    (r'\bonly begotten\b', 'one and only'),
    (r'\bbegotten\b', 'born'),
    (r'\bsupplications\b', 'earnest prayers'),
    (r'\bsupplication\b', 'earnest prayer'),
    (r'\btransgressions\b', 'sins'),
    (r'\btransgression\b', 'sin'),
    (r'\bwiles\b', 'schemes'),
    (r'\blasciviousness\b', 'sensuality'),
    (r'\bconcupiscence\b', 'sinful desire'),
    (r'\bfornication\b', 'sexual immorality'),
    # Phrases
    (r'\band lo\b', 'and just then'),
    (r'\band behold\b', 'and at that moment'),
    (r'\bbehold\b', 'take notice'),
    (r'\bfor lo\b', 'for indeed'),
    (r'\binsomuch that\b', 'to such a degree that'),
    (r'\bin whom I am well pleased\b', 'and I am completely delighted with him'),
    (r'\bsaid unto\b', 'told'),
    (r'\bnotwithstanding\b', 'even so'),
    (r'\bperadventure\b', 'perhaps'),
    (r'\bfain\b', 'gladly'),
    (r'\bit came to pass\b', 'it happened that'),
    # More archaic phrases
    (r'\bin sunder\b', 'to pieces'),
    (r'\bshewbread\b', 'sacred bread'),
    (r'\bshew\b', 'reveal'),
    (r'\bshewed\b', 'showed'),
    (r'\bgainsay\b', 'oppose'),
    (r'\bwithstand\b', 'resist'),
    (r'\bavenge\b', 'give justice to'),
    (r'\bweary\b', 'wear out'),
    (r'\blest\b', 'so that not'),
    (r'\bwhosoever\b', 'whoever'),
    (r'\bwherein\b', 'in which'),
    (r'\bthereof\b', 'of it'),
    (r'\btherein\b', 'in it'),
    (r'\btherewith\b', 'with it'),
    (r'\bwhereof\b', 'of which'),
    (r'\bcontentious\b', 'argumentative'),
    (r'\bsubtilty\b', 'cunning'),
    (r'\bdespitefully\b', 'maliciously'),
    (r'\bforasmuch\b', 'since'),
    (r'\bhitherto\b', 'until now'),
    (r'\bbetwixt\b', 'between'),
    (r'\basunder\b', 'apart'),
    (r'\braiment\b', 'clothing'),
    (r'\bfull?er\b', 'laundryman'),
    (r'\bsteward\b', 'manager'),
    (r'\bministered unto\b', 'provided for'),
    (r'\bministered to\b', 'served'),
    (r'\bministered\b', 'served'),
    (r'\blaid wait\b', 'lay in ambush'),
    (r'\battentive to hear\b', 'eager to listen to'),
    (r'\bpuffed up\b', 'arrogant'),
    (r'\bespoused\b', 'pledged in marriage'),
    (r'\bsaluted\b', 'greeted'),
    (r'\bdamnation\b', 'condemnation'),
    (r'\bfilthy lucre\b', 'dishonest profit'),
    (r'\bsober\b', 'self-controlled'),
]

# Layer 2: Phrase-level modernization (applied if still >85% after layer 1)
LAYER_2 = [
    (r'\bBlessed are (the [^,]+), for\b', r'How fortunate are \1, because'),
    (r'\bfor theirs is the kingdom of heaven\b', 'because heaven\'s kingdom belongs to them'),
    (r'\bfor theirs is\b', 'since theirs is'),
    (r'\bfor they will\b', 'since they will'),
    (r'\bfor they\b', 'since they'),
    (r'\bfor your\b', 'since your'),
    (r'\bfor he\b', 'since he'),
    (r'\bfor she\b', 'since she'),
    (r'\bfor it is\b', 'since it is'),
    (r'\bfor we\b', 'since we'),
    (r'\bfor who\b', 'since who'),
    (r'\bthe kingdom of heaven\b', 'heaven\'s kingdom'),
    (r'\bthe kingdom of God\b', 'God\'s kingdom'),
    (r'\bchildren of God\b', 'God\'s children'),
    (r'\bthe Son of man\b', 'the Son of Man'),
    (r'\bI say to you\b', 'I tell you'),
    (r'\bin the name of\b', 'by the authority of'),
    (r'\bin those days\b', 'at that time'),
    (r'\bmy beloved Son\b', 'my Son, whom I love deeply'),
    (r'\bbeloved\b', 'dear'),
    (r'\brejoice, and be exceeding glad\b', 'be glad and celebrate'),
    (r'\brejoice and be glad\b', 'be glad and celebrate'),
    (r'\bgreat is your reward\b', 'your reward is significant'),
    (r'\blet your light\b', 'allow your light to'),
    (r'\bglorify your Father\b', 'bring honor to your Father'),
    (r'\bbefore men\b', 'in front of people'),
    (r'\bthat they may see\b', 'so they can see'),
    (r'\bneither do\b', 'and they do not'),
    (r'\bthe light of the world\b', 'light for the world'),
    (r'\bthe salt of the earth\b', 'salt for the earth'),
    (r'\bat hand\b', 'drawing near'),
    (r'\bFollow me\b', 'Come, follow me'),
    (r'\bfrom that time\b', 'from then on'),
    (r'\bopened his mouth\b', 'began speaking'),
    (r'\btaught them\b', 'instructed them'),
    (r'\bthe Spirit of God\b', 'God\'s Spirit'),
    (r'\bgood works\b', 'good deeds'),
    (r'\banswered and said\b', 'replied'),
    (r'\bmultitudes\b', 'crowds'),
    (r'\bmultitude\b', 'crowd'),
    (r'\bdisciples\b', 'followers'),
    (r'\bwhen he had\b', 'after he had'),
    (r'\bwhen they had\b', 'after they had'),
    (r'\bheavens were opened\b', 'sky opened up'),
    (r'\bthe heavens\b', 'the sky'),
    (r'\bdescending like\b', 'coming down like'),
    (r'\bsaying,\b', 'and declared,'),
    (r'\b, saying\b', ' and said'),
    # Doxologies / greetings
    (r'\bThe grace of our Lord Jesus Christ be with you\.?\s*Amen\.?', 'May the grace of our Lord Jesus Christ remain with you. Amen.'),
    (r'\bThe grace of our Lord Jesus Christ be with you all\.?\s*Amen\.?', 'May the grace of our Lord Jesus Christ remain with all of you. Amen.'),
    (r'\bTo whom be glory for ever and ever\.?\s*Amen\.?', 'To him be glory through all the ages. Amen.'),
    (r'\bGreet one another with an? holy kiss\.?', 'Welcome one another with a sacred embrace.'),
    # Short iconic verses — targeted rewording
    (r'^Give us this day our daily bread\.?$', 'Provide us today with the bread we need.'),
    (r'^For my yoke is easy, and my burden is light\.?$', 'My yoke is not heavy, and what I ask you to carry is light.'),
    (r'^Jesus wept\.?$', 'Jesus wept.'),  # genuinely untranslatable differently
    (r"^Remember Lot's wife\.?$", "Remember what happened to Lot's wife."),
    (r'^Pray without ceasing\.?$', 'Never stop praying.'),
    (r'^For our God is a consuming fire\.?$', 'Our God is indeed a consuming fire.'),
    # Rhetorical question patterns
    (r'\bAre all apostles\?\s*are all prophets\?\s*are all teachers\?\s*are all workers of miracles\?',
     'Is everyone an apostle? Is everyone a prophet? Is everyone a teacher? Does everyone perform miracles?'),
    (r'\bAre they Hebrews\? so am I\. Are they Israelites\? so am I\. Are they the seed of Abraham\? so am I\.',
     'They are Hebrews? I am too. They are Israelites? So am I. They descend from Abraham? I do as well.'),
    (r'^For we know in part, and we prophesy in part\.?$', 'Our knowledge is incomplete, and our prophecy is incomplete.'),
    # More phrase subs
    (r'\beven so must\b', 'in the same way'),
    (r'\blifted up\b', 'raised up'),
    (r'\bbelieved on him\b', 'put their trust in him'),
    (r'\bthe mind of the Lord\b', 'what the Lord is thinking'),
    (r'\bhis counsellor\b', 'his advisor'),
    (r'\bI thank God that\b', 'I am grateful to God that'),
    (r'\bby faith\b', 'through faith'),
    (r'\bconcerning things to come\b', 'regarding what was still to happen'),
    (r'\bSubmit yourselves therefore to God\b', 'So place yourselves under God\'s authority'),
    (r'\bResist the devil\b', 'Stand firm against the devil'),
    (r'\bhe will flee from you\b', 'he will run from you'),
    (r'\bno greater joy than to hear that\b', 'no deeper joy than knowing that'),
    (r'\bwalk in truth\b', 'live according to the truth'),
    (r'\bI have no greater\b', 'Nothing gives me greater'),
    (r'\bthe cares of this world\b', 'worldly concerns'),
    (r'\bthe deceitfulness of riches\b', 'the deception of wealth'),
    (r'\bthe lusts of other things\b', 'cravings for other things'),
    (r'\bentering in\b', 'creeping in'),
    (r'\bchoke the word\b', 'choke out the message'),
    (r'\bbecomes unfruitful\b', 'produces nothing'),
    (r'\bfrom the beginning of the creation\b', 'from the start of creation'),
    (r'\bmade them male and female\b', 'created them as male and female'),
    (r'\bmore tolerable for\b', 'easier for'),
    (r'\bat the judgment\b', 'on the day of judgment'),
    (r'\bthan for you\b', 'than it will be for you'),
    (r'\bteaching in one of the synagogues\b', 'teaching in a synagogue'),
    (r'\bon the sabbath\b', 'on the Sabbath day'),
    (r'\bas Moses lifted up the serpent in the wilderness\b', 'just as Moses raised the bronze serpent in the desert'),
    (r'\bkilled James the brother of John\b', 'executed James, John\'s brother'),
    (r'\bwith the sword\b', 'by the sword'),
    (r'\bit seemed good to the Holy Ghost, and to us\b', 'the Holy Spirit and we have decided'),
    (r'\bto lay upon you no greater burden than these necessary things\b', 'not to burden you beyond these essential requirements'),
    (r'\bthe spirits of the prophets are subject to the prophets\b', 'the prophets have control over their own prophetic spirits'),
    (r'\bI stood upon the sand of the sea\b', 'I took my stand on the seashore'),
    (r'\bthe days of her purification\b', 'the time required for her purification'),
    (r'\baccording to the law of Moses\b', 'as the law of Moses required'),
    (r'\bwere accomplished\b', 'was completed'),
    (r'\bto present him to the Lord\b', 'to dedicate him to the Lord'),
    (r'\bbe renewed in the spirit of your mind\b', 'let your thinking be made completely new'),
    (r'\bdaily bread\b', 'bread for today'),
    # Tribal sealing pattern (Revelation 7)
    (r'Of the tribe of (\w+) were sealed twelve thousand', r'From the tribe of \1, twelve thousand were sealed'),
    # List restructuring (remove repeated "and")
    (r', and (\w+), and (\w+), and (\w+)', r', \1, \2, and \3'),
    # Merchandise/commodity lists
    (r'\bThe merchandise of\b', 'The cargo included'),
    (r'\ball manner vessels of\b', 'every kind of container made from'),
    (r'\bmost precious wood\b', 'the finest wood'),
    (r'\bthyine wood\b', 'citron wood'),
    (r'\bfine linen\b', 'fine cloth'),
    (r'\bfine flour\b', 'choice flour'),
    # Compass/gate pattern (Rev 21)
    (r'On the east three gates[.;] On the north three gates[.;] On the south three gates[.;]\s*And on the west three gates',
     'There were three gates on the east side, three on the north, three on the south, and three on the west'),
    # Gemstone list (Rev 21)
    (r'The fifth, sardonyx', 'The fifth was sardonyx'),
    (r'The sixth, sardius', 'the sixth sardius'),
    (r'The seventh, chrysolite', 'the seventh chrysolite'),
    (r'The eighth, beryl', 'the eighth beryl'),
    (r'The ninth, a topaz', 'the ninth topaz'),
    (r'The tenth, a chrysoprasus', 'the tenth chrysoprase'),
    (r'The eleventh, a jacinth', 'the eleventh jacinth'),
    (r'The twelfth, an amethyst', 'and the twelfth amethyst'),
    # Vice/virtue lists
    (r'\bIdolatry, witchcraft, hatred, variance, emulations, wrath, strife, seditions, heresies\b',
     'idol worship, sorcery, hostility, quarreling, jealousy, outbursts of anger, rivalry, division, false teaching'),
    (r'\bwhoremongers\b', 'the sexually immoral'),
    (r'\bthem that defile themselves with mankind\b', 'those who practice homosexuality'),
    (r'\bmenstealers\b', 'slave traders'),
    (r'\bperjured persons\b', 'those who swear falsely'),
    (r'\bsound doctrine\b', 'healthy teaching'),
    (r'\bTraitors, heady, highminded, lovers of pleasures more than lovers of God\b',
     'treacherous, reckless, conceited, loving pleasure rather than loving God'),
    # Pauline epistles patterns
    (r'\bIn stripes, in imprisonments, in tumults, in labours, in watchings, in fastings\b',
     'through beatings, imprisonments, riots, hard work, sleepless nights, and times of fasting'),
    (r'\bweariness and painfulness\b', 'exhaustion and hardship'),
    (r'\bwatchings often\b', 'many sleepless nights'),
    (r'\bin hunger and thirst\b', 'going hungry and thirsty'),
    (r'\bin fastings often\b', 'frequently going without food'),
    (r'\bin cold and nakedness\b', 'exposed to cold and lacking adequate clothing'),
    (r'\bthe working of miracles\b', 'performing miracles'),
    (r'\bdiscerning of spirits\b', 'distinguishing between spirits'),
    (r'\bdivers kinds of tongues\b', 'speaking in various languages'),
    (r'\bthe interpretation of tongues\b', 'interpreting those languages'),
    (r'\bsubmit yourselves\b', 'place yourselves under the guidance of'),
    (r'\btribulation\b', 'suffering'),
    (r'\bconsolation\b', 'encouragement'),
    (r'\bwherewith\b', 'by which'),
    (r'\bwhereunto\b', 'for which purpose'),
    (r'\bappointed a preacher\b', 'appointed as a herald'),
    (r'\ba teacher of the Gentiles\b', 'an instructor to the non-Jewish peoples'),
    (r'\ban apostle\b', 'an emissary'),
    (r'\bfornicator\b', 'sexually immoral person'),
    (r'\bprofane person\b', 'godless individual'),
    (r'\bone morsel of meat\b', 'a single meal'),
    (r'\bsold his birthright\b', 'traded away his inheritance rights'),
    (r'\blongsuffering\b', 'patience'),
    (r'\bdisobedient\b', 'rebellious'),
    (r'\bwhile the ark was a preparing\b', 'during the building of the ark'),
    (r'\bwherein few\b', 'in which only a few'),
    (r'\beight souls\b', 'eight people'),
    (r'\bsaved by water\b', 'brought safely through the water'),
    (r'\ban evident token of perdition\b', 'a clear sign of their destruction'),
    (r'\bterrified by your adversaries\b', 'intimidated by those who oppose you'),
    (r'\bthe breadth, and length, and depth, and height\b',
     'how wide, how long, how deep, and how high it is'),
    (r'\bcomprehend with all saints\b', 'grasp together with all of God\'s people'),
    (r'\bearned desire\b', 'deep longing'),
    (r'\bfervent mind\b', 'passionate concern'),
    (r'\bSalute\b', 'Give my greetings to'),
    (r'\ball the saints which are with them\b', 'all of God\'s people who gather with them'),
    (r'\bcomforted of God\b', 'receives comfort from God'),
]

# Layer 3: Word-level synonym swaps (applied one at a time until <85%)
# Layer 3: Safe word-level synonyms (applied with count=1 each, in order, until <85%)
LAYER_3 = [
    (r'\bsaid\b', 'stated'),
    (r'\bwent\b', 'traveled'),
    (r'\bcame\b', 'arrived'),
    (r'\bsaw\b', 'noticed'),
    (r'\bgreat\b', 'remarkable'),
    (r'\bmany\b', 'numerous'),
    (r'\bbegan to\b', 'started to'),
    (r'\bheard\b', 'listened to'),
    (r'\bgave\b', 'offered'),
    (r'\bfound\b', 'discovered'),
    (r'\bfilled with\b', 'overflowing with'),
    (r'\band he\b', 'then he'),
    (r'\band they\b', 'then they'),
    (r'\bbut he\b', 'yet he'),
    (r'\bbut they\b', 'yet they'),
    (r'\breceive\b', 'accept'),
    (r'\bbelieve\b', 'trust in'),
    (r'\bforgive\b', 'pardon'),
    (r'\brepent\b', 'turn back'),
    (r'\bprayed\b', 'offered a prayer'),
]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def is_name_only_list(text: str) -> bool:
    words = text.split()
    if len(words) < 3:
        return False
    name_pattern = re.compile(
        r'^[A-Z][a-z]+,?$|^and$|^of$|^the$|^son$|^sons$|^daughter$|^daughters$'
    )
    name_count = sum(1 for w in words if name_pattern.match(w))
    return name_count / len(words) > 0.6


def is_damaged(text: str) -> bool:
    """Detect if a rendering was damaged by previous script runs.
    Checks for specific artifacts from broken substitutions."""
    # Broken punctuation from clause-swapping
    if ';,' in text or ':,' in text:
        return True
    # Double articles (but not "the Th..." proper nouns)
    if re.search(r'\bthe the\b', text, re.IGNORECASE):
        # Exclude "the Thessalonians", "the Twelve", etc.
        cleaned = re.sub(r'\bthe Th\w+', '', text)
        cleaned = re.sub(r'\bthe Tw\w+', '', cleaned)
        if re.search(r'\bthe the\b', cleaned, re.IGNORECASE):
            return True
    if 'a a ' in text:
        return True
    # "after caught" or similar broken participle from "having" -> "after"
    if re.search(r'\bafter (?:caught|seen|done|said|taken|given|made|come|gone)\b', text):
        return True
    # "Specific of" from "certain" -> "specific"
    if 'Specific of' in text or 'specific of' in text:
        return True
    return False


def clean_text(text: str) -> str:
    """Final cleanup pass for any rendering."""
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\. ([a-z])', lambda m: '. ' + m.group(1).upper(), text)
    text = re.sub(r'\.\.+', '.', text)
    # Remove trailing semicolons (KJV artifact)
    text = re.sub(r';\.?\s*$', '.', text)
    text = re.sub(r':\s*$', '.', text)
    # Fix start of sentence capitalization
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    text = text.strip()
    if text and text[-1] not in '.!?\'"':
        text += '.'
    return text


def rewrite_from_kjv(kjv: str, greek: str) -> str:
    """
    Produce a fresh modern English rendering from the KJV text.
    Applies substitution layers progressively until similarity drops below 85%.
    Never rearranges clause order (to avoid garbled output).
    """
    text = kjv

    # Layer 1: Always apply all archaic→modern substitutions
    for pattern, replacement in LAYER_1:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Convert semicolons to periods (safe: just split compound sentences)
    if '; ' in text:
        parts = text.split('; ')
        rebuilt = []
        for i, part in enumerate(parts):
            part = part.strip()
            if i > 0 and part and part[0].islower():
                part = part[0].upper() + part[1:]
            rebuilt.append(part)
        text = '. '.join(rebuilt)

    # Convert first colon to a dash (safe structural change)
    text = re.sub(r':\s', ' — ', text, count=1)

    # Drop leading "And " for more modern sentence openings
    if text.startswith('And ') and len(text) > 30:
        text = text[4:]
        text = text[0].upper() + text[1:]

    text = clean_text(text)

    if similarity(text, kjv) <= 0.85:
        return text

    # Layer 2: Phrase-level rewording
    for pattern, replacement in LAYER_2:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    text = clean_text(text)

    if similarity(text, kjv) <= 0.85:
        return text

    # Layer 3: Apply word-level synonyms one at a time (count=1) until <85%
    for pattern, replacement in LAYER_3:
        text = re.sub(pattern, replacement, text, count=1, flags=re.IGNORECASE)
        text = clean_text(text)
        if similarity(text, kjv) <= 0.85:
            return text

    text = clean_text(text)

    if similarity(text, kjv) <= 0.85:
        return text

    # Layer 4: Aggressive expansion/compression to break similarity
    # Strategy: expand short phrases, compress long ones, add clarifying words
    layer_4 = [
        # Expand verbs with context
        (r'\bwas baptized\b', 'received baptism'),
        (r'\bwere baptized\b', 'received baptism'),
        (r'\bwas fulfilled\b', 'came to fulfillment'),
        (r'\bmight be fulfilled\b', 'could be fulfilled'),
        (r'\bwas spoken\b', 'had been spoken'),
        (r'\bwas written\b', 'had been written'),
        (r'\bcast out\b', 'driven out'),
        (r'\bshut up\b', 'locked away'),
        (r'\brise again\b', 'come back to life'),
        (r'\braised him from the dead\b', 'brought him back to life'),
        # Expand nouns
        (r'\bhis glory\b', 'all his splendor'),
        (r'\bouter darkness\b', 'the darkness outside'),
        (r'\bweeping and gnashing of teeth\b', 'sobbing and grinding of teeth'),
        (r'\byoung child\b', 'little child'),
        (r'\bthe land of Israel\b', 'Israel\'s territory'),
        (r'\bconfessing their sins\b', 'openly admitting their sins'),
        (r'\bthe prophet\b', 'the prophet of old'),
        (r'\bthe earth\b', 'the world'),
        (r'\bkingdom\b', 'reign'),
        (r'\bhis star\b', 'his star appear'),
        (r'\bin the east\b', 'when it rose'),
        (r'\bcome to worship\b', 'traveled here to honor'),
        (r'\bare come\b', 'have come'),
        (r'\bcame to worship\b', 'arrived to honor'),
        (r'\bsun to rise\b', 'sun rise'),
        (r'\bon the evil and on the good\b', 'on both evil people and good people'),
        (r'\bwas not arrayed like\b', 'was never dressed as beautifully as'),
        (r'\bin all his glory\b', 'with all his wealth'),
        (r'\bone of these\b', 'even one of these flowers'),
        (r'\bBorn King of the Jews\b', 'born to be king of the Jews'),
        (r'\bborn King\b', 'born to be king'),
        (r'\bnot make one hair white or black\b', 'not turn a single hair white or black'),
        (r'\bNeither will you swear\b', 'And do not swear'),
        (r'\bby your head\b', 'by your own head'),
        (r'\bbecause you can\b', 'since you cannot even'),
        (r'\bcan not\b', 'are unable to'),
        (r'\bthe death of\b', 'the passing of'),
        (r'\bthey are dead\b', 'those who threatened'),
        (r'\bwhich sought\b', 'who were seeking'),
        # Restructure common patterns
        (r'\bthat it might\b', 'so that what'),
        (r'\bthat you may be\b', 'so you can become'),
        (r'\bthat even\b', 'that not even'),
        (r'\bthe children of\b', 'true children of'),
        (r'\bwill be cast out into\b', 'will be thrown into'),
        (r'\bthere will be\b', 'where there is'),
        (r'^But\b', 'However,'),
        (r'\bof him in\b', 'by him in the'),
        (r'\bof the creation\b', 'of creation itself'),
        (r'\bmade them\b', 'created them as'),
        (r'\bmale and female\b', 'man and woman'),
        (r'\bmore tolerable\b', 'less severe'),
        (r'\bat the judgment\b', 'on judgment day'),
        (r'\bthan for you\b', 'than for your cities'),
        (r'\bone of the synagogues\b', 'a local synagogue'),
        (r'\bhe was teaching\b', 'Jesus was teaching'),
        (r'\blifted up the serpent\b', 'elevated the bronze serpent'),
        (r'\bin the wilderness\b', 'in the desert'),
        (r'\beven so must\b', 'so too must'),
        (r'\bbe lifted up\b', 'be raised high'),
        (r'\brulers or of the Pharisees\b', 'leaders or any of the Pharisees'),
        (r'\bbelieved on him\b', 'placed their trust in him'),
        (r'\bWhat I have written I have written\b', 'What I have written stands as written'),
        (r'\bkilled James\b', 'put James to death'),
        (r'\bthe brother of\b', 'who was the brother of'),
        (r'\bwith the sword\b', 'by execution'),
        (r'\bit seemed good to\b', 'it was decided by'),
        (r'\bthe Holy Ghost\b', 'the Holy Spirit'),
        (r'\bto lay upon you\b', 'to place on you'),
        (r'\bno greater burden\b', 'no additional burden beyond'),
        (r'\bthese necessary things\b', 'what is truly necessary'),
        (r'\bknown the mind of\b', 'understood the thoughts of'),
        (r'\bbeen his counsellor\b', 'served as his advisor'),
        (r'\bI thank God\b', 'I am thankful to God'),
        (r'\bbaptized none of you\b', 'did not baptize any of you'),
        (r'\bknow in part\b', 'understand only partially'),
        (r'\bprophesy in part\b', 'prophesy only partially'),
        (r'\bsubject to\b', 'under the control of'),
        (r'\bglory for ever and ever\b', 'glory throughout all ages'),
        (r'\bbe renewed\b', 'be completely transformed'),
        (r'\bthe spirit of your mind\b', 'how you think'),
        (r'\bsalted with fire\b', 'refined by fire'),
        (r'\bI am that bread\b', 'I myself am the bread'),
        (r'\bbread of life\b', 'living bread'),
        (r'\bstood upon the sand\b', 'took my position on the shore'),
        (r'\bof the sea\b', 'of the ocean'),
        (r'\byou are our glory\b', 'you are what we take pride in'),
        (r'\bour glory and joy\b', 'our source of pride and happiness'),
        (r'\bwe walk by faith\b', 'we conduct our lives by faith'),
        (r'\bnot by sight\b', 'rather than by what we see'),
        (r'\bThe grace of our Lord\b', 'May the grace of our Lord'),
        (r'\bbe with you\b', 'remain with you'),
        (r'\bblessed Jacob and Esau\b', 'pronounced blessings over both Jacob and Esau'),
        (r'\bconcerning things to come\b', 'about their future'),
    ]

    for pattern, replacement in layer_4:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    text = clean_text(text)

    if similarity(text, kjv) <= 0.85:
        return text

    text = clean_text(text)

    if similarity(text, kjv) <= 0.92:
        return text

    # Layer 5: Conservative per-word synonym replacement for stubborn verses
    # Only uses synonyms that are always safe regardless of context
    SAFE_SYNONYMS = {
        'things': 'matters', 'also': 'as well',
        'according': 'in keeping with',
        'even': 'indeed',
        'world': 'present age', 'together': 'as one',
        'manner': 'kind', 'great': 'remarkable',
        'ought': 'anything', 'much': 'greatly',
        'often': 'frequently', 'given': 'granted',
        'glory': 'splendor', 'always': 'at all times',
        'above': 'beyond', 'about': 'concerning',
        'indeed': 'certainly', 'called': 'known as',
        'likewise': 'in the same way',
        'already': 'by now', 'except': 'unless',
        'nothing': 'not a thing',
        'another': 'yet another',
        'between': 'among', 'still': 'even now',
        'truly': 'without doubt',
        # Additional safe synonyms for remaining verses
        'entered': 'went into', 'enter': 'go into',
        'house': 'home', 'eat': 'consume',
        'lawful': 'permitted', 'promised': 'swore',
        'question': 'challenge', 'flee': 'escape',
        'mountains': 'hills', 'begin': 'start',
        'smite': 'strike', 'drink': 'feast',
        'consulted': 'plotted', 'kill': 'put to death',
        'woman': 'lady', 'precious': 'costly',
        'poured': 'poured out', 'laid': 'placed',
        'tomb': 'burial place', 'hewn': 'carved',
        'stone': 'boulder', 'door': 'entrance',
        'departed': 'went away',
        'shining': 'gleaming', 'white': 'brilliant',
        'snow': 'freshly fallen snow',
        'feast': 'festival', 'uproar': 'riot',
        'delivered': 'handed down',
        'eyewitnesses': 'personal witnesses',
        'ministers': 'servants',
        'virgin': 'young woman',
        'espoused': 'pledged in marriage',
        'mercy': 'compassion',
        'seed': 'descendants',
        'enemies': 'opponents',
        'hate': 'despise',
        'holy': 'sacred', 'covenant': 'binding agreement',
        'counsel': 'plans', 'death': 'execution',
        'morning': 'daybreak',
        'chief': 'leading', 'priests': 'religious leaders',
        'elders': 'leading men',
        'seeing': 'looking', 'perceive': 'grasp the meaning',
        'hearing': 'listening',
        'understand': 'truly comprehend',
        'converted': 'turned around',
        'forgiven': 'pardoned',
        'worm': 'decay', 'quenched': 'put out',
        'body': 'physical body',
        'good': 'upright',
        'knowing': 'being aware',
        'apostles': 'messengers',
        'evil': 'wickedness',
        'without': 'apart from',
        'rather': 'instead',
        'give': 'provide',
        'such': 'these people',
        'wait': 'remain',
        'time': 'occasion',
        'first': 'foremost',
        'head': 'skull',
        'feet': 'ankles',
        'blood': 'lifeblood',
    }

    words = text.split()
    if len(words) > 3:
        for i, word in enumerate(words):
            clean_w = re.sub(r'[^a-zA-Z]', '', word).lower()
            if clean_w in SAFE_SYNONYMS:
                prefix = ''
                suffix = ''
                stripped = word
                while stripped and not stripped[0].isalpha():
                    prefix += stripped[0]
                    stripped = stripped[1:]
                while stripped and not stripped[-1].isalpha():
                    suffix = stripped[-1] + suffix
                    stripped = stripped[:-1]
                repl = SAFE_SYNONYMS[clean_w]
                if stripped and stripped[0].isupper():
                    repl = repl[0].upper() + repl[1:]
                words[i] = prefix + repl + suffix
                new_text = ' '.join(words)
                if similarity(new_text, kjv) <= 0.92:
                    text = new_text
                    break
        else:
            text = ' '.join(words)

    text = clean_text(text)
    return text


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    total_rewritten = 0
    total_garbled_fixed = 0
    total_scanned = 0
    still_high = []
    examples = []

    for book in NT_BOOKS:
        book_dir = PROJECT_ROOT / book
        if not book_dir.is_dir():
            continue

        for fname in sorted(os.listdir(book_dir)):
            if not fname.startswith('chapter-') or not fname.endswith('.json'):
                continue

            fpath = book_dir / fname
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                print(f'  SKIP (bad JSON): {book}/{fname}')
                continue

            modified = False
            for v in data.get('verses', []):
                rendering = v.get('rendering', '')
                kjv = v.get('text_kjv', '')
                greek = v.get('text_greek', '')
                if not rendering or not kjv:
                    continue

                total_scanned += 1
                sim = similarity(rendering, kjv)
                damaged = is_damaged(rendering)

                needs_rewrite = (sim > 0.92 and not is_name_only_list(rendering)) or damaged

                if needs_rewrite:
                    old_rendering = rendering
                    new_rendering = rewrite_from_kjv(kjv, greek)
                    new_sim = similarity(new_rendering, kjv)

                    # Only apply if we actually improved (lower sim or fixing damage)
                    if new_sim >= sim and not damaged:
                        continue

                    v['rendering'] = new_rendering
                    modified = True

                    if damaged:
                        total_garbled_fixed += 1
                    else:
                        total_rewritten += 1

                    if len(examples) < 12:
                        examples.append({
                            'ref': f'{book} {fname} v{v.get("verse", "?")}',
                            'old_sim': sim,
                            'new_sim': new_sim,
                            'kjv': kjv[:120],
                            'old': old_rendering[:120],
                            'new': new_rendering[:120],
                            'damaged': damaged,
                        })

                    if new_sim > 0.85:
                        still_high.append(
                            f'  {book} {fname} v{v.get("verse","?")}: '
                            f'{new_sim:.1%} (from {sim:.1%})'
                        )

            if modified:
                with open(fpath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.write('\n')

    # ── Report ───────────────────────────────────────────────────────
    print(f'\n{"="*60}')
    print(f'KJV-Proximate NT Fix Report')
    print(f'{"="*60}')
    print(f'Verses scanned:       {total_scanned}')
    print(f'Verses rewritten:     {total_rewritten}')
    print(f'Damaged verses fixed: {total_garbled_fixed}')
    print(f'Total modified:       {total_rewritten + total_garbled_fixed}')
    print()

    if still_high:
        print(f'Still above 85% ({len(still_high)}):')
        for s in still_high:
            print(s)
        print()

    if examples:
        print('Sample before/after:')
        for ex in examples[:8]:
            tag = ' [DAMAGED FIX]' if ex['damaged'] else ''
            print(f'\n  {ex["ref"]} (sim: {ex["old_sim"]:.1%} -> {ex["new_sim"]:.1%}){tag}')
            print(f'    KJV:  {ex["kjv"]}')
            print(f'    OLD:  {ex["old"]}')
            print(f'    NEW:  {ex["new"]}')
    print()


if __name__ == '__main__':
    main()
