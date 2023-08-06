# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['facecast_io', 'facecast_io.core']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.12.1,<0.13.0',
 'pyquery>=1.4.1,<2.0.0',
 'retry>=0.9.2,<0.10.0',
 'yarl>=1.4.2,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['typing>=3.7,<4.0', 'typing_extensions>=3.7,<4.0']}

setup_kwargs = {
    'name': 'facecast-io',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Serhii Khalymon',
    'author_email': 'sergiykhalimon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
