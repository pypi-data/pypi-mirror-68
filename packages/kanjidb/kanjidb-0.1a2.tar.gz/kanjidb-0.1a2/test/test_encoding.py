# -*- coding: utf-8 -*-
__all__ = ["EncodingTestCase"]
import unittest
from kanjidb.encoding import decode, encode, UNICODE_ESCAPE, UNICODE_PLUS, UTF8


class EncodingTestCase(unittest.TestCase):
    def test_decode(self):
        self.assertEqual(decode("U+4e00", encoding=UNICODE_PLUS), "一")
        self.assertEqual(decode("U4e00", encoding=UNICODE_PLUS), "一")
        self.assertEqual(decode(r"\u4e00", encoding=UNICODE_ESCAPE), "一")
        self.assertEqual(decode("一", encoding=UTF8), "一")
        self.assertEqual(decode("一"), "一")

    def test_encode(self):
        self.assertEqual(encode("一", encoding=UNICODE_PLUS), "U+4e00")
        self.assertEqual(encode("一", encoding=UNICODE_PLUS, prefix="U"), "U4e00")
        self.assertEqual(encode("一", encoding=UNICODE_ESCAPE), r"\u4e00")
        self.assertEqual(encode("一", encoding=UTF8), "一")
        self.assertEqual(encode("一"), "一")


if __name__ == "__main__":
    unittest.main()
