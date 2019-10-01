
from . segment import Segment
import matplotlib.pyplot as plt
import itertools

class Segments(object):
    
    def __init__(self, vlines, speed, fault_index):
        self._vlines = vlines
        self._speed = speed
        self._fault_index = fault_index
        self._segments = []
        self.create()
    
    def create(self, lines=100, left_color="blue", right_color="green"):   
        
        self._segments = []
        BLUES = ['#f0f9e8','#ccebc5','#a8ddb5','#7bccc4','#4eb3d3','#2b8cbe','#08589e']
        GREENS = ['#fef0d9','#fdd49e','#fdbb84','#fc8d59','#ef6548','#d7301f','#990000']

        self._dist = [ x - y for x, y in zip(self._vlines[1:], self._vlines[:-1]) ]
        self._drop = [ x/y for x, y in zip(self._dist, self._speed)]
        
        line_left = Segment(self._vlines[self._fault_index], 
                            0, 
                            self._vlines[self._fault_index-1], 
                            self._drop[self._fault_index-1], 
                            self._fault_index-1, 
                            left_color)
        
        self._segments.append( line_left )

        line_right =  Segment(self._vlines[self._fault_index], 
                              0, 
                              self._vlines[self._fault_index+1], 
                              self._drop[self._fault_index], 
                              self._fault_index+1, 
                              right_color)
        
        self._segments.append( line_right )

        for x in range(lines):

            # get the leaf with the lowest y1 value
            line = sorted([ x for x in self._segments if x.leaf ], key=lambda x: x.y1)[0]
            line.leaf = False
            try:
                index = line.column-1
                if index >= 0:
                    tmp = Segment(line.x1, 
                                  line.y1, 
                                  self._vlines[line.column-1], 
                                  self._drop[line.column-1], 
                                  line.column-1, 
                                  line.color)
                    self._segments.append( tmp )
            except IndexError:   
                pass

            try:
                tmp = Segment(line.x1, 
                              line.y1, 
                              self._vlines[line.column+1], 
                              self._drop[line.column], 
                              line.column+1, 
                              line.color)
                self._segments.append( tmp )
            except IndexError:
                pass   
    
    def min(self):
        return min([ x.y0 for x in self._segments])

    def max(self):
        return max([ x.y0 for x in self._segments])

    def range(self):
        return (self.max(), self.min())

    @property
    def critical_points(self):
        yvals = [ (x.color, x.y1) for x in self._segments ] + [ (x.color, x.y0) for x in self._segments ]
        yvals = sorted(yvals, key=lambda x: x[0])

        res = {}
        for key, group in itertools.groupby(yvals, lambda x: x[0]):
            res[key] = sorted([ x[1] for x in group])
        return res


    def plot(self, ax=None, lw=2):
        if ax is None:
            fig, ax = plt.subplots(figsize=(12,8))
         
        for v in self._vlines:
            ax.axvline(v, linestyle='--', color="steelblue", lw=1)

        for seg in self._segments:
            ax.plot([ seg._x0, seg._x1 ], 
                    [ seg._y0, seg._y1 ], 
                     zorder=-100,
                     color=seg.color, alpha=0.75, lw=lw)

        ax.invert_yaxis()
        ax.set_ylim(self.max(), self.min())
        
        ax.set_xlabel("bus position")
        ticks = ax.get_yticks()
        ax.set_yticklabels([ round(x*1e6) for x in ticks])
        ax.set_ylabel("Time (microseconds)")

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        