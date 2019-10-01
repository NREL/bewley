import matplotlib.pyplot as plt
from . segments import Segments


class Bewley(object):

    def __init__(self, line_length, speed, fault_location, depth=5):

        self._line_length = line_length
        self._speed = speed
        self._fault_location = fault_location
        self._depth = depth

