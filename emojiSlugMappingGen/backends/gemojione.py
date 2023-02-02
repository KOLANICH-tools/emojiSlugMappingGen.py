import sys

from emojiNorm import isSingleGrapheme, normalizeEmoji

from ..core import DictGenFromJSON


class GemojiOneDictGen(DictGenFromJSON):
	URI = "https://raw.githubusercontent.com/bonusly/gemojione/master/config/index.json"
	CACHE_NAME = "gemojione"
	LICENSE_URI = "https://raw.githubusercontent.com/bonusly/gemojione/master/LICENSE.txt"
	LICENSE_SPDX = "MIT"
	LICENSE_HASH = "K/r40A6lx+FY4F8kRgt6odLczHFboXnLBYWjdA9jnIQ="
	COPYRIGHT_STRING = "Copyright (c) 2013 Jonathan Wiesel\n\nOriginal work by Steve Klabnik on [emoji gem](https://github.com/steveklabnik/emoji)"

	def convert(self, gemojiOneSourceJSON):
		res = {}
		for k, d in gemojiOneSourceJSON.items():
			seq = origSeq = d["moji"]
			#seq = normalizeEmoji(origSeq)
			if not isSingleGrapheme(seq):
				print("Not single emoji according to current icu lib, skipped: ", k + ": " + seq + " " + origSeq, file=sys.stderr)
				continue

			res[k] = seq
			for a in d["aliases"]:
				if a[0] == ":" and a[-1] == ":":
					a = a[1:-1]
					res[a] = seq
		return res
