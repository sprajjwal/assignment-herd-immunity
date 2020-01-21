import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import io
import numpy as np
from pylab import *
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_pdf import PdfPages
import boto3

plt.rcdefaults()

'''
Info for using matplotlib and numpy came from this tutorials:
https://pythonspot.com/matplotlib-bar-chart/
'''


class Visualizer:
    def __init__(self, y_label, title):
        '''Set up object.'''
        self.y_label = y_label
        self.x_label = ""
        self.title = title

    def set_x_label(self, time_step):
        '''Define x_label for bar graph every time step.'''
        self.x_label = f'Population Sizes During Time Step {time_step}'

    def bar_graph(self, time_step, vacc, infected, dead, neither):
        """Return self, with metadata about graph initialized.
           Optimized to work in the web UI.

           Parameters:
           time_step(int): numeric id of the time step which the graph is for
           vacc(int): number of people alive
           infected(int): number of infected people in the population
           dead(int): number of dead people
           neither(int): number of miscellaneous people

           Return:
           name(str): name of the png file created, which shows the bar graph
        """
        self.populations = ["Vaccinated", "Infected", "Dead", "No Interaction"]
        self.y_pos = np.arange(len(self.populations))
        self.num_alive = [vacc, infected, dead, neither]
        self.set_x_label(time_step)
        plt.switch_backend('Agg')  # switching off the main thread
        plt.bar(self.y_pos, self.num_alive, align='center', alpha=0.5)
        plt.xticks(self.y_pos, self.populations)
        plt.ylabel(self.y_label)
        plt.xlabel(self.x_label)
        plt.title(self.title)


class WebVisualizer(Visualizer):
    def __init__(self, y_label, title):
        super().__init__(y_label, title)
        self.populations = list()
        self.y_pos = None
        self.num_alive = list()

    def bar_graph(self, time_step, vacc, infected, dead, neither, experiment):
        """Return self, with metadata about graph initialized.
           Optimized to work in the web UI.

           Parameters:
           time_step(int): numeric id of the time step which the graph is for
           vacc(int): number of people alive
           infected(int): number of infected people in the population
           dead(int): number of dead people
           neither(int): number of miscellaneous people
           experiment(Experiment): the related Experiment model

           Return:
           name(str): name of the png file created, which shows the bar graph
        """
        self.populations = ["Vaccinated", "Infected", "Dead", "No Interaction"]
        self.y_pos = np.arange(len(self.populations))
        self.num_alive = [vacc, infected, dead, neither]
        self.set_x_label(time_step)
        plt.switch_backend('Agg')  # switching off the main thread
        plt.bar(self.y_pos, self.num_alive, align='center', alpha=0.5)
        plt.xticks(self.y_pos, self.populations)
        plt.ylabel(self.y_label)
        plt.xlabel(self.x_label)
        plt.title(self.title)
        # send file to AWS S3
        bucket_name = 'herd-immunity-files'
        file_name = ('static/images/matplot' + str(experiment.title) +
                     str(time_step) + '.png')
        s3client = boto3.client('s3')
        # s3client.put_object(Bucket=bucket_name, Key=file_name, Body=plt)
        # plt.savefig(name)
        # plt.close()
        return plt


if __name__ == "__main__":
    graph = Visualizer("Number of Survivors",
                       ("Herd Immunity Defense Against Disease " +
                        "Spread"))
    graph.bar_graph(1)
