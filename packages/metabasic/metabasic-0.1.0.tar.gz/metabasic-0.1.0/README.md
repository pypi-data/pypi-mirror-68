# Metabasic
Dead simple client for interacting with the Metabase dataset API

## Install
```sh
pip install metabasic
```

## Examples
```python
from metabasic import Metabasic
domain = "https://my-metabase-domain.com"

# Authentication with an existing session
db = Metabasic(domain, session_id="foo" database_id=1)
db.query("SELECT * FROM bar")

# Email/Password authentication
ga = Metabasic(domain, database_id=2)
ga.authenticate("foo@email.com", "password")
ga_query = {
    "ids": "ga:1234567890",
    "start-date": "30daysAgo",
    "end-date": "today",
    "metrics": "ga:someMetric",
    "dimensions": "ga:someDimension",
    "sort": "ga:someDimension",
    "max-results": 10000
)
ga.query(json.dumps(ga_query))

# Select a database interactively
m = Metabasic(domain, session_id="foo")
m.select_database()
```
