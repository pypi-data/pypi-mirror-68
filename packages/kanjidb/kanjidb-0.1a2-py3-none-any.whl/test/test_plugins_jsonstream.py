# -*- coding: utf-8 -*-
__all__ = ["JSONStreamTestCase"]
import sys
import unittest
from kanjidb.builder.plugins import jsonstream

UTF8_OUTPUT = """{
"一": {},
"二": {}
}"""


class JSONStreamTestCase(unittest.TestCase):
    def test_dump(self):
        db = {"一": {}, "二": {}}
        jsonstream.dump(db, "-", sort_keys=True)


if __name__ == "__main__":
    unittest.main()
