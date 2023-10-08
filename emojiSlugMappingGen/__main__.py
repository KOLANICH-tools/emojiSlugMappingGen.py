import argparse
import gettext
import sys
from collections import defaultdict
from io import BytesIO
from pathlib import Path

import transformerz.serialization.json
import transformerz.serialization.libintl
import transformerz.serialization.pon
from transformerz.core import registry as transformerzRegistry

from .backends import backends

try:
	import transformerz.serialization.plist
except ImportError:
	pass

try:
	import transformerz.serialization.yaml
except ImportError:
	pass

try:
	import transformerz.serialization.neon
except ImportError:
	pass

try:
	import transformerz.serialization.msgpack
except ImportError:
	pass

try:
	import transformerz.serialization.bson
except ImportError:
	pass

try:
	import transformerz.serialization.cbor
except ImportError:
	pass


thisDir = Path(__file__).resolve().absolute().parent
licensesDir = thisDir / "licenses"


def main():
	p = argparse.ArgumentParser(description="A tool to generate emoji database")
	p.add_argument("-f", "--format", type=str, default="libintl_mo_with_hashtable", help="Format to serialize")
	p.add_argument("-l", "--license-file", type=str, default=None, help="Where to output license file")
	args = p.parse_args()

	tr = transformerzRegistry[args.format]

	cacheDir = Path(".") / "cache"
	cacheDir.mkdir(exist_ok=True)

	emojis = {}
	licenses = defaultdict(list)
	for bC in backends:
		b = bC()
		generated, licenseBytes = b(cacheDir)
		emojis.update(generated)
		licenses[bC.LICENSE_SPDX].append((licenseBytes, bC.COPYRIGHT_STRING))
	emojis = type(emojis)(sorted(emojis.items(), key=lambda x: x[0]))

	if args.format in {"libintl_mo_with_hashtable", "libintl_mo"}:
		print("Serializing", file=sys.stderr)
		moFile = tr.unprocess(emojis)

		print("Self-check - parsing mo", file=sys.stderr)
		with BytesIO(moFile) as fp:
			t = gettext.GNUTranslations(fp)

		print("Self-check - checking mo contents", file=sys.stderr)
		for k, v in emojis.items():
			if t.gettext(k) != v:
				raise KeyError(k)

		print("Dumping into stdout", file=sys.stderr)
		sys.stdout.buffer.write(moFile)
		print("Success!", file=sys.stderr)
	else:
		res = tr.unprocess(emojis)
		if isinstance(res, str):
			sys.stdout.write(res)
		else:
			sys.stdout.buffer.write(res)

	if args.license_file:
		licensesFiles = []
		licensesFiles.extend(sorted(set(licBytes for licBytes, copyrightStr in licenses[None])))
		del licenses[None]

		for spdxId, licDescrs in licenses.items():
			licCopyrightLines = "\n".join(copyrightStr for licBytes, copyrightStr in licDescrs).encode("utf-8")
			licText = (licensesDir / (spdxId + ".md")).read_bytes()
			licText = licText.replace(b"{COPYRIGHT_LINES}", licCopyrightLines)
			licensesFiles.append(licText)

		Path(args.license_file).write_bytes(b"\n\x0c\n".join(licensesFiles))


if __name__ == "__main__":
	main()
