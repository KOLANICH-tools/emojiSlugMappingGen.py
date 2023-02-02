import sys
from pathlib import Path
from urllib.parse import urlparse

from emojiNorm import isSingleGrapheme, normalizeEmoji, sequenceStrIntoEmoji

from ..core import DictGenFromJSON


class EmojiLookupDictGen(DictGenFromJSON):
	URI = "https://raw.githubusercontent.com/subpath/emoji-lookup/main/shortnames.json"
	CACHE_NAME = "emoji-lookup.py"
	LICENSE_URI = "https://raw.githubusercontent.com/subpath/emoji-lookup/main/LICENSE"
	LICENSE_SPDX = "CC0-1.0"
	LICENSE_HASH = "ogEPNDSH0/dhiv/lT3ifVIdgIzHAqNA/SemnxUfPBJk="
	COPYRIGHT_STRING = ""

	def convert(self, emojis):
		res = {}
		for k, v in emojis.items():
			#v = normalizeEmoji(v)
			assert isSingleGrapheme(v)
			k = k[1:-1]
			if k:
				res[k] = v
		return res
