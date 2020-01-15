from django.db import models
import analysis.person as ap
import analysis.simulation as a_s
import analysis.virus as av
import analysis.visualizer as avl


class ImmunityTest(models.Model):
    '''An experiment by the user to test the herd immunity of a population.'''
    pass


class Graph(models.Model):
    '''A visual representation of a time step for a Simulation.'''
    pass
