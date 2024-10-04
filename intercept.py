class Intercept(object):
    def __init__(self, point, normal, distance, obj, rayDirection, texCoords):
        self.point = point
        self.normal = normal
        self.distance = distance
        self.obj = obj
        self.rayDirection = rayDirection
        self.texCoords = texCoords
