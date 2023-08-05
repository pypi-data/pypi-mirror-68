# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['disguise', 'disguise.templatetags']

package_data = \
{'': ['*'],
 'disguise': ['locale/*', 'locale/ru/LC_MESSAGES/*', 'templates/disguise/*']}

setup_kwargs = {
    'name': 'django-disguise',
    'version': '1.0',
    'description': '',
    'long_description': '===============\ndjango-disguise\n===============\n\n.. image:: https://travis-ci.org/marazmiki/django-disguise.svg?branch=master\n     :target: https://travis-ci.org/marazmiki/django-disguise\n     :alt: Travis CI building status\n\n.. image:: https://coveralls.io/repos/github/marazmiki/django-disguise/badge.svg?branch=master\n     :target: https://coveralls.io/github/marazmiki/django-disguise?branch=master\n     :alt: Code coverage status\n\n.. image:: https://badge.fury.io/py/django-disguise.svg\n     :target: http://badge.fury.io/py/django-disguise\n     :alt: PyPI release\n\n.. image:: https://pypip.in/wheel/django-disguise/badge.svg\n     :target: https://pypi.python.org/pypi/django-disguise/\n     :alt: Wheel Status\n\n.. image:: https://img.shields.io/pypi/pyversions/django-disguise.svg\n     :target: https://img.shields.io/pypi/pyversions/django-disguise.svg\n     :alt: Supported Python versions\n\n.. image:: https://img.shields.io/pypi/djversions/django-disguise.svg\n     :target: https://pypi.python.org/pypi/django-disguise/\n     :alt: Supported Django versions\n\n.. image:: https://readthedocs.org/projects/django-disguise/badge/?version=latest\n     :target: https://django-disguise.readthedocs.io/en/latest/?badge=latest\n     :alt: Documentation Status\n\nThis application allows a site superuser (or some staff user authorized for\nthe action) to *disguise* into an arbitrary user without knowing its password and without losing the original session.\n\n* See the full documentation on `RTFD <https://django-disguise.readthedocs.io/latest/>`_.\n* Look it in action on the `DEMO site <https://django-disguise.herokuapp.com>`_.\n',
    'author': 'Mikhail Porokhovnichenko',
    'author_email': 'marazmiki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marazmiki/django-disguise',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
