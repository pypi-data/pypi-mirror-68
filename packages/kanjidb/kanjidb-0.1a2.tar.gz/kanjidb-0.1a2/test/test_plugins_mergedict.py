# -*- coding: utf-8 -*-
__all__ = ["PluginsMergeDictTestCase"]
import os
import unittest
from kanjidb import builder
from kanjidb.builder.plugins import mergedict

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SAMPLE_TXT = os.path.join(DATA_DIR, "sample_mergedict.yml")

FIRST = {"a": None}
SECOND = {"a": True}
RESULT = dict(FIRST)
RESULT.update(SECOND)


class PluginsMergeDictTestCase(unittest.TestCase):
    def test_plugin(self):
        """Running via Plugin interface.
        """
        plugin = mergedict.Plugin()
        config = plugin.required_config
        config.update(
            {"inputs": ["first", "second"], "output": "result",}
        )

        plugin.configure(global_config={}, plugin_config=config)

        result = plugin(first=FIRST, second=SECOND)
        self.assertTrue("result" in result, "Invalid output")
        self.assertEqual(result["result"], RESULT, "Invalid result")

    def test_run(self):
        """Running via code.
        """
        result = mergedict.run(
            inputs=["first", "second"], kwargs={"first": FIRST, "second": SECOND},
        )

        self.assertTrue(result, "Invalid output")
        self.assertEqual(result, RESULT, "Invalid result")

    def test_sample(self):
        builder.main([SAMPLE_TXT])


if __name__ == "__main__":
    unittest.main()
