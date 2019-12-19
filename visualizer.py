import matplotlib.pyplot as plt
import io
import numpy as np
from pylab import *
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_pdf import PdfPages
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

    def bar_graph(self, time_step, vacc, infected, dead, neither):
        """Plot a bar histogram showing numbers of alive people who are
           either vaccinated, infected, or neither during one time step.
        """
        populations = ["Vaccinated", "Infected", "Dead", "No Interaction"]
        y_pos = np.arange(len(populations))
        num_alive = [vacc, infected, dead, neither]
        plt.bar(y_pos, num_alive, align='center', alpha=0.5)
        plt.xticks(y_pos, populations)
        plt.ylabel(self.y_label)
        self.set_x_label(time_step)
        plt.xlabel(self.x_label)
        plt.title(self.title)
        # show graph for 5 seconds, then close
        plt.show(block=False)
        plt.pause(5)
        # plt.close()


class Web_Visualizer(Visualizer):
    def __init__(self, y_label, title):
        self.populations = list()
        self.y_pos = None
        self.num_alive = list()
        super().__init__(y_label, title)

    def bar_graph(self, time_step, vacc, infected, dead, neither):
        """Return self, with metadata about graph initialized.
           Optimized to work in the web UI.

        """
        # pp = PdfPages('multipage.pdf')
        # print(f'Can I print this? {plt}')
        self.populations = ["Vaccinated", "Infected", "Dead", "No Interaction"]
        self.y_pos = np.arange(len(populations))
        self.num_alive = [vacc, infected, dead, neither]
        self.set_x_label(time_step)
        return self
        '''
        fig = plt.figure()
        plt.bar(y_pos, num_alive, align='center', alpha=0.5)
        plt.xticks(y_pos, populations)
        plt.ylabel(self.y_label)
        plt.xlabel(self.x_label)
        plt.title(self.title)
        # save the figure as a pdf
        # plt.savefig(pp, format='pdf')
        return plt
        '''



if __name__ == "__main__":
    graph = Visualizer("Number of Survivors",
                       ("Herd Immunity Defense Against Disease " +
                        "Spread"))
    graph.bar_graph(1)
