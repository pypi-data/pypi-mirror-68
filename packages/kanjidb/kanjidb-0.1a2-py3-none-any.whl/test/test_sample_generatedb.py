# -*- coding: utf-8 -*-
__all__ = ["PluginsKanjidic2TestCase"]
import os
import unittest
from kanjidb import builder
from kanjidb.builder.plugins import kanjistream, kanjidic2

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KANJIDIC2_XML = os.path.join(DATA_DIR, "kanjidic2.xml")
KANJIS_UTF8_TXT = os.path.join(DATA_DIR, "kanjis_utf8.txt")
SAMPLE_TXT = os.path.join(DATA_DIR, "sample_kanjidic2.yml")


class PluginsKanjidic2TestCase(unittest.TestCase):
    def test_plugin(self):
        plugin = kanjidic2.Plugin()
        config = plugin.required_config
        config.update(
            {
                "inputs": [{"type": "var", "name": "kanjis"}],
                "outputs": [{"type": "var", "name": "db"}],
                "kd2_file": KANJIDIC2_XML,
            }
        )
        plugin.configure(global_config={}, plugin_config=config)

        result = plugin(kanjis=kanjistream.load(KANJIS_UTF8_TXT, sep=";"))
        print(result)
        self.assertTrue("db" in result, "Invalid output")
        db = result["db"]
        self.assertTrue(len(db) == 2, "Invalid result")

    def test_run(self):
        db = kanjidic2.run(
            inputs=[{"type": "var", "name": "kanjis"}],
            outputs=[{"type": "var", "name": "db"}],
            kd2_file=KANJIDIC2_XML,
            kwargs={"kanjis": kanjistream.load(KANJIS_UTF8_TXT, sep=";")},
        )

        self.assertTrue(len(db) == 2, "Invalid result")

    def test_sample(self):
        builder.main([SAMPLE_TXT])


if __name__ == "__main__":
    unittest.main()
