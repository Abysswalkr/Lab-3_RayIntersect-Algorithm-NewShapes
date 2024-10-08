from math import acos, asin, pi
from MathLib import *


def refractVector(normal, incident, n1, n2):
    # Snell's Law
    c1 = dot(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = scalar_multiply(normal, -1)
        n1, n2 = n2, n1

    n = n1 / n2

    temp_vec = scalar_multiply(normal, c1)
    incident_plus_normal = vector_add(incident, temp_vec)

    T1 = scalar_multiply(incident_plus_normal, n)

    factor = (1 - n ** 2 * (1 - c1 ** 2)) ** 0.5
    T2 = scalar_multiply(normal, factor)

    T = vector_add(T1, T2)

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

    s2 = (n1 * (1 - c1 ** 2) ** 0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5

    F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2))) ** 2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1))) ** 2

    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt