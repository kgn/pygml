from xml.etree import ElementTree

class MathBase(object):
    def _store(self, xml):
        for key, value in self._data():
            if value is None:
                continue
            entry = ElementTree.SubElement(xml, key)
            entry.text = str(value)

class Location(MathBase):
    def __init__(self, lon=0.0, lat=0.0):
        self.lon = lon
        self.lat = lat
     
    def _data(self):
        return (
            ('lon',self.lon),
            ('lat',self.lat),
        )
     
    def __str__(self):
        return '<%s(%.2f, %.2f)>' % (self.__class__.__name__, self.lon, self.lat)

class Vect2d(MathBase):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
     
    def _data(self):
        return (
            ('x',self.x),
            ('y',self.y),
        )
     
    def __str__(self):
        return '<%s(%.2f, %.2f)>' % (self.__class__.__name__, self.x, self.y)
        
class Vect3d(MathBase):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def _data(self):
        return (
            ('x',self.x),
            ('y',self.y),
            ('z',self.z),
        )
     
    def __str__(self):
        return '<%s(%.2f, %.2f, %.2f)>' % (self.__class__.__name__, self.x, self.y, self.z)

class Color(MathBase):
    '''0 to 255 color space'''
    def __init__(self, r=0, g=0, b=0, a=None):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        
    def _data(self):
        data = [
            ('r',self.r),
            ('g',self.g),
            ('b',self.b),
        ]
        if self.a:
            data.append(('a',self.a))
        return data
        
    def __str__(self):
        values = [self.r, self.g, self.b]
        if self.a:
            values.append(self.a)
        returnStr = '<%s(' % self.__class__.__name__
        for value in values:
            returnStr += '%d, ' % value
        return returnStr.rstrip(', ')+')>'

class Point(MathBase):
    #TODO: time can also be represented by the tag <t>
    def __init__(self, x=0.0, y=0.0, z=None, time=None):
        self.x = x
        self.y = y
        self.z = z
        self.time = time
        
    def _data(self):
        data = [
            ('x',self.x),
            ('y',self.y),
        ]
        if self.z:
            data.append(('z',self.z))
        if self.time:
            data.append(('time',self.time))
        return data
        
    def __str__(self):
        values = [self.x, self.y]
        if self.z:
            values.append(self.z)
        if self.time:
            values.append(self.time)
        returnStr = '<%s(' % self.__class__.__name__
        for value in values:
            returnStr += '%.2f, ' % value
        return returnStr.rstrip(', ')+')>'

#functions
def CrossProduct(U, V):
    '''Get the cross product of two vectors'''
    return Vect3d(U.y*V.z - U.z*V.y, U.z*V.x - U.x*V.z, U.x*V.y - U.y*V.x)

def Magnitude(vect):
    '''Get the magnitude/length of a vector'''
    return math.sqrt(vect.x**2+vect.y**2+vect.z**2)

def Normalize(vect):
    '''Normalize and vector'''
    mag = Magnitude(vect)
    return  Vect3d(vect.x/mag, vect.y/mag, vect.z/mag)

def TransformPoint(vect, matrix):
    '''Transform a vector by a matrix'''
    transPoint = Vect3d()
    transPoint.x = vect.x * matrix[0][0] + vect.y * matrix[1][0] + vect.z * matrix[2][0] + 1 * matrix[3][0]
    transPoint.y = vect.x * matrix[0][1] + vect.y * matrix[1][1] + vect.z * matrix[2][1] + 1 * matrix[3][1]
    transPoint.z = vect.x * matrix[0][2] + vect.y * matrix[1][2] + vect.z * matrix[2][2] + 1 * matrix[3][2]
    return transPoint

def MultiplyMatrix(matrix1, matrix2):
    '''
    Multiply two matrices
    Based on http://code.google.com/p/gameobjects
    '''
    m1_0,  m1_1,  m1_2,  m1_3 = matrix1[0]
    m1_4,  m1_5,  m1_6,  m1_7 = matrix1[1]
    m1_8,  m1_9,  m1_10, m1_11 = matrix1[2]
    m1_12, m1_13, m1_14, m1_15 = matrix1[3]
        
    m2_0,  m2_1,  m2_2,  m2_3 = matrix2[0]
    m2_4,  m2_5,  m2_6,  m2_7 = matrix2[1]
    m2_8,  m2_9,  m2_10, m2_11 = matrix2[2]
    m2_12, m2_13, m2_14, m2_15 = matrix2[3]
                
    return ((m2_0 * m1_0 + m2_1 * m1_4 + m2_2 * m1_8 + m2_3 * m1_12,
        m2_0 * m1_1 + m2_1 * m1_5 + m2_2 * m1_9 + m2_3 * m1_13,
        m2_0 * m1_2 + m2_1 * m1_6 + m2_2 * m1_10 + m2_3 * m1_14,
        m2_0 * m1_3 + m2_1 * m1_7 + m2_2 * m1_11 + m2_3 * m1_15,),
           
        (m2_4 * m1_0 + m2_5 * m1_4 + m2_6 * m1_8 + m2_7 * m1_12,
        m2_4 * m1_1 + m2_5 * m1_5 + m2_6 * m1_9 + m2_7 * m1_13,
        m2_4 * m1_2 + m2_5 * m1_6 + m2_6 * m1_10 + m2_7 * m1_14,
        m2_4 * m1_3 + m2_5 * m1_7 + m2_6 * m1_11 + m2_7 * m1_15,),
           
        (m2_8 * m1_0 + m2_9 * m1_4 + m2_10 * m1_8 + m2_11 * m1_12,
        m2_8 * m1_1 + m2_9 * m1_5 + m2_10 * m1_9 + m2_11 * m1_13,
        m2_8 * m1_2 + m2_9 * m1_6 + m2_10 * m1_10 + m2_11 * m1_14,
        m2_8 * m1_3 + m2_9 * m1_7 + m2_10 * m1_11 + m2_11 * m1_15,),
           
        (m2_12 * m1_0 + m2_13 * m1_4 + m2_14 * m1_8 + m2_15 * m1_12,
        m2_12 * m1_1 + m2_13 * m1_5 + m2_14 * m1_9 + m2_15 * m1_13,
        m2_12 * m1_2 + m2_13 * m1_6 + m2_14 * m1_10 + m2_15 * m1_14,
        m2_12 * m1_3 + m2_13 * m1_7 + m2_14 * m1_11 + m2_15 * m1_15,),
    )

_deg2rad = (math.pi/180)
_yRotMatrix = (
    (0.0, 0.0, -1.0, 0.0), 
    (0.0, 1.0, 0.0, 0.0), 
    (1.0, 0.0, 0.0, 0.0), 
    (0.0, 0.0, 0.0, 1.0),
)
def VertRing(radius, sides, matrix):
    '''Get a ring of points transformed into the matrix space'''
    faces = []
    sideRad = _deg2rad*(360/sides)
    rotMatrix = MultiplyMatrix(matrix, _yRotMatrix)
    for i in range(sides):
        degInRad = i*sideRad
        origPoint = Vect3d()
        origPoint.x = radius*math.cos(degInRad)
        origPoint.y = radius*math.sin(degInRad)
        
        transPoint = TransformPoint(origPoint, rotMatrix)
            
        faces.append((transPoint.x, transPoint.y, transPoint.z))
        
    return faces
