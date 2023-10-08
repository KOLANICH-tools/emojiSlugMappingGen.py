import hashlib
from base64 import b64encode
from pathlib import Path

try:
	import httpx
except ImportError:
	import requests as httpx

from transformerz.serialization.json import jsonFancySerializer
from transformerz.text import utf8Transformer


def _retrieve(uri: str, cacheFileName: Path, serializer=None):
	noCacheFile = not cacheFileName.is_file()
	if noCacheFile:
		bytez = httpx.get(uri).content
	else:
		bytez = cacheFileName.read_bytes()

	if serializer:
		res = serializer.process(bytez)
	else:
		res = bytez

	if noCacheFile:
		if serializer:
			bytez = serializer.unprocess(res)
		cacheFileName.write_bytes(bytez)

	return res


def hash(b: bytes) -> str:
	return b64encode(hashlib.sha256(b).digest()).decode("ascii")


class DictGen:
	__slots__ = ()

	URI = None
	CACHE_NAME = None
	SERIALIZER = None
	LICENSE_URI = None
	LICENSE_SPDX = None
	LICENSE_HASH = None

	def __init__(self):
		if self.__class__.LICENSE_URI == None:
			raise ValueError("License URI must be specified", self.__class__)

	def convert(self, dic):
		raise NotImplementedError

	def retrieve(self, cacheDir: Path):
		cacheFileBaseName = self.__class__.CACHE_NAME + "." + jsonFancySerializer.fileExtension
		cacheFileName = cacheDir / cacheFileBaseName
		licenseCacheFileName = cacheDir / (cacheFileBaseName + ".license")
		licenseTextBytes = _retrieve(self.__class__.LICENSE_URI, licenseCacheFileName)
		licenseHash = hash(licenseTextBytes)
		if self.__class__.LICENSE_HASH != licenseHash:
			raise ValueError("License text has changed", self.__class__, self.__class__.LICENSE_HASH, licenseHash)
		return _retrieve(self.__class__.URI, cacheFileName, self.__class__.SERIALIZER), licenseTextBytes

	def getSourceObject(self, cacheDir: Path):
		return self.retrieve(cacheDir)

	def __call__(self, cacheDir: Path):
		sourceJSON, licenseBytes = self.retrieve(cacheDir)
		return self.convert(sourceJSON), licenseBytes


class DictGenFromJSON(DictGen):
	__slots__ = ()
	SERIALIZER = utf8Transformer + jsonFancySerializer
