# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ex4ml',
 'ex4ml.content',
 'ex4ml.deep',
 'ex4ml.experiments',
 'ex4ml.explainers',
 'ex4ml.statistical',
 'ex4ml.tools']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib', 'numpy', 'pandas', 'scikit-learn', 'scipy', 'tensorflow']

setup_kwargs = {
    'name': 'ex4ml',
    'version': '1.0a0',
    'description': 'A library for streamlining machine learning experiments',
    'long_description': None,
    'author': 'MInDS at Mines',
    'author_email': 'minds@mines.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
