
from plotly import graph_objs as go
from plotly.offline import iplot

import matplotlib.pyplot as plt

from . segments import Segments
from . utils import plotly_go, plotly_layout
from . utils import matplotlib_plot


class Bewley:

    def __init__(self, line_length, speed, fault_location, depth=5):

        self._line_length = line_length
        self._speed = speed
        self._fault_location = fault_location
        self._depth = depth

        self._create_segments()

    def _create_segments(self):
        y0 = 0
        x0 = 0
        x1 = self._line_length
        xf = self._fault_location

        self._left_segments = Segments(y0, x0, xf, x1, self._speed, "left")
        self._right_segments = Segments(y0, x0, xf, x1, self._speed, "right")

        self._left_segments._add_first_segment()
        self._right_segments._add_first_segment()

        for i in range(self._depth):
            if self._left_segments._min_leaf()._y1 < self._right_segments._min_leaf()._y1:
                self._left_segments._add_one_segment()
            else:
                self._right_segments._add_one_segment()

    def segments(self):
        return {'left': self._left_segments, 'right': self._right_segments }

    def plot(self):
        return matplotlib_plot(self.segments())
    
    def plotly_figure(self):
        scatter = plotly_go(self.segments())
        layout = plotly_layout()
        return go.Figure(data=scatter, layout=layout)

    def plotly(self):
        iplot(self.plotly_figure())

