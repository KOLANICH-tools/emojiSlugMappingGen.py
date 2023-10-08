from .cldr import CLDRDictGen, EmojiHelperDictGen, OpenMojiDictGen
from .emoji_lookup import EmojiLookupDictGen
from .gemoji import GemojiDictGen
from .gemojione import GemojiOneDictGen
from .iamcal import IamcalEmojiDataDictGen

# https://github.com/sphinx-contrib/emojicodes/blob/master/sphinxemoji/codes.json - seems like Unicode emoji file derived

# later ones override earlier ones
backends = [
	CLDRDictGen,  # official data by Unicode consorcium

	#OpenMojiDictGen,   # almost the same data, as in CLDRDictGen, + BY-SA license
	#EmojiHelperDictGen,  # same data, as in OpenMojiDictGen
	#DemojiDictGen,  # same data, as in the official data by Unicode consorcium + own license in the repo

	EmojiLookupDictGen,
	IamcalEmojiDataDictGen,
	GemojiOneDictGen,
	GemojiDictGen,
]
