# flake8: noqa
import logging

__author__ = "MondoBrain"
__version__ = "1.0.0-alpha.8"


# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("mondobrain").addHandler(logging.NullHandler)


from mondobrain.core.api import MondoDataFrame, MondoSeries  # isort:skip
from mondobrain.client import Client  # isort:skip
from mondobrain.prescriber import Solver  # isort:skip
