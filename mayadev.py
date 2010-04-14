import maya
import PyGML

gmlFile = open('SampleGML/159.gml', 'r')
gml = PyGML.GML(gmlFile)
gmlFile.close()

def iterTube(stroke, radius=0.01, sides=6, zScale=0.001):
    pointList = tuple(stroke.iterPoints())
    
    previousPoint = None
    for point in pointList:
        if not previousPoint:
            previousPoint = point
            continue
            
        timeDelta = point.time-previousPoint.time
        newRadius = radius-timeDelta            
            
        dirction = PyGML.Vect3d(point.x-previousPoint.x, point.y-previousPoint.y, 0)
        offZ = PyGML.Vect3d(previousPoint.x, previousPoint.y, 1)
        cross = CrossProduct(offZ, dirction)
        
        normPoint = Normalize(PyGML.Vect3d(point.x, point.y, point.z*zScale))
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

for stroke in gml.iterStrokes():
    for verts in iterTube(stroke):
        maya.cmds.polyCreateFacet(p=verts)
        
for stroke in gml.iterStrokes():
    curveArray = []
    for point in stroke.iterPoints():
        curveArray.append((point.x, point.y, point.z*0.001))
    maya.cmds.curve(d=True, p=curveArray)