# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['event_source']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'event-source',
    'version': '0.1.0a2',
    'description': 'W3C compliant EventSource client for Python.',
    'long_description': '',
    'author': 'overcat',
    'author_email': '4catcode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/overcat/event-source',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
