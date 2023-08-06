# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netmagus']

package_data = \
{'': ['*']}

install_requires = \
['autobahn-sync==0.3.2', 'autobahn>=20.4.3,<21.0.0']

setup_kwargs = {
    'name': 'netmagus',
    'version': '0.9.0',
    'description': 'Python module for JSON data exchange with the Intelligent Visibility NetMagus system.',
    'long_description': 'NetMāgus Python Package\n=======================\n\nThis Python package is to be used with the `NetMāgus <http://www.intelligentvisibility.com/netmagus>`_ product from `Intelligent Visbility, Inc <http://www.intelligentvisibility.com>`_.\n\nIt is used to create and exchange UI forms and Formula steps with the NetMāgus application.\n\nThe code has been tested and should work for both Python 3.6+.\n\nRefer to the `NetMāgus <http://www.intelligentvisibility.com/netmagus>`_ documentation for usage details.\n\nTo install: ``pip install netmagus``\n',
    'author': 'Richard Collins',
    'author_email': 'richardc@intelligentvisibility.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.intelligentvisibility.com/netmagus/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
