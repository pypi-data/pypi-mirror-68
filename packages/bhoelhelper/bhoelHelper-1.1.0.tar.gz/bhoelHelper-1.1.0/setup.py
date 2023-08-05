# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berhoel', 'berhoel.helper', 'berhoel.helper.test']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.3"': ['backports.functools-lru-cache>=1.6.1,<2.0.0'],
 ':python_version < "3.4"': ['pathlib2>=2.3.5,<3.0.0']}

setup_kwargs = {
    'name': 'bhoelhelper',
    'version': '1.1.0',
    'description': 'Misc helper functionalities.',
    'long_description': '# bhoelHelper module #\n\nSome helper modules used in my other modules.\n\n# Installation #\n\npip install bhoelHelper\n\n## Availability\n\nThe latest version should be available at my\n[GitLab](https://gitlab.com/berhoel/python/bhoelHelper.git) repository, the\npackage is avaliable at [pypi](https://pypi.org/project/bhoelHelper/) via\n`pip install bhoelHelper`.\n',
    'author': 'Berthold Höllmann',
    'author_email': 'berthold-gitlab@xn--hllmanns-n4a.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://python.xn--hllmanns-n4a.de/bhoelHelper/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
