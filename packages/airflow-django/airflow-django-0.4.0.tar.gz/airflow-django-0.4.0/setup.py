# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airflow_django']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow>=1.10,<2.0', 'django>=2.0']

setup_kwargs = {
    'name': 'airflow-django',
    'version': '0.4.0',
    'description': 'A kit for using Django features, like its ORM, in Airflow DAGs.',
    'long_description': None,
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@sourcelair.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.8',
}


setup(**setup_kwargs)
