class Location(object):
    def __init__(self, lon=0.0, lat=0.0):
        self.lon = lon
        self.lat = lat
     
    def __str__(self):
        return '<%s(%.2f, %.2f)>' % (self.__class__.__name__, self.lon, self.lat)

class Vect2d(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
     
    def __str__(self):
        return '<%s(%.2f, %.2f)>' % (self.__class__.__name__, self.x, self.y)
        
class Vect3d(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
     
    def __str__(self):
        return '<%s(%.2f, %.2f, %.2f)>' % (self.__class__.__name__, self.x, self.y, self.z)

class Color(object):
    '''0 to 255 color space'''
    def __init__(self, red=0, green=0, blue=0, alpha=0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        
    def __str__(self):
        return '<%s(%d, %d, %d, %d)>' % (self.__class__.__name__, self.red, self.green, self.blue, self.alpha)

class Point(object):
    #TODO: time can also be represented by the tag <t>
    def __init__(self, x=0.0, y=0.0, z=None, time=None):
        self.x = x
        self.y = y
        self.z = z
        self.time = time
        
    def __str__(self):
        values = [self.x, self.y]
        if self.z:
            values.append(self.z)
        if self.time:
            values.append(self.time)
        returnStr = '<%s(' % self.__class__.__name__
        for value in values:
            returnStr += '%.2f, ' % value
        return returnStr.rstrip(', ')+')>'
