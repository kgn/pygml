from Math import *
from Data import *

class Brush(Data):
    #TODO: implement brush
    def __init__(self, **args):
        self._keys = (
            'mode',
            'uniqueStyleID',
            'spec',
            'width',
            'speedToWidthRatio',
            'dripAmnt',
            'dripSpeed',
            'layerAbsolute',
            'color',
            'dripVecRelativeToUp',
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
            
            if key == 'color':
                colorData = {'r':0, 'g':0, 'b':0, 'a':None}
                for colorKey in colorData.iterkeys():
                    colorValue = item.find(colorKey)
                    if colorValue is not None:
                        colorData[colorKey] = float(colorValue.text)
                value = Color(**colorData)
            if key == 'dripVecRelativeToUp':
                dripData = {'x':0.0, 'y':0.0, 'z':0.0}
                for dripKey in dripData.iterkeys():
                    dripValue = item.find(dripKey)
                    if dripValue is not None:
                        dripData[dripKey] = float(dripValue.text)
                value = Vect3d(**dripData)
            else:
                value = item.text
            
            self.set(key, value)

class Info(Data):
    def __init__(self, **args):
        self._keys = (
            'curved',
        )
        Data.__init__(self, **args)
    
class Stroke(object):
    def __init__(self):
        self.__info = Info()
        self.__brush = Brush()
        self.__points = []
        self.__isDrawing = True
   
    def _load(self, xml=None):
        '''Load the stroke from the xml'''
        if xml is None:
            return
            
        for point in xml.findall('pt'):
            pointValues = {'x':0.0, 'y':0.0, 'z':None, 'time':None}
            for pointKey in pointValues.iterkeys():
                pointValue = point.find(pointKey)
                if pointValue is not None:
                    pointValues[pointKey] = float(pointValue.text)        
            self .addPoint(**pointValues)
   
    def _shouldStore(self):
        '''Determin if there is anything to store'''
        if self.info()._shouldStore():
            return True
            
        if self.brush()._shouldStore():
            return True
            
        if self.__points:
            return True
            
        return False
     
    def _store(self, xml):
        stroke = ElementTree.SubElement(xml, 'stroke')
        if self.isDrawing() is False:
            stroke.set('isDrawing', 'false')
            
        if self.info()._shouldStore():
            self.info()._store(ElementTree.SubElement(stroke, 'info'))
            
        if self.brush()._shouldStore():
            self.brush()._store(ElementTree.SubElement(stroke, 'brush'))
            
        for pointData in self.iterPoints():
            point = ElementTree.SubElement(stroke, 'pt')
            pointData._store(point)
   
    def info(self):
        '''Access the info for the stroke'''
        return self.__info
    
    def setInfo(self, info=None):
        '''Set the info for the stroke'''
        self.__info = info
        
    def brush(self):
        '''Access the brush for the stroke'''
        return self.__brush
    
    def setBrush(self, brush=None):
        '''Set the brush for the stroke'''
        self.__brush = brush
    
    def isDrawing(self):
        '''Get the value of isDrawing'''
        return self.__isDrawing
        
    def setIsDrawing(self, value=True):
        '''Set the value for isDrawing'''
        self.__isDrawing = (value is True)
    
    def addPoint(self, x=0.0, y=0.0, z=None, time=None):
        '''Add a point to the stroke'''
        self.__points.append(Point(x, y, z, time))
        
    def iterPoints(self, rotZ=True):
        '''Iterate over the points in the stroke'''
        for point in self.__points:
            if rotZ:
                newVect = ZupToYup(point)
                yield Point(newVect.x, newVect.y, newVect.x, point.time)
            else:
                yield point
            
    def iterRings(self, radius=0.01, sides=6, zScale=0.001, rotZ=True):    
        previousPoint = None
        for point in self.iterPoints(rotZ):
            if not previousPoint:
                previousPoint = point
                continue
               
            #TODO: vary the width based on the draw speed 
            timeDelta = point.time-previousPoint.time
            newRadius = radius-timeDelta
            newRadius = radius         
                
            #TODO: zScale does not work with rotating from z to y up
            dirction = Vect3d(point.x-previousPoint.x, point.y-previousPoint.y, 0)
            offZ = Vect3d(previousPoint.x, previousPoint.y, 1)
            cross = CrossProduct(offZ, dirction)
            
            normPoint = Normalize(Vect3d(point.x, point.y, point.z*zScale))
            normOffZ = Normalize(offZ)
            normCross = Normalize(cross)
            
            matrix = (
                (normPoint.x, normPoint.y, normPoint.z, 0),
                (normCross.x, normCross.y, normCross.z, 0),
                (normOffZ.x, normOffZ.y, normOffZ.z, 0),
                (previousPoint.x, previousPoint.y, previousPoint.z*zScale, 1),
            )
            
            previousPoint = point
            
            yield VertRing(newRadius, sides, matrix)
            
    def iterPolys(self, radius=0.01, sides=6, zScale=0.001, rotZ=True):         
        previousRing = None
        for ring in self.iterRings(radius, sides, zScale, rotZ):
            if not previousRing:
                previousRing = ring
                continue
            
            for poly in IterPolysInRing(previousRing, ring):
                yield poly
                
            previousRing = ring
                
            
