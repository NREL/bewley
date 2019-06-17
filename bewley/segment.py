


class Segment:
    
    def __init__(self, x0, y0, x1, drop, column, color):
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y0 + drop
        self._column = column
        self._leaf = True
        self._color = color
    
    @property
    def color(self):
        return self._color
    
    @property
    def x0(self):
        return self._x0
    
    @property
    def y0(self):
        return self._y0        
        
    @property
    def x1(self):
        return self._x1
    
    @property
    def y1(self):
        return self._y1
    
    @property
    def column(self):
        return self._column
    
    @property
    def leaf(self):
        return self._leaf
    
    @leaf.setter
    def leaf(self, value):
        self._leaf = value