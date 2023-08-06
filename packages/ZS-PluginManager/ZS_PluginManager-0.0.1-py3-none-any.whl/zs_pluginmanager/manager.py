import entrypoints  # type: ignore
import logging
import pathlib
import sys
from typing import Any
from typing import Dict
from typing import Generator
from typing import Iterator
from typing import KeysView
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

from . import utils
from .plugin import Plugin

LOG = logging.getLogger(__name__)


class PluginManager(object):
    """Find and manage plugins consistently."""

    def __init__(self) -> None:
        """Initialize the manager."""
        self.plugins: Dict[Any, Plugin] = {}

    @property
    def names(self) -> List[str]:
        return list(self.plugins.keys())

    def keys(self) -> KeysView[str]:
        return self.plugins.keys()

    def load_local(self, local_plugins: Any = None, label: str = "", path: str = "") -> "PluginManager":
        """Load local plugins from config.

        :param list local_plugins:
            Plugins from config (as "X = path.to:Plugin" strings).
        """

        self.add_external_path(path)
        for plugin_str in utils.to_list(local_plugins):
            try:
                name, _, entry_str = str(plugin_str).partition("=")
                name, entry_str = name.strip(), entry_str.strip()
                entry_point = entrypoints.EntryPoint.from_string(entry_str, name)
                self._load_plugin_from_entrypoint(entry_point, is_local=True, namespace="", label=label)
            except BaseException:
                LOG.warning(f"Can't load local plugin {plugin_str}")
        return self

    def load_global(self, namespace: str, label: str = "") -> "PluginManager":
        """Load plugins from entry point

        :param str namespace:
            Namespace of the plugins to manage, e.g., 'distutils.commands'.
        """
        LOG.info('Loading entry-points for "%s".', namespace)
        for entry_point in entrypoints.get_group_all(namespace):
            self._load_plugin_from_entrypoint(entry_point, is_local=False, namespace=namespace, label=label)
        return self

    def _load_plugin_from_entrypoint(self, entry_point: Any, is_local: bool = False, namespace: str = "", label: str = "") -> None:
        """Load a plugin from a setuptools EntryPoint.

        :param EntryPoint entry_point:
            EntryPoint to load plugin from.
        :param bool is_local:
            Is this a repo-local plugin?
        """
        key = (namespace, entry_point.name, label, is_local)
        self.plugins[key] = Plugin(entry_point, is_local=is_local, namespace=namespace, label=label)
        LOG.debug('Loaded %r for plugin "%s".', self.plugins[key], key, entry_point.name)

    def map(self, func: Any, *args: Any, **kwargs: Any) -> Any:
        for name in self.plugins:
            if isinstance(func, str):
                func_run = getattr(self.plugins[name].plugin(), func, None)
                if func_run is None:
                    LOG.warning("Can't run for plugin %r function %s.", self.plugins[name], func)
                    continue
                yield func_run(*args, **kwargs)
            else:
                yield func(self.plugins[name], *args, **kwargs)

    def map_all(self, func: Any, *args: Any, **kwargs: Any) -> List[Any]:
        """Execute generator created by map"""
        kwargs["func"] = func
        return list(self.map(*args, **kwargs))

    def versions(self) -> Generator[Tuple[Optional[str], Any], Any, Any]:
        """Generate the versions of plugins.

        :returns:
            Tuples of the plugin_name and version
        :rtype:
            tuple
        """
        plugins_seen: Set[str] = set()
        for entry_point_name in self.names:
            plugin = self.plugins[entry_point_name]
            plugin_name = plugin.plugin_name
            if plugin.plugin_name in plugins_seen:
                continue
            plugins_seen.add(str(plugin_name))
            yield (plugin_name, plugin.version)

    def index(self, i: int = 0) -> Plugin:
        key = self.names[i]
        return self.plugins[key]

    def filter(self, stype: Any = "all", **kwargs: Any) -> "PluginManager":
        """Filter plugins by Namespace and another methods
        stype == "any": if any is true of condition then select
        stype == "all": if all is true of condition then select

        kwargs["namespace"]: equal namespace
        kwargs["namespace_re"]: re.match namespace
        and etc. Case sensitive!
        """
        if stype.lower().strip() in ["all", "and", "&", "&&"]:
            func_stype = all
        else:
            func_stype = any

        _selected = PluginManager()
        for key in self.plugins:
            # set values to compare
            _engines: Dict[str, Any] = {}
            _engines["key"] = key
            _engines["name"] = self.plugins[key].name
            _engines["namespace"] = self.plugins[key].namespace
            _engines["label"] = self.plugins[key].label
            _engines["is_local"] = self.plugins[key].is_local

            # compare conditions: parse all kwargs without optimization for "any" condition
            if kwargs:
                _cond = []
            else:
                _cond = [True]

            for k in kwargs:
                kL = k.lower()
                if kL in _engines:
                    if utils.check_equal(value=_engines[kL], search=kwargs[k]):
                        _cond.append(True)
                    else:
                        _cond.append(False)
                if kL.endswith("_re") and kL[:-len("_re")] in _engines:
                    if utils.check_re(value=_engines[kL[:-len("_re")]], search=kwargs[k]):
                        _cond.append(True)
                    else:
                        _cond.append(False)

            if func_stype(_cond):
                _selected.plugins[key] = self.plugins[key]

        return _selected

    def __iter__(self) -> Iterator[Plugin]:
        for key in self.plugins:
            yield self.plugins[key]

    def add_external_path(self, path: str) -> None:
        """Extend sys.path to load modules in external locations"""
        for p in utils.to_list(path):
            sys.path.append(str(pathlib.Path(p).resolve()))
