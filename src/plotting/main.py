import plots as plt
import numpy as np


def main(inp):
    labels = ["Trace A", "Trace B", "Trace C", "Trace D"]
    plt.line_plot(inp["x"], inp["y"], labels=labels, x_title="X Axis", y_title="Y Axis")
    plt.four_plots(inp["x"], inp["y"], labels=labels, x_titles="X Axis", y_titles=["Y Axis A",
                                                                                   "Y Axis B",
                                                                                   "Y Axis C",
                                                                                   "Y Axis D"])


if __name__ == '__main__':
    x = np.linspace(0, 1, 100)

    data = {
        "x": x,
        "y": [x, x**2, x**3, x**4]
    }
    main(data)
