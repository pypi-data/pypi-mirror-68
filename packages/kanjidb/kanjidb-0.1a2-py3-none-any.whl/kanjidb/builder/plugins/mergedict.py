# -*- coding: utf-8 -*-
__all__ = ["Plugin", "run"]
from kanjidb.builder.plugins import PluginBase


class Plugin(PluginBase):
    @property
    def template_config(self):
        return {
            "inputs": ["first", "second"],
            "output": "result",
        }

    @property
    def required_config(self):
        config = self.template_config

        return config

    def __call__(self, **kwargs):
        run(
            inputs=self.plugin_config["inputs"],
            output=self.plugin_config["output"],
            kwargs=kwargs,
        )

        return kwargs

    def __repr__(self):
        return "MergeDict"


def run(inputs, output=None, *, kwargs=None):
    """Merge multiple JSON dicts to a single one.

    Configuration:

    .. code-block:: yaml

        run:
        - mergedict:
          inputs:
          - string
          output: string

    Merge dicts from "first" and "second" variables to "result":

    .. code-block:: yaml

        run:
        - mergedict:
          inputs:
          - first
          - second
          output: result

    Python equivalent:

    .. code-block:: python

        from kanjidb.builder.plugins import mergedict

        result = mergedict.run(
            inputs=["first", "second"],
            kwargs={"first": {...}, "second": {...}}
        )

    :param inputs: input vars
    :param output: output var
    :param kwargs: context
    :return: merged JSON dict
    """
    kwargs = kwargs if kwargs is not None else {}

    o = {}

    for _ in inputs:
        o.update(kwargs[_])

    if output:
        kwargs[output] = o

    return o
