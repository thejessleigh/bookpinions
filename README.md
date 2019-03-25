# bookpinions

Toy app for finding your 10 most "controversial" goodreads ratings

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://camo.githubusercontent.com/28a51fe3a2c05048d8ca8ecd039d6b1619037326/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667)](https://github.com/ambv/black)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Coverage Status](https://coveralls.io/repos/github/thejessleigh/bookpinions/badge.svg?branch=master)](https://coveralls.io/github/thejessleigh/bookpinions?branch=master)
[![Build Status](https://travis-ci.org/thejessleigh/bookpinions.svg?branch=master)](https://travis-ci.org/thejessleigh/bookpinions)

# Requirements

This project uses Python 3.7.0 and is built in Django 2.1.7.

This project also uses pre-commit to enforce `black` and `blackened-docs` code style for Python and `prettier` code style for html, css, js, md and yaml files. After installing the requirements from `requirements.txt`, run `pre-commit install` to get it up and running locally. Pre-commit will run on files staged for change automatically. You can also check pre-commit hook compliance on staged files by running pre-commit run at any time. Note that pre-commit ignores files that are not staged for change.
