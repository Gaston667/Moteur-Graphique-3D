from lib_math import Triangle2D, vec2
import moteur_graphique as mg


tri1 =  Triangle2D(
            vec2(-0.5, -0.5), 
            vec2(0, 0.5), 
            vec2(0.5, -0.5))


# Boucle de rendu principale
while True:
    mg.clear(' ')
    mg.putTriangle(tri1.to_Screen(mg.width, mg.height), '@')

    mg.draw()
