# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayush']

package_data = \
{'': ['*']}

install_requires = \
['hues>=0.2.2,<0.3.0',
 'pafy>=0.5.5,<0.6.0',
 'python-slugify>=4.0.0,<5.0.0',
 'youtube_dl>=2020.5.3,<2021.0.0']

entry_points = \
{'console_scripts': ['ytd = ayush.youtube:create_arguments']}

setup_kwargs = {
    'name': 'ayush',
    'version': '0.1.3',
    'description': "personal scripts & stuff; you probably shouldn't use it",
    'long_description': None,
    'author': 'Ayush Shanker',
    'author_email': 'ayushshanker@outlook.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
