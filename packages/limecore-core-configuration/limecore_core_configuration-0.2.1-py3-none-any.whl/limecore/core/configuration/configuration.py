from typing import Any, Dict, List, Optional


class Configuration:
    def __init__(self, data: Dict[str, Any], base: Optional["Configuration"] = None):
        self._data = {}

        if base is not None:
            self._merge(base._data)

        self._merge(data)

    def get_bool(self, name: str) -> Optional[bool]:
        if name not in self._data:
            return None

        return bool(self._data[name])

    def get_int(self, name: str) -> Optional[int]:
        if name not in self._data:
            return None

        return int(self._data[name])

    def get_list(self, name: str) -> List["Configuration"]:
        if name not in self._data:
            return []

        return list(Configuration(s) for s in (self._data[name] or []))

    def get_string(self, name: str) -> Optional[str]:
        if name not in self._data:
            return None

        return str(self._data[name])

    def section(self, *names: str) -> "Configuration":
        data = self._data

        for name in names:
            if name not in data:
                return Configuration({})

            data = data[name]

        return Configuration(data)

    def _merge(self, data: Dict[str, Any]):
        def merge(source: Dict[str, Any], target: Dict[str, Any]):
            for k, v in source.items():
                if isinstance(v, dict):
                    node = target.setdefault(k, {})
                    merge(v, node)
                else:
                    target[k] = v

            return target

        self._data = merge(data, self._data)

    def __str__(self):
        return str(self._data)
