from Math import Point

class Stroke(object):
    def __init__(self):
        self.__points = []
        
    def addPoint(self, x=0.0, y=0.0, z=0.0, time=0.0):
        self.__points.append(Point(x, y, z, time))
        
    def iterPoints(self):
        for point in self.__points:
            yield point
