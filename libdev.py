import PyGML
import urllib

#this file is only for testing the library

def readFile():
    #gmlFile = urllib.urlopen('http://000000book.com/data/154.gml')
    gmlFile = open('SampleGML/147.gml', 'r')
    gml = PyGML.GML(gmlFile)
    gmlFile.close()
    return gml
            
def createGML():
    gml = PyGML.GML()
    gml.client().set('name', 'PyGML')
    gml.client().addKeyword('PyGML')
    gml.client().addKeywords('test', 'python')
    gml.client().setNowTime()
    gml.environment().set('screenBounds', PyGML.Vect2d(480, 320))
    
    stroke = PyGML.Stroke()
    #stroke.setIsDrawing(False)
    stroke.addPoint(0.0, 0.0)
    stroke.addPoint(0.0, 1.0)
    stroke.addPoint(1.0, 1.0)
    stroke.addPoint(1.0, 0.0)
    stroke.addPoint(0.0, 0.0)
    gml.addStroke(stroke)
    
    return gml
            
if __name__ == '__main__':
    #gml = readFile()
    gml = createGML()
    
    print gml.client()
    #print gml.client().get('name')
    print gml.environment()
    #print gml.environment().get('screenBounds').x
    for stroke in gml.iterStrokes():
        for point in stroke.iterPoints():
            print point
            
    gml.save('test.gml')
