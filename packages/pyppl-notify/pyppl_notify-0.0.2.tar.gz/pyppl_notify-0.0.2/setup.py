# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyppl_notify']
install_requires = \
['pyppl>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'pyppl-notify',
    'version': '0.0.2',
    'description': 'Email notification for PyPPL',
    'long_description': '# pyppl_notify\nEmail notification for PyPPL\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/pyppl_notify',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
