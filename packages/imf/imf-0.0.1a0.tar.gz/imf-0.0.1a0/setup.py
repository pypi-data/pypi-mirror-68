# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['imf']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'imf',
    'version': '0.0.1a0',
    'description': 'Pythonic API access to IMF data - Unofficial',
    'long_description': '# IMF\n\nPythonic API access to IMF data - Unofficial\n',
    'author': 'nathanbegbie',
    'author_email': 'nathanbegbie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nathanbegbie/imf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
