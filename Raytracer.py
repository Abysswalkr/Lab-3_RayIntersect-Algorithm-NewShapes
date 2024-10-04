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

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)
#rt.envMap = Texture('Textures/fondo.bmp')

rt.glClearColor(0.5,0.0,0.0)
rt.glClear()

# Materiales
brick = Material(difuse = [1, 0.2, 0.2], spec = 128, Ks = 0.25)
grass = Material(difuse = [0.2, 1.0, 0.2], spec = 64, Ks = 0.2)
mirror = Material(difuse = [0.9,0.9,0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(difuse=[0.2,0.2,0.9], spec=128, Ks=0.2, matType=REFLECTIVE)
glass = Material(spec = 128, Ks=0.2, ior=1.5, matType= REFLECTIVE)
vidrio = Material(texture = Texture('Textures/vidrio.bmp'), spec=128, Ks=0.2, matType=REFLECTIVE)

lava = Material(texture = Texture('Textures/lava.bmp'), spec=128, Ks=0.2, matType=OPAQUE)
mandala = Material(texture = Texture('Textures/mandala.bmp'), spec=128, Ks=0.2)
bubuja = Material(texture = Texture('Textures/burbujas.bmp'), spec=128, Ks=0.2, matType=TRANSPARENT)
reptil = Material(texture = Texture('Textures/reptil.bmp'), spec=128, Ks=0.2, matType=OPAQUE)
deathStar = Material(difuse=[1, 1, 1], texture=Texture('Textures/deathStar.bmp'), spec=128, Ks=0.2, matType=OPAQUE)
champions = Material(texture = Texture('Textures/champions.bmp'), spec=128, Ks=0.2, matType=OPAQUE)
holograma = Material(texture = Texture('Textures/holograma.bmp'), spec=128, Ks=0.2, matType=OPAQUE)

yellow_material = Material(difuse=[1.0, 1.0, 0.5], spec=1.5, Ks=0.1  )  # Amarillo claro



# Colores personalizados
color_plano_1 = [86 / 255, 119 / 255, 234 / 255]  # #5677EA
color_plano_2 = [141 / 255, 61 / 255, 0 / 255]    # #8D3D00
color_plano_3_4 = [121 / 255, 134 / 255, 141 / 255]  # #79868D
color_plano_5 = [199 / 255, 234 / 255, 221 / 255]  # #C7EADD

# Colores de los planos
plano1_material = Material(difuse=color_plano_1, spec=64)  # Pared azul
plano2_material = Material(difuse=color_plano_2, spec=64)  # Piso marrón
plano3_material = Material(difuse=color_plano_3_4, spec=64)  # Paredes grises
plano4_material = Material(difuse=color_plano_3_4, spec=64)  # Pared izquierda con espejo
plano5_material = Material(difuse=color_plano_5, spec=64)  # Techo

# Materiales de los cubos
cube_material = Material(texture=Texture('Textures/crafteo.bmp'), spec=64)  # Cubos grises
brown_cube_material = Material(texture=Texture('Textures/horno.bmp'), spec=64)  # Cubo marrón

# Iluminación de la escena
rt.lights.append(DirectionalLight(direction=[0, 0, -1], intensity=1.0))  # Luz desde abajo hacia arriba
rt.lights.append(AmbientLight(intensity=0.5))  # Luz ambiental débil

# Alejar la cámara (ajustar posición de la cámara)
rt.camera.translate = [0, 0, 4]

# Creación de los planos (paredes y suelo)
rt.scene.append(Plane(position=[0, 0, -7], normal=[0, 0, 1], material=yellow_material)) # Plano 1 (Pared del fondo)
rt.scene.append(Plane(position=[0, -2, 0], normal=[0, 1, 0], material=plano2_material)) # Plano 2 (Piso)
rt.scene.append(Plane(position=[3.5, 0, 0], normal=[-1, 0, 0], material=plano3_material)) # Plano 3 (Pared derecha)
rt.scene.append(Plane(position=[-3.5, 0, 0], normal=[1, 0, 0], material=plano4_material)) # Plano 4 (Pared izquierda)
rt.scene.append(Plane(position=[0, 3, 0], normal=[0, -1, 0], material=plano5_material)) # Plano 5 (Techo)

# Creación de cubos
rt.scene.append(AABB(position=[-1, -1.5, -5], sizes=[1, 1, 1], material=cube_material)) # Cubo gris
rt.scene.append(AABB(position=[1, -1.5, -5], sizes=[1, 1, 1], material=brown_cube_material)) # Cubo marrón

# Crear espejos
rt.scene.append(Disk(position=[-3, 0, -3], normal=[1, 0, 0], radius=1.0, material=mirror)) # Espejo en la pared izquierda
rt.scene.append(Disk(position=[0, 2.5, -3], normal=[0, -1, 0], radius=1.5, material=mandala)) # Espejo en el techo


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