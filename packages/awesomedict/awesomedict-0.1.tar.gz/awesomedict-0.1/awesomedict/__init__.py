from .awesomedict import AwesomeDict

import logging as _logging
try:  # Python 2.7+
    from logging import NullHandler as _NullHandler
except ImportError:
    class _NullHandler(_logging.Handler):
        def emit(self, record):
            pass

_logger = _logging.getLogger(__name__)
_logger.addHandler(_NullHandler())
