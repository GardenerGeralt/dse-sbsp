import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import time
from skimage import io

# color palette for project. Credits to http://tsitsul.in/blog/coloropt/
COLORS = [(235, 172, 35), (184, 0, 88), (0, 140, 249), (0, 110, 0),
          (0, 187, 173), (209, 99, 230), (178, 69, 2), (255, 146, 135),
          (89, 84, 214), (0, 198, 248), (135, 133, 0), (0, 167, 108),
          (189, 189, 189)]

COLORS_FADED = [(235, 190, 100), (190, 130, 150), (150, 190, 240), (80, 120, 80),
                (110, 200, 190), (220, 160, 230), (170, 110, 70), (255, 160, 134),
                (70, 70, 150), (50, 150, 150), (135, 135, 70), (50, 140, 100),
                (150, 150, 150)]


def reformat_data(some_data):
    some_type = type(some_data)

    if (some_type is not np.ndarray) and (some_type is not list):
        raise TypeError(f"Data should be list or np.ndarray. Got {some_type} instead.")
    elif some_type == list:
        some_data = np.array(some_data)

    some_shape = some_data.shape
    if (len(some_shape) == 1) or (1 in some_shape):
        some_data = np.array([some_data.reshape((some_shape[0],))])

    return some_data


def line_plot(x_data, y_data, labels=None, x_title='x axis', y_title='y axis') -> None:
    """
    Makes a 2D plot with any number of traces (max. 12).
    Always add explicit labels and axis titles for final version of plot!

    Parameters:
    -----------
    x_data : list or numpy array
        Contains one or more vectors of x datapoint coordinates.
        Number of x vectors should be 1 or the same as of y vectors.
    y_data : list or numpy array
        Contains one or more vectors of y datapoint coordinates.
    labels : list, optional
        Labels of traces, to be shown in the legend.
    x_title : string, optional
        Title of x-axis. Please include units.
    y_title : string, optional
        Title of y-axis. Please include units.
    """
    x_data = reformat_data(x_data)
    y_data = reformat_data(y_data)

    n_lines = len(y_data)
    x_len = len(x_data)
    if x_len != 1 and x_len != n_lines:
        raise ValueError(f"Length of x data does not match y data\n",
                         f"Expected 1 or {n_lines}. Got {x_len}.")

    fig = go.Figure()
    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(title_text=y_title)
    for line_index in range(n_lines):
        if labels is None:
            line_label = None
        else:
            line_label = labels[line_index]
        if x_len == 1:
            x_vec = x_data[0]
        else:
            x_vec = x_data[line_index]
        y_vec = y_data[line_index]

        fig.add_trace(go.Scatter(x=x_vec, y=y_vec,
                                 line=dict(color=f'rgb{COLORS_FADED[line_index]}'),
                                 name=line_label))
    fig.update_layout(template="ggplot2", showlegend=True)
    fig.show()


