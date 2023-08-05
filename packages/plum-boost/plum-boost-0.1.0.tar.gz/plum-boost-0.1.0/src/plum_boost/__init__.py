# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2020 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""plum accelerated utility functions and accelerated methods."""

# FUTURE: remove theses (pipelines fail, but the dev env doesn't without them)
# pylint: disable=import-self,no-name-in-module

from . import _fastint as fastint
from . import _faststructure as faststructure
from ._utils import pack, unpack, unpack_from
