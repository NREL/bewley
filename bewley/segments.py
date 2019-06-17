
from . segment import Segment
import matplotlib.pyplot as plt

class Segments:
    
    def __init__(self, vlines, speed, fault_index):
        self._vlines = vlines
        self._speed = speed
        self._fault_index = fault_index
        self._segments = []
    
    def create(self, lines = 1000):   
        
        self._dist = [ x - y for x, y in zip(self._vlines[1:], self._vlines[:-1]) ]
        self._drop = [ x/y for x, y in zip(self._dist, self._speed)]
        
        line_left = Segment(self._vlines[self._fault_index], 
                            0, 
                            self._vlines[self._fault_index-1], 
                            self._drop[self._fault_index-1], 
                            self._fault_index-1, 
                            "red")
        
        self._segments.append( line_left )

        line_right =  Segment(self._vlines[self._fault_index], 
                              0, 
                              self._vlines[self._fault_index+1], 
                              self._drop[self._fault_index], 
                              self._fault_index+1, 
                              "blue")
        
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

    def plot(self, ax=None, lw=1):
        standalone = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(12,8))
            standalone = True

        for v in self._vlines:
            ax.axvline(v, linestyle='--', color="steelblue", lw=1)

        for seg in self._segments:
            ax.plot([ seg._x0, seg._x1 ], [ seg._y0, seg._y1 ], color=seg.color, alpha=0.5, lw=lw)

        ax.invert_yaxis()
        ax.set_ylim(max([ x.y0 for x in self._segments]), 0)
        if standalone:
            ax.set_ylabel("time(ns)")
            ax.set_xlabel("bus position")
        