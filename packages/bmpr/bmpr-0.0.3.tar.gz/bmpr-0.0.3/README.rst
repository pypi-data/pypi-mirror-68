========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-bmpr/badge/?style=flat
    :target: https://readthedocs.org/projects/python-bmpr
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/samesense/python-bmpr.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/samesense/python-bmpr

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/samesense/python-bmpr?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/samesense/python-bmpr

.. |requires| image:: https://requires.io/github/samesense/python-bmpr/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/samesense/python-bmpr/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/samesense/python-bmpr/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/samesense/python-bmpr

.. |version| image:: https://img.shields.io/pypi/v/bmpr.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/bmpr

.. |wheel| image:: https://img.shields.io/pypi/wheel/bmpr.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/bmpr

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/bmpr.svg
    :alt: Supported versions
    :target: https://pypi.org/project/bmpr

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/bmpr.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/bmpr

.. |commits-since| image:: https://img.shields.io/github/commits-since/samesense/python-bmpr/v0.0.3.svg
    :alt: Commits since latest release
    :target: https://github.com/samesense/python-bmpr/compare/v0.0.3...master



.. end-badges

Bump images

* Free software: MIT license

Installation
============

::

    pip install bmpr

You can also install the in-development version with::

    pip install https://github.com/samesense/python-bmpr/archive/master.zip


Documentation
=============


https://python-bmpr.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
