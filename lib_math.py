##############################################################################
# SECTION DES VECTEURS 2D ET 3D
#############################################################################

from math import cos, sin, sqrt


class vec2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __mul__(self, scalar):
        """ multiplie le vecteur par un scalaire en multipliant chaque composante par ce scalaire"""
        return vec2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        """ divise le vecteur par un scalaire en divisant chaque composante par ce scalaire"""
        return vec2(self.x / scalar, self.y / scalar)
    
    def __add__(self, otherVec):
        """ additionne deux vecteurs en additionnant chaque composante correspondante"""
        return vec2(self.x + otherVec.x, self.y + otherVec.y)

    def __sub__(self, otherVec):
        return vec2(self.x - otherVec.x, self.y - otherVec.y)

    __rsub__ = __sub__ # pour permettre la soustraction dans les deux sens (vec2 - vec2 et vec2 - vec2)
        
    __radd__ = __add__ # pour permettre l'addition dans les deux sens (vec2 + vec2 et vec2 + vec2)
    __rmul__ = __mul__ # pour permettre la multiplication dans les deux sens (vec2 * scalar et scalar * vec2)

    def to_Screen(self, width, height):
        """ convertit les coordonnées du vecteur en coordonnées d'écran on passe de -1 et 1 à 0 à width et height"""
        
        return vec2(
            (29/13) # ratio de pixel du teminal  pour compenser l'étirement vertical des pixels et obtenir des triangles plus réguliers
            * height/width # compense letirement de la fenetre
            * (self.x + 1) * width / 2,
            (-self.y + 1) * height / 2
        )

    def __repr__(self):
        return f'vecteur2({self.x}, {self.y})'
  

class vec3:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, scalar):
        """ multiplie le vecteur par un scalaire en multipliant chaque composante par ce scalaire"""
        return vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        """ divise le vecteur par un scalaire en divisant chaque composante par ce scalaire"""
        return vec3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __add__(self, otherVec):
        """ additionne deux vecteurs en additionnant chaque composante correspondante"""
        return vec3(self.x + otherVec.x, self.y + otherVec.y, self.z + otherVec.z)
    
    def __sub__(self, otherVec):
        return vec3(self.x - otherVec.x, self.y - otherVec.y, self.z - otherVec.z)

    __rsub__ = __sub__ # pour permettre la soustraction dans les deux sens (vec3 - vec3 et vec3 - vec3)
    __radd__ = __add__ # pour permettre l'addition dans les deux sens (vec3 + vec3 et vec3 + vec3)
    __rmul__ = __mul__ # pour permettre la multiplication dans les deux sens (vec3 * scalar et scalar * vec3)

    def projection(self, focallLength) -> vec2:
        """ projette le vecteur 3D en 2D en utilisant une projection perspective simple, en divisant les coordonnées x et y par la coordonnée z pour simuler la perspective"""
        return focallLength * vec2(self.x, self.y) / self.z

    def rotationX(self, pitch):
        """ fait tourner le vecteur autour de l'axe X en utilisant les formules de rotation 3D pour les coordonnées y et z"""
        y1 = cos(pitch) * self.y - sin(pitch) * self.z
        z1 = sin(pitch) * self.y + cos(pitch) * self.z
        return vec3(self.x, y1, z1)
    
    def rotationY(self, yaw):
        """ fait tourner le vecteur autour de l'axe Y en utilisant les formules de rotation 3D pour les coordonnées x et z"""
        x1 = cos(yaw) * self.x + sin(yaw) * self.z
        z1 = -sin(yaw) * self.x + cos(yaw) * self.z
        return vec3(x1, self.y, z1)
    
    def rotationZ(self, roll):
        """ fait tourner le vecteur autour de l'axe Z en utilisant les formules de rotation 3D pour les coordonnées x et y"""
        x1 = cos(roll) * self.x - sin(roll) * self.y
        y1 = sin(roll) * self.x + cos(roll) * self.y
        return vec3(x1, y1, self.z)
    
    def normalize(self):
        norm = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        return vec3(self.x/norm, self.y/norm, self.z/norm)





#############################################################################
# SECTION DES TRIANGLES 2D ET 3D
#############################################################################
class Triangle2D:
    def __init__(self, v1, v2, v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def to_Screen(self, width, height):
        return Triangle2D(self.v1.to_Screen(width, height),
                        self.v2.to_Screen(width, height),
                        self.v3.to_Screen(width, height))



class Triangle3D:
    def __init__(self, v1, v2, v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def projection(self, focallLength=1) -> Triangle2D:
        """
        projette les trois sommets du triangle 3D en 2D en utilisant 
        la méthode de projection de chaque sommet et retourne un triangle 2D avec les coordonnées projetées
        """
        return Triangle2D(self.v1.projection(focallLength), self.v2.projection(focallLength), self.v3.projection(focallLength))
    
    def translate(self, vec: vec3):
        """ translate le triangle en ajoutant un vecteur de translation à chaque sommet du triangle"""
        return Triangle3D(self.v1 + vec, self.v2 + vec, self.v3 + vec)
    
    def rotateX(self, pitch):
        """ fait tourner le triangle autour de l'axe X en faisant tourner chaque sommet du triangle en utilisant la méthode de rotationX de vec3"""
        return Triangle3D(self.v1.rotationX(pitch), self.v2.rotationX(pitch), self.v3.rotationX(pitch))
    
    def rotateY(self, yaw):
        """ fait tourner le triangle autour de l'axe Y en faisant tourner chaque sommet du triangle en utilisant la méthode de rotationY de vec3"""
        return Triangle3D(self.v1.rotationY(yaw), self.v2.rotationY(yaw), self.v3.rotationY(yaw))
    
    def rotateZ(self, roll):
        """ fait tourner le triangle autour de l'axe Z en faisant tourner chaque sommet du triangle en utilisant la méthode de rotationZ de vec3"""
        return Triangle3D(self.v1.rotationZ(roll), self.v2.rotationZ(roll), self.v3.rotationZ(roll))
    
