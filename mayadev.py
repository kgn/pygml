import maya
import PyGML

gmlFile = open('SampleGML/160.gml', 'r')
gml = PyGML.GML(gmlFile)
gmlFile.close()

#polys
for stroke in gml.iterStrokes():
    for poly in stroke.iterPolys(radius=0.02, rotZ=False):
        maya.cmds.polyCreateFacet(p=poly.vertsArray())
        
#curve
for stroke in gml.iterStrokes():
    curveArray = []
    for point in stroke.iterPoints(False):
        curveArray.append((point.x, point.y, point.z*0.001))
    maya.cmds.curve(d=True, p=curveArray)
