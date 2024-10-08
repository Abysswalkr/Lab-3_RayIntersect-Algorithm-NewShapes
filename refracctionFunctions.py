from math import acos, asin, pi, sqrt
from MathLib import dot, scalar_multiply, sum_elements, sub_elements, normalize_vector


def refractVector(normal, incident, n1, n2):
    # Ley de Snell
    c1 = dot(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = scalar_multiply(-1, normal)
        n1, n2 = n2, n1

    n = n1 / n2

    temp_vec = scalar_multiply(c1, normal)
    incident_plus_normal = sum_elements(incident, temp_vec)

    T1 = scalar_multiply(n, incident_plus_normal)

    factor = (1 - n ** 2 * (1 - c1 ** 2)) ** 0.5
    T2 = scalar_multiply(factor, normal)

    T = sub_elements(T1, T2)

    return normalize_vector(T)


def totalInternalReflection(normal, incident, n1, n2):
    c1 = dot(normal, incident)

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
    c1 = dot(normal, incident)

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
