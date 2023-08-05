# -*- coding: utf-8 -*-
__all__ = ["BuilderTestCase"]
import os
import unittest
from kanjidb import builder
from kanjidb.builder.configuration import Configuration

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KANJIDIC2_XML = os.path.join(DATA_DIR, "kanjidic2.xml")
KANJIS_UNICODE_TXT = os.path.join(DATA_DIR, "kanjis_unicode.txt")


class BuilderTestCase(unittest.TestCase):
    def test_build(self):
        config = Configuration(verbose=True)

        builder.build(config)


if __name__ == "__main__":
    unittest.main()
