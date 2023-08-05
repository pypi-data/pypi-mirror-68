# bifrostapi

Contains the python library for connecting with the bifrost database. Used by bifrost and beone dashboards.

## Installation

```bash
pip install bifrostapi
```

## Usage

```python
import bifrostapi

bifrostapi.connect("mongodb://user:pass@hostname:27017/dbname")
bifrostapi.get_run_list()

```

Or with multiple databases:

```python
import bifrostapi

bifrostapi.connect("mongodb://user:pass@hostname:27017/dbname", "db1")
bifrostapi.connect("mongodb://user:pass@hostname:27017/dbname", "db2")

bifrostapi.get_run_list(connection_name="db1")

bifrostapi.get_run_list(connection_name="db2")
```
