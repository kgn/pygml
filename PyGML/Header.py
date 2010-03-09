import time
from xml.etree import ElementTree
from Math import *

__all__ = ['Client', 'Environment']

class _Header(object):
    def __init__(self, **args):
        self._values = {}
        for key, value in args.iteritems():
            self.set(key, value)
        
    def iterKeys(self):
        '''Iterate the keys'''
        for key in self._keys:
            yield key
       
    def get(self, key):
        '''Get a value by it's key'''
        return self._values.get(key, None)
        
    def set(self, key, value):
        '''Set a value by it's key'''
        if key in self._keys:
            self._values[key] = value
    
    def _shouldStore(self):
        '''Determin if there is anything to store'''
        for key in self.iterKeys():
            if self.get(key):
                return True
        return False
     
    def _store(self, xml):
        '''Store the data in the input parent xml node'''
        for key in self.iterKeys():
            value = self.get(key)
            if value is None:
                continue
            entry = ElementTree.SubElement(xml, key)
            if isinstance(value, MathBase):
                value._store(entry)
            elif hasattr(value, '__iter__'):
                entry.text = ','.join(value)
            else:
                entry.text = str(value)
    
    def __str__(self):
        #build a dictionary of items who are not None
        ppDict = {}
        for key in self.iterKeys():
            value = self.get(key)
            if value:
                ppDict[key] = str(value)
        return '<%s(%s)>' % (self.__class__.__name__, ppDict)

class Environment(_Header):
    def __init__(self, **args):
        self._keys = (
            'offset',
            'rotation',
            'up',
            'screenBounds',
            'origin',
            'realScale',
        )
        _Header.__init__(self, **args)
    
    def _loadXml(self, xml=None):
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

class Client(_Header):
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
        _Header.__init__(self, **args)
    
    def _loadXml(self, xml=None):
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
