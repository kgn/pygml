import time
from Math import *
from Data import *

class Environment(Data):
    def __init__(self, **args):
        self._keys = (
            'offset',
            'rotation',
            'up',
            'screenBounds',
            'origin',
            'realScale',
        )
        Data.__init__(self, **args)
    
    def _load(self, xml=None):
        '''Load values from the xml'''
        if xml is None:
            return
            
        for key in self.iterKeys():
            item = xml.find(key)
            if item is None:
                continue
            
            axis = {'x':0.0, 'y':0.0, 'z':0.0}
            for axisKey in axis.iterkeys():
                value = item.find(axisKey)
                if value is not None:
                    axis[axisKey] = float(value.text)
            self.set(key, Vect3d(**axis))

class Client(Data):
    def __init__(self, **args):
        self._keys = (
            'name',
            'version',
            'username',
            'permalink',
            'keywords',
            'uniqueKey',
            'ip',
            'time',
            'location',
        )
        Data.__init__(self, **args)
    
    def _load(self, xml=None):
        '''Load values from the xml'''
        if xml is None:
            return
            
        for key in self.iterKeys():
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
        if self.get('keywords') is None:
            self.set('keywords', set())
        self.get('keywords').add(keyword)
         
    def addKeywords(self, *keywords):
        '''Add a list of keywords'''
        for keyword in keywords:
            self.addKeyword(keyword)
            
    def setNowTime(self):
        '''Set the time to the current time'''
        self.set('time', time.time())
