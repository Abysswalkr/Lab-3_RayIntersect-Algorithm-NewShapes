from math import pi, cos
from gl import *
from MathLib import *


class Light(object):
    def __init__(self, color=[1, 1, 1], intensity=1.0, lighType="None"):
        self.color = color
        self.intensity = intensity
        self.lighType = lighType

    def GetLightColor(self, intercept=None):
        return [(i * self.intensity) for i in self.color]

    def GetSpecularColor(self, intercept, viewPos):
        return [0, 0, 0]


class AmbientLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1.0):
        super().__init__(color, intensity, "Ambient")


class PointLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1, position=[0, 0, 0]):
        super().__init__(color, intensity)
        self.position = position
        self.lighType = "Point"

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept:
            dir = sub_elements(self.position, intercept.point)
            R = sum([comp ** 2 for comp in dir]) ** 0.5  # Magnitud de la dirección
            dir = [comp / R for comp in dir]  # Normalización

            intensity = dot(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
            intensity *= self.intensity

            # Ley de cuadrados inversos
            if R != 0:
                intensity /= R ** 2

            lightColor = [i * intensity for i in lightColor]

        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dir = sub_elements(self.position, intercept.point)
            R = sum([comp ** 2 for comp in dir]) ** 0.5  # Magnitud de la dirección
            dir = [comp / R for comp in dir]  # Normalización

            reflect = calc_reflection(intercept.normal, dir)

            viewDir = sub_elements(viewPos, intercept.point)
            viewDir = normalize_vector(viewDir)

            specularity = max(0, dot(viewDir, reflect) ** intercept.obj.material.spec)
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity

            if R != 0:
                specularity /= R ** 2

            specColor = [i * specularity for i in specColor]

        return specColor


class DirectionalLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1.0, direction=[0, -1, 0]):
        super().__init__(color, intensity, "Directional")
        self.direction = normalize_vector(direction)

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor()
        if intercept:
            dir = [-i for i in self.direction]
            intensity = dot(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
            lightColor = [(i * intensity) for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dir = [-i for i in self.direction]  # Dirección ya normalizada
            reflect = calc_reflection(intercept.normal, dir)

            viewDir = sub_elements(viewPos, intercept.point)
            viewDir = normalize_vector(viewDir)

            # Evitar el uso de números complejos en el cálculo de especularidad
            specularity = max(0, abs(dot(viewDir, reflect)) ** intercept.obj.material.spec)
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity

            specColor = [i * specularity for i in specColor]

        return specColor


class SpotLight(PointLight):
    def __init__(self, color=[1, 1, 1], intensity=1, position=[0, 0, 0], direction=[0, -1, 0], innerAngle=50, outerAngle=60):
        super().__init__(color, intensity, position)
        self.direction = normalize_vector(direction)  # Normalizar la dirección
        self.innerAngle = innerAngle
        self.outerAngle = outerAngle
        self.lighType = "Spot"

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept is not None:
            lightColor = [i * self.SpotlightAttenuation(intercept) for i in lightColor]

        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specularColor = super().GetSpecularColor(intercept, viewPos)

        if intercept is not None:
            specularColor = [i * self.SpotlightAttenuation(intercept) for i in specularColor]

        return specularColor

    def SpotlightAttenuation(self, intercept=None):
        if intercept is None:
            return 0

        # Direccion desde el punto de luz al punto de intercepción
        wi = sub_elements(self.position, intercept.point)
        wi = normalize_vector(wi)  # Normalizar el vector de dirección

        # Convertir los ángulos a radianes
        innerAngleRads = self.innerAngle * pi / 180
        outerAngleRads = self.outerAngle * pi / 180

        # Cálculo de la atenuación basado en el ángulo del spotlight
        attenuation = (-dot(self.direction, wi) - cos(outerAngleRads)) / (cos(innerAngleRads) - cos(outerAngleRads))

        # Asegurarse de que la atenuación esté entre 0 y 1
        attenuation = min(1, max(0, attenuation))

        return attenuation