# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_querybuilder']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy']

setup_kwargs = {
    'name': 'sqlalchemy-querybuilder',
    'version': '0.1.3',
    'description': 'Build sqlalchemy queries from jQuery-Query json',
    'long_description': 'SQLAlchemy query builder for jQuery QueryBuilder\n================================================\n\n[![builds.sr.ht\nstatus](https://builds.sr.ht/~ocurero/sqlalchemy-querybuilder/.build.yml.svg)](https://builds.sr.ht/~ocurero/sqlalchemy-querybuilder/.build.yml?) [![codecov](https://codecov.io/gh/ocurero/sqlalchemy-querybuilder/branch/master/graph/badge.svg)](https://codecov.io/gh/ocurero/sqlalchemy-querybuilder)\n\nThis package implements a sqlalchemy query builder for json data\ngenerated with (but not limited to) [`jQuery QueryBuilder`](http://querybuilder.js.org/).\n\n\nInstallation\n------------\n\n    #!python\n        pip install sqlalchemy-querybuilder\n\nQuickstart\n----------\n\nUsing **sqlalchemy-querybuilder** is very simple:\n\n```python\n\nfrom sqlalchemy_querybuilder import Filter\nfrom myapp import models, query\n\n    rule = {\n            "condition": "OR",\n            "rules": [{\n                       "field": "mytable.myfield",\n                       "operator": "equal",\n                       "value": "foo"\n                       },\n                      ],\n            }\n\n    myfilter = Filter(models, query)\n    print(myfilter)\n```\n\nThe following attributes from the rules are ignored and therefore can be omitted:\n\n-   `id`\n-   `type`\n-   `input`\n\n**WARNING**\n\nsqlalchemy-querybuilder does not do any kind of json validation.\n\nFilter class\n------------\n\n`Filter` accepts two arguments, `models` and `query`:\n\n-   models - can either be a module defining classes which inherit from\n    `declarative_base` or a dict of such classes with the name of the\n    tables as keys.\n-   query - a SQLAlchemy query object. Optionaly loaded with some\n    entity.\n\nRelease History\n---------------\n\n0.1.3 (2020-05-10)\n==================\n\n**Improvements**\n\n-   Use poetry for development.\n\n**Bugfixes**\n\n-   First release on sourcehut (bye bye bitbucket!).\n\n\n0.1.2 (2017-11-19)\n==================\n\n**Bugfixes**\n\n-   Fixed issue when models parameter was a dict() of classes.\n-   Added missing test for models parameter\n\n0.1 (2017-07-10)\n================\n\n**Improvements**\n\n-   First release\n',
    'author': 'Oscar Curero',
    'author_email': 'oscar@curero.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hg.sr.ht/~ocurero/sqlalchemy-querybuilder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
