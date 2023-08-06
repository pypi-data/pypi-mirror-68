import logging
import collections
import inspect
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from . import utils

LOG = logging.getLogger(__name__)


__prog__name__ = "ZS-PluginManager"


class FailedToLoadPlugin(Exception):
    """Exception raised when a plugin fails to load."""

    FORMAT = '%(prog_name)s failed to load plugin "%(name)s" due to %(exc)s.'

    def __init__(self, plugin: "Plugin", exception: Exception) -> None:
        """Initialize our FailedToLoadPlugin exception."""
        self.prog_name: str = __prog__name__
        self.plugin = plugin
        self.ep_name: str = self.plugin.name
        self.original_exception = exception
        super(FailedToLoadPlugin, self).__init__(plugin, exception)

    def __str__(self):  # type: () -> str
        """Format our exception message."""
        return self.FORMAT % {
            "prog_name": self.prog_name,
            "name": self.ep_name,
            "exc": self.original_exception,
        }


class Plugin(object):
    """Wrap an EntryPoint from setuptools and other logic."""

    def __init__(self, entry_point: Any, is_local: bool = False, namespace: str = "", label: str = ""):
        """Initialize our Plugin.

        :param str name:
            Name of the entry-point as it was registered with setuptools.
        :param entry_point:
            EntryPoint returned by setuptools.
        :type entry_point:
            setuptools.EntryPoint
        :param bool is_local:
            Is this a repo-local plugin?
        """
        self.entry_point = entry_point
        self.is_local: bool = is_local
        self.namespace: str = namespace
        self.label: str = label
        self._plugin: Any = None
        self._parameters = None
        self._parameter_names: Optional[List[Any]] = None
        self._plugin_name: Optional[str] = None
        self._version: Optional[str] = None

    def __repr__(self) -> str:
        """Provide an easy to read description of the current plugin."""
        return f"Plugin(name={self.name}, entry_point={self.entry_point})"

    @property
    def name(self) -> str:
        return str(self.entry_point.name)

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert this plugin to a dictionary."""
        return {
            "namespace": self.namespace,
            "name": self.name,
            "label": self.label,
            "parameters": self.parameters,
            "parameter_names": self.parameter_names,
            "plugin": self.plugin,
            "plugin_name": self.plugin_name,
        }

    @property
    def parameters(self) -> Any:
        """List of arguments that need to be passed to the plugin."""
        if self._parameters is None:
            self._parameters = self.parameters_for(self)
        return self._parameters

    def parameters_for(self, plugin: "Plugin") -> Any:
        """Return the parameters for the plugin.

        This will inspect the plugin and return either the function parameters
        if the plugin is a function or the parameters for ``__init__`` after
        ``self`` if the plugin is a class.

        :param plugin:
            The internal plugin object.
        :type plugin:
            flake8.plugins.manager.Plugin
        :returns:
            A dictionary mapping the parameter name to whether or not it is
            required (a.k.a., is positional only/does not have a default).
        :rtype:
            dict([(str, bool)])
        """
        func = plugin.plugin
        is_class = not inspect.isfunction(func)
        if is_class:  # The plugin is a class
            func = plugin.plugin.__init__

        parameters = collections.OrderedDict(
            [
                (parameter.name, parameter.default is parameter.empty)
                for parameter in inspect.signature(func).parameters.values()
                if parameter.kind == parameter.POSITIONAL_OR_KEYWORD
            ]
        )

        if is_class:
            parameters.pop("self", None)

        return parameters

    @property
    def parameter_names(self) -> Optional[List[Any]]:
        """List of argument names that need to be passed to the plugin."""
        if self._parameter_names is None:
            self._parameter_names = list(self.parameters)
        elif not isinstance(self._parameter_names, list):
            self._parameter_names = [self._parameter_names]
        return self._parameter_names

    @property
    def plugin(self) -> Any:
        """Load and return the plugin associated with the entry-point.

        This property implicitly loads the plugin and then caches it.
        """
        self.load_plugin()
        return self._plugin

    @property
    def version(self) -> Any:
        """Return the version of the plugin."""
        if self._version is None:
            try:
                self._version = self.plugin.version
            except BaseException:
                self._version = self.version_for(self)

        return self._version

    def version_for(self, plugin: "Plugin") -> Optional[str]:
        """Determine the version of a plugin by its module.

        :param plugin:
            The loaded plugin
        :type plugin:
            Plugin
        :returns:
            version string for the module
        :rtype:
            str
        """
        v = getattr(utils.get_module(self.plugin), "__version__", None)
        if v is None:
            return None
        return str(v)

    @property
    def plugin_name(self) -> Optional[str]:
        """Return the name of the plugin."""
        if self._plugin_name is None:
            self._plugin_name = self.plugin.name

        self._plugin_name = str(self._plugin_name)
        return self._plugin_name

    def _load(self) -> None:
        self._plugin = self.entry_point.load()
        if not callable(self._plugin):
            msg = (
                "Plugin %r is not a callable. It might be written for an older version of %s and might not work with this version" % (
                    self._plugin, __prog__name__)
            )
            LOG.critical(msg)
            raise TypeError(msg)

    def load_plugin(self) -> None:
        """Retrieve the plugin for this entry-point.

        This loads the plugin, stores it on the instance and then returns it.
        It does not reload it after the first time, it merely returns the
        cached plugin.

        :returns:
            Nothing
        """
        if self._plugin is None:
            LOG.info('Loading plugin "%s" from entry-point.', self.name)
            try:
                self._load()
            except Exception as load_exception:
                LOG.exception(load_exception)
                failed_to_load = FailedToLoadPlugin(
                    plugin=self, exception=load_exception
                )
                LOG.critical(str(failed_to_load))
                raise failed_to_load

    def register_CLI_args(self, argparser: Any) -> None:
        """Register the plugin's command-line arguments.

        :param argparser:
            Instantiated argparse.ArgumentParser to register options on.
        :returns:
            Nothing
        """
        func = getattr(self.plugin, "CLI__add_argument", None)
        if func is not None:
            LOG.debug(
                'Registering options from plugin "%s" on CLI argparser %r',
                self.name,
                argparser,
            )
            self.plugin().CLI__add_argument(argparser)

    def register_CLI_default_args(self, argparser: Any) -> None:
        func = getattr(self.plugin, "CLI__set_defaults", None)
        if func is not None:
            LOG.debug(
                'Registering default options from plugin "%s" on CLI argparser %r',
                self.name,
                argparser,
            )
            self.plugin().CLI__set_defaults(argparser)
