import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

# Configuración de pantalla
width =  1000
height = 740

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture('Textures/fondo.bmp')
rt.glClearColor(0.5, 0.0, 0.0)
rt.glClear()

# Material para la pirámide
pyramid_material = Material(difuse=[0.8, 0.5, 0.2], spec=64)
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
# Triángulos ajustados en tamaño y posición
v0 = [-4, 0.5, -10]
v1 = [-2, 0.5, -10]
v2 = [-3, 3, -10]
triangle = Triangle(v0, v1, v2, material=bubuja)
rt.scene.append(triangle)

v3 = [2.5, 2.5, -9]
v4 = [0.7, 2, -8]
v5 = [1.5, 4.5, -9]
triangle2 = Triangle(v3, v4, v5, material=lava)
rt.scene.append(triangle2)

v0 = [-3, -1.5, -4]
v1 = [2, -1.5, -4]
v2 = [-3, -1.5, -8]
triangle3 = Triangle(v0, v1, v2, material=holograma)
rt.scene.append(triangle3)

# Cilindros con posiciones y tamaños variados
cylinder = Cylinder(position=[-1, -2, -6], radius=0.8, height=1.2, material=reptil)
rt.scene.append(cylinder)

cylinder2 = Cylinder(position=[2.5, -1, -7], radius=1.5, height=1.5, material=glass)
rt.scene.append(cylinder2)

cylinder3 = Cylinder(position=[0.5, 1, -8], radius=0.7, height=0.8, material=mandala)
rt.scene.append(cylinder3)


# Crear el toroide y añadirlo a la escena
#toroide = Torus(position=[0, 0, -5], major_radius=2, minor_radius=0.5, material=bubuja)
#rt.scene.append(toroide)


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