def four_plots(x_data, y_data, labels=(None, None, None, None), x_titles='x axis', y_titles='y axis') -> None:
    """
    Makes a plot with four 2D subplots.
    Always add explicit labels and axis titles for final version of plot!

    Parameters:
    -----------
    x_data : list or numpy array
        Contains one or more vectors of x datapoint coordinates.
        Number of x vectors should be 1 or 4.
    y_data : list or numpy array
        Contains 4 vectors of y datapoint coordinates.
    labels : list, optional
        Labels of traces, to be shown in the legend.
    x_titles : string or list, optional
        Titles of x-axes. Should be 1 or 4.
        Please include units.
    y_titles : string or list, optional
        Titles of y-axes. Should be 1 or 4.
        Please include units.
    """
    x_data = reformat_data(x_data)
    y_data = reformat_data(y_data)

    x_len = len(x_data)
    y_len = len(y_data)
    if x_len != 1 and x_len != 4:
        raise ValueError(f"Length of x data is incorrect.\n",
                         f"Expected 1 or 4. Got {x_len}.")
    elif x_len == 1:
        x_data = np.tile(x_data, (4, 1))
    if y_len != 4:
        raise ValueError(f"Length of y data is incorrect.\n",
                         f"Expected 4. Got {x_len}.")
    if (len(x_titles) == 1) or isinstance(x_titles, str):
        x_titles = np.repeat(x_titles, 4)
    if (len(y_titles) == 1) or isinstance(y_titles, str):
        y_titles = np.repeat(y_titles, 4)

    fig = make_subplots(rows=2, cols=2)

    fig.add_trace(go.Scatter(x=x_data[0], y=y_data[0],
                             line=dict(color=f'rgb{COLORS_FADED[0]}'), name=labels[0]),
                  row=1, col=1)
    fig.update_xaxes(row=1, col=1, title_text=x_titles[0])
    fig.update_yaxes(row=1, col=1, title_text=y_titles[0])

    fig.add_trace(go.Scatter(x=x_data[1], y=y_data[1],
                             line=dict(color=f'rgb{COLORS_FADED[1]}'), name=labels[1]),
                  row=1, col=2)
    fig.update_xaxes(row=1, col=2, title_text=x_titles[1])
    fig.update_yaxes(row=1, col=2, title_text=y_titles[1])

    fig.add_trace(go.Scatter(x=x_data[2], y=y_data[2],
                             line=dict(color=f'rgb{COLORS_FADED[2]}'), name=labels[2]),
                  row=2, col=1)
    fig.update_xaxes(row=2, col=1, title_text=x_titles[2])
    fig.update_yaxes(row=2, col=1, title_text=y_titles[2])

    fig.add_trace(go.Scatter(x=x_data[3], y=y_data[3],
                             line=dict(color=f'rgb{COLORS_FADED[3]}'), name=labels[3]),
                  row=2, col=2)
    fig.update_xaxes(row=2, col=2, title_text=x_titles[3])
    fig.update_yaxes(row=2, col=2, title_text=y_titles[3])

    fig.update_layout(template="ggplot2", showlegend=True)
    fig.show()


def volume_slice(vals, coords):
    df = {'x': [coord for coord in coords[1]],
          'y': coords[2],
          'z': coords[0].flatten(),
          'value': vals}
    fig = px.density_heatmap(df, x='x', y='y', z='value', animation_frame='z')
    fig.show()

    # r, c = volume[0].shape
    # nb_frames = volume.shape[2]
    #
    # fig = go.Figure(frames=[go.Frame(data=go.Surface(
    #     z=(6.7 - k * 0.1) * np.ones((r, c)),
    #     surfacecolor=np.flipud(volume[nb_frames - 1 - k]),
    #     cmin=0, cmax=200
    # ),
    #     name=str(k)  # you need to name the frame for the animation to behave properly
    # )
    #     for k in range(nb_frames)])
    #
    # # Add data to be displayed before animation starts
    # fig.add_trace(go.Surface(
    #     z=(nb_frames - 1) / 10 * np.ones((r, c)),
    #     surfacecolor=np.flipud(volume[nb_frames - 1]),
    #     colorscale='Gray',
    #     colorbar=dict(thickness=20, ticklen=4)
    # ))
    #
    # def frame_args(duration):
    #     return {
    #         "frame": {"duration": duration},
    #         "mode": "immediate",
    #         "fromcurrent": True,
    #         "transition": {"duration": duration, "easing": "linear"},
    #     }
    #
    # sliders = [
    #     {
    #         "pad": {"b": 10, "t": 60},
    #         "len": 0.9,
    #         "x": 0.1,
    #         "y": 0,
    #         "steps": [
    #             {
    #                 "args": [[f.name], frame_args(0)],
    #                 "label": str(k),
    #                 "method": "animate",
    #             }
    #             for k, f in enumerate(fig.frames)
    #         ],
    #     }
    # ]
    #
    # # Layout
    # fig.update_layout(
    #     title='Slices in volumetric data',
    #     width=600,
    #     height=600,
    #     scene=dict(
    #         zaxis=dict(range=[-0.1, 6.8], autorange=False),
    #         aspectratio=dict(x=1, y=1, z=1),
    #     ),
    #     updatemenus=[
    #         {
    #             "buttons": [
    #                 {
    #                     "args": [None, frame_args(50)],
    #                     "label": "&#9654;",  # play symbol
    #                     "method": "animate",
    #                 },
    #                 {
    #                     "args": [[None], frame_args(0)],
    #                     "label": "&#9724;",  # pause symbol
    #                     "method": "animate",
    #                 },
    #             ],
    #             "direction": "left",
    #             "pad": {"r": 10, "t": 70},
    #             "type": "buttons",
    #             "x": 0.1,
    #             "y": 0,
    #         }
    #     ],
    #     sliders=sliders
    # )
    #
    # fig.show()