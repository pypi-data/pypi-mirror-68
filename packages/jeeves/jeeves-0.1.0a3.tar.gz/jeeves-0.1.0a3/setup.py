# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jeeves',
 'jeeves.cli',
 'jeeves.core',
 'jeeves.core.actions',
 'jeeves.core.actions.tests',
 'jeeves.core.tests',
 'jeeves.core.tests.tasks',
 'jeeves.frontend',
 'jeeves.frontend.templatetags']

package_data = \
{'': ['*'], 'jeeves.frontend': ['templates/*', 'templates/flows/*']}

install_requires = \
['click>=7.0,<8.0',
 'docker>=4.1.0,<5.0.0',
 'jinja2>=2.10,<3.0',
 'pydantic>=0.32.2,<0.33.0',
 'pyyaml>=5.3.1,<6.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['jeeves = jeeves.cli:main']}

setup_kwargs = {
    'name': 'jeeves',
    'version': '0.1.0a3',
    'description': '',
    'long_description': None,
    'author': 'Felipe Martin',
    'author_email': 'me@fmartingr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
