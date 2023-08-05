# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_prometheus_metrics_name']
install_requires = \
['flake8>=3.7.9,<4.0.0', 'prometheus_client>=0.7.1,<0.8.0']

entry_points = \
{'flake8.extension': ['PRM = flake8_prometheus_metrics_name:Checker']}

setup_kwargs = {
    'name': 'flake8-prometheus-metrics-name',
    'version': '0.1.0',
    'description': 'Flake8 plugin for prometheus metric name validation',
    'long_description': '# Flake8 prometheus metric name plugin\n\ncoming soon!\n',
    'author': 'perminovs',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/perminovs/flake8_prometheus_metrics_name',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
