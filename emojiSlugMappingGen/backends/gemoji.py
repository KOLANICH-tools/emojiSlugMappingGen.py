from emojiNorm import isSingleGrapheme, normalizeEmoji

from ..core import DictGenFromJSON


class GemojiDictGen(DictGenFromJSON):
	URI = "https://raw.githubusercontent.com/github/gemoji/master/db/emoji.json"
	CACHE_NAME = "gemoji"
	LICENSE_URI = "https://raw.githubusercontent.com/github/gemoji/master/LICENSE"
	LICENSE_SPDX = "MIT"
	LICENSE_HASH = "fqHR/QYC5mI7mmXnkUmaDqWi9fYPkb+teMuu7hnaJuY="
	COPYRIGHT_STRING = "Copyright (c) 2019 GitHub, Inc."

	def convert(self, gemojiOneSourceJSON):
		res = {}
		for d in gemojiOneSourceJSON:
			m = origM = d["emoji"]
			#m = normalizeEmoji(origM)
			assert isSingleGrapheme(m), m + " " + origM
			for a in d["aliases"]:
				res[a] = m
		return res
