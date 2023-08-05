from injector import Injector
from limecore.core.types import ARGV
from typing import Dict, Type

from .command import Command


class App:
    def __init__(
        self,
        argv: ARGV,
        commands: Dict[str, Type[Command]],
        injector: Injector,
        subparsers_name: str,
    ):
        self._argv = argv
        self._commands = commands
        self._injector = injector
        self._subparsers_name = subparsers_name

    def start(self):
        command_impl = self._commands[getattr(self._argv, self._subparsers_name)]

        self._injector.get(command_impl).run(self._argv)
