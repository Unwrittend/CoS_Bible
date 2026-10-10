"""Cross-link the bible: turn mentions of characters, items, sessions and "Section N"
references into relative markdown links, and maintain a generated "Mentioned in"
backlinks block at the bottom of each entity page.

Rules:
  - Only the first mention of each target per section (text between headings) is linked.
  - Headings, frontmatter, code, existing links and the backlinks block are never touched.
  - A file never links to itself (except to an anchor inside itself, e.g. "Section 9.6").
  - Idempotent: rerunning adds nothing if a section already links to a target.
  - Only link markup is added; the prose itself is unchanged.

usage (from the repo root): python3 tools/link_entities.py
Add new names to TERMS below when a new NPC/item file is created.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_FILES = {"index.md", "entity-index.md", "README.md"}
BL_START, BL_END = "<!-- backlinks:start -->", "<!-- backlinks:end -->"
BACKLINK_TYPES = {"pc", "npc", "item", "session", "lore", "prep"}

# target ("path" or "path#anchor") -> names that refer to it. Case-sensitive, whole words.
TERMS = {
    # Player characters
    "pcs/lyasra.md": ["Lyasra"],
    "pcs/cassandra-priam.md": ["Cassandra Priam", "Cassandra"],
    "pcs/jacob.md": ["Jacob"],
    "pcs/theren.md": ["Theren"],
    "pcs/gaille.md": ["Gaille"],
    "pcs/reyna.md": ["Reyna"],
    # NPCs
    "npcs/dismas.md": ["Dismas"],
    "npcs/reysatra.md": ["Reysatra"],
    "npcs/gertruda-stiegler.md": ["Gertruda Stiegler", "Gertruda"],
    "npcs/mad-mary.md": ["Mad Mary", "Mary"],
    "npcs/violet-larkwing.md": ["Violet Larkwing", "Violet"],
    "npcs/ninthalor.md": ["Ninthalor"],
    "npcs/amogano.md": ["Amogano"],
    "npcs/khirad.md": ["Khirad", "Void Child"],
    "npcs/madam-eva.md": ["Madam Eva"],
    "npcs/strahd-von-zarovich.md": ["Strahd von Zarovich", "Strahd"],
    "npcs/von-richten.md": ["Rudolph van Richten", "Von Richten", "von Richten", "van Richten",
                            "Rictavio", "Alenik", "Alanik"],
    "npcs/arturi.md": ["Arturi"],
    "npcs/esmeralda-davenir.md": ["Esmeralda D'Avenir", "Esmeralda"],
    "npcs/eliza.md": ["Eliza"],
    "npcs/stanimir.md": ["Stanimir"],
    "npcs/baba-lysaga.md": ["Baba Lysaga", "Lysaga"],
    "npcs/argonvost.md": ["Argonvost"],
    "npcs/rahadin.md": ["Rahadin"],
    "npcs/kasimir-velikov.md": ["Kasimir Velikov", "Kasimir", "Casimir"],
    "npcs/petrina-velikanova.md": ["Petrina Velikanova", "Petrina"],
    "npcs/lady-fiona-watcher.md": ["Lady Fiona Watcher", "Fiona Watcher", "Lady Watcher", "Fiona"],
    "npcs/stella-watcher.md": ["Stella Watcher", "Stella"],
    "npcs/victor-volokovich.md": ["Victor Volokovich", "Victor"],
    "npcs/ernest-larnack.md": ["Ernest Larnack", "Ernst Larnack", "Ernest", "Ernst"],
    "npcs/izek-strazani.md": ["Izek Strazani", "Izek", "Isaac"],
    "npcs/saint-markovia.md": ["Saint Markovia", "St. Markovia", "Markovia"],
    "npcs/lugdana.md": ["Lugdana"],
    "npcs/ismark-the-great.md": ["Ismark the Great"],
    "npcs/the-martikov-family.md": ["Martikov family", "Martikovs", "Martikov", "Mardikov",
                                    "Mordakov", "Urwin", "Danika", "Davian"],
    "npcs/baron-vargas-volokovich.md": ["Baron Vargas Volokovich", "Vargas Volokovich",
                                        "Vargas Vallakovich", "Vargas"],
    "npcs/father-lucien-petrovich.md": ["Father Lucien Petrovich", "Father Lucien", "Lucien",
                                        "Lucian"],
    "npcs/morgantha.md": ["Morgantha"],
    "npcs/elaine-groze.md": ["Elaine Groze", "Elaine"],
    "npcs/luvash.md": ["Luvash"],
    "npcs/arrigal.md": ["Arrigal"],
    "npcs/alexei.md": ["Alexei"],
    "npcs/arabelle.md": ["Arabelle"],
    "npcs/ireena-kolyana.md": ["Ireena Kolyana", "Ireena", "Irena"],
    "npcs/strahds-brides.md": ["Strahd's Brides", "Strahd's brides"],
    "npcs/strahds-brides.md#ludmilla-vilisevic": ["Ludmilla Vilisevic", "Ludmilla"],
    "npcs/strahds-brides.md#anastrasya-karelova": ["Anastrasya Karelova", "Anastrasya", "Anastrasia"],
    "npcs/strahds-brides.md#volenta-popofsky": ["Volenta Popofsky", "Volenta", "Violetta"],
    "npcs/woodcutters-bride.md": ["Woodcutter's Bride"],
    # Items
    "items.md#theren--hollow-dragons-tooth": ["Hollow Dragon's Tooth"],
    "items.md#gaille--amber-shard": ["Amber Shard"],
    "items.md#cassandra--dark-ones-tarokka-deck": ["Dark One's Tarokka Deck"],
    "items.md#lyasra--devas-feather": ["Deva's Feather"],
    "items.md#dismas--tin-pendant": ["Tin Pendant"],
    "items.md#jacob--werewolf-fang-bracelet": ["Werewolf Fang Bracelet"],
    "items.md#ring-of-mind-shielding-von-richten": ["Ring of Mind Shielding"],
    "items.md#the-sun-sword": ["Sun Sword"],
    "items.md#the-heart-of-darkness": ["Heart of Darkness"],
    "items.md#the-holy-symbol--amulet-of-ravenkind": ["Holy Symbol of Ravenkind",
                                                      "Amulet of Ravenkind"],
    "items.md#tatyanas-bracelet": ["Tatyana's Bracelet"],
    "items.md#belinda": ["Belinda", "Blinda"],
    "lore/tome-of-strahd.md": ["Tome of Strahd"],
}

# Old monolith section numbers -> files ("Section 5" is ambiguous: items vs session log).
SECTION_FILES = {
    "1": "about.md", "2": "conventions.md", "3": "pcs/index.md", "4": "npcs/index.md",
    "6": "templates.md", "7": "tech.md", "8": "conventions.md", "9": "lore/cosmology.md",
    "10": "lore/strahd-motivations.md", "11": "lore/tome-of-strahd.md",
    "12": "lore/vallaki-houses.md", "13": "archive/s09-prep.md", "14": "open-questions.md",
    "15": "archive/s10-prep.md", "16": "prep/s11-vallaki.md",
}


def gh_anchor(heading):
    """GitHub/kramdown-GFM heading id."""
    text = re.sub(r"^#+\s*", "", heading).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text).replace("_", "")
    return text.replace(" ", "-")


def read(path):
    return open(os.path.join(ROOT, path), encoding="utf-8").read()


def split_fm(text):
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4) + 5
        return text[:end], text[end:]
    return "", text


def fm_field(fm, key):
    m = re.search(r"^" + key + r': "?(.*?)"?$', fm, re.M)
    return m.group(1).replace('\\"', '"') if m else None


files = sorted(p for p in (os.path.relpath(f, ROOT) for f in
                           glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True))
               if not p.startswith(("tools/", "archive/campaign-bible-monolith"))
               and p not in SKIP_FILES)

# Subsection anchors: "Section 15.8" -> archive/s10-prep.md#158--arabelle-undecided
SUBSECTIONS = {}
for num, path in SECTION_FILES.items():
    for line in read(path).split("\n"):
        m = re.match(r"^## (\d+\.\d+) ", line)
        if m:
            SUBSECTIONS[m.group(1)] = f"{path}#{gh_anchor(line)}"

# Session files: "Session 1.5b" -> sessions/s01-5b.md
SESSIONS = {}
for p in files:
    m = re.match(r"sessions/s(\d+)(?:-(\d+)([a-z]?))?\.md$", p)
    if m:
        key = str(int(m.group(1))) + (f".{m.group(2)}{m.group(3)}" if m.group(2) else "")
        SESSIONS[key] = p

term_to_target = {t: tgt for tgt, ts in TERMS.items() for t in ts}
name_alt = "|".join(re.escape(t) for t in sorted(term_to_target, key=len, reverse=True))
TOKEN = re.compile(
    r"(?<![\w\[])(?:"
    r"(?P<section>Section (?P<secnum>\d+(?:\.\d+)?))"
    r"|(?P<session>Session (?P<sesnum>\d+(?:\.\d+[a-z]?)?))"
    r"|(?P<name>" + name_alt + r"))(?![\w])")
PROTECT = re.compile(
    r"`[^`]*`"                                   # inline code
    r"|(?<!\\)\[[^\]]*(?<!\\)\]\([^)]*\)"        # existing markdown link
    r"|<[^>]+>"                                  # html tags / comments
    r"|https?://\S+")


def resolve(m):
    if m.group("section"):
        num = m.group("secnum")
        return SUBSECTIONS.get(num) or SECTION_FILES.get(num.split(".")[0])
    if m.group("session"):
        num = m.group("sesnum")
        return SESSIONS.get(num)
    return term_to_target[m.group("name")]


def rel_link(src, target):
    path, _, anchor = target.partition("#")
    if path == src:
        return "#" + anchor if anchor else None
    rel = os.path.relpath(path, os.path.dirname(src) or ".")
    return rel + ("#" + anchor if anchor else "")


def existing_targets(line, src):
    """Targets already linked in a line, normalized to repo-relative 'path#anchor'."""
    out = set()
    for m in re.finditer(r"(?<!\\)\[[^\]]*(?<!\\)\]\(([^)]*)\)", line):
        url = m.group(1)
        if url.startswith(("http", "mailto")):
            continue
        path, _, anchor = url.partition("#")
        path = os.path.normpath(os.path.join(os.path.dirname(src), path)) if path else src
        out.add(path + ("#" + anchor if anchor else ""))
    return out


def link_body(src, body):
    out, linked, in_code = [], set(), False
    for line in body.split("\n"):
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if in_code or line.lstrip().startswith("```"):
            out.append(line)
            continue
        if line.startswith("#"):
            linked = set()
            out.append(line)
            continue
        linked |= existing_targets(line, src)
        protected = [(m.start(), m.end()) for m in PROTECT.finditer(line)]
        pieces, pos = [], 0
        for m in TOKEN.finditer(line):
            if any(a < m.end() and m.start() < b for a, b in protected):
                continue
            target = resolve(m)
            if not target or target in linked:
                continue
            url = rel_link(src, target)
            if url is None:
                continue
            linked.add(target)
            pieces += [line[pos:m.start()], f"[{m.group(0)}]({url})"]
            pos = m.end()
        out.append("".join(pieces) + line[pos:])
    return "\n".join(out)


def strip_backlinks(body):
    return re.sub(r"\n*" + re.escape(BL_START) + r".*?" + re.escape(BL_END) + r"\n*", "\n",
                  body, flags=re.S)


# ---- pass 1: forward links -------------------------------------------------
meta, bodies = {}, {}
for p in files:
    fm, body = split_fm(read(p))
    body = strip_backlinks(body)
    meta[p] = {"fm": fm, "title": fm_field(fm, "title") or p, "type": fm_field(fm, "type"),
               "session": fm_field(fm, "session")}
    bodies[p] = link_body(p, body)

# ---- pass 2: backlinks -------------------------------------------------------
refs = {p: set() for p in files}
for src, body in bodies.items():
    for line in body.split("\n"):
        for tgt in existing_targets(line, src):
            path = tgt.partition("#")[0]
            if path in refs and path != src:
                refs[path].add(src)


def sort_key(p):
    t = meta[p]["type"] or ""
    order = ["session", "pc", "npc", "item", "lore", "prep", "meta", "section"]
    s = float(meta[p]["session"]) if meta[p]["session"] else 0
    return (order.index(t) if t in order else 99, s, meta[p]["title"].lower())


changed = 0
for p in files:
    body = bodies[p].rstrip("\n")
    if meta[p]["type"] in BACKLINK_TYPES and refs[p]:
        items = [f"- [{meta[s]['title']}]({os.path.relpath(s, os.path.dirname(p) or '.')})"
                 for s in sorted(refs[p], key=sort_key)]
        body += "\n\n" + "\n".join([BL_START, "", "---", "", "**Mentioned in:**", ""] + items
                                   + ["", BL_END])
    new = meta[p]["fm"] + body + "\n"
    if new != read(p):
        open(os.path.join(ROOT, p), "w", encoding="utf-8").write(new)
        changed += 1
print(f"updated {changed} of {len(files)} files")
