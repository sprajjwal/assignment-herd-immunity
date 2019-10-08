import matplotlib.pyplot as plt
import numpy as np

'''
Info for using matplotlib and numpy came from this Medium post:
https://towardsdatascience.com/5-quick-and-easy-data-visualizations-in-python-
with-code-a2284bae952f
'''


class Visualizer:
    pass


def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    # Create the plot object
    _, ax = plt.subplots()

    # Plot the best fit line, set the linewidth (lw), color and
    # transparency (alpha) of the line
    ax.plot(x_data, y_data, lw=2, color='#539caf', alpha=1)

    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    plt.show()


if __name__ == "__main__":
    lineplot(5, 6, "Number of Days", "Number of Survivors",
             "Herd Immunity Simulation")
