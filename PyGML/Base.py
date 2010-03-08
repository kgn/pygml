# Conforms to the standard outlined at http://fffff.at/gml/
# Some additional logic has been added due to differences in GML files

from xml.etree import ElementTree
from Header import *
from Drawing import *

__all__ = ['GML']

def _indent(elem, level=0):
    '''Pretty print the xml'''
    i = '\n' + level*'    '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '    '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class GML(object):
    def __init__(self, gml=None):
        self.__client = Client()
        self.__env = Environment()
        self.__strokes = []
        
        if gml:
            self.load(gml)
    
    def load(self, gml):
        '''Load the gml from a file stream'''
        tree = ElementTree.parse(gml)
        
        #load client
        clientXml = tree.find('tag/client')
        if clientXml is None:
            clientXml = tree.find('tag/header/client')
        self.__client._loadXml(clientXml)
        
        #load environment
        envXml = tree.find('tag/environment')
        if envXml is None:
            envXml = tree.find('tag/header/environment')
        self.__env._loadXml(envXml)
        
        #load strokes
        for stroke in tree.findall('tag/drawing/stroke'):
            currentStroke = Stroke()
            for point in stroke.findall('pt'):
                pointValues = {'x':0.0, 'y':0.0, 'z':None, 'time':None}
                for pointKey in pointValues.iterkeys():
                    pointValue = point.find(pointKey)
                    if pointValue is not None:
                        pointValues[pointKey] = float(pointValue.text)        
                currentStroke.addPoint(**pointValues)
            self.addStroke(currentStroke)
    
    def save(self, file):
        '''Save the GML to a file'''
        root = ElementTree.Element('GML')
        tag = ElementTree.SubElement(root, 'tag')
        
        storeClient = self.client()._shouldStore()
        storeEnvironment = self.environment()._shouldStore()
        
        if storeClient or storeEnvironment:
            header = ElementTree.SubElement(tag, 'header')
            if storeClient:
                self.client()._store(ElementTree.SubElement(header, 'client'))
            if storeEnvironment:
                self.environment()._store(ElementTree.SubElement(header, 'environment'))
                
        if self.__strokes:
            drawing = ElementTree.SubElement(tag, 'drawing')
            for strokeData in self.iterStrokes():
                stroke = ElementTree.SubElement(drawing, 'stroke')
                if strokeData.isDrawing() is False:
                    stroke.set('isDrawing', 'false')
                for pointData in strokeData.iterPoints():
                    point = ElementTree.SubElement(stroke, 'pt')
                    pointData._store(point)
        
        _indent(root)         
        ElementTree.ElementTree(root).write(file)
            
    def client(self):
        '''Access the client'''
        return self.__client
            
    def environment(self):
        '''Access the environment'''
        return self.__env
    
    def addStroke(self, stroke):
        '''Add a stroke, this must be a PyGML.Stroke object'''
        #TODO: type check incoming stroke
        self.__strokes.append(stroke)
    
    def iterStrokes(self):
        '''Iterate over all the strokes'''
        for stroke in self.__strokes:
            yield stroke
