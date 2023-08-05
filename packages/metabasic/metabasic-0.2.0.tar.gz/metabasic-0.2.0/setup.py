# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metabasic']

package_data = \
{'': ['*']}

install_requires = \
['inquirer>=2.6.3,<3.0.0', 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'metabasic',
    'version': '0.2.0',
    'description': 'Dead simple client for interacting with the Metabase dataset API',
    'long_description': '[![CircleCI](https://circleci.com/gh/Ben-Hu/metabasic.svg?style=svg)](https://circleci.com/gh/Ben-Hu/metabasic)\n[![codecov](https://codecov.io/gh/Ben-Hu/metabasic/branch/master/graph/badge.svg)](https://codecov.io/gh/Ben-Hu/metabasic)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Ben-Hu/metabasic.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Ben-Hu/metabasic/context:python)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License](https://img.shields.io/github/license/Ben-Hu/metabasic)](https://github.com/Ben-Hu/metabasic/blob/master/LICENSE)\n[![Tag](https://img.shields.io/github/v/tag/Ben-Hu/metabasic)](https://github.com/Ben-Hu/metabasic/releases)\n[![PyPI](https://img.shields.io/pypi/v/metabasic?color=blue)](https://pypi.org/project/metabasic/)\n\n\n# Metabasic\nDead simple client for interacting with the Metabase dataset API\n\n## Install\n```sh\npip install metabasic\n```\n\n## Examples\n```python\nfrom metabasic import Metabasic\ndomain = "https://my-metabase-domain.com"\n\n# Authentication with an existing session\ndb = Metabasic(domain, session_id="foo" database_id=1)\ndb.query("SELECT * FROM bar")\n\n# Email/Password authentication\nga = Metabasic(domain, database_id=2)\nga.authenticate("foo@email.com", "password")\nga_query = {\n    "ids": "ga:1234567890",\n    "start-date": "30daysAgo",\n    "end-date": "today",\n    "metrics": "ga:someMetric",\n    "dimensions": "ga:someDimension",\n    "sort": "ga:someDimension",\n    "max-results": 10000\n)\nga.query(json.dumps(ga_query))\n\n# Select a database interactively\nm = Metabasic(domain, session_id="foo")\nm.select_database()\n```\n',
    'author': 'Ben-Hu',
    'author_email': 'benjqh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ben-Hu/metabasic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
