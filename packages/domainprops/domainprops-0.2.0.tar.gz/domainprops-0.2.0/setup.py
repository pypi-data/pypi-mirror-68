# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['domainprops']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'domainprops',
    'version': '0.2.0',
    'description': 'Parse domain name properties.',
    'long_description': '# Domainprops\n> Parse domain name properties\n\n![test](https://github.com/vikpe/domainprops/workflows/test/badge.svg?branch=master) [![codecov](https://codecov.io/gh/vikpe/domainprops/branch/master/graph/badge.svg)](https://codecov.io/gh/vikpe/domainprops) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Install\n```shell script\npython -m pip install domainprops\n```\n\n## Usage\n```python\nfrom domainprops import domainprops\n\ndomainprops.tld("foo.com")          # "com"\ndomainprops.sld("foo.com")          # "foo"\ndomainprops.is_alpha("foo.com")     # True\ndomainprops.is_numeric("foo.com")   # False\n```\n\n\n## API\nFunction | Returns | Description | Example | Result\n--- | --- | --- | --- | ---\n`tld` | `string` | Top level domain | `tld("foo.com")` | `"com"`\n`sld` | `string` | Sub level domain | `sld("foo.bar.com")` | `"foo.bar"`\n`bld` | `string` | Bottom level domain | `bld("foo.bar.com")` | `"foo"`\n`length` | `int` | Lenght of domain | `length("foo.com")` | `3`\n`idn` | `string` | IDN version of domain | `idn("f⊕⊕.com")` | `"xn--f-vioa.com"`\n`pattern` | `string` | Char pattern | `pattern("foo-123.com")` | `"lll-nnn"`\n`domains` | `list` | Domain parts of domain | `domains("foo.bar.com")` | `["foo", "bar", "com"]`\n`has_alpha` | `bool` | Has alpha characters | `has_alpha("foo.com")` | `True`\n`has_numbers` | `bool` | Has numbers | `has_numbers("foo.com")` | `False`\n`has_alphanum` | `bool` | Has alpha characters and numbers | `has_alphanum("foo.com")` | `False`\n`has_hyphens` | `bool` | Has hyphens | `has_hyphens("foo.com")` | `False`\n`is_alpha` | `bool` | Is strictly alpha characters | `is_alpha("foo.com")` | `True`\n`is_numeric` | `bool` | Is strictly numbers | `is_numeric("foo.com")` | `False`\n`is_alphanumeric` | `bool` | Is strictly alpha characters and/or numbers | `is_alphanumeric("foo.com")` | `True`\n`is_subdomain` | `bool` | Is sub domain | `is_subdomain("foo.com")` | `False`\n',
    'author': 'Viktor Persson',
    'author_email': 'viktor.persson@arcsin.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vikpe/domainprops',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
