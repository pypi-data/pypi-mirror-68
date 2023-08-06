# bifrostapi

Contains the python library for connecting with the bifrost database. Used by bifrost and beone dashboards.

## Installation

```bash
pip install bifrostapi
```

## Usage

```python
import bifrostapi
# Call this once before making any other calls.
bifrostapi.add_URI("mongodb://user:pass@hostname:27017/dbname")

bifrostapi.get_run_list()

```

Or with multiple databases:

```python
import bifrostapi

bifrostapi.add_URI("mongodb://user:pass@hostname:27017/dbname", "db1")
bifrostapi.add_URI("mongodb://user:pass@hostname:27017/dbname", "db2")

bifrostapi.get_run_list(connection_name="db1")

bifrostapi.get_run_list(connection_name="db2")
```
