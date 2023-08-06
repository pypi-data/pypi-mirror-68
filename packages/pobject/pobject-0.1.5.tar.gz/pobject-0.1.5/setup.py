# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pobject']

package_data = \
{'': ['*']}

install_requires = \
['is-url>=0.1.2,<0.2.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'pobject',
    'version': '0.1.5',
    'description': 'pobject',
    'long_description': '# pobject\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
