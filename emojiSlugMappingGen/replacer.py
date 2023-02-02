import gettext
import re

elRx = re.compile(":(?P<name>\w+):")


class Replacer:
	"""
	with Path("./emoji.mo").open("rb") as fp:
		r = Replacer(fp)

	r("sddsd :small_orange_diamond: sdds")
	"""

	__slots__ = ("catalogue",)

	def __init__(self, cat):
		if not isinstance(cat, gettext.GNUTranslations):
			cat = gettext.GNUTranslations(fp)
		self.catalogue = cat

	def _replacer(self, m):
		return self.catalogue._catalog.get(m.group("name"), m.group(0))

	def __call__(self, text: str) -> typing.Tuple[str, int]:
		return elRx.subn(self._replacer, text)
