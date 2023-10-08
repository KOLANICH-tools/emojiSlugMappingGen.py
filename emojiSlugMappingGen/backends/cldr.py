import re
import sys
import typing
import unicodedata
from pathlib import Path

from emojiNorm import isSingleGrapheme, normalizeEmoji, stripDiversity, stripDiversityPerson, zwj
from transformerz.text import utf8Transformer

from ..core import DictGenFromJSON, _retrieve


def filterInsignificant(ls):
	for l in ls:
		if l.startswith("#"):
			continue
		if not l:
			continue
		yield l


def extractCodePoints(ls):
	for l in ls:
		yield l.split(" ")[0]


def pointsStringsToRanges(prsS):
	for prs in prsS:
		prs = prs.split("..")
		if len(prs) > 1:
			beg, end = prs
		else:
			beg = end = prs[0]
		beg = int(beg, 16)
		end = int(end, 16)
		yield range(beg, end + 1)


def rangesToPoints(rs):
	for r in rs:
		yield from r


def getAllEmojiCodePoints(self, cldrDataLines: typing.Iterable[str]):
	ls = cldrDataLines
	ls = list(filterInsignificant(ls))
	prsS = extractCodePoints(ls)
	rs = pointsStringsToRanges(prsS)
	return tuple(rangesToPoints(rs))


def digit2word(digit: str) -> str:
	return unicodedata.name(digit).split(" ")[-1]


rxHair = re.compile("((white|curly|blond|red) hair|bald),?")
rxSkin = re.compile("((medium-)?(dark|light)|medium) skin tone,?")
rxGender = re.compile("^(man|woman|person) ")


def processPair(seq, name, res):
	origSeq = seq
	name = name.split(": ")
	if len(name) == 2:
		a, b = name
		a = a.strip()
		b = b.strip()
		if a == "keycap":
			# print(a, b, file=sys.stderr)
			name = b
			if len(name) == 1:
				name = digit2word(name)
		elif a == "flag":
			name = b
		else:
			b, hairMatched = rxHair.subn("", b)
			b, skinMatched = rxSkin.subn("", b)
			b = b.strip()
			if b:
				if b[-1] == ",":
					b = b[:-1]
					b = b.strip()
			name = a
			seq, extracted = stripDiversity(seq, genderDeity=False)
			if len(seq) > 1:
				seq, extractedGenderDeity = stripDiversity(seq, genderDeity=True)
				if "genderDeity" in extractedGenderDeity:
					name, genderMatched = rxGender.subn("", name)
				else:
					# trying to extract
					name1, genderMatched = rxGender.subn("person ", name)
					if genderMatched:
						seq1, extractedGenderPerson = stripDiversityPerson(seq)
						if "genderPerson" in extractedGenderPerson and len(extractedGenderPerson["genderPerson"]) == 1:
							seq = seq1
							name = name1
							extracted.update(extractedGenderPerson)
			# print(seq, extracted, name, ":", b, hairMatched, skinMatched, genderMatched, file=sys.stderr)
	elif len(name) == 1:
		name = name[0]
	else:
		raise ValueError

	seq = normalizeEmoji(seq)

	if seq:
		if not isSingleGrapheme(seq):
			print("Not single emoji according to current icu lib, skipped: ", name + ": " + seq + " " + origSeq, file=sys.stderr)
			return
		name = name.lower().replace(" ", "_")
		res[name] = seq


class CLDRDictGen(DictGenFromJSON):
	__slots__ = ()

	URI = "https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-annotations-derived-full/annotationsDerived/en/annotations.json"
	CACHE_NAME = "cldr-annotations"
	LICENSE_URI = "https://raw.githubusercontent.com/unicode-org/cldr-json/main/LICENSE"
	LICENSE_HASH = "5HRLrKdjwBsVnAtzPlsgatSJ1FqRPsho3SR4EIsmAbg="
	COPYRIGHT_STRING = "Copyright © 1991-2019 Unicode, Inc. All rights reserved. Distributed under the Terms of Use in http://www.unicode.org/copyright.html."

	def convert(self, jsonObj):
		anns = jsonObj["annotationsDerived"]["annotations"]

		res = {}
		for seq, v in anns.items():
			assert len(v["tts"]) == 1
			tts = v["tts"][0]
			processPair(seq, tts, res)

		return res


class OpenMojiDictGen(DictGenFromJSON):
	URI = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/data/openmoji.json"
	CACHE_NAME = "openmoji"
	NAME_ATTR = "annotation"
	LICENSE_URI = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/LICENSE.txt"
	LICENSE_SPDX = "CC-BY-SA-4.0"
	LICENSE_HASH = "XkNv+P+7d9hgciDpvOIMiRXYYAEP7rbB6+9ahWiOmzk="
	COPYRIGHT_STRING = ""

	def convert(self, gemojiOneSourceJSON):
		res = {}
		for d in gemojiOneSourceJSON:
			processPair(d["emoji"], d[self.__class__.NAME_ATTR], res)
		return res


class EmojiHelperDictGen(OpenMojiDictGen):
	"""Seems to be mirroring the data of OpenMoji"""

	URI = "https://raw.githubusercontent.com/jacksalici/emoji-helper/main/npm-package/emoji.json"
	CACHE_NAME = "emoji-helper.js"
	NAME_ATTR = "description"
	LICENSE_URI = "https://raw.githubusercontent.com/jacksalici/emoji-helper/main/LICENSE"
	LICENSE_SPDX = "MIT"
	LICENSE_HASH = "0r4KSfbSk87PZmUEW8qEUdEkGPhQnnmiKqe+AQMpu1I="
	COPYRIGHT_STRING = "Copyright 2022 Giacomo Salici"
