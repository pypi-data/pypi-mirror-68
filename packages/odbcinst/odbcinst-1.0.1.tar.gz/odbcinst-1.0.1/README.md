# odbcinst

return output from unixODBC `odbcinst` command

### Installation

```
pip install odbcinst
```
### Usage

The `.j()` function executes `odbcinst -j`. If called with no argument it
returns a dict. If called with a str argument it returns the specified value.

```python
from pprint import pprint

import odbcinst

pprint(odbcinst.j())
"""console output:
{'DRIVERS': '/etc/odbcinst.ini',
 'FILE DATA SOURCES': '/etc/ODBCDataSources',
 'SQLLEN Size': '8',
 'SQLSETPOSIROW Size': '8',
 'SQLULEN Size': '8',
 'SYSTEM DATA SOURCES': '/etc/odbc.ini',
 'USER DATA SOURCES': '/home/gord/.odbc.ini',
 'unixODBC': '2.3.4'}
"""

print(repr(odbcinst.j("unixODBC")))
# '2.3.4'
```

If unixODBC is not installed then the results are

```python
pprint(odbcinst.j())
"""console output:
{'unixODBC': None}
"""

print(repr(odbcinst.j("SYSTEM DATA SOURCES")))
# None
```
