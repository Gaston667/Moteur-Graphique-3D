from lib_math import Triangle3D, Triangle2D, vec3, vec2
import moteur_graphique as mg
import keyboard, time  

KEY_BINDINGS = {
    "ROLL_LEFT": 16,   # Q physique
    "ROLL_RIGHT": 18,  # E physique
    "LEFT": 30,        # A physique
    "RIGHT": 32,       # D physique
    "FORWARD": 17,     # W physique
    "BACKWARD": 31,    # S physique
    "UP": "space",
    "DOWN": "left shift",
}
def is_pressed(action):
    return keyboard.is_pressed(KEY_BINDINGS[action])

cam = mg.Camera(position=vec3(0, 0, 0), pitch=0, yaw=0, roll=0, focallLength=1)
light = mg.LigthSource(vec3(3,5,-1))

carre = [
    Triangle3D(vec3(-0.5, -0.5, 1), 
               vec3(-0.5, 0.5, 1), 
               vec3(0.5, 0.5, 1)
                ),
    Triangle3D(vec3(-0.5, -0.5, 1), 
               vec3(0.5, 0.5, 1), 
               vec3(0.5, -0.5, 1)
               )
]

def inpus():
    # Rotation de la camera avec les fleches
    if keyboard.is_pressed("down arrow"):
        if cam.pitch > -1.57:
            cam.pitch -= 0.01 * dt
    if keyboard.is_pressed("up arrow"):
        if cam.pitch < 1.57:
            cam.pitch += 0.01 * dt
    if keyboard.is_pressed("left arrow"):
        cam.yaw += 0.01 * dt
    if keyboard.is_pressed("right arrow"):
        cam.yaw -= 0.01 * dt

    # Roll avec A et E 
    if is_pressed("ROLL_LEFT"):
        cam.roll += 0.01 * dt
    if is_pressed("ROLL_RIGHT"):
        cam.roll -= 0.01 * dt

    # Deplacement avec Z, Q, S, D 
    if is_pressed("FORWARD"):
        cam.position += cam.getForwardDirection() * 0.01 * dt
    if is_pressed("BACKWARD"):
        cam.position += -1 * cam.getForwardDirection() * 0.01 * dt
    if is_pressed("RIGHT"):
        cam.position += cam.getRightDirection() * 0.01 * dt
    if is_pressed("LEFT"):
        cam.position += -1 * cam.getRightDirection() * 0.01 * dt

    # Monter et descendre avec espace et shift
    if is_pressed("UP"):
        cam.position.y += 0.01 * dt
    if is_pressed("DOWN"):
        cam.position.y -= 0.01 * dt



objet = mg.loadObject("cube.obj")
objet2 = mg.loadObject("wrop.obj")

last = time.time()

# Boucle de rendu principale
while True:
    current = time.time()
    dt = (current - last) * 100  # delta time en secondes,
    last = current  

    mg.clear(" ")
    inpus()

    mg.putMesh(objet, cam, light)

    mg.draw()
