# -*- coding: utf-8 -*-
__all__ = ["Plugin", "run", "load", "dump"]
import sys
import functools
import json
from kanjidb.builder.plugins import PluginBase


class Plugin(PluginBase):
    @property
    def template_config(self):
        return {
            "inputs": [{"type": "stream", "path": "-",}],
            "outputs": [{"type": "var", "name": "result"}],
        }

    @property
    def required_config(self):
        config = self.template_config

        return config

    def __call__(self, **kwargs):
        run(
            inputs=self.plugin_config["inputs"],
            outputs=self.plugin_config["outputs"],
            kwargs=kwargs,
        )

        return kwargs

    def __repr__(self):
        return "JSONStream"


def run(inputs, outputs=None, *, kwargs=None):
    """Read/write JSON objects from/to streams.

    Configuration:

    .. code-block:: yaml

        run:
        - jsonstream:
          inputs:
          - type: stream|var
            [path: string] # stream only
            [name: string] # var only
          outputs:
          - type: stream|var
            [path: string] # stream only
            [indent: int] # stream only
            [name: string] # var only

    Read from stdin and store to `result`:

    .. code-block:: yaml

        run:
        - jsonstream:
          inputs:
          - type: stream
            path: "-"
          outputs:
          - type: var
            name: result

    Python equivalent:

    .. code-block:: python

        from kanjidb.builder.plugins import jsonstream

        result = jsonstream.run(
            inputs=[{
                "type": "stream",
                "path": "-"
            }]
        )

    Get from `result` and write to stdout:

    .. code-block:: yaml

        run:
        - jsonstream:
          inputs:
          - type: var
            name: result
          outputs:
          - type: stream
            indent: 4
            path: "-"

    Python equivalent:

    .. code-block:: python

        from kanjidb.builder.plugins import jsonstream

        jsonstream.run(
            inputs=[{
                "type": "var",
                "name": "result"
            }],
            outputs=[{
                "type": "stream",
                "indent": 4,
                "path": "-"
            }],
            kwargs={"result": {...}}
        )

    :param inputs: input streams
    :param outputs: output streams
    :param kwargs: context
    :return: a JSON object read from input streams
    """
    outputs = outputs if outputs is not None else []
    kwargs = kwargs if kwargs is not None else {}

    o = {}

    # Read from inputs
    for _ in inputs:
        if _["type"] == "stream":
            o.update(load(_["path"]))
        elif _["type"] == "var":
            o.update(kwargs[_["name"]])
        else:
            raise Exception("Invalid input {}".format(_["type"]))

    # Write to outputs
    for _ in outputs:
        if _["type"] == "stream":
            dump(o, _["path"], indent=_.get("indent", 4))
        elif _["type"] == "var":
            kwargs[_["name"]] = o
        else:
            raise Exception("Invalid output {}".format(_["type"]))

    return o


def load(*streams, loads=None):
    loads = loads if loads is not None else json.loads

    def wrapper():
        for stream in streams:
            # stdin
            if stream == "-":
                stream = sys.stdin
            # Filelike object
            if hasattr(stream, "read"):
                content = stream.read()
            # Filename
            else:
                with open(stream, "rb") as f:
                    content = f.read().decode()

            yield from loads(content)

    return list(wrapper())


def dump(o, *streams, sort_keys=None, indent=None, dumps=None):
    indent = indent if indent is not None else 4
    dumps = (
        dumps
        if dumps is not None
        else functools.partial(
            json.dumps, indent=indent, sort_keys=sort_keys, ensure_ascii=False
        )
    )

    content = dumps(o)

    for stream in streams:
        # stdout
        if stream == "-":
            stream = sys.stdout.buffer
        # Filelike object
        if hasattr(stream, "write"):
            stream.write(content.encode())
        # Filename
        else:
            with open(stream, "wb") as f:
                f.write(content.encode())
