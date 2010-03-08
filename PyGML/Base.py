# Conforms to the standard outlined at http://fffff.at/gml/

from xml.etree import ElementTree
from Header import *
from Drawing import *

class GML(object):
    def __init__(self, gml=None):
        self.__client = None
        self.__env = None
        self.__strokes = []
        
        if gml:
            self.load(gml)
    
    def load(self, gml):
        tree = ElementTree.parse(gml)
        
        #load client
        self.__client = Client()
        clientXml = tree.find('tag/client')
        if clientXml is None:
            clientXml = tree.find('tag/header/client')
        self.__client.loadXml(clientXml)
        
        #load environment
        self.__env = Environment()
        envXml = tree.find('tag/environment')
        if envXml is None:
            envXml = tree.find('tag/header/environment')
        self.__env.loadXml(envXml)
        
        #load strokes
        for stroke in tree.findall('tag/drawing/stroke'):
            currentStroke = Stroke()
            for point in stroke.findall('pt'):
                pointValues = {'x':0.0, 'y':0.0, 'z':0.0, 'time':0.0}
                for pointKey in pointValues.iterkeys():
                    pointValue = point.find(pointKey)
                    if pointValue is not None:
                        pointValues[pointKey] = float(pointValue.text)        
                currentStroke.addPoint(**pointValues)
            self.__strokes.append(currentStroke)
    
    def save(self):
        pass
            
    def client(self):
        return self.__client
            
    def environment(self):
        return self.__env
        
    def iterStrokes(self):
        for stroke in self.__strokes:
            yield stroke
