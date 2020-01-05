# Pelican site builder helper

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d7c3dca874f04f4687b653f23f834630)](https://www.codacy.com/manual/dmytrohoi/pelican_makesite_script?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dmytrohoi/pelican_makesite_script&amp;utm_campaign=Badge_Grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/dmytrohoi/pelican_makesite_script )
![GitHub Release Date](https://img.shields.io/github/release-date/dmytrohoi/pelican_makesite_script)

## About

Script can help to build local server or push site to GitHub. Have additional 
sub-arguments.

        Attention! Use only in your virtual enviroment!

-----
## Usage

### Requirements
 - Pelican
 - Python >= 3.6
 - Git

### Instruction:
 1. Install and configure [Pelican](@getpelican) and Git
 2. Clone this repository to your Pelican folder
 3. When you first run - configure script

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
