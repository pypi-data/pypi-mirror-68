from injector import Module as _Module, provider, singleton
from limecore.core.types import ARGV, CWD
from pathlib import Path

from .configuration import Configuration
from .configuration_loader import ConfigurationLoader


class Module(_Module):
    def __init__(
        self,
        name: str,
        enable_commandline_arguments: bool = True,
        enable_environment_variables: bool = True,
    ):
        self._enable_commandline_arguments = enable_commandline_arguments
        self._enable_environment_variables = enable_environment_variables
        self._name = name

    @singleton
    @provider
    def provide_configuration(self, argv: ARGV, cwd: CWD) -> Configuration:
        configuration_loader = ConfigurationLoader()
        configuration_loader.add_file(cwd.joinpath(f"{self._name}.yaml"))
        configuration_loader.add_file(Path(f"~/.{self._name}").expanduser())

        if self._enable_commandline_arguments:
            configuration_loader.add_commandline_arguments(argv)

        if self._enable_environment_variables:
            configuration_loader.add_environment_variables(self._name)

        return configuration_loader.load()
