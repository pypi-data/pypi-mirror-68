# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['joblib_zstd']

package_data = \
{'': ['*']}

install_requires = \
['joblib', 'zstandard']

setup_kwargs = {
    'name': 'joblib-zstd',
    'version': '0.1.0',
    'description': 'Add Zstandard compression/decompression functionality for joblib',
    'long_description': None,
    'author': 'Hiroyuki Tanaka',
    'author_email': 'aflc0x@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
