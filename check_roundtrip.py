#!/usr/bin/env python3
"""
check_roundtrip.py -- compare a pristine torture file against the editor-saved copy.

Reports the invisible changes that `diff` shows badly, then a unified diff with
whitespace made visible.

Usage:
    python check_roundtrip.py torture.orig.md torture.md
"""

import difflib
import sys

SMART = {
    "\u2018": "left single quote",
    "\u2019": "right single quote / apostrophe",
    "\u201c": "left double quote",
    "\u201d": "right double quote",
    "\u2013": "en dash",
    "\u2014": "em dash",
    "\u2026": "ellipsis",
}


def visible(line: str) -> str:
    body = line.rstrip("\n")
    n_trail = len(body) - len(body.rstrip())
    body = body.rstrip()
    body = body.replace("\t", "\u2409").replace("\u00a0", "\u2423")
    return body + "\u00b7" * n_trail


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("usage: check_roundtrip.py ORIGINAL SAVED")

    orig_p, saved_p = sys.argv[1], sys.argv[2]
    orig = open(orig_p, "rb").read()
    saved = open(saved_p, "rb").read()

    if orig == saved:
        print("IDENTICAL -- byte-for-byte. This editor is safe for round-trips.")
        return

    print(f"DIFFERENT: {len(orig)} bytes -> {len(saved)} bytes\n")
    print("== invisible / structural changes ==")

    def report(label: str, before, after) -> None:
        flag = "  " if before == after else "**"
        print(f"{flag} {label.ljust(28)} {before!s:>10}  ->  {after!s}")

    report("CRLF line endings", orig.count(b"\r\n"), saved.count(b"\r\n"))
    report("LF-only line endings",
           orig.count(b"\n") - orig.count(b"\r\n"),
           saved.count(b"\n") - saved.count(b"\r\n"))
    report("ends with newline", orig.endswith(b"\n"), saved.endswith(b"\n"))
    report("UTF-8 BOM", orig.startswith(b"\xef\xbb\xbf"), saved.startswith(b"\xef\xbb\xbf"))
    report("literal TAB chars", orig.count(b"\t"), saved.count(b"\t"))
    report("NBSP (U+00A0)", orig.count(b"\xc2\xa0"), saved.count(b"\xc2\xa0"))

    ot = orig.decode("utf-8", "replace")
    st = saved.decode("utf-8", "replace")
    report("lines w/ trailing spaces",
           sum(1 for ln in ot.split("\n") if ln != ln.rstrip()),
           sum(1 for ln in st.split("\n") if ln != ln.rstrip()))

    print("\n== smart-typography substitutions ==")
    any_smart = False
    for ch, name in SMART.items():
        if st.count(ch) != ot.count(ch):
            any_smart = True
            print(f"** {name.ljust(28)} {ot.count(ch):>10}  ->  {st.count(ch)}")
    if not any_smart:
        print("   none")

    print("\n== unified diff (tab=\u2409  nbsp=\u2423  trailing space=\u00b7) ==")
    diff = difflib.unified_diff(
        [visible(x) for x in ot.splitlines(keepends=True)],
        [visible(x) for x in st.splitlines(keepends=True)],
        fromfile=orig_p, tofile=saved_p, lineterm="", n=1,
    )
    shown = 0
    for line in diff:
        print(line)
        shown += 1
        if shown > 400:
            print("... (truncated at 400 diff lines)")
            break


if __name__ == "__main__":
    main()
