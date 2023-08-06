# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyppl_lock']
install_requires = \
['filelock>=3,<4', 'pyppl']

entry_points = \
{'pyppl': ['pyppl_lock = pyppl_lock']}

setup_kwargs = {
    'name': 'pyppl-lock',
    'version': '0.0.5',
    'description': 'Preventing running processes from running again for PyPPL',
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
