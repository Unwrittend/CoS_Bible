---
title: "Conventions & canonicity rules"
type: "meta"
nav_order: 3
---

# SECTION 2: TONE & STYLE GUIDE

## Campaign Atmosphere

This campaign runs a **gothic horror** register — psychologically rich, atmospherically dense, and thematically concerned with grief, captivity, identity, and the seductive nature of darkness. Barovia is not merely a backdrop; it is an active antagonist with its own moods and pressures.

  

Players will have privileged knowledge that they will need to choose to share or not share.

## Primary Narrative Voice: Darkest Dungeon Narrator Style

All scene narration and GM-facing prose should draw on the **Darkest Dungeon narrator** as a model:

  

  - **Victorian Gothic diction** — elevated, slightly archaic, never modern or casual
  - **Fatalism** — the environment and situation are described as almost inevitably oppressive; hope is fragile and hard-won
  - **Personified environments** — the village, the fog, the castle are described as *feeling* and *intending*, not merely existing
  - **Aphoristic rhythm** — sentences often land with the weight of a proverb; short declarative beats follow longer build-ups
  - **Never comedic or ironic** — the tone is sincere and relentless

  

*Example of correct register:* "The inn offers warmth, but not comfort. Its walls have absorbed too many desperate nights for that."

  

*Example of incorrect register:* "The tavern looks pretty sketchy. There's a creepy barkeep and some shady folks in the corner."

## Secondary Influences

  - **Dragnacarta's Curse of [Strahd](npcs/strahd-von-zarovich.md) Reloaded** is the **secondary source** for all NPC characterization and motivations. It is used for inspiration and ideas
  - **MandyMod's** homebrewed content is also used as a secondary resource for additional idea generation
  - Character voice work (dialogue, letters, internal monologue) may draw on specific additional references noted in individual NPC entries below. If something is in any of the below sections, it is prioritized as the primary source for this campaign.

## Formatting Defaults

Unless instructed otherwise, all creative outputs should follow these conventions:

  

  - **Scene narrations:** Concise and short; read-aloud quality prose. Does not give directions / "control" players
  - **Dialogue:** In-character, no stage directions unless specifically requested
  - **Letters/journals:** Full literary voice matching the character's personality
  - **Design notes:** After every creative output, provide a brief paragraph of design notes explaining the key mechanical or thematic choices made — what pivot point was chosen, what was emphasized, and why
  - **Summarization of Sessions**: Do not embellish. Keep concise and to the main plot points and key characterizations.
  - **Multi-NPC or branching encounter scenes:** Use screenplay format (see [Section 6](templates.md) template) rather than prose narration. This is the default for any scene involving dialogue with conditional player responses, multiple NPCs in conversation, or a sequence with distinct narrative beats.
  - **Canonicity tagging (added 2026-08-30):** Content that originates from GM-to-GM worldbuilding/ideation sessions (as opposed to actual play) is tagged **\[IDEA — NONCANONICAL\]** wherever it appears in this document. Untagged content reflects either established published-module baseline or events that have actually occurred in a logged session. See Section 8 for the full maintenance rule.

  

# SECTION 8: MAINTENANCE NOTES

*For your own reference — how to keep this document useful over time.*

  

**After each gameplay session:**

  

  - Add 3–5 bullet points to the Session Log covering key decisions, revelations, and NPC interactions
  - Update any NPC's "Current narrative status" if something changed. Mark changes from a session as canonical.
      
    1.  If something was previously marked as an idea or noncanonical but occurred during a session. Have it updated to be marked as canonical

  

**After an ideation / planning session between Michelle and I**

  

  - Update campaign bible according to discussed topics. Mark these updates an inspirations / ideas but noncanonical
  - **Tagging convention (added 2026-08-30):** flag ideation-sourced content inline as **\[IDEA — NONCANONICAL\]** at the start of the relevant heading or bullet, so it's unambiguous at a glance which parts of this document reflect actual play vs. GM-only brainstorming. When a session canonizes an idea, remove the tag and fold the confirmed version into the relevant NPC/item/session entry, noting what changed.
  - When a worldbuilding session directly contradicts something already in this bible, flag it as **REVISION** rather than silently overwriting the old text, and note which version is currently preferred — this document has a running history of a few such revisions (see [Section 9](lore/cosmology.md)).
  - **Skill-assisted maintenance note (added 2026-09-06):** Chris now uses a Claude skill ("cos-bible-maintainer") to apply this section's rules automatically when he asks for an update — from a session transcript or notes, or from an ideation session. That skill also auto-backs up this doc (dated copy) before each edit, and auto-folds confirmed ideation into canon for gameplay/roleplay sessions per the rule above — it does not do this for ideation sessions, which still get tagged fresh per the rule above.
  - **Storage note (added 2026-09-07; corrected 2026-09-24):** the campaign bible lives in the shared **"CoS Bible"** Drive folder as two permanent files that always hold identical content:
      - **`campaign-bible.md`** — plain markdown and the **single source of truth**, so both Chris's and Michelle's AI tools read the same file without Google Docs conversion issues.
      - **"CoS Campaign Bible — Doc Mirror (for Project Knowledge sync)"** — a native Google Doc copy. It exists only because Claude Project Knowledge live-syncs Google Docs, not arbitrary Drive files. Read it; don't edit it directly. If someone does, the skill folds those edits back into the .md on its next run.
      - **Both files are edited in place** (the "[Unwrittend](players.md)'s Google Drive" connector's `file_update`), so their file IDs and links never change and neither is ever deleted and recreated. *(What changed: the 2026-09-07 note said the connector couldn't edit files in place and that each update replaced the file; that is no longer true.)*
      - Files named `CoS Campaign Bible - <DDMonYY HH:MM> Bkp.md` alongside them are dated backups taken before each update — superseded snapshots, not the current version.

  

**When developing a new NPC:**

  

  - Update the Bible using this template:
  - **Profile: \<Character Name\>**
  - **Roleplaying Information**

<!-- end list -->

1.  ***Resonance.*** \<how the NPC should feel to the player during interactions\>
2.  ***Emotions.*** \<NPC's frequent emotions\>
3.  ***Motivations.*** \<NPC motivations\>

<!-- end list -->

  - **Character Information**

<!-- end list -->

1.  ***Persona.*** \<What their knowledge is and who they are\>
2.  ***Morale.*** \<How they interact in a fight\>
3.  ***Relationships.*** \<Key relationships with PCs and NPCs\>

<!-- end list -->

  - For minor/supporting NPCs, the shorter stub format (Source characterization / Role / Key characterization principles / Voice notes if relevant / Current narrative status) remains acceptable — omit the Psychological core placeholder line from the older template at the bottom of [Section 4](npcs/index.md); it isn't used in practice.

  

**When your tone preferences evolve:**

  

  - Update Section 2 so future outputs automatically match your current vision

  

**Version control:**

  

  - Create a backup of the .md whenever updating the bible, named `CoS Campaign Bible - <DDMonYY HH:MM> Bkp.md` (e.g., `CoS Campaign Bible - 24Sep26 20:59 Bkp.md`). The skill does this automatically.

  
