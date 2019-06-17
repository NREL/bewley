
__version__ = "0.0.1"

from . bewley import Bewley

from . segment import Segment
from . segments import Segments

from . utils import plot_config

def init_notebook_mode():
    """ Wrapper for convenience"""
    from plotly.offline import init_notebook_mode

    init_notebook_mode(connected=True)