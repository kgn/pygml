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
        '''Access the brush for the stroke'''
        return self.__brush
    
    def setBrush(self, brush):
        '''Set the brush for the stroke'''
        self.__brush = brush
    
    def addPoint(self, x=0.0, y=0.0, z=None, time=None):
        '''Add a point to the stroke'''
        self.__points.append(Point(x, y, z, time))
        
    def iterPoints(self):
        '''Iterate over the points in the stroke'''
        for point in self.__points:
            yield point
