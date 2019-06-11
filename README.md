# Pelican site builder helper

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

Version: 0.2
Last change: 06/11/19
Created by Dmytro Hoi, 2019
