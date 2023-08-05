from argparse import ArgumentParser
from injector import Injector, Module, provider, singleton
from limecore import util
from limecore.core.types import ARGV
from types import ModuleType
from typing import Dict, Type

from .app import App
from .command import Command


class AppFactory(Module):
    def __init__(self, subparsers_name: str = "command"):
        self._commands: Dict[str, Type[Command]] = {}
        self._subparsers_name = subparsers_name

    def add(self, module: ModuleType) -> "AppFactory":
        for name in module.__all__:
            obj = getattr(module, name)

            if issubclass(obj, Command):
                self._commands[util.to_snakecase(name, "-")] = obj

        return self

    def create_argument_parser(self, argument_parser: ArgumentParser):
        subparsers = argument_parser.add_subparsers(dest=self._subparsers_name)

        for command_name, command_impl in self._commands.items():
            command_impl.create_argument_parser(subparsers.add_parser(command_name))

        return argument_parser

    @singleton
    @provider
    def provide_app(self, argv: ARGV, injector: Injector) -> App:
        return App(argv, self._commands, injector, self._subparsers_name)
