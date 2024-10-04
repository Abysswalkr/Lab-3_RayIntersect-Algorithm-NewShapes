class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in lines:
            line = line.rstrip()

            try:
                prefix, value = line.split(" ", 1)
            except:
                continue

            if prefix == "v":  # Vertices
                vert = list(map(float, value.split(" ")))
                self.vertices.append(vert)

            elif prefix == "vt":  # Coordenadas de textura
                vts = list(map(float, value.split(" ")))
                self.texcoords.append([vts[0], vts[1]])

            elif prefix == "vn":  # Normales
                norm = list(map(float, value.split(" ")))
                self.normals.append(norm)

            elif prefix == "f":  # Caras
                face = []
                verts = value.split(" ")
                for vert in verts:
                    vert = list(map(int, vert.split("/")))
                    face.append(vert)
                self.faces.append(face)