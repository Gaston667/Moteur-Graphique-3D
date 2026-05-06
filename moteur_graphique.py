from math import cos, sin
from lib_math import Triangle2D, Triangle3D, vec2, vec3

import os


width, height = os.get_terminal_size() 
height -= 1 # pour éviter la derniere soit vide (utilisé pour les commandes)
pixelBuffer = [' ']*(width*height) # contient les pixels à afficher

class Camera:
    def __init__(self, position, pitch, yaw, roll, focallLength) -> None:
        self.position = position
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.focallLength = focallLength

    def getLookATDirection(self):
        return vec3(-sin(self.yaw) * cos(self.pitch),
                    sin(self.pitch),
                    cos(self.yaw)* cos(self.pitch))

    def getForwardDirection(self):
        return vec3(-sin(self.yaw), 0, cos(self.yaw))
    
    def getRightDirection(self):
        return vec3(cos(self.yaw), 0, sin(self.yaw))


#################################################################################

class LigthSource:

    def __init__(self, position: vec3) -> None:
        self.position:vec3 = position


#################################################################################

def draw():
    """ affiche le contenu du buffer à l'écran en utilisant la fonction print()"""
    print(''.join(pixelBuffer), end='') # affiche le buffer

def clear(char):
    """ remplit le buffer avec le caractère char pour le nettoyer avant de dessiner à nouveau"""
    for i in range(width*height):
        pixelBuffer[i] = char

def putPixel(vecteur, char):
    """ place un pixel à la position (x, y) dans le buffer en utilisant le caractère char"""
    px = round(vecteur.x)
    py = round(vecteur.y)
    if 0 <= px < width and 0 <= py < height:
        # on utilise une liste a une dimension pour le buffer, donc on calcule l'index à partir de x et y en appliquant la formule : index = y * width + x
        pixelBuffer[py*width + px] = char 

def putTriangle(triangle, char):
    """ dessine un triangle dans le buffer en utilisant la fonction putPixel() pour chaque sommet du triangle"""
    def eq(p, a, b):
        """ calcule l'équation de la droite passant par les points a et b, et vérifie si le point p est au dessus ou en dessous de cette droite"""
        return (a.x - p.x) * (b.y - p.y) - (a.y - p.y) * (b.x - p.x)

    xmin = round(min(triangle.v1.x, triangle.v2.x, triangle.v3.x))
    xmax = round(max(triangle.v1.x, triangle.v2.x, triangle.v3.x)) + 1
    ymin = round(min(triangle.v1.y, triangle.v2.y, triangle.v3.y))
    ymax = round(max(triangle.v1.y, triangle.v2.y, triangle.v3.y)) + 1
    for y in range(ymin, ymax):
        if 0 <= y < height:
            for x in range(xmin, xmax):
                if 0 <= x < width:
                    pos = vec2(x, y) 
                    w1 = eq(pos, triangle.v2, triangle.v3)
                    w2 = eq(pos, triangle.v3, triangle.v1)
                    w3 = eq(pos, triangle.v1, triangle.v2)
                    # si les tois poids sont positifs ou nuls, cela signifie que le point est à l'intérieur du triangle ou sur son bord, donc on peut dessiner le pixel
                    if (w1 >= 0 and w2 >= 0 and w3 >= 0) or (-w1 >= 0 and -w2 >= 0 and -w3 >= 0):
                        putPixel(pos, char)


# sert a faire le clipping 
def clip(triangles: list[Triangle3D], camPos: vec3, planNormale: vec3):
    """"""
    def inZ(planNormal, planePoint, triangle):
        out = []
        in_ = []

        vect1 = dot(planePoint - triangle.v1, planNormal)
        vect2 = dot(planePoint - triangle.v2, planNormal)
        vect3 = dot(planePoint - triangle.v3, planNormal)

        out.append(triangle.v1) if vect1 > 0 else in_.append(triangle.v1)
        out.append(triangle.v2) if vect2 > 0 else in_.append(triangle.v2)
        out.append(triangle.v3) if vect3 > 0 else in_.append(triangle.v3) 
        
        # pour eviter que le triangle ne se recreer dans le mauvais sens apres le clipping 
        # car sinon certain triangle peuve apparaitre a des moments non voulue par exemple quand on entre dans un carre un des triangles est sensé disparatire a cause du face culling mais il reaparaitra au mauvais moment 
        isInverted = vect1 * vect2 > 0
        return out, in_, isInverted

    nearDist = 0.1
    # on calcule la distance entre la camera et le plan de clipping en projetant le vecteur de la camera vers un point du plan sur la normale du plan, en faisonsans camPos + nearDist * planNormale, on obtient la position du plan de clipping dans l'espace 3D, et en calculant la distance entre cette position et la camera, on obtient la distance de clipping qui nous permettra de déterminer quels triangles sont devant ou derrière le plan de clipping
    nearPoint = camPos + nearDist * planNormale
    out, in_, isInverted =  inZ(planNormale, nearPoint, triangles)

    if len(out) == 0:
        return [triangles]
    elif len(out) == 3:
        return []
    elif len(out) == 1:
        colision0 = LinePlaneIntersection(planNormale, nearPoint, out[0], in_[0])
        colision1 = LinePlaneIntersection(planNormale, nearPoint, out[0], in_[1])
        if isInverted:
            return[
                Triangle3D(colision1, in_[1], colision0),
                Triangle3D(colision0, in_[1], in_[0])
            ]
        else:    
            return[
                Triangle3D(colision0, in_[0], colision1),
                Triangle3D(colision1, in_[0], in_[1])
            ]
    
    elif len(out) == 2:
        if isInverted:
            return[
                Triangle3D(LinePlaneIntersection(planNormale, nearPoint, out[0], in_[0]),
                        in_[0],
                        LinePlaneIntersection(planNormale, nearPoint, out[1], in_[0])                        
                )
            ]
        else:   
            return[
                Triangle3D(LinePlaneIntersection(planNormale, nearPoint, out[0], in_[0]), 
                        LinePlaneIntersection(planNormale, nearPoint, out[1], in_[0]),
                        in_[0]
                )
            ]

