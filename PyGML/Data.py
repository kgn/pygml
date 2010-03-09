from xml.etree import ElementTree
from Math import MathBase

class Data(object):
    def __init__(self, **args):
        self._values = {}
        for key, value in args.iteritems():
            self.set(key, value)
    
    def _load(self, xml=None):
        '''Load values from the xml'''
        if xml is None:
            return
            
        for key in self.iterKeys():
            item = xml.find(key)
            if item is None:
                continue
            
            self.set(key, item.text)
       
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
            if self.get(key) is not None:
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
            elif isinstance(value, bool):
                entry.text = str(value).lower()
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