from xml.etree import ElementTree

class MathBase(object):
    def _store(self, xml):
        for key, value in self._data():
            if value is None:
                continue
            entry = ElementTree.SubElement(xml, key)
            entry.text = str(value)

class Location(MathBase):
    def __init__(self, lon=0.0, lat=0.0):
        self.lon = lon
        self.lat = lat
     
    def _data(self):
        return (
            ('lon',self.lon),
            ('lat',self.lat),
        )
     
    def __str__(self):
        return '<%s(%.2f, %.2f)>' % (self.__class__.__name__, self.lon, self.lat)

class Vect2d(MathBase):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
     
    def _data(self):
        return (
            ('x',self.x),
            ('y',self.y),
        )
     
    def __str__(self):
        return '<%s(%.2f, %.2f)>' % (self.__class__.__name__, self.x, self.y)
        
class Vect3d(MathBase):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def _data(self):
        return (
            ('x',self.x),
            ('y',self.y),
            ('z',self.z),
        )
     
    def __str__(self):
        return '<%s(%.2f, %.2f, %.2f)>' % (self.__class__.__name__, self.x, self.y, self.z)

class Color(MathBase):
    '''0 to 255 color space'''
    def __init__(self, r=0, g=0, b=0, a=None):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        
    def _data(self):
        data = [
            ('r',self.r),
            ('g',self.g),
            ('b',self.b),
        ]
        if self.a:
            data.append(('a',self.a))
        return data
        
    def __str__(self):
        values = [self.r, self.g, self.b]
        if self.a:
            values.append(self.a)
        returnStr = '<%s(' % self.__class__.__name__
        for value in values:
            returnStr += '%d, ' % value
        return returnStr.rstrip(', ')+')>'

class Point(MathBase):
    #TODO: time can also be represented by the tag <t>
    def __init__(self, x=0.0, y=0.0, z=None, time=None):
        self.x = x
        self.y = y
        self.z = z
        self.time = time
        
    def _data(self):
        data = [
            ('x',self.x),
            ('y',self.y),
        ]
        if self.z:
            data.append(('z',self.z))
        if self.time:
            data.append(('time',self.time))
        return data
        
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
