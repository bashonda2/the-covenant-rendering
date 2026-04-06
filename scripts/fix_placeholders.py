# -*- coding: utf-8 -*-
"""Fix placeholder key_terms entries in Isaiah 49-62."""
import json

# Map of (file, verse, transliteration) -> (rendered_as, semantic_range, note)
fixes = {
    # Isaiah 49
    ("isaiah/chapter-49.json", 6, "or goyim"): (
        "a light for the nations",
        "light, illumination, enlightenment",
        "The Servant's mission extends beyond restoring Israel: he becomes or goyim ('a light for the nations'). The universal scope transforms a national restoration into a global revelation. This phrase echoes 42:6 and anticipates Luke 2:32 (Simeon's 'a light for revelation to the Gentiles')."
    ),
    ("isaiah/chapter-49.json", 7, "go'el"): (
        "Redeemer",
        "redeemer, kinsman-redeemer, one who reclaims what was lost",
        "God as Israel's go'el — the kinsman obligated to buy back what the family has lost. Capitalized when applied to God. Here paired with 'the Holy One of Israel,' combining intimacy (kinsman) with transcendence (Holy One)."
    ),
    ("isaiah/chapter-49.json", 26, "go'alekh"): (
        "your Redeemer",
        "your redeemer, your kinsman-redeemer",
        "The suffixed form go'alekh ('your Redeemer') makes the kinship personal — God is not a generic redeemer but Israel's own kin. The context is rescue from oppressors who have consumed Israel."
    ),
    # Isaiah 50
    ("isaiah/chapter-50.json", 4, "limmudim"): (
        "those who are taught",
        "disciples, learners, those instructed, trained ones",
        "The word limmudim ('taught ones, disciples') from the root l-m-d ('to learn') describes the Servant's tongue as that of a disciple — one who has been trained by God to speak the right word at the right time. The Servant speaks not from his own wisdom but from what he has received."
    ),
    # Isaiah 51
    ("isaiah/chapter-51.json", 9, "rahab"): (
        "Rahab",
        "Rahab (mythological sea monster), pride, arrogance, storm",
        "Rahab is the primordial sea monster of chaos, not the woman of Jericho. The name represents cosmic opposition to God's order. Here the prophet calls on God's arm to act as it did when it 'cut Rahab to pieces' — a reference to both creation mythology and the Exodus (the sea as chaos defeated)."
    ),
    ("isaiah/chapter-51.json", 17, "kos chamato"): (
        "the cup of His wrath",
        "cup of wrath, cup of staggering, goblet of fury",
        "The kos chamat YHWH ('cup of the LORD's wrath') is a prophetic metaphor for divine judgment experienced as forced intoxication — the nations drink and stagger. Jerusalem has drained this cup (v. 17); now it will be transferred to her oppressors (v. 22-23). The image recurs in Jeremiah 25:15-28 and Revelation 14:10."
    ),
    # Isaiah 52
    ("isaiah/chapter-52.json", 7, "mevasser"): (
        "the one who brings good news",
        "herald, bearer of good tidings, evangelist",
        "The mevasser ('herald of good news') on the mountains announces shalom, good, and salvation — 'Your God reigns!' The word is the verbal form of the root b-s-r, from which besorah ('good news, gospel') derives. Paul cites this verse in Romans 10:15."
    ),
    ("isaiah/chapter-52.json", 10, "zeroa qodsho"): (
        "His holy arm",
        "holy arm, sacred arm, arm of holiness",
        "The zeroa ('arm') is God's instrument of power — bared (chasaf) for all nations to see. The 'holy arm' combines divine power with divine purity. The image of God rolling up His sleeve for battle runs through Isaiah (40:10, 51:9, 53:1)."
    ),
    ("isaiah/chapter-52.json", 13, "avdi"): (
        "my servant",
        "my servant, my slave, my worker",
        "The Fourth Servant Song begins: avdi ('my servant') will prosper (yaskil), be raised and lifted up (yarum venissa), and be very high (gavah me'od). The three verbs of exaltation are among the strongest in Hebrew — the same language used for God's own exaltation in 6:1 (Isaiah's throne vision)."
    ),
    # Isaiah 53
    ("isaiah/chapter-53.json", 1, "zeroa YHWH"): (
        "the arm of the LORD",
        "arm of the LORD, power of the LORD, strength of the LORD",
        "The zeroa YHWH ('arm of the LORD') represents God's active intervention in history. The question 'to whom has the arm of the LORD been revealed?' implies that the Servant's suffering is itself the revelation of divine power — but in a form no one expected or recognized."
    ),
    ("isaiah/chapter-53.json", 3, "ish makh'ovot"): (
        "a man of sorrows",
        "man of pains, man of sufferings, one acquainted with grief",
        "The phrase ish makh'ovot ('man of pains/sorrows') and yadu'a choli ('acquainted with illness/grief') describe the Servant's intimate familiarity with human suffering — not as observer but as participant. The rendering 'man of sorrows' follows a long translation tradition that captures the Hebrew's weight."
    ),
    ("isaiah/chapter-53.json", 5, "mecholal"): (
        "pierced",
        "pierced, wounded, profaned, defiled",
        "The verb mecholal (from chalal) can mean 'pierced,' 'wounded,' or 'profaned.' We rendered it 'pierced' because the parallel with medukkah ('crushed') points to physical violence, not merely defilement. The preposition min ('because of, from') makes the cause clear: our transgressions, our iniquities."
    ),
    ("isaiah/chapter-53.json", 10, "asham"): (
        "guilt offering",
        "guilt offering, reparation offering, compensation sacrifice",
        "The asham ('guilt offering') is a specific Levitical sacrifice (Leviticus 5:14-6:7, 7:1-10) that provides restitution for wrongs committed. Applying sacrificial language to a person is unprecedented in the Hebrew Bible. The Servant's life becomes the reparation that restores what sin destroyed."
    ),
    # Isaiah 54
    ("isaiah/chapter-54.json", 5, "bo'alayikh"): (
        "your Maker is your husband",
        "your husband, your lord, your master, your owner",
        "The verb ba'al means both 'to marry' and 'to be lord/master over.' God is simultaneously Israel's creator (osayikh, 'your Maker') and husband (bo'alayikh). The marital metaphor for the God-Israel relationship runs from Hosea through Isaiah to Revelation."
    ),
    ("isaiah/chapter-54.json", 5, "go'alekh"): (
        "your Redeemer",
        "your redeemer, your kinsman-redeemer",
        "Three titles in one verse: Maker, husband, Redeemer (go'el). The go'el obligation — family duty to rescue what is lost — is combined with the marriage covenant. God claims Zion by every possible bond: creation, marriage, and kinship."
    ),
    ("isaiah/chapter-54.json", 8, "chesed olam"): (
        "everlasting faithful love",
        "eternal faithful love, perpetual lovingkindness, covenant loyalty forever",
        "The phrase chesed olam ('everlasting faithful love') combines the covenant loyalty term chesed with olam ('eternity'). God's momentary anger (v. 7-8a) is contrasted with His permanent compassion — the disproportion is deliberate and comforting."
    ),
    ("isaiah/chapter-54.json", 10, "berit shelomi"): (
        "my covenant of peace",
        "covenant of peace, treaty of well-being, pact of wholeness",
        "The berit shalom ('covenant of peace') promises that God's commitment to Zion is as unshakeable as His commitment to the cosmic order (mountains may depart, hills may shake). The same phrase appears in Numbers 25:12 (Phinehas) and Ezekiel 34:25, 37:26."
    ),
    # Isaiah 55
    ("isaiah/chapter-55.json", 3, "chasdei David hanne'emanim"): (
        "the faithful mercies of David",
        "the sure mercies of David, the reliable covenant promises to David, David's guaranteed covenant blessings",
        "The phrase chasdei David hanne'emanim ('the faithful/sure mercies of David') refers to God's covenant promises to the Davidic dynasty (2 Samuel 7:8-16). The adjective ne'emanim ('faithful, sure, reliable') from the root a-m-n (amen) guarantees their permanence. Acts 13:34 cites this verse."
    ),
    # Isaiah 56
    ("isaiah/chapter-56.json", 7, "beit tefillah"): (
        "a house of prayer",
        "house of prayer, place of worship, sanctuary of intercession",
        "The phrase beit tefillah lekhol ha'ammim ('a house of prayer for all peoples') is God's vision for the Temple — not an ethnic sanctuary but a universal place of worship. Jesus quotes this in Mark 11:17 when cleansing the Temple, emphasizing the 'for all peoples' that had been violated."
    ),
    # Isaiah 57
    ("isaiah/chapter-57.json", 15, "dakka"): (
        "the crushed",
        "crushed, contrite, broken, ground to dust",
        "God dwells with the dakka ('crushed one') — the same root as Psalm 34:18 ('the LORD is near to the brokenhearted') and Isaiah 53:5 ('crushed for our iniquities'). The Most High inhabits both eternity and the lowest human experience simultaneously."
    ),
    ("isaiah/chapter-57.json", 15, "shefal ruach"): (
        "the lowly in spirit",
        "humble in spirit, low in spirit, those of a low disposition",
        "The phrase shefal ruach ('lowly/humble in spirit') pairs with dakka to describe those God chooses to dwell with — not the exalted but the broken. The purpose is restoration: 'to revive the spirit of the lowly, to revive the heart of the crushed.'"
    ),
    ("isaiah/chapter-57.json", 19, "shalom shalom"): (
        "peace, peace",
        "peace peace, wholeness wholeness, complete well-being",
        "The doubled shalom shalom ('peace, peace') echoes 26:3 and extends healing to both 'the far and the near' — those in exile and those who remained. The doubling intensifies: this is not partial peace but total restoration."
    ),
    # Isaiah 58
    ("isaiah/chapter-58.json", 6, "tsom"): (
        "fast",
        "fast, fasting, abstinence from food, self-denial",
        "God redefines tsom ('fasting') from ritual self-denial to social justice: loosing bonds of wickedness, freeing the oppressed, sharing bread with the hungry. The true fast is not empty stomachs but full hands — the chapter's revolutionary claim."
    ),
    # Isaiah 59
    ("isaiah/chapter-59.json", 17, "qin'ah"): (
        "zeal",
        "zeal, jealousy, passionate ardor, fierce devotion",
        "God puts on qin'ah ('zeal, jealousy') as a cloak — the divine warrior dresses for battle not in armor alone but in passionate commitment to His people. The same root describes God's jealous love in Exodus 20:5 and 34:14."
    ),
    ("isaiah/chapter-59.json", 20, "go'el"): (
        "Redeemer",
        "redeemer, kinsman-redeemer, one who reclaims what was lost",
        "The go'el ('Redeemer') comes to Zion specifically for 'those in Jacob who turn from transgression.' The kinsman-redeemer arrives not for the righteous but for the repentant. Paul cites this verse in Romans 11:26."
    ),
    # Isaiah 60
    ("isaiah/chapter-60.json", 1, "or"): (
        "light",
        "light, illumination, daylight, dawn",
        "The imperative qumi ori ('arise, shine') uses or ('light') as both the reason and the result: Zion's light has come because the LORD's glory (kavod) has risen upon her. The light is not Zion's own but God's — reflected, not generated."
    ),
    ("isaiah/chapter-60.json", 19, "or olam"): (
        "everlasting light",
        "eternal light, perpetual light, light of eternity",
        "The phrase or olam ('everlasting light') replaces the sun and moon — God Himself becomes Zion's permanent illumination. This image is taken up in Revelation 21:23 and 22:5, where the heavenly city needs no sun because the Lamb is its light."
    ),
    # Isaiah 61
    ("isaiah/chapter-61.json", 1, "mashach"): (
        "anointed",
        "anointed, consecrated by anointing, smeared with oil",
        "The verb mashach ('anointed') is the root of mashiach ('messiah'). The speaker declares divine anointing for a specific mission: good news to the poor, binding up the brokenhearted, liberty to captives. Jesus reads this passage in the Nazareth synagogue (Luke 4:18-21) and declares 'Today this Scripture is fulfilled in your hearing.'"
    ),
    ("isaiah/chapter-61.json", 1, "deror"): (
        "liberty",
        "liberty, release, freedom, emancipation",
        "The word deror ('liberty, release') is the same word used for the Jubilee year proclamation in Leviticus 25:10 — the fiftieth year when slaves go free, debts are cancelled, and land returns to original owners. The Servant's mission is a cosmic Jubilee."
    ),
    ("isaiah/chapter-61.json", 3, "pe'er"): (
        "a crown of beauty",
        "beauty, glory, headdress, turban, garland",
        "The exchange in verse 3 — pe'er ('beauty/garland') for efer ('ashes') — is a wordplay: the two words sound nearly identical in Hebrew but mean opposite things. Mourning ashes become a crown of beauty. The assonance makes the transformation audible."
    ),
    # Isaiah 62
    ("isaiah/chapter-62.json", 4, "Cheftsi-vah / Hephzibah"): (
        "Hephzibah — My Delight Is in Her",
        "my delight is in her, I take pleasure in her",
        "God renames Zion from Azuvah (Forsaken) to Cheftsi-vah (My Delight Is in Her). The name is a declaration of restored covenant affection — God takes pleasure in the city He once abandoned to judgment. The same name belonged to Hezekiah's wife (2 Kings 21:1), anchoring the eschatological promise in royal history."
    ),
    ("isaiah/chapter-62.json", 4, "Be'ulah / Beulah"): (
        "Beulah — Married",
        "married, owned, possessed by a husband",
        "The land is renamed from Shemamah (Desolate) to Be'ulah (Married). The verb ba'al means both to marry and to possess as lord. The land that was widowed by exile is now claimed again by its divine husband. The marital metaphor extends through verse 5, where God rejoices over Zion as a bridegroom over his bride."
    ),
}

# Apply fixes
fixed = 0
files_changed = set()
for (fpath, verse_num, translit), (new_ra, new_sr, new_note) in fixes.items():
    with open(fpath) as f:
        data = json.load(f)

    for v in data['verses']:
        if v['verse'] != verse_num:
            continue
        for kt in v.get('key_terms', []):
            if kt.get('transliteration', '') == translit:
                kt['rendered_as'] = new_ra
                kt['semantic_range'] = new_sr
                kt['note'] = new_note
                fixed += 1
                files_changed.add(fpath)

    with open(fpath, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Fixed {fixed} placeholder entries across {len(files_changed)} files")
for f in sorted(files_changed):
    print(f"  {f}")
