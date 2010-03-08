class Location(object):
    def __init__(self, lon=0.0, lat=0.0):
        self.lon = lon
        self.lat = lat
     
    def __str__(self):
        return '<%s(%.2f, %.2f)>' % (self.__class__.__name__, self.lon, self.lat)
        
class Vect3d(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
     
    def __str__(self):
        return '<%s(%.2f, %.2f, %.2f)>' % (self.__class__.__name__, self.x, self.y, self.x)

class Point(object):
    def __init__(self, x=0.0, y=0.0, z=0.0, time=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.time = time
        
    def __str__(self):
        return '<%s(%.2f, %.2f, %.2f, %.2f)>' % (self.__class__.__name__, self.x, self.y, self.z, self.time)
