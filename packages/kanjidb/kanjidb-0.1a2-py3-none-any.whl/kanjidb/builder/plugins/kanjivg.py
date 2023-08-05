__all__ = ["Plugin", "load"]
import os
from kanjidb.builder.plugins import PluginBase
from kanjidb import encoding


class Plugin(PluginBase):
    @property
    def template_config(self):
        return {"sources": "vectorials/"}

    @property
    def required_config(self):
        config = self.template_config
        config.update({"input": {"type": "var", "name": "db"}})

        return config

    def __call__(self, **kwargs):
        """Fill database with Kanjidic2 infos.

        :param db: database
        """
        run(input=self.plugin_config["input"], kwargs=kwargs)

        return kwargs

    def __repr__(self):
        return "KanjiVG"


def run(input, *, kwargs):
    """Produce a JSON dict containing kanjis data from a Kanjidic2 XML file
    (`download here <http://www.edrdg.org/wiki/index.php/KANJIDIC_Project>`_).

    Kanjidic2 contains the whole dictionary, but only kanjis read from
    input streams are generated.

    Configuration:

    .. code-block:: yaml

        run:
        - kanjidic2:
          kd2_file: string
          inputs:
          - type: stream|var
            [separator: string] # stream only
            [encoding: string] # stream only
            [path: string] # stream only
            [name: string] # var only
          outputs:
          - type: stream|var
            [path: string] # stream only
            [indent: int] # stream only
            [name: string] # var only

    Generate data for kanjis read from stdin:

    .. code-block:: yaml

        run:
        - kanjidic2:
          kd2_file: path/to/kanjidic2.xml
          inputs:
          - type: stream
            encoding: utf8
            separator: "\\n"
            path: "-"
          outputs:
          - type: var
            name: result

    Python equivalent:

    .. code-block:: python

        from kanjidb.builder.plugins import kanjidic2

        result = kanjidic2.run(
            kd2_file="path/to/kanjidic2.xml",
            inputs=[{
                "type": "stream",
                "encoding": "utf8",
                "separator": "\\n",
                "path": "-"
            }]
        )

    Read kanjis from file and export generated data to file:

    .. code-block:: yaml

        run:
        - kanjidic2:
          kd2_file: path/to/kanjidic2.xml
          inputs:
          - type: stream
            encoding: utf8
            separator: "\\n"
            path: path/to/kanjis.txt
          outputs:
          - type: stream
            indent: 4
            path: path/to/db.json

    Python equivalent:

    .. code-block:: python

        from kanjidb.builder.plugins import kanjidic2

        kanjidic2.run(
            kd2_file="path/to/kanjidic2.xml",
            inputs=[{
                "type": "stream",
                "encoding": "utf8",
                "separator": "\\n",
                "path": "path/to/kanjis.txt"
            }],
            outputs=[{
                "type": "stream",
                "indent": 4,
                "path": "path/to/db.json"
            }]
        )

    :param inputs: input streams
    :param output: output streams
    :param kwargs: context
    :return: a JSON object with kanjis data
    """
    db = kwargs[input["name"]]

    for kanji, data in db.items():
        cp = encoding.get_codepoint(kanji)
        if len(cp) < 5:
            cp = "0{}".format(cp)
        filename = "{}.svg".format(cp)

        data["vectorial"] = (
            filename
            if os.path.isfile(os.path.join(self.plugin_config["sources"], filename))
            else None
        )
