# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydig']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydig',
    'version': '0.3.0',
    'description': "Python wrapper library for the 'dig' command line tool",
    'long_description': "# pydig\n\npydig is a python wrapper library for the 'dig' command line tool.\n\n[![Build Status](https://travis-ci.org/leonsmith/pydig.svg?branch=master)](https://travis-ci.org/leonsmith/pydig)\n[![Python Versions](https://img.shields.io/pypi/pyversions/pydig.svg)](https://pypi.org/project/pydig/)\n[![License](https://img.shields.io/pypi/l/pydig.svg?color=informational)](https://pypi.org/project/pydig/)\n\n## Versioning\n\npydig follows [SemVer](https://semver.org/) (MAJOR.MINOR.PATCH) to track what is in each release.\n\n* Major version number will be bumped when there is an incompatible API change\n* Minor version number will be bumped when there is functionality added in a backwards-compatible manner.\n* Patch version number will be bumped when there is backwards-compatible bug fixes.\n\nAdditional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.\n\n\n## Installation\n\nInstallation the package from pypi with your tool of choice `pip`, `poetry`\nor `pipenv`.\n\n```bash\npip install pydig\n```\n\n## Usage\n\nTo use the default resolver you can call `pydig.query` this resolver will use\nthe `dig` command found in your `$PATH`.\n```\n>>> import pydig\n>>> pydig.query('example.com', 'A')\n['93.184.216.34']\n>>> pydig.query('www.github.com', 'CNAME')\n['github.com.']\n>>> pydig.query('example.com', 'NS')\n['a.iana-servers.net.', 'b.iana-servers.net.']\n```\n\nIf your want to adjust the executable location, the nameservers to dig will\nquery against or would like to pass additional arguments/flags, you can\nconfigure your own instance of a resolver. and call the `query` method of your\ncustom resolver.\n\n```\n>>> import pydig\n>>> resolver = pydig.Resolver(\n...     executable='/usr/bin/dig',\n...     nameservers=[\n...         '1.1.1.1',\n...         '1.0.0.1',\n...     ],\n...     additional_args=[\n...         '+time=10',\n...     ]\n... )\n>>> resolver.query('example.com', 'A')\n>>> ['93.184.216.34']\n```\n\n## Documentation\n\nThe code is 150~ lines with 100% test coverage\n\nhttps://github.com/leonsmith/pydig/tree/master/pydig\n",
    'author': 'Leon Smith',
    'author_email': '_@leonmarksmith.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leonsmith/pydig',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
