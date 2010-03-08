from Math import Point

class Brush(object):
    #TODO: implement brush
    def __init__(self, **args):
        pass

class Stroke(object):
    def __init__(self):
        self.__brush = None
        self.__points = []
   
    def brush(self):
        return self.__brush
    
    def setBrush(self, brush):
        self.__brush = brush
    
    def addPoint(self, x=0.0, y=0.0, z=0.0, time=0.0):
        self.__points.append(Point(x, y, z, time))
        
    def iterPoints(self):
        for point in self.__points:
            yield point
