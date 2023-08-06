# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['as_fastapi_toolbox',
 'as_fastapi_toolbox.auth',
 'as_fastapi_toolbox.requests',
 'as_fastapi_toolbox.validators']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=1.7.1,<2.0.0',
 'cryptography>=2.9.2,<3.0.0',
 'email-validator>=1.1.0,<2.0.0',
 'fastapi>=0.54.1,<0.55.0',
 'httpx>=0.12.1,<0.13.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'pytz>=2020.1,<2021.0',
 'starlette>=0.13.2,<0.14.0',
 'uvicorn>=0.11.5,<0.12.0']

setup_kwargs = {
    'name': 'as-fastapi-toolbox',
    'version': '0.3.6',
    'description': '',
    'long_description': None,
    'author': 'Andreas Moll',
    'author_email': 'andreasm@ansto.gov.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
