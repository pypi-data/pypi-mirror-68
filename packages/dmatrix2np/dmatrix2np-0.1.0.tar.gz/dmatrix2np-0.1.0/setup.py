# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dmatrix2np']

package_data = \
{'': ['*']}

install_requires = \
['numpy']

setup_kwargs = {
    'name': 'dmatrix2np',
    'version': '0.1.0',
    'description': "Convert XGBoost's DMatrix to numpy array",
    'long_description': None,
    'author': 'Aporia technologies ltd',
    'author_email': 'dev@aporia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
