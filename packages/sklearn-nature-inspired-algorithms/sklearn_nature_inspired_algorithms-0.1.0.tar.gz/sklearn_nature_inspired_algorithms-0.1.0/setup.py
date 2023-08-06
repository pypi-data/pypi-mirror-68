# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sklearn_nature_inspired_algorithms',
 'sklearn_nature_inspired_algorithms.model_selection']

package_data = \
{'': ['*']}

install_requires = \
['NiaPy==2.0.0rc10',
 'numpy>=1.18.4,<2.0.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'sklearn-nature-inspired-algorithms',
    'version': '0.1.0',
    'description': 'Search using nature inspired algorithms over specified parameter values for an sklearn estimator.',
    'long_description': '# Nature Inspired Algorithms for scikit-learn\n',
    'author': 'Timotej Zatko',
    'author_email': 'timi.zatko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timzatko/Sklearn-Nature-Inspired-Algorithms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
