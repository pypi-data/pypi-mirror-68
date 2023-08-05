# -*- coding: utf-8 -*-
__all__ = ["JSONWriterTestCase"]
import sys
import unittest
from kanjidb.builder.plugins import jsonwriter

UTF8_OUTPUT = """{
"一": {},
"二": {}
}"""


class JSONWriterTestCase(unittest.TestCase):
    def test_dumps(self):
        db = {"一": {}, "二": {}}
        self.assertEqual(jsonwriter.dumps(db, indent=0), UTF8_OUTPUT)

    def test_dump(self):
        db = {"一": {}, "二": {}}
        jsonwriter.dump(db, sys.stdout)


if __name__ == "__main__":
    unittest.main()
