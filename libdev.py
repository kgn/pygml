from PyGML import GML
import urllib
#this file is only for testing the library
if __name__ == '__main__':
    #gmlFile = urllib.urlopen('http://000000book.com/data/154.gml')
    gmlFile = open('SampleGML/140.gml', 'r')
    gml = GML(gmlFile)
    gmlFile.close()
    
    print gml.client()
    #print gml.client().get('name')
    print gml.environment()
    #print gml.environment().get('screenBounds').x
    for stroke in gml.iterStrokes():
        for point in stroke.iterPoints():
            print point