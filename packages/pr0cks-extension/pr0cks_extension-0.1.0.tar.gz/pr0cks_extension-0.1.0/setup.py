# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pr0cks_extension']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pr0cks-extension',
    'version': '0.1.0',
    'description': 'Basis for CLI extensions for pr0cks',
    'long_description': '# pr0cks-extension\n\nThe base package for extensions to pr0cks to inherit from.\n\nExtensions are discovered using [setuptools\' entrypoint feature][entrypoint].\nThey can also be declared in [poetry][poetry plugin].\n\nFor now the only type of extension that exists is a CLI extension.\nIt allows adding parameters to the `pr0cks` CLI.\n\n## Writing a basic extension\n\nThe easiest way is to start a project with [poetry] using `poetry init`.\n\nIt would be convention to prefix the project name with **pr0cks-**.\nFor this example let\'s call it **pr0cks-debug** which will have the sole task\n of adding the `--debug` param and thus alias `--verbose`.\n \n```python\nimport argparse\nimport logging\n\nfrom pr0cks_extension.cli import Pr0cksCommand\n\nclass DebugCommand(Pr0cksCommand):\n    NAME = "debug"  # Will be used as the name of argparse group\n    \n    def _add_args(self):\n        """Adds arguments to the argparse group"""\n        self.arg_group.add_argument(\n            "--debug",\n            action="store_true",\n            help="Activate debug logging"\n)       \n    \n    def execute(self, args: argparse.Namespace, bind_address: str):\n        """Activates debug logging for pr0cks"""\n        logging.getLogger().setLevel(logging.DEBUG)\n```\n\n[entrypoint]: https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins\n[poetry]: https://python-poetry.org\n[poetry plugin]: https://python-poetry.org/docs/pyproject/#plugins\n',
    'author': 'LoveIsGrief',
    'author_email': 'loveisgrief@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/NamingThingsIsHard/net/pr0cks/pr0cks-extension',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