# sert a  connaitre le point dintersection entre le plan near et les triangle 
def LinePlaneIntersection(planeNormal, planePoint, v1, v2):
    u = v2 - v1
    dotp = dot(planeNormal, u)
    if abs(dotp) < 1e-6:
        return (0, 0, 0)
    w = (v1 - planePoint)
    si = -dot(planeNormal, w) / dotp
    u = si * u
    return (v1 + u)
  

def dot(v1: vec3, v2: vec3):
    """ calcule le produit scalaire de deux vecteurs 3D en multipliant les composantes correspondantes et en les additionnant"""
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

# utile dans le face culling pour faire le calcule vectoriel qui sert a determiner la normale de la face 
def crossProd(v1: vec3, v2:vec3):
    #produit vectoriel
    return vec3(v1.y * v2.z - v1.z * v2.y,
                v1.z * v2.x - v1.x * v2.z,
                v1.x * v2.y - v1.y * v2.x)


lightGradient  = ".,;la#@"

def diffuseLight(lightSoure:LigthSource, surfaceNomal:vec3, pointTriangle:vec3):
    lightDir = lightSoure.position - pointTriangle
    intensity = dot(lightDir.normalize(), surfaceNomal.normalize()) # entre -1 et 1 
    return lightGradient[round(intensity*(len(lightGradient)-1))] if intensity >= 0 else lightGradient[0]


def loadObject(filePath) -> list[Triangle3D]:
    with open(filePath, "r") as file:
        lines = [line.rstrip('\n').split(' ') for line in file.readlines() if line.rstrip('\n')]
        # sommet et face
        vertices = []
        faces= []
        for line in lines:
            if line[0] == 'v':
                vertex = list(map(float, line[1:]))
                vertices.append(vec3(vertex[0], vertex[1], vertex[2]))
            if line[0] == 'f':
                faces.append(list(map(int, line[1:])))
      
        # Creon les triangle a present 
        triangles = []
        for face in faces:
            if len(face) == 3:
               triangles.append(Triangle3D(vertices[face[0]-1], vertices[face[1]-1], vertices[face[2]-1]))
            if len(face) == 4:
               triangles.append(Triangle3D(vertices[face[0]-1], vertices[face[1]-1], vertices[face[2]-1]))
               triangles.append(Triangle3D(vertices[face[2]-1], vertices[face[3]-1], vertices[face[0]-1]))
        return triangles




def putMesh(mesh: list[Triangle3D], cam: Camera, ligthSource:LigthSource):
    """ Dessine un maillage (une liste de triangles) dans le buffer en utilisant la fonction putTriangle() pour chaque triangle du maillage"""
    lookAt = cam.getLookATDirection()
    for triangle in mesh:
        # Decoupage de triangle qui ne sont pas la zone visible
        clippedTrianglesList = clip(triangle, cam.position, lookAt)

        for clippedTriangle in clippedTrianglesList:
            # cette partie corene le cliping des face 
            line1 = clippedTriangle.v2 - clippedTriangle.v1
            line2 = clippedTriangle.v3 - clippedTriangle.v1
            surfaceNormal = crossProd(line1, line2) 
            if dot(surfaceNormal, clippedTriangle.v1 - cam.position) < 0:
                lightStr:str = diffuseLight(ligthSource, surfaceNormal, clippedTriangle.v1)
                putTriangle(clippedTriangle
                    .translate(-1*cam.position)
                    .rotateY(cam.yaw)
                    .rotateX(cam.pitch)
                    .rotateZ(cam.roll)
                    .projection(cam.focallLength)
                    .to_Screen(width, height),lightStr)
         


