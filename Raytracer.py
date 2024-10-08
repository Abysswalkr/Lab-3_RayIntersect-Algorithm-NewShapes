import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

# Configuración de pantalla
width =  400
height = 216

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture('Textures/fondo.bmp')
rt.glClearColor(0.5, 0.0, 0.0)
rt.glClear()

# Materiales
brick = Material(difuse = [1, 0.2, 0.2], spec = 128, Ks = 0.25)
grass = Material(difuse = [0.2, 1.0, 0.2], spec = 64, Ks = 0.2)
mirror = Material(difuse = [0.9,0.9,0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(difuse=[0.2,0.2,0.9], spec=128, Ks=0.2, matType=REFLECTIVE)
glass = Material(spec = 128, Ks=0.2, ior=1.5, matType= TRANSPARENT)


vidrio = Material(texture = Texture('Textures/vidrio.bmp'), spec=128, Ks=0.2, matType=REFLECTIVE)
lava = Material(texture = Texture('Textures/lava.bmp'), spec=128, Ks=0.2, matType=OPAQUE)
mandala = Material(texture = Texture('Textures/mandala.bmp'), spec=128, Ks=0.2)
bubuja = Material(texture = Texture('Textures/burbujas.bmp'), spec=128, Ks=0.2, matType=TRANSPARENT)
reptil = Material(texture = Texture('Textures/reptil.bmp'), spec=128, Ks=0.2, matType=OPAQUE)
deathStar = Material(difuse=[1, 1, 1], texture=Texture('Textures/deathStar.bmp'), spec=128, Ks=0.2, matType=OPAQUE)
champions = Material(texture = Texture('Textures/champions.bmp'), spec=128, Ks=0.2, matType=OPAQUE)
holograma = Material(texture = Texture('Textures/holograma.bmp'), spec=128, Ks=0.2, matType=OPAQUE)


# Coordenadas de la pirámide
# Vértices de la base cuadrada
v0 = [-3, 1, -7]
v1 = [-1, 1, -7]
v2 = [-2, 2.5, -8]
triangle = Triangle(v0, v1, v2, material=glass)
rt.scene.append(triangle)


v3 = [3, 2, -9]
v4 = [1.2, 2, -8]
v5 = [2, 4, -8]
triangle2 = Triangle(v3, v4, v5, material=lava)
rt.scene.append(triangle2)

v0 = [-2, -1.5, -3]
v1 = [1, -1.5, -3]
v2 = [-2, -1.5, -6]
triangle3 = Triangle(v0, v1, v2, material=holograma)
rt.scene.append(triangle3)

# Ajustar la cámara para una vista lateral en perspectiva



# Iluminación
#rt.lights.append(DirectionalLight(direction=[0, 0, -1], intensity=1.0))
rt.lights.append(AmbientLight(intensity=0.5))

# Renderizado de la escena
rt.glRender()

isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
