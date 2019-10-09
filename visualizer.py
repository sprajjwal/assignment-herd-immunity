import matplotlib.pyplot as plt
import numpy as np
from pylab import *
plt.rcdefaults()

'''
Info for using matplotlib and numpy came from this tutorials:
https://pythonspot.com/matplotlib-bar-chart/
'''


class Visualizer:
    def __init__(self, y_label, title):
        """Set up object."""
        self.y_label = y_label
        self.x_label = ""
        self.title = title

    def set_x_label(self, time_step):
        """Define x_label for bar graph every time step."""
        self.x_label = f'Population Sizes During Time Step {time_step}'

    def bar_graph(self, time_step):
        """Plot a bar histogram showing numbers of alive people who are
           either vaccinated, infected, or neither during one time step.
        """
        populations = ["Vaccinated", "Infected", "Neither"]
        y_pos = np.arange(len(populations))
        num_alive = [10, 40, 70]
        plt.bar(y_pos, num_alive, align='center', alpha=0.5)
        plt.xticks(y_pos, populations)
        plt.ylabel(self.y_label)
        self.set_x_label(time_step)
        plt.xlabel(self.x_label)
        plt.title(self.title)
        # show graph for 5 seconds, then close
        plt.show(block=False)
        plt.pause(5)
        plt.close()


if __name__ == "__main__":
    graph = Visualizer("Number of Survivors",
                       ("Herd Immunity Defense Against Disease " +
                        "Spread"))
    graph.bar_graph(1)

    # 5, 2, "Populations", "Number of Survivors",
    # "Herd Immunity Defense Against Disease Spread", False)
    # graph.lineplot(arange(5), arange(5), "Number of Days",
    #                 "Number of Survivors", "Herd Immunity Simulation")
    """
        # def histogram(self, data, n_bins, x_label,
        # y_label, title, cumulative):
        # _, ax = plt.subplots()
        population_sizes = [20, 30, 70]
        bins = [2, 3]
        plt.hist(population_sizes, bins, histtype="bar", rwidth=0.8)
        plt.set_ylabel(y_label)
        plt.set_xlabel(x_label)
        plt.set_title(title)
        plt.show()
        # ax.hist(data, n_bins, cumulative, color='#539caf')
        # ax.set_ylabel(y_label)
        # ax.set_xlabel(x_label)
        # ax.set_title(title)

        # ax.show()

    def lineplot(self, x_data, y_data, x_label="", y_label="", title=""):
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
    """
