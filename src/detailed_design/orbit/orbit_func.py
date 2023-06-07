import numpy as np
from numpy import sin, cos, tan, pi


# General orbit
def deg2rad(value):
    return np.multiply(value,pi/180)


def rad2deg(value):
    return np.multiply(value,180/pi)

def sec2hrs(value):
    return np.multiply(value,1/3600)


def yrs2sec(value):
    return np.multiply(value,365.25*24*3600)


def percentage(part, total):
    return np.multiply(part,100/total)


def position3D(SMA, ECC, INC, RAAN, AOP, TA):
    # 2D position
    r = SMA * (1 - ECC ** 2) / (1 + ECC * cos(TA))  # [km]
    ksi = r * cos(TA)  # [km]
    eta = r * sin(TA)  # [km]
    pos_2D = [ksi, eta]

    # 3D transformation
    l1 = cos(RAAN) * cos(AOP) - sin(RAAN) * sin(AOP) * cos(INC)
    l2 = -cos(RAAN) * sin(AOP) - sin(RAAN) * cos(AOP) * cos(INC)
    m1 = sin(RAAN) * cos(AOP) + cos(RAAN) * sin(AOP) * cos(INC)
    m2 = -sin(RAAN) * sin(AOP) + cos(RAAN) * cos(AOP) * cos(INC)
    n1 = sin(AOP) * sin(INC)
    n2 = cos(AOP) * sin(INC)
    T = np.array([[l1, l2],
                  [m1, m2],
                  [n1, n2]])
    return np.matmul(T, pos_2D)


# Plotting
def cylinder(r, h, a=0, nt=100, nv=50):
    """
    parametrize the cylinder of radius r, height h, base point a
    """
    theta = np.linspace(0, 2 * np.pi, nt)
    v = np.linspace(a, a + h, nv)
    theta, v = np.meshgrid(theta, v)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = v
    return x, y, z

