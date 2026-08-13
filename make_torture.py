#!/usr/bin/env python3
"""
make_torture.py -- generate a byte-exact markdown round-trip torture file.

Purpose: open the generated file in an editor, CHANGE NOTHING, save, then diff.
Any difference is the editor normalizing your file.

Usage:
    python make_torture.py               # writes ./torture.md
    python make_torture.py OUTPATH       # writes to OUTPATH

Deliberate byte-level features (invisible to diff -- use `od -c` / Format-Hex):
    * one section written with CRLF line endings, rest LF
    * a hard line break (exactly two trailing spaces)
    * a line with three trailing spaces (meaningless -- prime deletion target)
    * a "blank" line containing only spaces
    * a literal TAB inside body text and a TAB-indented list item
    * a NO-BREAK SPACE (U+00A0) inside a sentence
    * NO final newline at end of file
    * straight quotes / apostrophes / -- / ... as smart-typography bait
"""

import sys

NBSP = "\u00a0"
TAB = "\t"

# ---------------------------------------------------------------- part 1 (LF)

part1 = [
    "---",
    "# comment inside frontmatter -- does it survive?",
    "title: Round-Trip Torture Test",
    "unquoted_string: don't touch my apostrophe",
    "quoted_string: 'single quoted'",
    "tags: [alpha, beta, gamma]",
    "block_list:",
    "  - one",
    "  - two",
    "version: 1.0",
    "date: 2026-08-13",
    "empty_value:",
    "zzz_key_deliberately_last: if this moves, key order was rewritten",
    "---",
    "",
    "S01 Setext H1 -- should NOT become an ATX heading",
    "==================================================",
    "",
    "S02 Setext H2",
    "-------------",
    "",
    "## S03 ATX heading, no closing hashes",
    "",
    "## S04 ATX heading, with closing hashes ##",
    "",
    "###### S05 deep heading",
    "",
    "## S06 emphasis markers",
    "",
    "Here is *asterisk emphasis* and here is _underscore emphasis_.",
    "Here is **asterisk strong** and here is __underscore strong__.",
    "Here is ***triple*** and ___triple underscore___.",
    "Intra-word: snake_case_word should NOT become emphasis.",
    "",
    "## S07 bullet markers -- three separate lists",
    "",
    "- dash item one",
    "- dash item two",
    "",
    "* star item one",
    "* star item two",
    "",
    "+ plus item one",
    "+ plus item two",
    "",
    "## S08 ordered list numbering",
    "",
    "1. sequential one",
    "2. sequential two",
    "3. sequential three",
    "",
    "1. lazy one",
    "1. lazy two -- all written as 1.",
    "1. lazy three",
    "",
    "3. starts at three",
    "4. continues at four",
    "",
    "5) paren delimiter, not dot",
    "6) second paren item",
    "",
    "## S09 nested list indentation",
    "",
    "- two-space parent",
    "  - two-space child",
    "    - two-space grandchild",
    "",
    "- four-space parent",
    "    - four-space child",
    "        - four-space grandchild",
    "",
    "- tab-indented parent",
    TAB + "- tab-indented child",
    "",
    "1. ordered parent",
    "   - unordered child (3-space, aligned under text)",
    "     1. ordered grandchild",
    "",
    "## S10 line breaks and whitespace",
    "",
    "This line ends with exactly two spaces (hard break).  ",
    "So this should render on a new line.",
    "",
    "This line ends with three trailing spaces (meaningless).   ",
    "The next line is 'blank' but contains four spaces:",
    "    ",
    "Three consecutive blank lines follow this one.",
    "",
    "",
    "",
    "End of the blank-line run.",
    "",
    "There is a literal" + TAB + "TAB in the middle of this sentence.",
    "There is a no-break" + NBSP + "space between 'no-break' and 'space'.",
    "",
    "## S11 paragraph wrapping",
    "",
    "This paragraph is one single very long unwrapped line and it should stay one "
    "single very long unwrapped line because reflowing prose is a destructive "
    "normalization that produces enormous diff noise in version control even "
    "though the rendered output is completely identical.",
    "",
    "This paragraph is hand-wrapped at roughly eighty columns and each of these",
    "line breaks is deliberate. If the editor joins these lines into one long",
    "line, or re-wraps them at a different column, it has rewritten the source.",
    "",
    "## S12 tables",
    "",
    "| Ragged | Table | Here |",
    "|---|:---:|--:|",
    "| a | b | c |",
    "| a much longer cell | x | 1 |",
    "",
    "| Aligned  | Table    | Here     |",
    "| -------- | -------- | -------- |",
    "| a        | b        | c        |",
    "| d        | e        | f        |",
    "",
    "## S13 code blocks",
    "",
    "```python",
    "# backtick fence with language",
    "x = {'a': 1}   # trailing spaces inside code follow -->   ",
    "```",
    "",
    "~~~",
    "tilde fence, no language",
    "~~~",
    "",
    "````",
    "four-backtick fence containing ``` three backticks",
    "````",
    "",
    "    indented code block, four spaces",
    "    second line of indented code",
    "",
    "Inline: `code span` and ``span with ` backtick inside``.",
    "",
    "## S14 raw HTML",
    "",
    "<div align=\"center\">",
    "  <b>raw HTML block</b>",
    "</div>",
    "",
    "Inline <kbd>Ctrl</kbd>+<kbd>S</kbd> and a self-closing <br/> tag.",
    "",
    "<!-- an HTML comment that must survive -->",
    "",
    "## S15 links",
    "",
    "An [inline link](https://example.com \"With Title\") here.",
    "A [reference link][ref-one] and a [collapsed one][].",
    "A bare autolink: <https://example.com/autolink>",
    "A naked URL: https://example.com/naked",
    "An ![image](./img/pic.png) reference.",
    "A footnote reference.[^fn1]",
    "",
    "[ref-one]: https://example.com/one",
    "[collapsed one]: https://example.com/collapsed",
    "",
    "[^fn1]: The footnote body. Definitions at the bottom is a style choice.",
    "",
    "## S16 escapes and literals",
    "",
    "Escaped: \\*not emphasis\\* and \\_not emphasis\\_ and \\# not a heading.",
    "Unescaped literals that an editor may decide to escape: 50% * 3 < 4 > 2.",
    "A lone asterisk * floating in text.",
    "A lone underscore _ floating in text.",
    "Ampersand & and entity &amp; side by side.",
]

