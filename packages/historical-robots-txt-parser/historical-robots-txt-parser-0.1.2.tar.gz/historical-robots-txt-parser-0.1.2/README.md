[![PyPI version shields.io](https://img.shields.io/pypi/v/historical-robots-txt-parser.svg)](https://pypi.python.org/pypi/historical-robots-txt-parser/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)



# Historical Robots.txt Parser

This is a small Python package that parses the historical robots.txt files from the Internet Archive's Wayback Machine and coerces the data into a CSV file for tracking addition and removal of `Allow` and `Disallow` rules by timestamp of addition, path, user-agent, rule type (optional). It's a fairly narrow use case but may be helpful to researchers or journalists.

It also includes a parser to coerce a robots.txt file into a dictionary.

## Requirements
* Python 3.7 or later

## Installation
#### Install with Python
```
pip3 install historical-robots-txt-parser
```

#### Install with Git
This package was developed using [Poetry](https://github.com/python-poetry/poetry), which greatly simplifies the experience of dealing with dependencies and everything. Using Poetry is strongly recommended.

```
git clone https://github.com/alexlitel/historical-robots-txt-parser
cd historical-robots-txt-parser
poetry install
```

There is a `requirements.txt` file included here, so you can also use `pip3 install -r requirements.txt` if you don't want to use Poetry.

## Usage
There are two functions included in the package: `parse_robots_txt` and `historical_scraper`. `historical_scraper` scrapes the historical files for a domain from the Wayback Machine and exports to a CSV. `parse_robots_txt` makes a request to a robots.txt file, parses and coerces it to a dictionary. If you clone the repo, there's a file `app.py` which takes command line arguments for domains to scrape.


### historical_scraper
#### Usage
```
from historical_robots import historical_scraper

historical_scraper('website.com', 'website.csv', <optional arguments>)
```

#### Parameters
| parameter | type | required | default value | description |
|----------------------|------------|----------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| domain | string | true |  | The domain to scrape records from. Only should be hostname without `www`. |
| file_path | string | true |  | Path of CSV file to export to |
| accept_allow | boolean | false | False | Whether to allow parser to parse `Allow` rules and include those in dataset. Adds a new column to CSV for `Rule` to note `Disallow` or `Allow` rule. By default, function only checks `Disallow` rules.
| skip_scrape_interval | boolean | false | False | Whether to skip the default sleep interval between each historical robots.txt request.  `True` value may cause errors. |
| sleep_interval | number | false | 0.05 | Number of seconds to sleep in between robots.txt requests.  Ignored if `skip_scrape_interval` is `True` |
| params | dictionary | false | {} | Key value pairs representing [valid URL params for the Wayback CDX API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) |



### parse_robots_txt
#### Usage
```
from historical_robots import parse_robots_text

parse_robots_txt('https://www.website.com/robots.txt', False)
```

#### Parameters
| parameter | type | required | default value | description |
|----------------------|------------|----------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| URL | string | true |  | The URL to request robots.txt file from. |
| accept_allow | boolean | false | False | Whether to parse `Allow` rules. By default, function only checks `Disallow` rules.


