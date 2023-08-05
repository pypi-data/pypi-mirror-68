# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gandi', 'gandi.commands']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['gandi = gandi.console:run']}

setup_kwargs = {
    'name': 'gandi',
    'version': '0.2.3',
    'description': 'Command line interface to the Gandi API',
    'long_description': None,
    'author': 'Greg Anders',
    'author_email': 'greg@gpanders.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
