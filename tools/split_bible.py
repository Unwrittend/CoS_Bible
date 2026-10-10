"""ONE-TIME tool (already run 2026-10-10; rerunning overwrites hand edits). Mechanically split the monolithic CoS campaign bible into a Jekyll/GitHub-Pages
friendly folder of small files. Prose is never rewritten: every source line lands
in exactly one output file (verified separately by check_lossless.py).

usage: python3 -I split_bible.py <campaign-bible.md> <out_dir>
"""
import os
import re
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
lines = open(SRC, encoding="utf-8").read().split("\n")

IDEA_TAG = "[IDEA — NONCANONICAL]"

# Hand-written alias map (keyed by output slug).
ALIASES = {
    "von-richten": ["Rudolph van Richten", "Rictavio", "Alenik", "Van Richten"],
    "kasimir-velikov": ["Kasimir", "Casimir"],
    "izek-strazani": ["Isaac", "Izek"],
    "father-lucien-petrovich": ["Lucien", "Lucian"],
    "lugdana": ["Lugdana"],
    "strahds-brides": ["Ludmilla", "Anastrasya", "Anastrasia", "Volenta", "Violetta"],
    "woodcutters-bride": ["Ludmilla Vilisevic", "The Woodcutter's Bride"],
    "strahd-von-zarovich": ["Strahd", "The Devil Strahd"],
    "khirad": ["Void Child", "Khirad", "The Star of Secrets"],
    "esmeralda-davenir": ["Esmeralda"],
    "ismark-the-great": ["Ismark the Great"],
    "madam-eva": ["Eva"],
    "the-martikov-family": ["Martikovs", "Urwin", "Danika"],
    "mad-mary": ["Mary"],
    "ernest-larnack": ["Ernst", "Ernst Larnack"],
    "baron-vargas-volokovich": ["Vargas", "Vargas Vallakovich", "the Burgomaster"],
    "victor-volokovich": ["Victor", "Victor Vallakovich"],
    "lady-fiona-watcher": ["Fiona", "Lady Watcher"],
    "stella-watcher": ["Stella"],
}

# Explicit slugs for headings that don't slugify cleanly.
SLUG_OVERRIDES = {
    "Void Child - Khirad, the Star of Secrets": "khirad",
    "Von Richten (Rudolph van Richten)": "von-richten",
    "Esmeralda D'Avenir (Von Richten's former apprentice)": "esmeralda-davenir",
    'Isaac "Izek" Strazani': "izek-strazani",
    "[NPC TEMPLATE — Copy for new characters]": "npc-template",
    "The Woodcutter's Bride — Ludmilla Vilisevic (Session 9)": "woodcutters-bride",
}


def clean(text):
    """Heading text -> plain title (drop #, markdown emphasis and escapes)."""
    text = re.sub(r"^#+\s*", "", text)
    text = text.replace("\\", "").replace("*", "").strip()
    return re.sub(r"\s+", " ", text)


def slugify(text):
    if text in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[text]
    text = re.split(r"\s+[—–(]\s*|\s+-\s+", text)[0]
    text = text.lower().replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def session_slug(title):
    m = re.search(r"Session\s+(\d+)(?:\.(\d+)([a-z]?))?", title)
    num, half, letter = m.group(1), m.group(2), m.group(3) or ""
    slug = f"s{int(num):02d}"
    if half:
        slug += f"-{half}{letter}"
    return slug, float(num + "." + half) if half else int(num)


def last_session(body):
    nums = [int(n) for n in re.findall(r"Session\s+(\d+)", body)]
    return max(nums) if nums else None


def status_of(body, default="canon"):
    if IDEA_TAG in body or "NONCANONICAL" in body:
        return "mixed" if default == "canon" else default
    return default


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


files = {}   # path -> {"meta": dict, "chunks": [list of lines]}
order = []


def emit(path, chunk, **meta):
    if path not in files:
        files[path] = {"meta": dict(meta), "chunks": []}
        order.append(path)
    else:
        files[path]["meta"].update({k: v for k, v in meta.items() if v is not None})
    files[path]["chunks"].append(chunk)


