__all__ = ["Plugin", "run", "load"]
from kanjidb.builder.plugins import PluginBase, kanjistream, jsonstream

try:
    from jamdict.kanjidic2 import Kanjidic2XMLParser
except Exception as e:
    raise Exception("kanjidic2 requires jamdict to be installed") from e


class Plugin(PluginBase):
    @property
    def template_config(self):
        return {
            "inputs": [{"type": "var", "name": "kanjis"}],
            "outputs": [{"type": "var", "name": "db"}],
            "kd2_file": "kd2.xml",
        }

    @property
    def required_config(self):
        return self.template_config

    def __call__(self, **kwargs):
        """Fill database with Kanjidic2 infos.
        """
        run(
            inputs=self.plugin_config["inputs"],
            outputs=self.plugin_config["outputs"],
            kd2_file=self.plugin_config["kd2_file"],
            kwargs=kwargs,
        )

        return kwargs

    def __repr__(self):
        return "Kanjidic2"


def run(inputs, outputs=None, *, kd2_file, kwargs=None):
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
    outputs = outputs if outputs is not None else []
    kwargs = kwargs if kwargs is not None else {}

    # Read kanjis to generate
    kanjis = kanjistream.run(inputs=inputs, kwargs=kwargs)

    # Load external Kanjidic2 XML file
    data = load(kd2_file)
    data = {_.literal: _ for _ in data.characters}
    data = {_: data[_].to_json() for _ in kanjis}

    # Write to output streams
    jsonstream.run(
        inputs=[{"type": "var", "name": "data"}],
        outputs=outputs,
        kwargs={"data": data},
    )

    # Store to variables
    for _ in outputs:
        if _["type"] == "var":
            kwargs[_["name"]] = data

    return data


def load(stream):
    """Load a Kanjidic2 XML file using `jamdict`.

    :param stream: filelike object or filename
    :return: data loaded with `jamdict`.
    """
    parser = Kanjidic2XMLParser()
    if hasattr(stream, "read"):
        return parser.parse_str(stream.read())
    else:
        return parser.parse_file(stream)
