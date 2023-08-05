# -*- coding: utf-8 -*-
__all__ = ["Plugin", "run"]
from kanjidb.builder.plugins import PluginBase, kanjistream
import kanjidb.encoding


class Plugin(PluginBase):
    MESSAGE = ["今", "日", "わ"]
    STDOUT = {"type": "stream", "encoding": kanjidb.encoding.UTF8, "path": "-"}

    @property
    def template_config(self):
        return {}

    @property
    def required_config(self):
        return {"outputs": [Plugin.STDOUT]}

    def __call__(self, **kwargs):
        run(outputs=self.plugin_config["outputs"], kwargs=kwargs)

        return kwargs

    def __repr__(self):
        return "HelloWorld"


def run(outputs=None, *, kwargs=None):
    """Write "今日わ" to streams.

    Configuration:

    .. code-block:: yaml

        run:
        - helloworld:
          outputs:
          - type: stream|var
            [separator: string] # stream only
            [encoding: string] # stream only
            [path: string] # stream only
            [name: string] # var only

    Write to stdout:

    .. code-block:: yaml

        run:
        - helloworld: {}

    Python equivalent:

    .. code-block:: python

        from kanjidb.builder.plugins import helloworld

        helloworld.run()

    Store to `result`:

    .. code-block:: yaml

        run:
        - helloworld:
          outputs:
          - type: var
            name: result

    Python equivalent:

    .. code-block:: python

        from kanjidb.builder.plugins import helloworld

        result = helloworld.run()

    :param outputs: output streams
    :param kwargs: context
    :return: a list containing ["今", "日", "わ"]
    """
    outputs = outputs if outputs is not None else [Plugin.STDOUT]
    kwargs = kwargs if kwargs is not None else {}

    for _ in outputs:
        if _["type"] == "stream":
            _["separator"] = ""

    return kanjistream.run(
        inputs=[{"type": "var", "name": "kanjis"}],
        outputs=outputs,
        kwargs={"kanjis": Plugin.MESSAGE},
    )
