from emojiNorm import isSingleGrapheme, normalizeEmoji, sequenceStrIntoEmoji

from ..core import DictGenFromJSON


class IamcalEmojiDataDictGen(DictGenFromJSON):
	URI = "https://raw.githubusercontent.com/iamcal/emoji-data/master/emoji.json"
	CACHE_NAME = "emoji-data.js"
	LICENSE_URI = "https://raw.githubusercontent.com/iamcal/emoji-data/master/LICENSE"
	LICENSE_SPDX = "MIT"
	LICENSE_HASH = "7plTp5vyEytZsTQrIX8cN3s9A9nncTAG9sO4nrFZ8ds="
	COPYRIGHT_STRING = "Copyright (c) 2013 Cal Henderson"

	def convert(self, gemojiOneSourceJSON):
		res = {}
		for d in gemojiOneSourceJSON:
			k = d["short_name"]
			m = origM = sequenceStrIntoEmoji(d["unified"])
			#m = normalizeEmoji(origM)
			assert isSingleGrapheme(m), m + " " + origM
			res[k] = m
			for k in d["short_names"]:
				res[k] = m
		return res
