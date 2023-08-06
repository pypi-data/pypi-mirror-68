# pr0cks-extension

The base package for extensions to pr0cks to inherit from.

Extensions are discovered using [setuptools' entrypoint feature][entrypoint].
They can also be declared in [poetry][poetry plugin].

For now the only type of extension that exists is a CLI extension.
It allows adding parameters to the `pr0cks` CLI.

## Writing a basic extension

The easiest way is to start a project with [poetry] using `poetry init`.

It would be convention to prefix the project name with **pr0cks-**.
For this example let's call it **pr0cks-debug** which will have the sole task
 of adding the `--debug` param and thus alias `--verbose`.
 
```python
import argparse
import logging

from pr0cks_extension.cli import Pr0cksCommand

class DebugCommand(Pr0cksCommand):
    NAME = "debug"  # Will be used as the name of argparse group
    
    def _add_args(self):
        """Adds arguments to the argparse group"""
        self.arg_group.add_argument(
            "--debug",
            action="store_true",
            help="Activate debug logging"
)       
    
    def execute(self, args: argparse.Namespace, bind_address: str):
        """Activates debug logging for pr0cks"""
        logging.getLogger().setLevel(logging.DEBUG)
```

[entrypoint]: https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins
[poetry]: https://python-poetry.org
[poetry plugin]: https://python-poetry.org/docs/pyproject/#plugins
