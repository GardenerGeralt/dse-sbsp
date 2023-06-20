import math

def Apptrans(Beamdim,appdim,power):
    apppower = power*(1-math.exp(-(2*(appdim**2)/(Beamdim**2))))
    return apppower
def I_r(Power,w_z,r):
    I_r = (Power/(math.pi*0.5*(w_z**2)))*math.exp(-2*((r**2)/(w_z**2)))
    return I_r
def spotsize(initial_radius,distance,theta2):
    spotsize = initial_radius + distance*theta2
    return spotsize
def theta2(labda,initial_radius):
    theta2 = labda/(math.pi*initial_radius)
    return theta2

def focal_length(pointingangle,pixelsize):
    focallength = pixelsize/math.atan(pointingangle)
    return focallength

distance = 18000000 #m
reflector_rad = 1 #m
initial_radius = 0.1 #m
basepower = 5 #Watt
pixelsize = 1.67e-6 #m
labda = 455e-9 #m
pointingangle = 0.65e-6
aperture = 0.18 #m

divergence_angle = theta2(labda,initial_radius)
w_z_receiver = spotsize(initial_radius,distance,divergence_angle) #radius
w_z_sensor = spotsize(reflector_rad,distance,divergence_angle) #radius

fl = focal_length(pointingangle,pixelsize)
print(fl)

power = Apptrans(w_z_receiver,reflector_rad,basepower)
I_r_avg = power/(math.pi*w_z_sensor**2)
intensity_pp = I_r(power,w_z_sensor,w_z_sensor-(0*pixelsize)) - I_r(power,w_z_sensor,w_z_sensor+(1*pixelsize))
print(I_r_avg)
aperture_power = I_r_avg*math.pi*((aperture*0.5)**2)
print(aperture_power)
I_pixel = aperture_power/(pixelsize**2)
print(I_pixel)

