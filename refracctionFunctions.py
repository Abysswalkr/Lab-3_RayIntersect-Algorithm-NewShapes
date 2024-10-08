from math import acos, asin, pi
from MathLib import *


def refractVector(normal, direction, ior1, ior2):
    cosi = max(-1, min(1, dot(direction, normal)))
    etai = ior1
    etat = ior2
    n = normal

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        n = scalar_multiply(-1, normal)  # Negar el vector normal si estamos dentro del objeto

    eta = etai / etat
    k = 1 - eta ** 2 * (1 - cosi ** 2)

    if k < 0:
        return None  # Total internal reflection

    temp_vec = scalar_multiply(eta, direction)
    normal_vec = scalar_multiply((eta * cosi - sqrt(k)), n)

    return sum_elements(temp_vec, normal_vec)


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