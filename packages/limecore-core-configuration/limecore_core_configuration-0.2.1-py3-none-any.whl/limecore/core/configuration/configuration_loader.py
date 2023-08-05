import os

from enum import Enum
from limecore.core.types import ARGV
from pathlib import Path
from typing import Any, List, Tuple
from yaml import safe_load

from .configuration import Configuration


class ConfigurationType(Enum):
    ARGV = 0
    ENV = 1
    FILE = 2


class ConfigurationLoader:
    def __init__(self):
        self._search_path: List[Tuple[ConfigurationType, Any]] = []

    def add_commandline_arguments(self, argv: ARGV):
        self._search_path.append((ConfigurationType.ARGV, argv))

    def add_environment_variables(self, prefix: str):
        prefix = prefix.upper() + ("_" if not prefix.endswith("_") else "")

        self._search_path.append((ConfigurationType.ENV, prefix))

    def add_file(self, path: Path):
        self._search_path.append((ConfigurationType.FILE, path))

    def load(self) -> Configuration:
        configuration = Configuration({})

        for configuration_type, args in self._search_path:
            if configuration_type == ConfigurationType.ARGV:
                configuration = self._load_argv(args, configuration=configuration)
            elif configuration_type == ConfigurationType.ENV:
                configuration = self._load_environment_variables(
                    args, configuration=configuration
                )
            elif configuration_type == ConfigurationType.FILE:
                configuration = self._load_file(args, configuration=configuration)
            else:
                raise NotImplementedError(configuration_type)

        return configuration

    def _load_argv(self, argv: ARGV, configuration: Configuration):
        for k, v in [i.split("=", maxsplit=1) for i in argv.config]:
            item = {}

            for i, l in enumerate(reversed(k.split("_"))):
                if i == 0:
                    item = {l.lower(): v}
                else:
                    item = {l.lower(): item}

            configuration = Configuration(item, base=configuration)

        return configuration

    def _load_environment_variables(self, prefix: str, configuration: Configuration):
        for k, v in os.environ.items():
            if k.startswith(prefix):
                item = {}

                for i, l in enumerate(reversed(k.split("_")[1:])):
                    if i == 0:
                        item = {l.lower(): v}
                    else:
                        item = {l.lower(): item}

                configuration = Configuration(item, base=configuration)

        return configuration

    def _load_file(self, path: Path, configuration: Configuration):
        if path.exists() and path.suffix == ".yaml":
            with open(path) as f:
                return Configuration(safe_load(f), base=configuration)
        else:
            return configuration
