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
# rt.envMap = Texture('Textures/fondo.bmp')

rt.glClearColor(0.5, 0.0, 0.0)
rt.glClear()

# Materiales
tri_material = Material(difuse=[0.2, 0.8, 0.3], spec=64)

# Crear un triángulo
triangle = Triangle(v0=[-1, -1, -5], v1=[1, -1, -5], v2=[0, 1, -5], material=tri_material)

# Añadir el triángulo a la escena
rt.scene.append(triangle)

# Ajustar la cámara para que se aleje y se centre en la escena
rt.camera.position = [0, 0, 1]  # La cámara se coloca en el origen y se aleja en Z

# Iluminación
rt.lights.append(DirectionalLight(direction=[0, 0, -1], intensity=1.0))  # Luz desde abajo hacia arriba
rt.lights.append(AmbientLight(intensity=0.5))  # Luz ambiental débil

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
