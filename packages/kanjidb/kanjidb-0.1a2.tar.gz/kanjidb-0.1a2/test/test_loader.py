# -*- coding: utf-8 -*-
__all__ = ["LoaderTestCase"]
import os
import unittest
from kanjidb.encoding import UNICODE_PLUS
from kanjidb import loader

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KANJIS_UTF8_TXT = os.path.join(DATA_DIR, "kanjis_utf8.txt")
KANJIS_UNICODE_TXT = os.path.join(DATA_DIR, "kanjis_unicode.txt")


class LoaderTestCase(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
