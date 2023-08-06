# ⛩️God Slayer⚔️

[![See Build Status on Travis CI](https://travis-ci.org/yukihiko-shinoda/god-slayer.svg?branch=master)](https://travis-ci.org/yukihiko-shinoda/god-slayer)
[![Test Coverage](https://api.codeclimate.com/v1/badges/2d37a5447afd27d46af1/test_coverage)](https://codeclimate.com/github/yukihiko-shinoda/god-slayer/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/2d37a5447afd27d46af1/maintainability)](https://codeclimate.com/github/yukihiko-shinoda/god-slayer/maintainability)
[![Updates](https://pyup.io/repos/github/yukihiko-shinoda/god-slayer/shield.svg)](https://pyup.io/repos/github/yukihiko-shinoda/god-slayer/)
[![Python versions](https://img.shields.io/pypi/pyversions/god-slayer.svg)](https://pypi.org/project/god-slayer)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fyukihiko-shinoda%2Fgod-slayer)](http://twitter.com/share?text=God%20Slayer&url=https://pypi.org/project/godslayer/&hashtags=python)

Provides generator to read Kami (god) CSV record as list of string.

## Context

### It's beyond CSV module😱

We often face CSV files like this:

population|&nbsp;|&nbsp;|&nbsp;
-|-|-|-
age|total number|male|female
0～4|21303|10867|10436
0|4062|2069|1993
1|4279|2171|2108
2|4285|2152|2133
3|4434|2268|2166
4|4243|2207|2036
5～9|21017|10956|10061
5|4369|2283|2086
6|4345|2213|2132
7|4117|2163|1954
8|4155|2146|2009
9|4031|2151|1880
sum|42320|21823|20497
material: Residents' Culture Department Resident Registration Section|&nbsp;|&nbsp;|&nbsp;

It's beyond [CSV module]😱
We just want the population for each age ...

We call such a CSV file [Kami CSV](#what-is-kami-csv).

## Features

### Let's iterate to read only required row from CSV💡

- ⚔️ Skips to the row after the header row
- ⚔️ Skips partition rows
- ⚔️ Stops iteration bedore footer row

## Quickstart

```console
pip install godslayer
```

Let's resolve above example:

```python
from pathlib import Path

def print_required_row():
    god_slayer_factory = GodSlayerFactory(
        header=["age", "total", "male", "female"],
        partition=[r"^\d*〜\d*$", r"^\d*$", r"^\d*$", r"^\d*$"],
        footer=["sum", r"^\d*$", r"^\d*$", r"^\d*$"],
        encoding="shift_jis_2004",
    )
    god_slayer = god_slayer_factory.create(Path("/path/to/file.csv"))

    for record in god_slayer:
        print(record)
```

```console
['0', '4062', '2069', '1993']
['1', '4279', '2171', '2108']
['2', '4285', '2152', '2133']
['3', '4434', '2268', '2166']
['4', '4243', '2207', '2036']
['5', '4369', '2283', '2086']
['6', '4345', '2213', '2132']
['7', '4117', '2163', '1954']
['8', '4155', '2146', '2009']
['9', '4031', '2151', '1880']
```

Note that file will be closeed automatically when variable `god_slayer` goes out of scope.

## Specification

### Argument of GodSlayerFactory

property|type|defalut|explanation
-|-|-|-
header|Optional\[List\[str\]\]|None|If present, God Slayer will skip to the row after the header row
partition|Optional\[List\[str\]\]|None|If present, God Slayer will skip partition rows
footer|Optional\[List\[str\]\]|None|If present, God Slayer will stop iteration bedore footer row
encoding|str|"utf-8"|Encoding to open CSV file

### How to match list of string with row

- List of strings has the same length as row
- All strings in the list are compared with the string at the same index in the row and must be one of the following:
  - Same string
  - Matched the regular expression

cf. [list_string_matcher.py]

<!-- markdownlint-disable no-trailing-punctuation -->
## What is "Kami CSV"?
<!-- markdownlint-enaable no-trailing-punctuation -->

"Kami CSV" is a CSV that has become a non-normal form
by adding headers, footers, intermediate lines, and notes
even though the purpose is to export data.
The etymology comes from [Kami Excel].
It's often found in government office or Legacy company service.

## Contributing

Check [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## Credits

This package was created with [Cookiecutter] and the [audreyr/cookiecutter-pypackage] project template.

[list_string_matcher.py]: https://github.com/yukihiko-shinoda/god-slayer/blob/master/godslayer/list_string_matcher.py
[CSV module]: https://docs.python.org/3/library/csv.html
[Kami Excel]: https://www.atmarkit.co.jp/ait/articles/1612/26/news032.html
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[audreyr/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
