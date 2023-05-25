from orbit_func import deg2rad


# General constants
R_M = 1737.4  # [km]
mu_M = 4.9048696 * 10 ** 3  # [km^3/s^2]

# Orbital params
SMA = 10529.23951  # [km]
ECC = 0.763762616  # [-]
INC = deg2rad(60)  # [rad]
RAAN = deg2rad(0)  # [rad]
AOP = deg2rad(90)  # [rad]

orbpar = [SMA, ECC, INC, RAAN, AOP]

# Satellite params
n_sat = 80

# Transmitter params
trans_angle = deg2rad(70)

# Resolution?
res_t = 10000
res_e = 1


