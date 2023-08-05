__all__ = ["PluginBase"]
from abc import ABC, abstractmethod


class PluginBase(ABC):
    @property
    def template_config(self):
        """Return the template config for this plugin.

        This config will appear in default generated file.

        :return: a dict containing template config
        """
        return {}

    @property
    def required_config(self):
        """Return the required config for this plugin.

        This config will be merged with the loaded one.

        :return: a dict containing required config
        """
        return {}

    def configure(self, *, global_config, plugin_config):
        """Configure this plugin.

        Parameter `plugin_config` is the combination of loaded
        config and `required_config`, ensuring all parameters
        required to run this plugin are present.

        :param global_config: global builder configuration
        :param plugin_config: plugin configuration
        """
        self.global_config = global_config
        self.plugin_config = plugin_config

    @abstractmethod
    def __call__(self, **kwargs):
        """Execute this plugin.

        :param kwargs: inputs
        :return: outputs
        """
        raise NotImplementedError()
