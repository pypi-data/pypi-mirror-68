######################################################
[plum-boost] Performance enhancer for plum-py package.
######################################################

The |plum-py| Python package provides strictly Python based classes and
utility functions to efficiently pack and unpack bytes. When installed,
the "C" based implementations in this package are leveraged by the
|plum-py| package to improve packing and unpacking performance in the
following areas:

    - Integers (including Enums, Bit Fields, and Bit Flags)
    - Floats
    - Structures (fixed sized)


The same as the |plum-py| package, this package requires Python 3.6 or later.
At a shell prompt, use `pip <https://pypi.python.org/pypi/pip>`_ to
automatically download and install the latest version of this package::

    python -m pip install --upgrade plum-boost


.. Note::
    Installation of this package requires a C or C++ compiler on your system.
    On Microsoft Windows, follow the instructions contained within the traceback
    should the installation fail for this reason. For OS-X and Linux, your system
    likely has the ``gcc` compiler already installed. But you may need to install
    the necessary Python header (.h) files for the version of Python on your
    system (e.g. on Debian based Linux: ``$sudo apt-get install python3.8-dev``).


The |plum-py| package inspects the ``ENABLE_PLUM_BOOST`` environment variable
to control usage of this package and supports the following selections:

    :AUTO: use this package if installed (the default)
    :YES:  use this package (raise exception if not installed)
    :NO:   do not use this package (regardless if installed)

If ``plum-boost`` is installed and the ``ENABLE_PLUM_BOOST`` is set to ``AUTO``
or ``YES`` (or isn't set at all), the |plum-py| package package utilizes the
"C" based implementations this package offers. The full |plum-py| API and feature
set remain available when ``plum-boost`` is enabled, but only certain |plum-py|
features benefit from performance enhancements offered by this package. If
``ENABLE_PLUM_BOOST`` is set to ``NO``, |plum-py| does not leverage this package,
regardless if it is installed.


*******
License
*******

``plum-boost`` is licensed under the same "MIT License" as the |plum-py| package. See the
`plum-py license documentation <https://plum-py.readthedocs.io/en/latest/about.html#license>`_
for the full license text.


************
Contributors
************

- Dan Gass, primary author (dan.gass@gmail.com)


***********
Development
***********

``plum-boost`` shares the same development resources, standards, and work-flows
as the |plum-py| package. See the
`plum-py development documentation <https://plum-py.readthedocs.io/en/latest/about.html#development>`_
for details.


*************
Release Notes
*************

Versions increment per `semver <http://semver.org/>`_ (except for 0.X.Y beta versions).

+ 0.1.0 2020-May-TBD (BETA)

    - Initial release.

.. |plum-py| replace:: `plum-py <https://plum-py.readthedocs.io/en/latest/index.html>`_
