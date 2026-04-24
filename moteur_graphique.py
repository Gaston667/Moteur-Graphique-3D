from lib_math import Triangle2D, vec2
import os


width, height = os.get_terminal_size() 
height -= 1 # pour éviter la derniere soit vide (utilisé pour les commandes)
pixelBuffer = [' ']*(width*height) # contient les pixels à afficher

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


