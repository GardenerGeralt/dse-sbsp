from numpy import pi

class Receiver:
    def __init__(self, diameter, eff_rx):
        self.diameter = diameter
        self.area = pi/4*self.diameter**2
        self.eff_rx = eff_rx

    def __str__(self):
        return  f"\nReceiver:\n" \
               f"------------------\n" \
               f"         Receiver area : {self.area:.4e} [Hz],\n" \
               f"   Receiver efficiency : {self.eff_rx} [-],\n"

