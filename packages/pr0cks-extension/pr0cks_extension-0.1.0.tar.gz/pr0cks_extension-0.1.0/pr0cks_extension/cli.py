"""
pr0cks-extension
Copyright (C) 2020 LoveIsGrief

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import abc
import argparse
import logging

import pkg_resources
from pkg_resources import EntryPoint


class Pr0cksCommand(abc.ABC):
    """
    Extend this class to extend the pr0cks CLI.

    This docstring will be used as the description in the output
    """

    NAME: str = None

    # noinspection PyProtectedMember
    def __init__(self, arg_group: argparse._ArgumentGroup):
        self.log = logging.getLogger(self.__class__.__name__)

        self.arg_group = arg_group
        self.arg_group.description = self.__doc__

        self._add_args()

    def _add_args(self):
        """
        Adds arguments to the argument group
        """
        raise NotImplementedError()

    def execute(self, args: argparse.Namespace, bind_address: str):
        """
        Do something with the arguments by pr0cks
        """
        raise NotImplementedError()


def iter_extensible_commands():
    """
    Finds commands that extend pr0cks and iterates over them
    """
    for entry_point in pkg_resources.iter_entry_points("pr0cks.cli"):
        entry_point: EntryPoint
        # pylint: disable=invalid-name
        Command = entry_point.load()
        if not (isinstance(Command, type) and issubclass(Command, Pr0cksCommand)):
            logging.warning(
                "Ignored command extension %s:%s: it's not a subclass of %s",
                entry_point.module_name,
                entry_point.name,
                Pr0cksCommand
            )
            continue
        yield Command
