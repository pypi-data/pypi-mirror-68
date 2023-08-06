<a href="https://covid19datahub.io"><img src="https://storage.covid19datahub.io/logo.svg" align="right" height="128"/></a>

# Python Interface to COVID-19 Data Hub

Python csv parser `csv.reader()` does not seem to parse the csv well,
since it cannot work with the quotation marks around strings.

However `read_csv()` from [pandas](https://pandas.pydata.org/) is processing it fine.

To make a successful call, you also have to specify `User-Agent` header, see [here](https://datascience.stackexchange.com/questions/49751/read-csv-file-directly-from-url-how-to-fix-a-403-forbidden-error), the request is hence sent separately using [requests](https://requests.readthedocs.io/en/master/) library.

Install `pandas` and `requests` by typing into terminal:

```bash
pip install pandas requests
```

Once installed, fetch the data:

```python
# standard library
from io import StringIO
# nonstandard - download separately
import pandas as pd # Pandas
import requests # HTTP Request library
# download
url = "https://storage.covid19datahub.io/data-1.csv"
response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})
# make response iterable string
data = StringIO(response.text)
# load into pandas
df = pd.read_csv(data)
```
