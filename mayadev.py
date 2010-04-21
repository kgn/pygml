from maya import OpenMaya, cmds
import PyGML
import reimport
for module in reimport.modified():
    print module
    reimport.reimport(module)

gmlFile = open('/Users/dkeegan/dev/mercurial/projects/pygml/SampleGML/134.gml', 'r')
gml = PyGML.GML(gmlFile)
gmlFile.close()

#gml = PyGML.GML()
#stroke = PyGML.Stroke()
#stroke.addPoint(0.0, 0.0, 0.0, 0.0)
#stroke.addPoint(0.0, 1.0, 0.0, 0.1)
#stroke.addPoint(0.0, 2.0, 0.0, 0.2)
#gml.addStroke(stroke)

for stroke in gml.iterStrokes():
    meshPoints = OpenMaya.MPointArray()
    meshPolyCounts = OpenMaya.MIntArray()
    meshPolyConnects = OpenMaya.MIntArray()
    
    indices, vertices = stroke.getPolyData(radius=0.04, sides=20, rotZ=False)
    for face in indices:
        meshPolyCounts.append(len(face))
        for index in face:
            meshPolyConnects.append(index)
    for vert in vertices:
        meshPoints.append(OpenMaya.MPoint(*vert.asArray()))
    
    meshFn = OpenMaya.MFnMesh()
    nullObj = OpenMaya.MObject()
    newTransform = meshFn.create(meshPoints.length(), meshPolyCounts.length(), meshPoints, meshPolyCounts, meshPolyConnects, nullObj)
    edgeIt = OpenMaya.MItMeshEdge(newTransform)
    while not edgeIt.isDone():
        edgeIt.setSmoothing(False)
        edgeIt.next()
    meshFn.cleanupEdgeSmoothing()
    meshFn.updateSurface()
    
    cmds.sets(meshFn.name(), edit=True, forceElement='initialShadingGroup')

#curve
#for stroke in gml.iterStrokes():
#    curveArray = []
#    for point in stroke.iterPoints(False):
#        curveArray.append((point.x, point.y, point.z*0.001))
#    cmds.curve(d=True, p=curveArray)