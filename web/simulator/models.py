from django.db import models
import analysis.person as ap
import analysis.simulation as a_s
import analysis.virus as av
import analysis.visualizer as avl
from web import settings
from django.utils import timezone
from django.urls import reverse


class Experiment(models.Model):
    '''An experiment by the user to test the herd immunity of a population.'''
    title = models.CharField(max_length=settings.EXPER_TITLE_MAX_LENGTH,
                             unique=True,
                             help_text="Title of your experiment.")
    pop_size = models.IntegerField(help_text="How large is the population?")
    vacc_percentage = models.FloatField(help_text=(
        "What percentage of the population is initially vaccinated " +
        "against the virus?"
    ))
    mortality_rate = models.FloatField(help_text=(
        "How likely is a patient infected with the virus likely to succumb?" +
        "Must be a percentage between 0.00 and 1.00."
    ))
    repro_rate = models.FloatField(help_text=(
        "How effective is the virus at spreading between individuals?" +
        "Must be a percentage between 0.00 and 1.00."
    ))
    init_infected = models.IntegerField(help_text=(
        "At the beginning of the experiment, how many people in the " +
        "population are infected with the virus?"
    ))
    # initialize using a method below, and use it in analysis.simulation
    init_report = models.TextField(help_text=(
                                    "Summary of initial conditions."))
    final_summary = models.TextField(help_text=(
                                    "Summary of what happened to the " +
                                    "population over the entire experiment."
                                    ))

    def __str__(self):
        '''Return the title of the Experiment instance.'''
        return self.title

    def get_absolute_url(self):
        '''Returns a path to the experimental results after form submission.'''
        pass  # will be implemented alongside the DetailView for this model


class TimeStep(models.Model):
    '''A visual representation of a time step for a Simulation.'''
    step_id = models.IntegerField(help_text=(
        "What time step is this TimeStep for?"))
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,
                                   help_text="The related Experiment model.")
    image = models.ImageField(upload_to='images/',
                              help_text=("Graph representing changes to the " +
                                         "population during the TimeStep."))
    description = models.TextField(help_text=(
                                    "What happened during this time step?"))
    created = models.DateTimeField(auto_now_add=True,
                                   help_text=("The date and time this TimeStep"
                                              + " was created. Auto-generated "
                                              + "when the model " +
                                              "saves, used for ordering."))

    def __str__(self):
        '''Return a unique phrase identifying the TimeStep.'''
        return f'{self.experiment} Step {self.step_id}'
