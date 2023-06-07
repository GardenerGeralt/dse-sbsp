import numpy as np
import numpy.ma as ma
import plotly.graph_objects as go
from scipy.integrate import simps
from scipy.ndimage import zoom

LIGHT_SPEED = 3e8  # [m/s]


def db2lin(db):
    """
    Args:
        db: value in dB
    Returns:
        lin: value in linear
    """
    return 10 ** (db / 10)


def calc_wavelength(freq):
    """
    Returns:
        wavelength: wavelength of microwave [m]
    """
    return LIGHT_SPEED / freq


def calc_circ_area(diameter):
    """
    Args:
        diameter: diameter of circle [m]
    Returns:
        area: area of circle [m2]
    """
    return np.pi * (diameter / 2) ** 2


def gaussian(range, beam):
    x = np.linspace(-range, range, 100)
    y = np.linspace(-range, range, 100)
    x, y = np.meshgrid(x, y)
    r = np.sqrt(x ** 2 + y ** 2)
    # z = ((1. / np.sqrt(2 * np.pi)) * np.exp(-.5 * r ** 2/(0.5*self.module_beam_width)**2))
    z = 2 * power_tx / (np.pi * self.module_beam_width ** 2) * np.exp(-2 * r ** 2 / self.module_beam_width ** 2)

def plotly_plot_bivariate_normal_pdf(x, y, z, name=""):
    fig = go.Figure(data=[go.Surface(x=y, y=x, z=z)])
    fig.update_traces(contours_z=dict(show=True,
                                      usecolormap=True,
                                      highlightcolor="limegreen",
                                      project_z=True))
    fig.update_layout(title=name, autosize=False,
                      scene_camera_eye=dict(x=1.5, y=-1.5, z=1.5),
                      width=1200, height=600,
                      scene=dict(
                          xaxis=dict(nticks=4, range=[-100, 100], ),
                          yaxis=dict(nticks=4, range=[-50, 100], ),
                          zaxis=dict(nticks=4, range=[-100, 100], ), ),
                      margin=dict(l=50, r=50, b=50, t=50))

    fig.show()

class Laser:
    def __init__(
        self, freq, eff_tx, beam_div_angle, min_beam_width, m_squared, spec_mass
    ):
        """
        :param freq: frequency of laser [Hz]
        :param eff_tx: transmitter (DC to RF) efficiency [-]
        :param div_angle: laser divergence HALF angle [rad]
        :param min_beam_width: minimum beam width, very close to transmitter [m]
        :param m_squared: M squared, the beam quality factor (deg of var from gaussian beam, lower is better)
        :param spec_mass: specific mass of laser [kg/W]
        """
        #  Frequency and wavelength
        self.freq = freq
        self.wavelength = calc_wavelength(freq)
        #  Efficiencies
        self.eff_tx = eff_tx
        # self.eff_rx = eff_rx
        # Beam parameters
        self.min_beam_width = min_beam_width
        self.min_beam_area = calc_circ_area(min_beam_width)
        self.m_squared = m_squared
        self.beam_div_angle = beam_div_angle
        #  Mass
        self.spec_mass = spec_mass
        #  Calculated parameters
        self.beam_div_angle_c = self.calc_beam_div_angle()

    def __str__(
        self,
    ):
        return (
            f"\nLaser:\n"
            f"------------------\n"
            f"       Laser frequency : {self.freq:.4e} [Hz],\n"
            f"      Laser wavelength : {self.wavelength:.4e} [m],\n"
            f"Transmitter efficiency : {self.eff_tx} [-],\n"
            f"    Minimum beam width : {self.min_beam_width:.4e} [m],\n"
            f"     Minimum beam area : {self.min_beam_area:.4e} [m2],\n"
            f"             M squared : {self.m_squared} [-],\n"
            f" Given beam divergence angle : {self.beam_div_angle:.4e} [rad]\n"
            f" Calculated beam divergence angle : {self.beam_div_angle_c:.4e} [rad], "
        )

    def calc_beam_div_angle(self):
        """
        Returns: full divergence angle theta (NOT HALF)
        """
        return 2 * self.m_squared * self.wavelength / (np.pi * self.min_beam_width)

    def calc_beam_width(self, distance):
        """
        Args:
            distance: distance from transmitter [m]
        Returns:
            w(distance): beam width at certain distance [m]
        """
        # according to https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7885601:
        return self.min_beam_width * np.sqrt(
            1
            + (
                self.m_squared
                * self.wavelength
                * distance
                / (np.pi * self.min_beam_width**2)
            )
            ** 2
        )

    def flux_density(self, power_tx, distance):
        """
        Args:
            power_tx: power at transmitter [W]
            distance: distance from transmitter [m]
        Returns:
            S(distance): flux density at certain distance, averaged over the entire beam? [W/m2]
        """
        return power_tx / calc_circ_area(self.calc_beam_width(distance))

    def calc_power_tx(self, power_rx, distance):
        """
        Args:
            power_rx: power at receiver [W]
            distance: distance from transmitter [m]
        Returns:
            power_tx: power at transmitter [W]
        """
        return power_rx / (self.eff_rx * self.eff_tx)

    def calc_mass_tx(self, power_tx):
        """
        Args:
            power_tx: power at transmitter [W]
        Returns:
            mass_tx: mass of transmitter [kg]
        """
        return power_tx * self.spec_mass


class LaserArray:
    def __init__(self, n_modules, module_spacing):
        self.n_modules = n_modules
        self.module_spacing = module_spacing

        # From laser class
        self.module = Laser(3e8 / 976e-9, 0.43, 0.33, 5.4e-3, 4, 1)
        self.module_power = 300 # W
        self.module_beam_width = self.module.calc_beam_width(18000)

    def __str__(self):
        return (
            f"\nLaser Array:\n"
            f"------------------\n"
            f"       Number of lasers : {self.n_modules},\n"
            f"      Module spacing    : {self.module_spacing:.4e} [m],\n"
            f"Transmitter efficiency : {self.module.eff_tx} [-],\n"
            f"    Minimum beam width : {self.module.min_beam_width:.4e} [m],\n"
            f"     Minimum beam area : {self.module.min_beam_area:.4e} [m2],\n"
            f"             M squared : {self.module.m_squared} [-],\n"
            f" Given beam divergence angle : {self.module.beam_div_angle:.4e} [rad],\n"
            f" Calculated beam divergence angle : {self.module.beam_div_angle_c:.4e} [rad],\n"
            f" Power per beam : {self.module_power:.4e} [W],\n"
            f" Beam width at 18000 km : {self.module_beam_width:.4e} [m],\n"
            f" Beam area at 18000 km : {calc_circ_area(self.module_beam_width):.4e} [m2],\n"
            # f" Beam width at 18000 km : {self.module_beam_width:.4e} [m],\n"

        )

    def square_array(self):
        n_mod_per_line = np.int(np.sqrt(self.n_modules))
        x = self.module_spacing * np.arange(0, n_mod_per_line)
        return np.meshgrid(x, x)

    def circ_array(self):
        #resolution = 100 # points per meter
        #ground_size = 10 # meters (*2)
        #biggrid = np.zeros((-1, 1000-1))
        modules_per_line = np.array(
            [5, 9, 11, 13, 13, 15, 15, 15, 15, 15, 13, 13, 11, 9, 5]
        )
        mask_array = np.array(
            [
                np.pad(
                    np.ones(modules_per_line[i]),
                    (
                        int((np.max(modules_per_line) - modules_per_line[i]) / 2),
                        int((np.max(modules_per_line) - modules_per_line[i]) / 2),
                    ),
                    mode="constant",
                    constant_values=(np.nan,),
                )
                for i in range(np.size(modules_per_line))
            ]
        )
        x = (
            self.module_spacing * np.arange(0, np.max(modules_per_line))
        )
        # print(np.shape(mask_array))
        grid = np.meshgrid(x, x)
        # print(np.shape(grid))
        grid = np.array([np.multiply(i, mask_array) for i in grid])
        return grid

    def gaussian_spot(self, domain):
        x = np.linspace(-domain, domain, 20)
        y = np.linspace(-domain, domain, 20)
        x, y = np.meshgrid(x, y)
        r = np.sqrt(x ** 2 + y ** 2)
        z = 2 * self.module_power / (np.pi * self.module_beam_width ** 2) * np.exp(-2 * r ** 2 / self.module_beam_width ** 2)
        return x, y, z

    def gaussian_field(self):
        trans_grid = self.circ_array()
        zoom_factor = 1.5  # Increase resolution by a factor of 2 (adjust as needed)

        # Perform zooming on the image
        zoomed_image = zoom(trans_grid, zoom_factor)

        # Round the values to the nearest integer (0 or 1)
        zoomed_image = np.round(zoomed_image)

        # Convert the values to integers (0 or 1)
        # zoomed_image = zoomed_image.astype(int)
        print(trans_grid)
        print(zoomed_image)
        print(np.size(~np.isnan(zoomed_image)))
        return zoomed_image

    def calc_total_beam_diameter(self):
        # print(self.circ_array())
        return np.nanmax(self.circ_array())+self.module_beam_width

    def plot_flat_array(self, array):
        fig = go.Figure()

        # for x, y in zip(array[0].flatten(), array[1].flatten()):
        #     if not np.isnan(x) and not np.isnan(y):
        #         fig.add_shape(
        #             type="circle",
        #             xref="x",
        #             yref="y",
        #             fillcolor="PaleTurquoise",
        #             x0=x - self.module_beam_width / 2,
        #             y0=y - self.module_beam_width / 2 ,
        #             x1=x + self.module_beam_width / 2,
        #             y1=y + self.module_beam_width / 2,
        #             line_color="LightSeaGreen",
        #             opacity=0.05,
        #         )
        fig.add_trace(go.Scatter(
            x=array[0].flatten(),
            y=array[1].flatten(),
            mode="markers",
            marker=dict(
                # size=self.module_beam_width * np.ones(np.size(array)),
                # sizemode="diameter",
                # sizeref=self.module_beam_width,
            ),
            opacity=1,
        ))
        # fig.data = fig.data[::-1]
        fig.update_layout(
            autosize=True,
            width=1000,
            height=1000,
            margin=dict(l=50, r=50, b=50, t=50, pad=4),
        )
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
        fig.show()

    def plot_3d_array(self, array):
        x, y, z = self.gaussian_spot(5)
        # print(np.max(z))
        # print(simps(simps(z.flatten(), y.flatten()), x.flatten()))
        # VERIFY WITH INTEGRAL!!!!!!!!!!!!!!!!!!!!!
        # integ = power_tx*(1-np.exp(-1/2))
        # print(integ)
        fig = go.Figure()
        # for xi, yi in zip(array[0].flatten(), array[1].flatten()):
        #     if not np.isnan(xi) and not np.isnan(yi):
        #         fig.add_trace(go.Surface(x=xi+x, y=yi+y, z=z)
        #         )

        fig.add_trace(go.Surface(x=x,y=y,z=z))


        fig.update_traces(contours_z=dict(show=True,
                                          usecolormap=True,
                                          highlightcolor="limegreen",
                                          project_z=True))
        fig.update_layout(autosize=False,
                          scene_camera_eye=dict(x=1.5, y=-1.5, z=1.5),
                          width=1200, height=600,
                          margin=dict(l=50, r=50, b=50, t=50))
        fig.show()
        return x,y,z

    def calc_pointing_accuracy(self, distance, size_rx):
        return np.arctan(0.5*(size_rx-self.calc_total_beam_diameter())/distance)
        # return np.arctan(0.5 * (size_rx - 5) / distance)