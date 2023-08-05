# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2020 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""plum-boost package builder/installer."""

from setuptools import Extension, setup, find_packages

LONG_DESCRIPTION = """
################################################
[plum-boost] plum-py Package Performance Booster
################################################

The ``plum-py`` Python package provides strictly Python based classes and
utility functions to efficiently pack and unpack bytes. When installed,
the "C" based implementations in this package are leveraged by the
``plum-py`` package to improve packing and unpacking performance in the
following areas:

    - Integers (including Enums, Bit Fields, and Bit Flags)
    - Floats
    - Structures (fixed sized)

"""

setup(
    # pylint: disable=no-member
    name='plum-boost',
    version='0.1.0',
    description='plum-py performance booster.',
    long_description=LONG_DESCRIPTION,
    url='https://gitlab.com/dangass/plum/-/blob/master/boost/README.rst',
    author='Dan Gass',
    author_email='dan.gass@gmail.com',
    maintainer='Dan Gass',
    maintainer_email='dan.gass@gmail.com',
    license='MIT License; http://opensource.org/licenses/MIT',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
    ],
    package_dir={"": "src"},
    packages=find_packages('src'),
    ext_modules=[
        Extension('plum_boost._fastint', sources=['src/extmods/fastint.c']),
        Extension('plum_boost._faststructure', sources=['src/extmods/faststructure.c']),
        Extension('plum_boost._utils', sources=['src/extmods/utils.c']),
    ],
    install_requires=[
        'plum-py',
    ]
)
