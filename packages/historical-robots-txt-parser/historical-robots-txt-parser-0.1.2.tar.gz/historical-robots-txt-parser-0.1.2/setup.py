# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['historical_robots']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'historical-robots-txt-parser',
    'version': '0.1.2',
    'description': 'Parses historical robots.txt files from Wayback Machine',
    'long_description': "[![PyPI version shields.io](https://img.shields.io/pypi/v/historical-robots-txt-parser.svg)](https://pypi.python.org/pypi/historical-robots-txt-parser/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n\n\n\n# Historical Robots.txt Parser\n\nThis is a small Python package that parses the historical robots.txt files from the Internet Archive's Wayback Machine and coerces the data into a CSV file for tracking addition and removal of `Allow` and `Disallow` rules by timestamp of addition, path, user-agent, rule type (optional). It's a fairly narrow use case but may be helpful to researchers or journalists.\n\nIt also includes a parser to coerce a robots.txt file into a dictionary.\n\n## Requirements\n* Python 3.7 or later\n\n## Installation\n#### Install with Python\n```\npip3 install historical-robots-txt-parser\n```\n\n#### Install with Git\nThis package was developed using [Poetry](https://github.com/python-poetry/poetry), which greatly simplifies the experience of dealing with dependencies and everything. Using Poetry is strongly recommended.\n\n```\ngit clone https://github.com/alexlitel/historical-robots-txt-parser\ncd historical-robots-txt-parser\npoetry install\n```\n\nThere is a `requirements.txt` file included here, so you can also use `pip3 install -r requirements.txt` if you don't want to use Poetry.\n\n## Usage\nThere are two functions included in the package: `parse_robots_txt` and `historical_scraper`. `historical_scraper` scrapes the historical files for a domain from the Wayback Machine and exports to a CSV. `parse_robots_txt` makes a request to a robots.txt file, parses and coerces it to a dictionary. If you clone the repo, there's a file `app.py` which takes command line arguments for domains to scrape.\n\n\n### historical_scraper\n#### Usage\n```\nfrom historical_robots import historical_scraper\n\nhistorical_scraper('website.com', 'website.csv', <optional arguments>)\n```\n\n#### Parameters\n| parameter | type | required | default value | description |\n|----------------------|------------|----------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------|\n| domain | string | true |  | The domain to scrape records from. Only should be hostname without `www`. |\n| file_path | string | true |  | Path of CSV file to export to |\n| accept_allow | boolean | false | False | Whether to allow parser to parse `Allow` rules and include those in dataset. Adds a new column to CSV for `Rule` to note `Disallow` or `Allow` rule. By default, function only checks `Disallow` rules.\n| skip_scrape_interval | boolean | false | False | Whether to skip the default sleep interval between each historical robots.txt request.  `True` value may cause errors. |\n| sleep_interval | number | false | 0.05 | Number of seconds to sleep in between robots.txt requests.  Ignored if `skip_scrape_interval` is `True` |\n| params | dictionary | false | {} | Key value pairs representing [valid URL params for the Wayback CDX API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) |\n\n\n\n### parse_robots_txt\n#### Usage\n```\nfrom historical_robots import parse_robots_text\n\nparse_robots_txt('https://www.website.com/robots.txt', False)\n```\n\n#### Parameters\n| parameter | type | required | default value | description |\n|----------------------|------------|----------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------|\n| URL | string | true |  | The URL to request robots.txt file from. |\n| accept_allow | boolean | false | False | Whether to parse `Allow` rules. By default, function only checks `Disallow` rules.\n\n\n",
    'author': 'Alex Litel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexlitel/historical-robots-txt-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
