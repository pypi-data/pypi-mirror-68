# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['b5', 'b5.lib', 'b5.modules', 'b5.tests.lib']

package_data = \
{'': ['*'], 'b5': ['bash/*', 'legacy/*', 'legacy/modules/*']}

install_requires = \
['jinja2>=2.10.0,<3.0.0',
 'markupsafe>=1.1.0,<2.0.0',
 'packaging>=16.0',
 'pyyaml>=5.1.0,<6.0.0',
 'termcolor>=1.1.0,<1.2.0']

entry_points = \
{'console_scripts': ['b5 = b5.main:main',
                     'b5-execute = b5.execute:main',
                     'b5-init = b5.init:main']}

setup_kwargs = {
    'name': 'b5',
    'version': '1.1.6',
    'description': 'b5 - simple and sane task runner',
    'long_description': None,
    'author': 'David Danier',
    'author_email': 'danier@team23.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
