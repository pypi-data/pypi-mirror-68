[![pipeline status](https://gitlab.com/coopdevs/pyopencell/badges/master/pipeline.svg)](https://gitlab.com/coopdevs/pyopencell/commits/master)
[![coverage report](https://gitlab.com/coopdevs/pyopencell/badges/master/coverage.svg)](https://gitlab.com/coopdevs/pyopencell/commits/master)

> :heart: Inspired by [PyOTRS](https://gitlab.com/rhab/PyOTRS) :heart:

PyOpenCell is a Python wrapper for accessing [Open Cell](https://www.opencellsoft.com/) (Version 6) using the
REST API.

You can see all the API information [here](https://api.opencellsoft.com/6.0.0)

Features
--------

Access an OpenCell instance to:

* find a Customer by ID

Installation
============

Dependencies
------------

Create a virtualenv before installing dependencies.

If you are using `virtualenvwrapper` (https://virtualenvwrapper.readthedocs.io/en/latest/).

* Create virtualenv with python 2.7

```commandline
$ which python
/usr/bin/python
$ mkvirtualenv --python=/usr/bin/python pyopencell
```
If you are using [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin:
```commandline
$ pyenv virtualenv pyopencell
```

* Install requirements:

```commandline
$ pip install -r requirements.txt
```

Configuration Environment
-------------------------

You need define the OpcenCell API credentials as environment variables. You need define:

```
OPENCELL_BASEURL=<YOUR OC HOST>/opencell
OPENCELL_USER=<YOUR OC USER>
OPENCELL_PASSWORD=<YOUR OC PASSWORD>
```

If this envvars are not defined, a exception will be raised with the name of the envvar not defined.

Python Usage
============

Run test suite
----------

```commandline
$ tox
```

Release process
---

Update CHANGELOG.md following this steps:

1. Add any entries missing from merged merge requests.
1. Duplicate the `[Unreleased]` header.
1. Replace the second `Unreleased` with a version number followed by the current date. Copy the exact format from previous releases.

Then, you can release and publish the package to PyPi:

1. Update the `VERSION` var in `setup.py` matching the version you specified in the CHANGELOG.
1. Open a merge request with these changes for the team to approve
1. Merge it, add a git tag on that merge commit and push it.
1. Once the pipeline has successfully passed, go approve the `publish` step.

License
=======