# -------------------------------------------------------------- part 2 (CRLF)

part2 = [
    "## S17 CRLF SECTION -- these lines use CRLF endings",
    "",
    "If the whole file comes back as CRLF, or this section comes back as LF,",
    "the editor normalized line endings across the file.",
    "",
    "- crlf bullet one",
    "- crlf bullet two",
]

# ---------------------------------------------------------------- part 3 (LF)

part3 = [
    "## S18 smart typography bait",
    "",
    "Straight quotes: \"double quoted\" and 'single quoted'.",
    "Apostrophe: it's Joe's file, the 1990s, rock 'n' roll.",
    "Dashes: hyphen - en-dash candidate -- em-dash candidate ---.",
    "Ellipsis candidate: wait for it ...",
    "Fractions and math: 1/2 and (c) and (r) and 1 x 2 != 3.",
    "",
    "## S19 blockquotes",
    "",
    "> Quote line one.",
    "> Quote line two.",
    ">",
    "> Second paragraph in quote.",
    "",
    "> Lazy continuation quote",
    "where this line has no marker at all.",
    "",
    "> - bullet inside quote",
    ">   - nested bullet inside quote",
    "",
    ">> double-nested with no space",
    "",
    "## S20 thematic breaks -- three different styles",
    "",
    "---",
    "",
    "***",
    "",
    "___",
    "",
    "## S21 task lists",
    "",
    "- [ ] unchecked task",
    "- [x] checked lowercase x",
    "- [X] checked uppercase X",
    "",
    "## S22 misc inline",
    "",
    "Strikethrough ~~like this~~ and single ~tilde~.",
    "Highlight ==like this== if supported.",
    "Superscript^2^ and subscript~2~ if supported.",
    "Math inline $E = mc^2$ and block:",
    "",
    "$$",
    "\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}",
    "$$",
    "",
    "Emoji shortcode :smile: and literal emoji.",
    "Accented: naive, resume, Zurich, Nino.",
    "",
    "## S23 definition list (pandoc style)",
    "",
    "Term one",
    ": Definition of term one.",
    "",
    "Term two",
    ": Definition of term two.",
    "",
    "## S24 final line -- NO trailing newline after this",
    "",
    "The byte immediately after the final period is EOF, not a newline.",
]


def main() -> None:
    outpath = sys.argv[1] if len(sys.argv) > 1 else "torture.md"

    blob1 = ("\n".join(part1) + "\n\n").encode("utf-8")
    blob2 = ("\r\n".join(part2) + "\r\n").encode("utf-8")
    blob3 = ("\n" + "\n".join(part3)).encode("utf-8")  # no final newline

    data = blob1 + blob2 + blob3

    with open(outpath, "wb") as fh:
        fh.write(data)

    # ---- self-verification: assert the byte-level features actually landed ---
    checks = [
        ("no final newline", not data.endswith(b"\n")),
        ("CRLF present", b"\r\n" in data),
        ("LF-only region present", b"\n## S18" in data),
        ("hard break (2 trailing sp)", b"(hard break).  \n" in data),
        ("3 trailing spaces", b"(meaningless).   \n" in data),
        ("whitespace-only line", b"\n    \n" in data),
        ("literal tab", b"\t" in data),
        ("NBSP", b"\xc2\xa0" in data),
        ("no BOM", not data.startswith(b"\xef\xbb\xbf")),
    ]
    width = max(len(n) for n, _ in checks)
    print(f"wrote {outpath}  ({len(data)} bytes)\n")
    for name, ok in checks:
        print(f"  [{'OK' if ok else 'FAIL'}] {name.ljust(width)}")
    if not all(ok for _, ok in checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
