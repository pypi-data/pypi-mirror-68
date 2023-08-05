# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gigabloat', 'gigabloat.coverter', 'gigabloat.gatherer']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'click>=7.1.2,<8.0.0',
 'humanize>=2.4.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'gigabloat',
    'version': '0.1.0',
    'description': 'Tool to get general file and directory stats',
    'long_description': None,
    'author': 'Artem Kolichenkov',
    'author_email': 'artem@kolichenkov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.2,<4.0.0',
}


setup(**setup_kwargs)
