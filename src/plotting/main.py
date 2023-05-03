import plots as plt
import numpy as np


def main(inp):
    plt.line_plot(inp["x"], inp["y"])
    plt.four_plots(inp["x"], inp["y"])


if __name__ == '__main__':
    x = np.linspace(0, 1, 100)

    data = {
        "x": x,
        "y": [x, x**2, x**3, x**4]
    }
    main(data)
