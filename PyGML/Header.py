import time
from xml.etree import ElementTree
from Math import *

__all__ = ['Client', 'Environment']

class _Header(object):
    def iterKeys(self):
        '''Iterate the keys'''
        for key in self._values.iterkeys():
            yield key
       
    def get(self, key):
        '''Get a value by it's key'''
        return self._values.get(key, None)
        
    def set(self, key, value):
        '''Set a value by it's key'''
        if key in self._values:
            self._values[key] = value
    
    def _shouldStore(self):
        '''Determin if there is anything to store'''
        for value in self._values.itervalues():
            if value:
                return True
        return False
     
    def _store(self, xml):
        '''Store the data in the input parent xml node'''
        for key, value in self._values.iteritems():
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
        for key, value in self._values.iteritems():
            if value:
                ppDict[key] = str(value)
        return '<%s(%s)>' % (self.__class__.__name__, ppDict)

class Environment(_Header):
    def __init__(self, **args):
        self._values = {
            'offset':args.get('name', None),
            'rotation':args.get('rotation', None),
            'up':args.get('up', None),
            'screenBounds':args.get('screenBounds', None),
            'origin':args.get('origin', None),
            'realScale':args.get('realScale', None),
        }
    
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
        self._values = {
            'name':args.get('name', None),
            'version':args.get('version', None),
            'username':args.get('username', None),
            'permalink':args.get('permalink', None),
            'keywords':args.get('keywords', None),
            'uniqueKey':args.get('uniqueKey', None),
            'ip':args.get('ip', None),
            'time':args.get('time', None),
            'location':args.get('location', None),
        }
    
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
        if self._values['keywords'] is None:
            self._values['keywords'] = set()
        self._values['keywords'].add(keyword)
         
    def addKeywords(self, *keywords):
        '''Add a list of keywords'''
        for keyword in keywords:
            self.addKeyword(keyword)
            
    def setNowTime(self):
        '''Set the time to the current time'''
        self._values['time'] = time.time()
