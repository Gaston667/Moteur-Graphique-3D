class vec2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

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
  
class Triangle2D:
    def __init__(self, v1, v2, v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def to_Screen(self, width, height):
        return Triangle2D(self.v1.to_Screen(width, height),
                        self.v2.to_Screen(width, height),
                        self.v3.to_Screen(width, height))

    def __repr__(self):
        return f'Triangle2D({self.v1}, {self.v2}, {self.v3})'



class vec3:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def to_Screen(self, width, height):
        """ convertit les coordonnées du vecteur en coordonnées d'écran on passe de -1 et 1 à 0 à width et height"""
        
        return vec2(
            (29/13) # ratio de pixel du teminal  pour compenser l'étirement vertical des pixels et obtenir des triangles plus réguliers
            * height/width # compense letirement de la fenetre
            * (self.x + 1) * width / 2,
            (-self.y + 1) * height / 2
        )

    def __repr__(self):
        return f'vec3({self.x}, {self.y}, {self.z})'
      