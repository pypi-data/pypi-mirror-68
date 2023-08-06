# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyppl_runcmd']
install_requires = \
['cmdy', 'pyppl>=3.0.0,<4.0.0']

entry_points = \
{'pyppl': ['pyppl_runcmd = pyppl_runcmd']}

setup_kwargs = {
    'name': 'pyppl-runcmd',
    'version': '0.0.2',
    'description': 'Allowing to run local command before and after each process for PyPPL',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
