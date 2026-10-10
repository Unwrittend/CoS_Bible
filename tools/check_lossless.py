"""Verify every non-blank source line appears exactly as often across the split files
(frontmatter stripped) as in the original. usage: check_lossless.py <orig.md> <out_dir> <file>..."""
import sys
from collections import Counter

orig, out, paths = sys.argv[1], sys.argv[2], sys.argv[3:]


def norm(text):
    return [l.strip() for l in text.split("\n") if l.strip()]


def strip_fm(text):
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4)
        return text[end + 5:]
    return text


a = Counter(norm(open(orig, encoding="utf-8").read()))
b = Counter()
for p in paths:
    b.update(norm(strip_fm(open(p, encoding="utf-8").read())))

missing, extra = a - b, b - a
print(f"original lines: {sum(a.values())}  split lines: {sum(b.values())}")
print(f"missing: {sum(missing.values())}  extra: {sum(extra.values())}")
for l, n in list(missing.items())[:20]:
    print("MISSING", n, l[:100])
for l, n in list(extra.items())[:20]:
    print("EXTRA", n, l[:100])
sys.exit(1 if missing or extra else 0)
