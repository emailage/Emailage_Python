"""Package for Emailage."""

import sys

PYTHON_VERSION = 2, 7

if sys.version_info < PYTHON_VERSION:  # pragma: no cover (manual test)
    sys.exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))


from emailage.client import TlsVersions
protocols = TlsVersions()


