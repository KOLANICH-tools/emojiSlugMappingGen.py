emojiSlugMappingGen.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
======================
~~[wheel (GitLab)](https://gitlab.com/KOLANICH-tools/emojiSlugMappingGen.py/-/jobs/artifacts/master/raw/dist/emojiSlugMappingGen-0.CI-py3-none-any.whl?job=build)~~
~~[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-tools/emojiSlugMappingGen.py/workflows/CI/master/emojiSlugMappingGen-0.CI-py3-none-any.whl)~~
~~![GitLab Build Status](https://gitlab.com/KOLANICH-tools/emojiSlugMappingGen.py/badges/master/pipeline.svg)~~
~~![GitLab Coverage](https://gitlab.com/KOLANICH-tools/emojiSlugMappingGen.py/badges/master/coverage.svg)~~
~~[![GitHub Actions](https://github.com/KOLANICH-tools/emojiSlugMappingGen.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-tools/emojiSlugMappingGen.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-tools/emojiSlugMappingGen.py.svg)](https://libraries.io/github/KOLANICH-tools/emojiSlugMappingGen.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

This is a tool to generate mappings from emoji slugs into emojis for use by tools doing automatic replacements.

To generate mappings in `mo` format, type

```bash
python3 -m emojiSlugMappingGen -l license.txt > emoji.mo
```

To generate mappings in `json` format, type

```bash
python3 -m emojiSlugMappingGen -f json:fancy -l license.txt > emoji.json
```

Pregenerated files [can be downloaded here](https://github.com/KOLANICH-tools/emojifilt.cpp/files/10667460/emoji.zip).

## Limitations
Currently some compound emoji (i.e. `"👩🏿\u200d❤\ufe0f\ufe0f\u200d👨🏻"`) can contain a sequence of 2 presentation selectors right after each other (`\ufe0f\ufe0f`). `emojiNorm.normalizeEmoji` (intended to fix artificially created (i.e from the incomplete data, such as GitHub emoji API endpoint, that excludes zwjs and presentation selectors)/edited emoji sequencies) breaks those emoji since it first strips all emoji presentation selectors, and then generates them from scratch. It seems that for those emoji the only way is to remember that they are constructed this way. Currently I'm not sure how to handle them, so they are broken.

I guess for now this can be mitigated by non-doing normalization in some cases.
