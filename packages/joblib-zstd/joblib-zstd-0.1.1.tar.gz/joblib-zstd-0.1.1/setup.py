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
    'version': '0.1.1',
    'description': 'Add Zstandard compression/decompression functionality for joblib',
    'long_description': "joblib-zstd is a plugin, which enables Zstandard (.zst) compression and decompression through joblib.dump and joblib.load.\n\n# Prerequisites\n\nYou need [joblib](https://joblib.readthedocs.io/en/latest/).\n\n# Install\n\n```\npip install joblib-zstd\n```\n\nIf you failed to install, update version of pip and setuptools:\n\n```\npip install -U pip setuptools\n```\n\n# Usage\n\n```python\nimport joblib\nimport joblib_zstd\njoblib_zstd.register()\n\njoblib.dump({'a': 1, 'b': 2}, 'obj.zst', compress=5)  # implicit compression\njoblib.dump({'a': 1, 'b': 2}, 'obj.bin', compress=('zstd', 5))  # explicit compression\n\njoblib.load('obj.zst')  # implicit decompression\n```\n\n# LISENCE\n\nMIT\n",
    'author': 'Hiroyuki Tanaka',
    'author_email': 'aflc0x@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roy-ht/joblib-zstd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
