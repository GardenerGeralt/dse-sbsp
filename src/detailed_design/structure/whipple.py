import numpy as np
from scipy.optimize import root
from src.plotting import plots as plt
from tqdm import tqdm


def Delta_MLI(S, m_MLI, S_MLI):
    """
    Calculates the MLI correction factor for the critical diameter.
    Args:
        S: spacing between outer bumper and rear wall [cm]
        m_MLI: areal density of multi-layer insulation [g/cm^2]
        S_MLI: distance between bumper and MLI [cm]
    Returns:
        delta critical particle size due to MLI [cm]
    """
    k_MLI = 1.4     # [cm^2] MLI correction factor
    return k_MLI * m_MLI * (S_MLI / S)**(1/2)


def crit_diameter(rho_p, rho_b, rho_w, t_w, t_b, S, V, theta, sigma_y, m_MLI, S_MLI):
    """
    Calculates the critical diameter of the Whipple shield.
    Args:
        rho_p: density of projectile [g/cm^3]
        rho_b: density of bumper [g/cm^3]
        rho_w: density of rear wall [g/cm^3]
        t_w: thickness of rear wall [cm]
        t_b: thickness of bumper [cm]
        S: spacing between bumper and rear wall [cm]
        V: velocity of projectile [km/s]
        theta: impact angle [deg]
        sigma_y: yield strength of rear wall material [Pa]
        m_MLI: areal density of multi-layer insulation [g/cm^2]
        S_MLI: distance between bumper and MLI [cm]
    Returns:
        critical diameter of projectile [cm]
    """
    sigma_y_norm = sigma_y / 482.63e6
    if (t_b / (t_w**(2/3) * S**(1/2))) >= 0.126:
        k_h = 1.35
    else:
        k_h = 7.451 * t_b / (t_w**(2/3) * S**(1/3)) + 0.411
    return k_h * rho_p**(-1/3) * (V * np.cos(np.deg2rad(theta)))**(-2/3) * \
        rho_b**(-1/9) * S**(1/2) * (t_w * rho_w)**(2/3) * sigma_y_norm**(1/3) + Delta_MLI(S, m_MLI, S_MLI)


def micrometeoroid_flux(m, h):
    """
    Calculates the micrometeoroid flux at a given a
    Args:
        m: mass of micrometeoroid [g]
        h: altitude [km]
    Returns:
        micrometeoroid flux [#/m^2/yr]
    """
    R_M = 1737.5    # [km] radius of the moon
    F_1 = (2.2e3 * m**0.306 + 15)**(-4.38)
    F_2 = 1.3e-9 * (m + 1e11 * m**2 + 1e27 * m**4)**(-0.36)
    F_3 = 1.3e-16 * (m + 1e6 * m ** 2) ** (-0.85)
    xi = 0.5 * (1 + np.sqrt(1 - (R_M / (R_M + h))**2))
    G_M = 1 + (R_M / (R_M + h))
    return 3.15576e7 * (F_1 + F_2 + F_3) * xi * G_M


def nr_hits(A_1, A_2, m, h, T):
    """
    Calculates the number of micrometeoroid hits on a given area in a given time.
    Args:
        A_1: first frontal area [m^2]
        A_2: second frontal area [m^2]
        m: mass of micrometeoroid [g]
        h: altitude [km]
        T: time in service [yr]
    Returns:
        number of micrometeoroid hits per spacecraft in time T [#hits/#sc]
    """
    A = np.sqrt(A_1**2 + A_2**2) / 2
    F = micrometeoroid_flux(m, h)
    return F * A * T


bumper_thickness = np.linspace(0.01, 0.1, 100)
bumper_spacing = np.linspace(0.1, 10, 100)
MLI_spacing =  np.linspace(0.1, 10, 100)

side_area = 1.500 * 0.650
front_area = np.pi * (0.650 / 2)**2

values = {
    'total hits': np.zeros([1_000_000]),
    'bumper thickness': np.zeros([1_000_000]),
    'bumper spacing': np.zeros([1_000_000]),
    'MLI spacing': np.zeros([1_000_000])
}

cnt = 0
for i in tqdm(range(len(bumper_thickness))):
    tb = bumper_thickness[i]
    for sb in bumper_spacing:
        for sm in MLI_spacing:
            dc = crit_diameter(0.5, 2.7, 2.7, 0.3, tb, sb, 20, 0, 255e6, 0.17, sm)
            mc = np.pi * (dc / 2)**2 * 0.5
            v = nr_hits(side_area, front_area, mc, 9428.2, 25) * 80
            values['total hits'][cnt] = v
            values['bumper thickness'][cnt] = tb
            values['bumper spacing'][cnt] = sb
            values['MLI spacing'][cnt] = sm
            cnt += 1

plt.line_plot(values['total hits'], [values['bumper thickness'], values['bumper spacing'], values['MLI spacing']])
print()

# print(root(lambda x:
#              nr_hits(side_area, front_area,
#                      np.pi * (crit_diameter(0.5, 2.7, 2.7, 0.3, x[0], x[1], 20, 0, 255e6, 0.17, x[2]) / 2)**2 * 0.5,
#                      9428.2, 25) * 80 - 0.01, x0=[0.1, 0.1, 0.1]))
