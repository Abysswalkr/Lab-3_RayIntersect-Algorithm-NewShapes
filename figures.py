from intercept import Intercept
from MathLib import *
from math import tan, pi, atan2, acos, isclose, sqrt


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


class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cylinder"
        self.top_center = sum_elements(position, [0, height / 2, 0])    # Centro de la tapa superior
        self.bottom_center = sub_elements(position, [0, height / 2, 0])  # Centro de la tapa inferior

    def ray_intersect(self, orig, dir):
        # Coeficientes para la ecuación cuadrática de la superficie lateral del cilindro
        a = dir[0]**2 + dir[2]**2
        b = 2 * ((orig[0] - self.position[0]) * dir[0] + (orig[2] - self.position[2]) * dir[2])
        c = (orig[0] - self.position[0])**2 + (orig[2] - self.position[2])**2 - self.radius**2

        discriminant = b**2 - 4 * a * c
        t_values = []

        # Intersección con la superficie lateral del cilindro
        if discriminant >= 0:
            sqrt_discriminant = sqrt(discriminant)
            t0 = (-b - sqrt_discriminant) / (2 * a)
            t1 = (-b + sqrt_discriminant) / (2 * a)

            for t in [t0, t1]:
                y = orig[1] + t * dir[1]
                if self.bottom_center[1] <= y <= self.top_center[1] and t > 0:
                    t_values.append(t)

        # Intersección con las tapas superior e inferior del cilindro
        if dir[1] != 0:
            # Tapa inferior
            t_bottom = (self.bottom_center[1] - orig[1]) / dir[1]
            if t_bottom > 0:
                x_bottom = orig[0] + t_bottom * dir[0]
                z_bottom = orig[2] + t_bottom * dir[2]
                if (x_bottom - self.position[0])**2 + (z_bottom - self.position[2])**2 <= self.radius**2:
                    t_values.append(t_bottom)

            # Tapa superior
            t_top = (self.top_center[1] - orig[1]) / dir[1]
            if t_top > 0:
                x_top = orig[0] + t_top * dir[0]
                z_top = orig[2] + t_top * dir[2]
                if (x_top - self.position[0])**2 + (z_top - self.position[2])**2 <= self.radius**2:
                    t_values.append(t_top)

        # Si no hay intersecciones válidas
        if not t_values:
            return None

        # Escoger el punto de intersección más cercano al origen
        t = min(t_values)
        P = sum_elements(orig, scalar_multiply(t, dir))

        # Determinar la normal y las coordenadas de textura
        if abs(P[1] - self.top_center[1]) < 1e-6:
            # Intersección con la tapa superior
            normal = [0, 1, 0]
            u = ((P[0] - self.position[0]) / (2 * self.radius)) + 0.5
            v = ((P[2] - self.position[2]) / (2 * self.radius)) + 0.5
        elif abs(P[1] - self.bottom_center[1]) < 1e-6:
            # Intersección con la tapa inferior
            normal = [0, -1, 0]
            u = ((P[0] - self.position[0]) / (2 * self.radius)) + 0.5
            v = ((P[2] - self.position[2]) / (2 * self.radius)) + 0.5
        else:
            # Intersección con la superficie lateral
            normal = [P[0] - self.position[0], 0, P[2] - self.position[2]]
            normal = normalize(normal)
            u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
            v = (P[1] - self.bottom_center[1]) / self.height

        # Asegurarse de que u y v están en el rango [0, 1)
        u = u % 1.0
        v = v % 1.0

        return Intercept(
            point=P,
            normal=normal,
            distance=t,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )


class Torus(Shape):
    def __init__(self, position, major_radius, minor_radius, material):
        super().__init__(position, material)
        self.major_radius = major_radius  # Radio mayor (distancia al centro del toroide)
        self.minor_radius = minor_radius  # Radio menor (radio del tubo)
        self.type = "Torus"

    def ray_intersect(self, orig, dir):
        # Transformar el origen y dirección del rayo al sistema de coordenadas del toroide
        L = sub_elements(orig, self.position)

        # Coeficientes de la ecuación de cuarto grado para un toroide
        sum_dir2 = dir[0] ** 2 + dir[1] ** 2 + dir[2] ** 2
        sum_L2 = L[0] ** 2 + L[1] ** 2 + L[2] ** 2
        R2 = self.major_radius ** 2
        r2 = self.minor_radius ** 2

        k1 = sum_dir2 ** 2
        k2 = 4 * sum_dir2 * dot(L, dir)
        k3 = 2 * sum_dir2 * (sum_L2 - (R2 + r2)) + 4 * (dot(L, dir) ** 2) + 4 * R2 * (dir[0] ** 2 + dir[1] ** 2)
        k4 = 4 * (sum_L2 - (R2 + r2)) * dot(L, dir) + 8 * R2 * (L[0] * dir[0] + L[1] * dir[1])
        k5 = (sum_L2 - (R2 + r2)) ** 2 - 4 * R2 * (self.minor_radius ** 2 - L[0] ** 2 - L[1] ** 2)

        # Resolver la ecuación de cuarto grado
        roots = solve_quartic(k1, k2, k3, k4, k5)
        roots = [t for t in roots if t > 0]

        if not roots:
            return None

        # Seleccionar la intersección más cercana
        t = min(roots)
        P = sum_elements(orig, scalar_multiply(t, dir))

        # Calcular la normal en el punto de intersección
        temp = sqrt(P[0] ** 2 + P[1] ** 2) - self.major_radius
        normal = normalize([P[0] * temp, P[1] * temp, P[2]])

        # Calcular las coordenadas UV para la textura
        u = (atan2(P[1], P[0]) / (2 * pi)) + 0.5
        v = (atan2(P[2], temp) / (2 * pi)) + 0.5

        return Intercept(
            point=P,
            normal=normal,
            distance=t,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )
