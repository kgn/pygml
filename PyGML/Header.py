import time
from Math import *

__all__ = ['Client', 'Environment']

class Header(object):
    def iterKeys(self):
        for key in self._values.iterkeys():
            yield key
       
    def get(self, key):
        return self._values.get(key, None)
        
    def set(self, key, value):
        if key in self._values:
            self._values[key] = value
    
    def __pprintDict(self):
        ppDict = {}
        for key, value in self._values.iteritems():
            if value:
                ppDict[key] = str(value)
        return ppDict
           
    def __str__(self):
        return '<%s(%s)>' % (self.__class__.__name__, self.__pprintDict())

class Environment(Header):
    def __init__(self, **args):
        #TODO: overwrite values with passed in args
        self._values = {
            'offset':None,
            'rotation':None,
            'up':None,
            'screenBounds':None,
            'origin':None,
            'realScale':None,
        }
    
    def loadXml(self, xml=None):
        '''Load values from the xml'''
        if xml is None:
            return
            
        for key in self._values.iterkeys():
            item = xml.find(key)
            if item is None:
                continue
            
            axis = {'x':0.0, 'y':0.0, 'z':0.0}
            for axisKey in axis.iterkeys():
                value = item.find(axisKey)
                if value is not None:
                    axis[axisKey] = float(value.text)
            self.set(key, Vect3d(**axis))

class Client(Header):
    def __init__(self, **args):
        #TODO: overwrite values with passed in args
        self._values = {
            'name':None,
            'version':None,
            'username':None,
            'permalink':None,
            'keywords':set(),
            'uniqueKey':None,
            'ip':None,
            'time':None,
            'location':None,
        }
    
    def loadXml(self, xml=None):
        '''Load values from the xml'''
        if xml is None:
            return
            
        for key in self._values.iterkeys():
            item = xml.find(key)
            if item is None:
                continue
            
            if key == 'keywords':
                value = set(item.text.split(','))
            elif key == 'location':
                lonLat = {'lon':0.0, 'lat':0.0}
                for lonLatKey in lonLat.iterkeys():
                    lonLatValue = item.find(lonLatKey)
                    if lonLatValue is not None:
                        lonLat[lonLatKey] = float(lonLatValue.text)
                value = Location(**lonLat)
            else:
                value = item.text
            
            self.set(key, value)
     
    def addKeyword(self, keyword):
        '''Add a keyword'''
        self.keywords.add(keyword)
            
    def setNowTime(self):
        '''Set the time to the current time'''
        self.time = time.time()
