import re
import logging
from types import SimpleNamespace
from typing import Any
from typing import List
from typing import Union

LOG = logging.getLogger(__name__)


def get_module(cls: Any) -> Any:
    def get_submodule(mod: Any, path: Union[str, List[Any]], level: int = 0) -> Any:
        if isinstance(path, str):
            path = path.split(".")

        if len(path) == level + 1:
            return mod
        return get_submodule(mod.__dict__[path[level + 1]], path=path, level=level + 1)

    try:
        module_name = cls.__module__
        module = __import__(module_name)
        return get_submodule(module, module_name)
    except BaseException:
        pass

    try:
        module_name = cls.__package__
        module = __import__(module_name)
        return get_submodule(module, module_name)
    except BaseException:
        pass

    return None


def check_equal(value: Any, search: Any, none_is_true: bool = True) -> bool:
    found = False
    for sel in to_list(search):
        if sel is None:
            if none_is_true:
                found = True
                break
            if value is None:
                found = True
                break
        elif str(value) == str(sel):
            found = True
            break
    return found


def check_re(value: Any, search: Any, none_is_true: bool = True) -> bool:
    for sel in to_list(search):
        if sel is None:
            if none_is_true:
                return True
            if value is None:
                return True
        elif (re.search(sel, str(value)) is not None):
            return True
    return False


def to_list(value: Any, dict_to_keys: bool = True) -> List[Any]:
    if value is None:
        return [None]
    elif isinstance(value, SimpleNamespace):
        if dict_to_keys:
            return list(value.__dict__.keys())
        else:
            return list(value.__dict__)
    elif isinstance(value, dict):
        if dict_to_keys:
            return list(value.keys())
        else:
            return list(value)
    elif isinstance(value, (list)):
        return value
    else:
        return [value]
