# Lab 3_RayIntersect Algorithm NewShapes

## Descripción del Proyecto

Este proyecto extiende el motor de trazado de rayos en Python con **pygame**, añadiendo soporte para nuevas figuras geométricas: **triángulo**, **cilindro** y **toroide**. Estas figuras permiten ampliar las posibilidades de modelado y renderizado en escenas 3D, proporcionando un mayor detalle y flexibilidad en la creación de objetos. Además, se incluye un sistema de materiales que permite aplicar texturas y ajustar las propiedades de reflexión, refracción y opacidad de cada figura.

El motor de trazado de rayos es capaz de renderizar estas figuras aplicando algoritmos de intersección de rayos específicos para cada tipo de forma, junto con un sistema de iluminación ambiental y direccional que proporciona una representación visual más realista.

## Características

- **Formas Soportadas**: Triángulo, Cilindro, Toroide.
- **Intersección de Rayos**: Algoritmos de intersección de rayos específicos para cada figura, incluyendo superficies curvas y formas complejas.
- **Materiales**: Soporte para materiales con propiedades ajustables como difusividad, especularidad, reflexión, transparencia y textura.
- **Texturas**: Compatibilidad con imágenes en formato .bmp para aplicarlas como texturas en las figuras.
- **Iluminación**: Iluminación direccional y ambiental, con ajuste de intensidad para una mejor visualización de sombras y reflejos.
- **Cámara**: Control de posición de cámara para manipular el ángulo de visión de la escena.

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Abysswalkr/Lab-3_RayIntersect-Algorithm-NewShapes.git
   ```

2. Instalar las dependencias necesarias, como **pygame**:
   ```bash
   pip install pygame
   ```

3. Ejecutar el programa:
   ```bash
   python main.py
   ```

## Estructura del Proyecto

- **gl.py**: Renderizador que gestiona el trazado de rayos, el manejo de texturas y la creación de la imagen final.
- **figures.py**: Definición de las nuevas figuras geométricas (Triángulo, Cilindro, Toroide) y algoritmos de intersección.
- **material.py**: Gestión de materiales para los objetos, permitiendo configuraciones opacas, reflectantes o transparentes.
- **lights.py**: Implementación de iluminación direccional y ambiental.
- **texture.py**: Carga y aplicación de texturas en los objetos.
- **Raytracer.py**: Configuración de la escena, incluyendo materiales, texturas, luces y figuras, así como la ejecución del renderizado.

## Uso

El archivo `Raytracer.py` contiene la configuración de la escena que se renderizará. Puedes modificar las propiedades de los materiales, añadir o eliminar objetos, o cambiar la posición de la cámara para personalizar la visualización.

Ejemplo de creación de un cilindro con textura:
```python
cylinder_material = Material(texture=Texture('Textures/piedra.bmp'), spec=64)
cylinder = Cylinder(position=[1.5, -1, -5], radius=1, height=2, material=cylinder_material)
rt.scene.append(cylinder)
```

## Figuras Implementadas

### Triángulo
El triángulo utiliza el algoritmo de Möller-Trumbore para calcular la intersección de rayos con su superficie. Esta figura es útil para construir modelos complejos al combinar múltiples triángulos.

### Cilindro
El cilindro incluye cálculos de intersección tanto para las tapas superior e inferior como para la superficie lateral. Esto permite una visualización precisa desde cualquier ángulo y permite el mapeo de texturas en las superficies curvas del cilindro.

### Toroide
El toroide utiliza una ecuación cuártica para calcular las intersecciones de rayos con su superficie. Su forma de "donut" añade un nivel avanzado de complejidad y se puede personalizar con un radio mayor y menor para modificar su forma.

## Capturas de Pantalla

Aquí se muestra una captura de pantalla de la escena con las nuevas figuras renderizadas:

![Captura de pantalla 2024-10-09 170258](https://github.com/user-attachments/assets/c81fc0bc-2da4-4ce7-88de-ed1b8f0cc1d9)

## Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar el proyecto o encuentras errores, por favor abre un "issue" o envía un "pull request" en el repositorio oficial.
