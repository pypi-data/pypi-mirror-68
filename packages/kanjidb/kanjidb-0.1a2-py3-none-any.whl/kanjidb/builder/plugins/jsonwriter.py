__all__ = ["Plugin", "dumps", "dump"]
import sys
import os
import json
from kanjidb.builder.plugins import PluginBase


class Plugin(PluginBase):
    """This plugin simply dumps a JSON object to file or stream.

    in: variable
    out: [stream]
    """

    @property
    def template_config(self):
        return {"indent": 4}

    @property
    def required_config(self):
        config = self.template_config
        config.update({"in": "db", "out": ["-"]})

        return config

    def __call__(self, **kwargs):
        db = kwargs[self.plugin_config["in"]]

        dump(
            db, *self.plugin_config["out"], indent=self.plugin_config["indent"],
        )

    def __repr__(self):
        return "JSONWriter"


def dumps(o, *, indent=None):
    """Dump a JSON object.

    :param o: JSON object
    """
    indent = indent if indent is not None else 4

    return json.dumps(o, indent=indent, ensure_ascii=False)


def dump(o, *streams, indent=None):
    """Dump a JSON object to streams.

    Parameter `output` may be a `str` or `filelike` object:

    .. code-block:: python

        # Create and write to "foo.json" file
        with open("foo.json", "wb+") as f:
            save_db(f, db=db)

        # Create and write to "foo.json" file
        save_db("foo.json", db=db)

        # Write to sys.stdout
        save_db(sys.stdout, db=db)

    Parameter `output` may be omitted to print to `sys.stdout`:

    .. code-block:: python

        save_db(db=db)

    Parameter `dumps` can be provided to customize how db is printed:

    .. code-block:: python

        save_db(db=db, dumps=json.dumps)

    :param o: JSON object
    :param streams: output streams
    :param indent: JSON indent level
    :param dumps: dumps JSON database
    :param verbose: verbosity level
    """
    streams = streams if streams else sys.stdout

    content = dumps(o, indent=indent)

    for stream in streams:
        if stream == "-":
            stream = sys.stdout

        # Filelike object
        if hasattr(stream, "write"):
            stream.write(content)
        # For filename
        elif isinstance(stream, str):
            parent = os.path.dirname(stream)
            if parent:
                os.makedirs(parent, exist_ok=True)

            with open(stream, "wb+") as f:
                f.write(content.encode())
        # Unknown output type
        else:
            raise Exception("output expected to be str, filelike or callable")
