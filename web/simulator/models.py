from django.db import models
from analysis.person import Person
from analysis.simulation import Simulation
from analysis.virus import Virus
from analysis.visualizer import Visualizer
from web import settings
from django.utils import timezone
from django.urls import reverse


class Experiment(models.Model, Simulation):
    '''An experiment by the user to test the herd immunity of a population.'''
    title = models.CharField(max_length=settings.EXPER_TITLE_MAX_LENGTH,
                             unique=True,
                             help_text="Title of your experiment.")
    pop_size = models.IntegerField(help_text="How large is the population?")
    vacc_percentage = models.FloatField(help_text=(
        "What percentage of the population is initially vaccinated " +
        "against the virus?"
    ))
    virus_name = models.CharField(max_length=settings.EXPER_TITLE_MAX_LENGTH,
                                  unique=False, null=True,
                                  help_text="What virus are you testing?")
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

    def __init__(self, *args, **kwargs):
        '''Resolve conflict between initializers of superclasses.'''
        # set Simulation properties to None for now
        self.population = list()  # List of Person objects
        self.pop_size = None  # Int
        self.next_person_id = None  # Int
        self.virus = None  # Virus object
        self.initial_infected = None  # Int
        self.total_infected = 0  # Int
        self.vacc_percentage = 0.0  # float between 0 and 1
        self.total_dead = 0  # Int
        self.newly_infected = list()
        # call init method of the Model class
        return super(Model, self).__init__(*args, **kwargs)

    def __str__(self):
        '''Return the title of the Experiment instance.'''
        return self.title

    def get_absolute_url(self):
        '''Returns a path to the experimental results after form submission.'''
        pass  # will be implemented alongside the DetailView for this model

    def set_init_report(self, report):
        """Initializes a value for the init_report field.

          Parameters:
          report(str): a summary of population size, init_infected,
                       vacc_percentage, mortality_rate, and repro_rate before
                       any interactions have occurred

          Returns:
          None

        """
        pass

    def set_final_summary(self, report):
        """Initializes a value for the init_summary field.

          Parameters:
          report(str): a summary of population size, init_infected,
                       vacc_percentage, mortality_rate, and repro_rate after
                       the experiment has expired.

          Returns:
          None

        """
        pass

    def run_experiment(self):
        '''Runs through the experiment, and generates time step graphs.'''
        # update Simulation properties with form data
        # run the time steps
        # save the images with Graph instances
        # initialize the init and final report
        pass


class TimeStep(models.Model, Visualizer):
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
