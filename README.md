# torture-txt-md
torture the file by opening or saving it in various text editors and seeing if it has material changes.
* Use make_torture.py to generate the test file (torture.md),
* copy the generated file ('copy.md'), open or save it in the text editor of choice,
* then run check_roundtrip.py torture.md copy.md to check for changes.
Includes an html block, a md table, etc...
Created with Claude Opus 5.
