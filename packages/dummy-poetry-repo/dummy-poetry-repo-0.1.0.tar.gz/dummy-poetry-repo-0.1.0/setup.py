# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dummy_poetry_repo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dummy-poetry-repo',
    'version': '0.1.0',
    'description': "Just a repository for testing out different stuff so I don't have to clutter my offiail repos",
    'long_description': None,
    'author': 'Lovecraftian Horror',
    'author_email': 'LovecraftianHorror@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