# ---- 1. find top-level sections -------------------------------------------
tops = [i for i, l in enumerate(lines) if re.match(r"^# SECTION \d+", l)]
first_section = tops[0]
sections = []  # (num_label, title, start, end)
for k, start in enumerate(tops):
    end = tops[k + 1] if k + 1 < len(tops) else len(lines)
    sections.append((clean(lines[start]), start, end))


def find(prefix):
    hits = [s for s in sections if s[0].upper().startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return hits[0]


def split_sub(start, end, level):
    """Split lines[start:end] on headings of exactly `level` #'s.
    Returns (preamble_range, [(heading_line_idx, end_idx), ...])."""
    pat = re.compile(r"^" + "#" * level + r" (?!#)")
    heads = [i for i in range(start, end) if pat.match(lines[i])]
    pre = (start, heads[0] if heads else end)
    parts = [(h, heads[j + 1] if j + 1 < len(heads) else end) for j, h in enumerate(heads)]
    return pre, parts


def seg(a, b):
    return lines[a:b]


# ---- 2. front matter + Section 1 -> about.md ------------------------------
s2 = find("SECTION 2:")
emit("about.md", seg(0, s2[1]), title="About this bible", type="meta", nav_order=90)

# ---- 3. Section 2 + Section 8 -> conventions.md ----------------------------
s8 = find("SECTION 8:")
emit("conventions.md", seg(s2[1], s2[2]), title="Conventions & canonicity rules",
     type="meta", nav_order=3)
emit("conventions.md", seg(s8[1], s8[2]))

# ---- 4. Player characters ---------------------------------------------------
s3 = find("SECTION 3:")
pre, parts = split_sub(s3[1], s3[2], 3)
emit("pcs/index.md", seg(*pre), title="Player Characters", type="section",
     nav_order=10, has_children=True)
for n, (a, b) in enumerate(parts, 1):
    t = clean(lines[a])
    body = "\n".join(seg(a, b))
    emit(f"pcs/{slugify(t)}.md", seg(a, b), title=t, name=t, type="pc",
         parent="Player Characters", nav_order=n, status=status_of(body),
         last_session=last_session(body))

# ---- 5. NPCs ----------------------------------------------------------------
s4 = find("SECTION 4:")
pre, parts = split_sub(s4[1], s4[2], 3)
emit("npcs/index.md", seg(*pre), title="NPCs", type="section", nav_order=11,
     has_children=True)
for n, (a, b) in enumerate(parts, 1):
    raw = clean(lines[a])
    slug = slugify(raw)
    body = "\n".join(seg(a, b))
    if slug == "npc-template":
        emit("npcs/npc-template.md", seg(a, b), title="NPC template", type="template",
             parent="NPCs", nav_order=999, nav_exclude=True)
        continue
    if slug == "strahds-brides":
        title = "Strahd's Brides"
    elif slug == "woodcutters-bride":
        title = "The Woodcutter's Bride (Ludmilla)"
    else:
        title = re.split(r"\s+\(", raw)[0]
    emit(f"npcs/{slug}.md", seg(a, b), title=title, name=raw, type="npc",
         parent="NPCs", nav_order=n, status=status_of(body),
         last_session=last_session(body), aliases=ALIASES.get(slug))

# ---- 6. Items (short entries -> one file) ----------------------------------
s5_items = find("SECTION 5: KEY ITEMS")
body = "\n".join(seg(s5_items[1], s5_items[2]))
emit("items.md", seg(s5_items[1], s5_items[2]), title="Key Items", type="item",
     nav_order=12, status=status_of(body))

# ---- 7. Session log ----------------------------------------------------------
s5_log = find("SECTION 5: SESSION LOG")
pre, parts = split_sub(s5_log[1], s5_log[2], 3)
emit("sessions/index.md", seg(*pre), title="Session Log", type="section",
     nav_order=13, has_children=True)
for n, (a, b) in enumerate(parts, 1):
    t = clean(lines[a])
    slug, num = session_slug(t)
    emit(f"sessions/{slug}.md", seg(a, b), title=t, name=t, type="session",
         parent="Session Log", nav_order=n, session=num, status="canon")

# ---- 8. Templates / tech -----------------------------------------------------
s6 = find("SECTION 6:")
emit("templates.md", seg(s6[1], s6[2]), title="Prompt templates", type="meta", nav_order=91)
s7 = find("SECTION 7:")
emit("tech.md", seg(s7[1], s7[2]), title="Technical reference", type="meta", nav_order=92)

# ---- 9. Lore (Sections 9-12) -------------------------------------------------
emit("lore/index.md", [], title="Lore & Worldbuilding", type="section", nav_order=14,
     has_children=True)
lore = [("SECTION 9:", "cosmology", "Cosmology: Fanes, Strahd's deaths & the Silver Dragon"),
        ("SECTION 10:", "strahd-motivations", "Strahd's motivations & the power struggle"),
        ("SECTION 11:", "tome-of-strahd", "The Tome of Strahd questline"),
        ("SECTION 12:", "vallaki-houses", "Vallaki's noble houses")]
for n, (pfx, slug, title) in enumerate(lore, 1):
    s = find(pfx)
    body = "\n".join(seg(s[1], s[2]))
    emit(f"lore/{slug}.md", seg(s[1], s[2]), title=title, type="lore",
         parent="Lore & Worldbuilding", nav_order=n, status=status_of(body, "idea"))

# ---- 10. Open questions -------------------------------------------------------
s14 = find("SECTION 14:")
emit("open-questions.md", seg(s14[1], s14[2]), title="Open questions", type="meta",
     nav_order=4, status="idea")

# ---- 11. Prep: current + archive ---------------------------------------------
s16 = find("SECTION 16:")
# The trailing "*Last updated: ...*" line belongs to the whole document -> changelog.
s16_end = s16[2]
last_upd = [i for i in range(s16[1], s16_end) if lines[i].startswith("*Last updated:")]
assert len(last_upd) == 1, last_upd
lu = last_upd[0]
emit("prep/index.md", [], title="Prep", type="section", nav_order=15, has_children=True)
emit("prep/s11-vallaki.md", seg(s16[1], lu), title="Session 11 prep — Vallaki",
     type="prep", parent="Prep", nav_order=1, status="idea")
emit("changelog.md", seg(lu, s16_end), title="Changelog", type="meta", nav_order=5)

emit("archive/index.md", [], title="Archive", type="section", nav_order=16,
     has_children=True)
s13 = find("SECTION 13:")
emit("archive/s09-prep.md", seg(s13[1], s13[2]), title="Session 9 prep (superseded)",
     type="prep", parent="Archive", nav_order=2, status="idea")
s15 = find("SECTION 15:")
emit("archive/s10-prep.md", seg(s15[1], s15[2]), title="Session 10 prep (partly played)",
     type="prep", parent="Archive", nav_order=1, status="idea")

# ---- write -------------------------------------------------------------------
FIELD_ORDER = ["title", "name", "aliases", "type", "status", "session", "last_session",
               "parent", "nav_order", "has_children", "nav_exclude"]
for path in order:
    meta = files[path]["meta"]
    fm = ["---"]
    for k in FIELD_ORDER:
        v = meta.get(k)
        if v is None:
            continue
        key = k.replace("_", "-") if k in ("last_session",) else k
        if isinstance(v, bool):
            fm.append(f"{key}: {'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            fm.append(f"{key}: {v}")
        elif isinstance(v, list):
            fm.append(f"{key}: [" + ", ".join(yaml_str(x) for x in v) + "]")
        else:
            fm.append(f"{key}: {yaml_str(v)}")
    fm.append("---")
    body = "\n\n".join("\n".join(c).rstrip("\n") for c in files[path]["chunks"] if c)
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write("\n".join(fm) + "\n\n" + body + ("\n" if body else ""))

# Machine-readable manifest for index generation
import json
json.dump({p: files[p]["meta"] for p in order}, open(os.path.join(OUT, ".split-manifest.json"), "w"),
          indent=1, ensure_ascii=False)
print(f"wrote {len(order)} files")
