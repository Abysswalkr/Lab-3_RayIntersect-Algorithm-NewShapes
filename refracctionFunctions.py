from math import acos, asin, pi, sqrt


# Producto punto entre dos vectores
def dot_product(v1, v2):
    return sum(v1[i] * v2[i] for i in range(len(v1)))


# Normalización de un vector
def normalize_vector(v):
    magnitude = sqrt(sum(comp ** 2 for comp in v))
    return [comp / magnitude for comp in v]


# Multiplicación escalar-vector
def scalar_multiply(scalar, v):
    return [scalar * comp for comp in v]


# Suma de vectores
def vector_add(v1, v2):
    return [v1[i] + v2[i] for i in range(len(v1))]


# Resta de vectores
def vector_subtract(v1, v2):
    return [v1[i] - v2[i] for i in range(len(v1))]


def refractVector(normal, incident, n1, n2):
    # Ley de Snell
    c1 = dot_product(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = scalar_multiply(-1, normal)
        n1, n2 = n2, n1

    n = n1 / n2

    term1 = scalar_multiply(n, vector_add(incident, scalar_multiply(c1, normal)))
    term2 = scalar_multiply(-1, normal)
    term3 = sqrt(1 - n ** 2 * (1 - c1 ** 2))

    T = vector_add(term1, scalar_multiply(term3, term2))

    return normalize_vector(T)


def totalInternalReflection(normal, incident, n1, n2):
    c1 = dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    theta1 = acos(c1)
    thetaC = asin(n2 / n1)

    return theta1 >= thetaC


def fresnel(normal, incident, n1, n2):
    c1 = dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    s2 = (n1 * sqrt(1 - c1 ** 2)) / n2
    c2 = sqrt(1 - s2 ** 2)

    F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2))) ** 2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1))) ** 2

    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt
