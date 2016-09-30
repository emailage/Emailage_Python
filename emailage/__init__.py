"""Package for Emailage."""

import sys

__project__ = 'emailage-official'
__version__ = '1.0.1'

VERSION = "{0} v{1}".format(__project__, __version__)

PYTHON_VERSION = 2, 7

if sys.version_info < PYTHON_VERSION:  # pragma: no cover (manual test)
    sys.exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))
