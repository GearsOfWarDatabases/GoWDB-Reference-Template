"""Brings new screenshots into this reference repository, without anything that identifies you or when they
were taken.

For every image in SOURCE (or the folders given on the command line) that isn't in the ledger yet, by content:
  - saves it here as shot-NNNN.jpg (the next free number), so no Steam date-time names (YYYYMMDDHHMMSS_N.jpg)
  - re-encodes it without metadata (EXIF, comments, Steam/camera tags)
  - sets its file times to 2000-01-01, so they don't show when it was taken either
  - logs it in _import-log.csv (hash, new name, no original name or date) so it's never imported twice

Then sort them into the section folders (Characters/, Weapons/ ...) by hand or with your own script.

  python import-screenshots.py                 import from SOURCE
  python import-screenshots.py D:\\shots        import from another folder instead (several allowed)
  python import-screenshots.py --dry-run       show what would happen, change nothing

Needs: pip install pillow
"""
import csv
import hashlib
import os
import re
import sys
from pathlib import Path

from PIL import Image

# Your game's Steam screenshots folder: Steam\userdata\<your id>\760\remote\<game's app id>\screenshots.
# Empty: pass the folder on the command line instead.
SOURCE = r""

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "_import-log.csv"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
EPOCH_2000 = 946684800  # 2000-01-01 00:00:00 UTC
QUALITY = 92


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_ledger():
    if not LEDGER.exists():
        return set()
    with open(LEDGER, newline="", encoding="utf-8") as f:
        return {row["hash"] for row in csv.DictReader(f)}


def next_number():
    used = [int(m.group(1)) for p in HERE.rglob("shot-*.jpg") if (m := re.fullmatch(r"shot-(\d+)\.jpg", p.name))]
    return max(used, default=0) + 1


def clean_copy(src, dst):
    with Image.open(src) as im:
        im = im.convert("RGB")  # drops alpha and palette; JPEG has neither
        clean = Image.new("RGB", im.size)
        clean.paste(im)  # a fresh image carries none of the original's info/EXIF
        clean.save(dst, "JPEG", quality=QUALITY, optimize=True)
    os.utime(dst, (EPOCH_2000, EPOCH_2000))


def main(argv):
    dry = "--dry-run" in argv
    folders = [Path(a) for a in argv if not a.startswith("--")] or ([Path(SOURCE)] if SOURCE else [])
    if not folders:
        print("Set SOURCE at the top of this script, or give a folder: python import-screenshots.py <folder>")
        return 1
    seen = load_ledger()
    number = next_number()
    new_rows = []
    for folder in folders:
        if not folder.is_dir():
            print(f"Skipping {folder}: not a folder")
            continue
        for src in sorted(p for p in folder.iterdir() if p.suffix.lower() in EXTS):
            digest = file_hash(src)
            if digest in seen:
                continue
            name = f"shot-{number:04d}.jpg"
            print(f"{'Would import' if dry else 'Importing'} {src.name} -> {name}")
            if not dry:
                clean_copy(src, HERE / name)
                new_rows.append({"hash": digest, "file": name})
            seen.add(digest)
            number += 1
    if new_rows:
        write_header = not LEDGER.exists()
        with open(LEDGER, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["hash", "file"])
            if write_header:
                w.writeheader()
            w.writerows(new_rows)
    print(f"{len(new_rows)} imported." if not dry else "Dry run: nothing changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
