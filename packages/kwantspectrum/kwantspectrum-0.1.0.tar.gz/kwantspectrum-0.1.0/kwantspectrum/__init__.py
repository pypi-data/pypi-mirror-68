# Copyright 2018-2020 kwantspectrum authors.
#
# This file is part of kwantspectrum.  It is subject to the license terms in
# the file LICENSE.rst found in the top-level directory of this distribution.

__all__ = []

from . import version, kwant_spectrum

version.ensure_python()
__version__ = version.version

available = [
    ('kwant_spectrum', kwant_spectrum.__all__)
]

for module, names in available:
    exec('from .{0} import {1}'.format(module, ', '.join(names)))
    __all__.extend(names)

