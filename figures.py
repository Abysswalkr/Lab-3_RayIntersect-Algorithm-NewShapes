from intercept import Intercept
from MathLib import *
from math import tan, pi, atan2, acos, isclose


class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None


class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def ray_intersect(self, origin, direction):
        distance_vect = sub_elements(self.position, origin)
        tca = dot(distance_vect, direction)

        normDistSq = sum([comp ** 2 for comp in distance_vect])  # ||L||^2
        projDistSq = normDistSq - tca ** 2
        if projDistSq < 0:
            return None  # No hay intersección

        projDist = sqrt(projDistSq)

        if projDist > self.radius:
            return None

        thc = (self.radius ** 2 - projDist ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        # Punto de intersección = origin + direction * t0
        scaledDir = [comp * t0 for comp in direction]  # direction * t0
        intersectPoint = sum_elements(origin, scaledDir)  # origin + (direction * t0)

        # normalVec = (PuntoIntersección - self.centro).normalize()
        pointDiff = sub_elements(intersectPoint, self.position)
        normalVec = normalize_vector(pointDiff)

        u = 1 - ((atan2(normalVec[2], normalVec[0])) / (2 * pi) + 0.5)
        v = acos(-normalVec[1]) / pi

        return Intercept(point=intersectPoint,
                         normal=normalVec,
                         distance=t0,
                         obj=self,
                         rayDirection=direction,
                         texCoords= [u,v]
                         )

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normalize_vector(normal)
        self.type = "Plane"

    def ray_intersect(self, orig, dir):
        # distancia = ((planePos - rayOrig) o normal) / (rayDir o normal)
        denom = dot(dir, self.normal)

        if isclose(0, denom):
            return None

        num = dot(sub_elements(self.position, orig), self.normal)
        t = num / denom

        if t < 0:
            return None

        # P orig + dir * t0
        P = sum_elements(orig, scalar_multiply(t, dir))

        u = (P[0] - self.position[0]) % 1
        v = (P[1] - self.position[1]) % 1

        return Intercept(point=P,
                         normal=self.normal,
                         distance=t,
                         texCoords=None,
                         rayDirection=dir,
                         obj=self)


class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"

    def ray_intersect(self, orig, dir):
        planeIntercept = super().ray_intersect(orig, dir)

        if planeIntercept is None:
            return None

        contact = sub_elements(planeIntercept.point, self.position)
        contact = sqrt(sum([comp ** 2 for comp in contact]))

        if contact > self.radius:
            return None

        return planeIntercept

class AABB(Shape):
    # Axis-Aligned Bounding Box
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"

        self.planes = []

        rightPlane = Plane([position[0] + sizes[0] / 2, position[1], position[2]], [1, 0, 0], material)
        leftPlane = Plane([position[0] - sizes[0] / 2, position[1], position[2]], [-1, 0, 0], material)
        upPlane = Plane([position[0], position[1] + sizes[1] / 2, position[2]], [0, 1, 0], material)
        downPlane = Plane([position[0], position[1] - sizes[1] / 2, position[2]], [0, -1, 0], material)
        frontPlane = Plane([position[0], position[1], position[2] + sizes[2] / 2], [0, 0, 1], material)
        backPlane = Plane([position[0], position[1], position[2] - sizes[2] / 2], [0, 0, -1], material)

        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        # Bounds
        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i] / 2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i] / 2)

    def ray_intersect(self, orig, dir):

        intercept = None
        t = float("inf")

        for plane in self.planes:
            planeIntercept = plane.ray_intersect(orig, dir)

            if planeIntercept is not None:

                planePoint = planeIntercept.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeIntercept.distance < t:
                                t = planeIntercept.distance
                                intercept = planeIntercept

        if intercept is None:
            return None

        u, v = 0, 0
        if abs(intercept.normal[0]) > 0:
            # Mapear las uvs para el eje x, usando las coordenadas de Y y Z
            u = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[1]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[2]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]

        u = min(0.999, max(0, u))
        v = min(0.999, max(0, u))

        return Intercept(point=intercept.point,
                         normal=intercept.normal,
                         distance=t,
                         texCoords=[u, v],
                         rayDirection=dir,
                         obj=self)


