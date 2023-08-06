# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdesk', 'sdesk.api', 'sdesk.proc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0', 'requests_toolbelt>=0.9.1,<0.10.0']

entry_points = \
{'console_scripts': ['published = sdesk:published']}

setup_kwargs = {
    'name': 'sdesk',
    'version': '0.2.2',
    'description': 'ScienceDesk helper library',
    'long_description': '# ScienceDesk Python helpers\n\nThis module provides Python code to help you interact with and extend the\nScienceDesk platform.\n\n## Modules\n\n- api: helpers to interact with the ScienceDesk API\n- proc: helpers to write ScienceDesk algorithms\n\n\n## Documentation\nYou can check the current documentation at [Read The Docs](https://sciencedesk-helper-library.readthedocs.io)\n',
    'author': 'ScienceDesk GmbH',
    'author_email': 'github@sciencedesk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sciencedesk.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
