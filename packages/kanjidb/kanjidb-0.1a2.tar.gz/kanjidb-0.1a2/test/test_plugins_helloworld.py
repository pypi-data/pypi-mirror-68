# -*- coding: utf-8 -*-
__all__ = ["PluginsHelloWorldTestCase"]
import os
import unittest
from kanjidb import builder
from kanjidb.builder.plugins import helloworld
import kanjidb.encoding

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SAMPLE_TXT = os.path.join(DATA_DIR, "sample_helloworld.yml")


class PluginsHelloWorldTestCase(unittest.TestCase):
    def test_plugin(self):
        """Running via Plugin interface.
        """
        plugin = helloworld.Plugin()
        config = plugin.required_config
        config.update(
            {
                "outputs": [
                    {
                        "type": "stream",
                        "encoding": kanjidb.encoding.UNICODE_ESCAPE,
                        "path": "-",
                    }
                ]
            }
        )

        plugin.configure(global_config={}, plugin_config=config)

        plugin()

    def test_run(self):
        """Running via code.
        """
        helloworld.run()

    def test_sample(self):
        builder.main([SAMPLE_TXT])


if __name__ == "__main__":
    unittest.main()
