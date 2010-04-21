import sys, os
import PyGML

def GmlToObj(gml, output):
    output.write('#PyGML: GML >> OBJ\n\n')
    for stroke in gml.iterStrokes():
        indices, vertices = stroke.getPolyData(radius=0.04, sides=8, rotZ=False)
        for vert in vertices:
            output.write('v %s\n' % ' '.join(map(str, vert.asArray())))
        for face in indices:
            faceString = []
            for index in face:
                #obj indices go from 1 to n
                faceString.append(str(index+1))
            output.write('f %s\n' % ' '.join(faceString))
            
if __name__ == '__main__':
    gmlFile = sys.argv[1]
    inputFile = open(gmlFile, 'r')
    objFile = os.path.splitext(gmlFile)[0]+'.obj'
    outputFile = open(objFile, 'w')
    gml = PyGML.GML(inputFile)
    GmlToObj(gml, outputFile)
    inputFile.close()
    outputFile.close()