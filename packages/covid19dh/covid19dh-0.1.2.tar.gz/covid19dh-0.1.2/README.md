<a href="https://covid19datahub.io"><img src="https://storage.covid19datahub.io/logo.svg" align="right" height="128"/></a>

# Python Interface to COVID-19 Data Hub

Library [covid19dh](https://pypi.org/project/covid19dh/) helps Python users to fetch *COVID-19 Data Hub* data directly into Python.

## Setup and usage

Install with

```python
pip install covid19dh
```

Importing main `covid19()` function with 

```python
from covid19dh import covid19

x = covid19("ITA") # load data
```

## Parametrization

### Date filter

Date can be specified with `datetime.datetime`, `datetime.date`
or as a `str` in format `YYYY-mm-dd`.

```python
from datetime import datetime

x = covid19("SWE", start = datetime(2020,4,1), end = "2020-05-01")
```

### Level

Levels work the same way as in all the other our data fetchers.

1. Country level
2. State, region or canton level
3. City or municipality level

```python
from datetime import date

x = covid19("USA", level = 2, start = date(2020,5,1))
```

### Cache

Library keeps downloaded data in simple way during runtime. By default, using the cached data is enabled.

Caching can be disabled (e.g. for long running programs) by

```python
x = covid19("FRA", cache=False)
```


