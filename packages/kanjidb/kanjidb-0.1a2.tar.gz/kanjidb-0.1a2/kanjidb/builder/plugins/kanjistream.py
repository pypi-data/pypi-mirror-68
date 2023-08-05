# -*- coding: utf-8 -*-
__all__ = ["Plugin", "run", "loads", "load", "dump"]
import sys
import os
import functools
import re
from kanjidb.builder.plugins import PluginBase
import kanjidb.encoding


class Plugin(PluginBase):
    @property
    def template_config(self):
        return {
            "inputs": [
                {
                    "type": "stream",
                    "separator": os.linesep,
                    "encoding": kanjidb.encoding.UTF8,
                    "path": "-",
                }
            ],
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
        return "KanjiStream"


def run(inputs, outputs=None, *, kwargs=None):
    """Read/write kanjis from/to streams.

    Given an input stream containing one unicode encoded kanji
    per line such as:

    .. code-block::

        U+4E00
        U+4E8C
        ...

    This plugin will produce a list containing:

    .. code-block::

        ["一", "二", ...]

    Configuration:

    .. code-block:: yaml

        run:
        - kanjistream:
          inputs:
          - type: stream|var
            [separator: string] # stream only
            [encoding: string] # stream only
            [path: string] # stream only
            [name: string] # var only
          outputs:
          - type: stream|var
            [separator: string] # stream only
            [encoding: string] # stream only
            [path: string] # stream only
            [name: string] # var only

    Read from stdin and store to `result`:

    .. code-block:: yaml

        run:
        - kanjistream:
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

        from kanjidb.builder.plugins import kanjistream

        result = kanjistream.run(
            inputs=[{
                "type": "stream",
                "encoding": "utf8",
                "separator": "\\n",
                "path": "-"
            }]
        )

    Get from `result` and write to stdout:

    .. code-block:: yaml

        run:
        - kanjistream:
          inputs:
          - type: var
            name: result
          outputs:
          - type: stream
            encoding: utf8
            separator: "\\n"
            path: "-"

    Python equivalent:

    .. code-block:: python

        from kanjidb.builder.plugins import kanjistream

        kanjistream.run(
            inputs=[{
                "type": "var",
                "name": "result"
            }],
            outputs=[{
                "type": "stream",
                "encoding": "utf8",
                "separator": "\\n",
                "path": "-"
            }],
            kwargs={"result": ["一", "二"]}
        )

    :param inputs: input streams
    :param output: output streams
    :param kwargs: context
    :return: a list of kanjis read from input streams
    """
    outputs = outputs if outputs is not None else []
    kwargs = kwargs if kwargs is not None else {}

    kanjis = []

    # Read from inputs
    for _ in inputs:
        if _["type"] == "stream":
            in_kanjis = load(_["path"], sep=_.get("separator", None))
        elif _["type"] == "var":
            in_kanjis = kwargs[_["name"]]
        else:
            raise Exception("Invalid input {}".format(_["type"]))

        kanjis += kanjidb.encoding.decode_all(
            in_kanjis, encoding=_.get("encoding", None)
        )

    # Write to outputs
    for _ in outputs:
        out_kanjis = kanjidb.encoding.encode_all(kanjis, encoding=_.get("encoding"))

        if _["type"] == "stream":
            dump(out_kanjis, _["path"], sep=_.get("separator", None))
        elif _["type"] == "var":
            kwargs[_["name"]] = out_kanjis
        else:
            raise Exception("Invalid output {}".format(_["type"]))

    return kanjis


def loads(s, *, encoding=None, decode=None, sep=None):
    """Load a list of kanjis from string.

    Usage example:

    .. code-block:: python

        >> loader.loads("一二")
        ['一', '二']

    Using custom separator:

    .. code-block:: python

        >> loader.loads("一;二"), sep=";")
        ['一', '二']

    Default behaviour is that kanjis must be UTF-8 encoded, but
    this can customized:

    .. code-block:: python

        >> loader.loads("U+4E00", encoding=encoding.UNICODE_PLUS)
        ['一']

        >> loader.loads("\u4E00", encoding=encoding.UNICODE_ESCAPE)
        ['一']

    :param s: string to decode
    :param encoding: kanjis encoding
    :param decode: how to decode kanjis
    :param sep: separator between kanjis
    :return: list of decoded kanjis
    """
    decode = (
        decode
        if decode is not None
        else functools.partial(kanjidb.encoding.decode, encoding=encoding)
    )

    symbols = s if sep is None else s.split(sep)
    symbols = [re.sub("[ \t\r\n]", "", _) for _ in symbols]

    return [decode(_) for _ in symbols]


def load(*streams, encoding=None, decode=None, sep=None):
    """Load a list of kanjis from input streams.

    Usage example:

    .. code-block:: python

        load_kanjis("a.txt", "b.txt")

    Using filelike objects:

    .. code-block:: python

        load_kanjis(sys.stdin)

        with open("a.txt", "rb") as f:
            load_kanjis(f)

    Default kanjis separator is the newline character, but this can
    be customized as such:

    .. code-block:: python

        load_kanjis("a.txt", "b.txt", sep=";")

    :param streams: list of input streams to read
    :param encoding: kanjis encoding
    :param decode: how to decode kanjis
    :param sep: separator between kanjis
    :return: list of decoded kanjis
    """
    sep = sep if sep is not None else os.linesep

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

            yield from loads(content, encoding=encoding, decode=decode, sep=sep)

    return list(wrapper())


def dump(kanjis, *streams, encoding=None, encode=None, sep=None):
    sep = sep if sep is not None else os.linesep
    encode = (
        encode
        if encode is not None
        else functools.partial(kanjidb.encoding.encode, encoding=encoding)
    )

    content = sep.join([encode(_) for _ in kanjis])

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
