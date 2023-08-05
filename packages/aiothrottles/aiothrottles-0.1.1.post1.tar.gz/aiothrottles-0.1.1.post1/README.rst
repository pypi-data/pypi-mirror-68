.. image:: https://img.shields.io/badge/license-BSD-blue.svg
    :target: https://github.com/KonstantinTogoi/aiothrottles/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/aiothrottles.svg
    :target: https://pypi.python.org/pypi/aiothrottles

.. image:: https://img.shields.io/pypi/pyversions/aiothrottles.svg
    :target: https://pypi.python.org/pypi/aiothrottles

.. image:: https://readthedocs.org/projects/aiothrottles/badge/?version=latest
    :target: https://aiothrottles.readthedocs.io/en/latest/

.. image:: https://travis-ci.org/KonstantinTogoi/aiothrottles.svg
    :target: https://travis-ci.org/KonstantinTogoi/aiothrottles

.. index-start-marker1

aiothrottles
============

aiothrottles synchronization primitives are designed to be extension
(along the time) to `asyncio synchronization primitives <https://docs.python.org/3/library/asyncio-sync.html>`__.

aiothrottles has the following basic synchronization primitives:

- Throttle

For more details, see `aiothrottles Documentation <https://aiothrottles.readthedocs.io/>`_.

Usage
-----

Throttle implements a rate limiting for asyncio task.
A throttle can be used to guarantee limited access to a shared resources.

The preferred way to use a Throttle is an
`async with <https://docs.python.org/3/reference/compound_stmts.html#async-with>`__ statement:

.. code-block:: python

    throttle = Throttle('3/s')

    # ... later
    async with throttle:
        # access shared state

which is equivalent to:

.. code-block:: python

    throttle  = Throttle('3/s')

    # ... later
    await throttle.acquire()
    try:
        # access shared state
    finally:
        throttle.release()

A call rate is determined by the :code:`rate` argument.
Pass the rate in the following formats:

* :code:`"{integer limit}/{unit time}"`
* :code:`"{limit's numerator}/{limit's denominator}{unit time}"`

Examples:

* :code:`4/s`, :code:`5/m`, :code:`6/h`, :code:`7/d`
* :code:`1/second`, :code:`2/minute`, :code:`3/hour`, :code:`4/day`
* :code:`1/3s`, :code:`12/37m`, :code:`1/5h`, :code:`8/3d`

Installation
------------

.. code-block:: shell

    pip install aiothrottles

or

.. code-block:: shell

    python setup.py install

Supported Python Versions
-------------------------

Python 3.5, 3.6, 3.7 and 3.8 are supported.

.. index-end-marker1

Test
----

Run all tests.

.. code-block:: shell

    python setup.py test

Run tests with PyTest.

.. code-block:: shell

    python -m pytest [-k TEST_NAME] [-m MARKER]

License
-------

**aiothrottles** is released under the BSD 3-Clause License.
