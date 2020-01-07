# Pelican Quick Site Builder (pelican-qsb)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d7c3dca874f04f4687b653f23f834630)](https://www.codacy.com/manual/dmytrohoi/pelican_makesite_script?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dmytrohoi/pelican_makesite_script&amp;utm_campaign=Badge_Grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/dmytrohoi/pelican-qsb/blob/master/LICENSE.md)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/dmytrohoi/pelican_makesite_script)](https://github.com/dmytrohoi/pelican-qsb/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/dmytrohoi/pelican_makesite_script)](https://github.com/dmytrohoi/pelican-qsb/releases)
[![PyPI](https://img.shields.io/pypi/v/pelican-qsb)](https://pypi.org/project/pelican-qsb/)

## About

Script can help to build local server or push site to GitHub. Have additional
sub-arguments.

**Attention!**
Use only in your virtual environment!
All "git push" actions are used with the `--force` flag, so all commits will be rewritten.

-----
## Usage

### Requirements
 - [Pelican](https://github.com/getpelican/pelican)
 - [Python](https://python.org) >= 3.6
 - [ghp-import](https://github.com/davisp/ghp-import)

### Get start:

Pre-requirements:

- Install and configure [Pelican](@getpelican) - _[Instruction](https://docs.getpelican.com/en/stable/install.html)_

Install script:
  - From sources:
1. Clone this repository using Git to your Pelican folder

``` bash
# Simple way to clone pelican-qsb
git clone --depth=1 https://github.com/dmytrohoi/pelican-qsb.git qsb && rm -rf ./qsb/.git
```

2. Run pelican-qsb script for the first time and configure it

``` bash
# NOTE: './qsb/' it's the PATH to pelican-qsb project dir
python ./qsb/make_site.py
```

  - From pip:

1. Install script from pip:

``` bash
pip install pelican-qsb
```

2. Run pelican-qsb script in your Pelican directory for the first time and configure it:

``` bash
pelican-qsb
```


## Functions:

``` bash
github   [-d] [-b]    # make gh-output and push it to github repository
                      # (without [d]raft and [b]ackup as default)
local                 # make local server using pelicanconf.py file
backup                # backup all files in your Pelican directory to backup repository

-h, --help                # print help info
```
-----

_Created by Dmytro Hoi, 2019_
