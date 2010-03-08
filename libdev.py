import PyGML
import urllib
#this file is only for testing the library
if __name__ == '__main__':
    gmlFile = urllib.urlopen('http://000000book.com/data/154.gml')
    #gmlFile = open('155.gml', 'r')
    gml = PyGML.GML(gmlFile)
    gmlFile.close()
    
    print gml.client()
    print gml.environment()
    for stroke in gml.iterStrokes():
        for point in stroke.iterPoints():
            print point