# The Covenant Rendering — Quality Correction Addendum v1.3

## Add this section to the master prompt context in Cursor

This addendum addresses three systemic issues identified during QA of Exodus chapters 1-10. Apply these rules to ALL future chapter generation AND when regenerating any flagged chapters.

---

## RULE 1: No KJV Pass-Through

**Your rendering MUST be an independent translation from the Hebrew. It must NOT match the KJV.**

The KJV text is provided as a reference for readers — it is NOT your source. You are translating from the Westminster Leningrad Codex. Your rendering should read like clean, modern, literary English written in 2026, not like 17th-century English.

**Self-check before finalizing each verse:** Compare your `rendering` field against the `text_kjv` field. If they match word-for-word or nearly word-for-word, you have copied the KJV instead of translating from Hebrew. Rewrite the rendering in your own modern English.

**Examples of what NOT to do:**

❌ KJV copy:
```
"rendering": "And there went a man of the house of Levi, and took to wife a daughter of Levi."
```

✅ Independent rendering from Hebrew:
```
"rendering": "A man from the house of Levi went and married a daughter of Levi."
```

❌ KJV copy:
```
"rendering": "And his sister stood afar off, to wit what would be done to him."
```

✅ Independent rendering from Hebrew:
```
"rendering": "His sister stood at a distance to see what would happen to him."
```

❌ KJV copy:
```
"rendering": "And the magicians did so with their enchantments, and brought up frogs upon the land of Egypt."
```

✅ Independent rendering from Hebrew:
```
"rendering": "The magicians did the same with their secret arts, bringing frogs up over the land of Egypt."
```

**The goal:** A reader should be able to place any verse of The Covenant Rendering next to the KJV and immediately see that these are two different translations from the same Hebrew source — not one copied from the other.

---

## RULE 2: No Boilerplate Translator Notes

**Every translator_note must be specific to the verse it appears on. Generic observations that could apply to any verse are not acceptable.**

The following phrases (and variants) are BANNED from translator_notes because they have been used as placeholders instead of real scholarship:

- "The narrative advances the confrontation between divine promise and imperial power in this verse's movement and wording."
- "The narrative advances the conflict between covenant promise and imperial resistance in this verse."
- Any generic note that does not reference specific Hebrew words, translation decisions, or contextual details unique to that verse.

**What a good translator_note does:**
- Explains WHY you chose a specific English word over alternatives
- Documents Hebrew wordplay, idiom, or ambiguity that the English cannot capture
- Notes intertextual connections to other specific passages
- Flags where the Hebrew is uncertain or debated among scholars
- Provides cultural or historical context relevant to that specific verse

**Self-check:** If your translator_note could be copy-pasted onto a different verse and still make sense, it is too generic. Rewrite it with specific reference to the Hebrew text of THIS verse.

**Examples:**

❌ Generic/boilerplate:
```
"translator_notes": ["The narrative advances the confrontation between divine promise and imperial power in this verse's movement and wording."]
```

✅ Verse-specific:
```
"translator_notes": ["The Hebrew verb chazaq ('to strengthen, harden') is used here rather than kavad ('to make heavy'). Exodus alternates between these two hardening verbs — chazaq suggests God actively reinforcing Pharaoh's existing resistance, while kavad (used in 8:15, 8:32) describes Pharaoh making his own heart heavy. The theological distinction matters: this is not arbitrary divine coercion but judicial confirmation of a posture Pharaoh has already chosen."]
```

**Also:** Make sure each note corresponds to its own verse. Do not place a note about verse 7's content on verse 6.

---

## RULE 3: Consistent Modern English — No Archaic Forms

**The rendering must use consistent modern English throughout. No archaic pronouns, verb forms, or syntax.**

**Banned in the `rendering` field:**
- "thou," "thee," "thy," "thine" → use "you," "your," "yours"
- "hath," "doth," "saith" → use "has," "does," "says"
- "goest," "takest," "dealest," "killedst" → use "go," "take," "deal," "killed"
- "ye" → use "you"
- "behold" → use "look," "see," or integrate naturally (context-dependent)
- "wherefore" → use "why"
- "unto" → use "to"
- "lest" → acceptable in formal contexts, but prefer "so that...not" when more natural
- "ought" (meaning "anything") → use "anything"
- "to wit" → use "to see" or "to know"
- "whence," "thence," "hither," "thither" → use modern equivalents

**Exception:** When God is speaking in formal declaration or when the text is clearly elevated/liturgical, slightly heightened diction is acceptable — but never archaic grammar. "I AM WHO I AM" is fine. "Thou goest" is not.

**Exception:** Direct divine speech may retain "My" (capitalized) for God's self-reference when contextually appropriate.

**Self-check:** Read your rendering aloud. If it sounds like it was written before 1900, modernize it.

---

## Summary

| Rule | Issue | Fix |
|------|-------|-----|
| 1 | Rendering matches KJV verbatim | Translate independently from Hebrew; compare against KJV and rewrite if matching |
| 2 | Generic/boilerplate translator notes | Every note must reference specific Hebrew, translation choices, or verse-level context |
| 3 | Archaic pronouns and verb forms | Use consistent modern English; no thou/thee/hath/goest/ye/behold |

These rules apply to all future generation. Chapters 2-10 of Exodus should be regenerated with these corrections applied.
