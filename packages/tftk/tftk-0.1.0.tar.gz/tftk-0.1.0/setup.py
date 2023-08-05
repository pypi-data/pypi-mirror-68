# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tftk',
 'tftk.augment_ok',
 'tftk.image',
 'tftk.image.dataset',
 'tftk.image.model',
 'tftk.optimizer',
 'tftk.rl',
 'tftk.train']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.14,<0.15',
 'gym>=0.17.1,<0.18.0',
 'icrawler>=0.6.2,<0.7.0',
 'optuna>=1.2.0,<2.0.0',
 'pillow>=7.0.0,<8.0.0',
 'pydot-ng>=2.0.0,<3.0.0',
 'tensorboard_plugin_profile>=2.2.0,<3.0.0',
 'tensorflow>=2.2.0,<3.0.0',
 'tensorflow_datasets>=2.1.0,<3.0.0',
 'tensorflow_probability>=0.9.0,<0.10.0',
 'tfa-nightly>=0.10.0-alpha.20200505184857,<0.11.0']

setup_kwargs = {
    'name': 'tftk',
    'version': '0.1.0',
    'description': 'TensorFlow Toolkit',
    'long_description': None,
    'author': 'Naruhide KITADA',
    'author_email': 'kitfactory@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
