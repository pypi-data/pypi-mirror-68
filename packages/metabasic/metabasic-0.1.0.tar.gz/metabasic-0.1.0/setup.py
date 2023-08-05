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
    'version': '0.1.0',
    'description': 'Dead simple client for interacting with the Metabase dataset API',
    'long_description': '# Metabasic\nDead simple client for interacting with the Metabase dataset API\n\n## Install\n```sh\npip install metabasic\n```\n\n## Examples\n```python\nfrom metabasic import Metabasic\ndomain = "https://my-metabase-domain.com"\n\n# Authentication with an existing session\ndb = Metabasic(domain, session_id="foo" database_id=1)\ndb.query("SELECT * FROM bar")\n\n# Email/Password authentication\nga = Metabasic(domain, database_id=2)\nga.authenticate("foo@email.com", "password")\nga_query = {\n    "ids": "ga:1234567890",\n    "start-date": "30daysAgo",\n    "end-date": "today",\n    "metrics": "ga:someMetric",\n    "dimensions": "ga:someDimension",\n    "sort": "ga:someDimension",\n    "max-results": 10000\n)\nga.query(json.dumps(ga_query))\n\n# Select a database interactively\nm = Metabasic(domain, session_id="foo")\nm.select_database()\n```\n',
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
