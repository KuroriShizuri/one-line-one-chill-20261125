#!/usr/bin/env python3
"""Write the one-line horror entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

The entry is a single sentence of 95 characters. The program writes it
byte-identical, with no trailing newline, and reads it back to confirm.
Python standard library only.
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

ENTRY = "The baby monitor whispered my name in my own voice \u2014 I live alone, and I have never had a baby."


def validate(text):
    """Check the entry against the competition gate: 1-200 chars, not blank."""
    if not 1 <= len(text) <= 200:
        raise ValueError(
            "entry must be 1-200 characters, got %d" % len(text)
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def write_entry(out_dir):
    """Write ENTRY to <out_dir>/entry.txt (no trailing newline)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ENTRY, encoding="utf-8")
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the One Line, One Chill entry."
    )
    parser.add_argument(
        "--check", action="store_true",
        help="validate the entry only, write nothing",
    )
    parser.add_argument(
        "--self-test", action="store_true",
        help="validate and check a byte-identical write/read round-trip "
             "in a temporary directory",
    )
    args = parser.parse_args(argv)

    validate(ENTRY)

    if args.check:
        print("check ok: %d characters, 1 line" % len(ENTRY))
        return 0

    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            target = write_entry(tmp)
            back = target.read_text(encoding="utf-8")
            if back != ENTRY:
                raise SystemExit("self-test failed: round-trip mismatch")
            print("self-test ok: %d characters, byte-identical round-trip"
                  % len(ENTRY))
        return 0

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = write_entry(out_dir)
    back = target.read_text(encoding="utf-8")
    if back != ENTRY:
        raise SystemExit("write failed: entry.txt does not match ENTRY")
    print("wrote %s (%d characters, no trailing newline)"
          % (target, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
