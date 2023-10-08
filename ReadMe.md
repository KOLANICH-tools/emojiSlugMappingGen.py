emojiSlugMappingGen.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
======================
~~[wheel (GitLab)](https://gitlab.com/KOLANICH-tools/emojiSlugMappingGen.py/-/jobs/artifacts/master/raw/dist/emojiSlugMappingGen-0.CI-py3-none-any.whl?job=build)~~
~~[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-tools/emojiSlugMappingGen.py/workflows/CI/master/emojiSlugMappingGen-0.CI-py3-none-any.whl)~~
~~![GitLab Build Status](https://gitlab.com/KOLANICH-tools/emojiSlugMappingGen.py/badges/master/pipeline.svg)~~
~~![GitLab Coverage](https://gitlab.com/KOLANICH-tools/emojiSlugMappingGen.py/badges/master/coverage.svg)~~
~~[![GitHub Actions](https://github.com/KOLANICH-tools/emojiSlugMappingGen.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-tools/emojiSlugMappingGen.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-tools/emojiSlugMappingGen.py.svg)](https://libraries.io/github/KOLANICH-tools/emojiSlugMappingGen.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

**We have moved to https://codeberg.org/KOLANICH-tools/emojiSlugMappingGen.py, grab new versions there.**

Under the disguise of "better security" Micro$oft-owned GitHub has [discriminated users of 1FA passwords](https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13/) while having commercial interest in success of [FIDO 1FA specifications](https://fidoalliance.org/specifications/download/) and [Windows Hello implementation](https://support.microsoft.com/en-us/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422) which [it promotes as a replacement for passwords](https://github.blog/2023-07-12-introducing-passwordless-authentication-on-github-com/). It will result in dire consequencies and is competely inacceptable, [read why](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

If you don't want to participate in harming yourself, it is recommended to follow the lead and migrate somewhere away of GitHub and Micro$oft. Here is [the list of alternatives and rationales to do it](https://github.com/orgs/community/discussions/49869). If they delete the discussion, there are certain well-known places where you can get a copy of it. [Read why you should also leave GitHub](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

---

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
