# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonschema_default']

package_data = \
{'': ['*']}

install_requires = \
['xeger>=0.3.5,<0.4.0']

setup_kwargs = {
    'name': 'jsonschema-default',
    'version': '1.0.0',
    'description': 'Create default objects from a JSON schema',
    'long_description': '# jsonschema-instance\n\nA Python package that creates default objects from a JSON schema.\n\n## Note\nThis is not a validator. Inputs should be valid JSON schemas. For Python you can use the [jsonschema](https://github.com/Julian/jsonschema) package to validate schemas.',
    'author': 'Martin Boos',
    'author_email': 'mboos@outlook.com',
    'maintainer': 'Martin Boos',
    'maintainer_email': 'mboos@outlook.com',
    'url': 'https://github.com/mnboos/jsonschema-default',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