class Triangle(Shape):
    def __init__(self, v0, v1, v2, material):
        super().__init__(None, material)  # No tiene una posición como tal
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.type = "Triangle"

        # Precalcula la normal del triángulo usando los vértices
        edge1 = sub_elements(self.v1, self.v0)
        edge2 = sub_elements(self.v2, self.v0)
        self.normal = cross_product(edge1, edge2)
        self.normal = normalize(self.normal)  # Normalizar la normal

    def ray_intersect(self, orig, dir):
        epsilon = 1e-6
        edge1 = sub_elements(self.v1, self.v0)
        edge2 = sub_elements(self.v2, self.v0)

        # Intersección del rayo con el triángulo
        h = cross_product(dir, edge2)
        a = dot(edge1, h)

        if -epsilon < a < epsilon:
            return None  # El rayo es paralelo al triángulo

        f = 1.0 / a
        s = sub_elements(orig, self.v0)
        u = f * dot(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = cross_product(s, edge1)
        v = f * dot(dir, q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * dot(edge2, q)

        if t > epsilon:
            P = sum_elements(orig, scalar_multiply(t, dir))  # Cambio aquí, primero el escalar y luego el vector
            return Intercept(
                point=P,
                normal=self.normal,
                distance=t,
                texCoords=[u, v],  # Podemos usar (u, v) como coordenadas de textura
                rayDirection=dir,
                obj=self
            )
        else:
            return None


#class Cilinder(object):
#    def __init__(self, position, radius, height, material):
#        self.position = position
#        self.radius = radius
#        self.height = height
#        self.material = material
#
#        # Parte superior e inferior del cilindro
#        self.upper_disk = Disk(
#            [self.position[0], self.position[1] + self.height / 2, self.position[2]],
#            self.radius,
#            (0, 1, 0),
#            self.material
#        )
#        self.lower_disk = Disk(
#            [self.position[0], self.position[1] - self.height / 2, self.position[2]],
#            self.radius,
#            (0, -1, 0),
#            self.material
#        )
#
#    def ray_intersect(self, orig, dir):
#        # Verificar intersección con los discos superior e inferior
#        intersect_upper = self.upper_disk.ray_intersect(orig, dir)
#        intersect_lower = self.lower_disk.ray_intersect(orig, dir)
#
#        # Intersección con la superficie lateral del cilindro
#        # Transformar origen y dirección del rayo al sistema de coordenadas del cilindro
#        oc = np.subtract(orig, self.position)
#        a = dir[0] ** 2 + dir[2] ** 2
#        b = 2 * (oc[0] * dir[0] + oc[2] * dir[2])
#        c = oc[0] ** 2 + oc[2] ** 2 - self.radius ** 2
#
#        discriminant = b ** 2 - 4 * a * c
#        if discriminant < 0:
#            lateral_intersect = None
#        else:
#            # Calcular t0 y t1 para la superficie lateral
#            t0 = (-b - np.sqrt(discriminant)) / (2 * a)
#            t1 = (-b + np.sqrt(discriminant)) / (2 * a)
#
#            # Escoger el valor más cercano a la cámara
#            t = min(t0, t1) if t0 > 0 else t1
#            if t < 0:
#                lateral_intersect = None
#            else:
#                # Calcular el punto de intersección
#                P = np.add(orig, t * np.array(dir))
#                y = P[1] - self.position[1]
#
#                # Verificar si el punto de intersección está dentro de la altura del cilindro
#                if -self.height / 2 <= y <= self.height / 2:
#                    normal = np.array([P[0] - self.position[0], 0, P[2] - self.position[2]])
#                    normal = normal / np.linalg.norm(normal)
#                    lateral_intersect = Intersect(
#                        distance=t,
#                        point=P,
#                        normal=normal,
#                        texcoords=None,
#                        sceneObj=self
#                    )
#                else:
#                    lateral_intersect = None
#
#        # Escoger el punto de intersección más cercano entre los discos y la superficie lateral
#        closest_intersect = None
#        if intersect_upper and (closest_intersect is None or intersect_upper.distance < closest_intersect.distance):
#            closest_intersect = intersect_upper
#        if intersect_lower and (closest_intersect is None or intersect_lower.distance < closest_intersect.distance):
#            closest_intersect = intersect_lower
#        if lateral_intersect and (closest_intersect is None or lateral_intersect.distance < closest_intersect.distance):
#            closest_intersect = lateral_intersect
#
#        return closest_intersect
#