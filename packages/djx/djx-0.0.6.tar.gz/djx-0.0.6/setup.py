# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djx']

package_data = \
{'': ['*']}

install_requires = \
['dj-database-url', 'dj-static', 'django', 'gunicorn']

setup_kwargs = {
    'name': 'djx',
    'version': '0.0.6',
    'description': 'Common utilities and dependencies for the modern Django project',
    'long_description': None,
    'author': 'aleontiev',
    'author_email': 'alonetiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3',
}


setup(**setup_kwargs)
