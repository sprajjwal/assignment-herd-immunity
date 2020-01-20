from django.db import models
from analysis.person import Person
from analysis.simulation import WebSimulation
from analysis.virus import Virus
from web import settings
from django.utils import timezone
from django.urls import reverse


class Experiment(models.Model):
    '''An experiment by the user to test the herd immunity of a population.'''
    title = models.CharField(max_length=settings.EXPER_TITLE_MAX_LENGTH,
                             unique=False,
                             help_text="Title of your experiment.")
    population_size = models.IntegerField(help_text=(
        "How large is the population?"))
    vaccination_percent = models.FloatField(help_text=(
        "What percentage of the population is initially vaccinated " +
        "against the virus?"
    ))
    virus_name = models.CharField(max_length=settings.EXPER_TITLE_MAX_LENGTH,
                                  unique=False, null=True,
                                  help_text="What virus are you testing?")
    mortality_chance = models.FloatField(help_text=(
        "How likely is a patient infected with the virus likely to succumb?" +
        " Must be a percentage between 0.00 and 1.00."
    ))
    reproductive_rate = models.FloatField(help_text=(
        "How effective is the virus at spreading between individuals?" +
        " Must be a percentage between 0.00 and 1.00."
    ))
    initial_infected = models.IntegerField(help_text=(
        "At the beginning of the experiment, how many people in the " +
        "population are infected with the virus?"
    ))

    def __str__(self):
        '''Return the title of the Experiment instance.'''
        return self.title

    def get_absolute_url(self):
        '''Returns a path to the experimental results after form submission.'''
        path_components = {'pk': self.pk}
        return reverse('simulator:simulation_detail', kwargs=path_components)

    def generate_web_sim(self):
        """Update atttributes for Simulation, based on new data from an
           Experiment instance.

           Parameters:
           self(Experiment): the calling Experiment instance

           Returns:
           WebSimulation: a new instance of the class

        """
        # init population related fields
        pop_size = self.population_size
        # init related fields, virus fields
        virus = Virus(self.virus_name, self.reproductive_rate,
                      self.mortality_chance)
        initial_infected = self.initial_infected
        vacc_percentage = self.vaccination_percent
        # create the population
        return WebSimulation(pop_size, vacc_percentage, virus,
                             initial_infected)

    def run_experiment(self):
        '''Runs through the experiment, and generates time step graphs.'''
        # update Simulation properties with form data
        web_sim = self.generate_web_sim()
        # run through time steps
        web_sim.run_and_collect(self)


class TimeStep(models.Model):
    '''A visual representation of a time step for a Simulation.'''
    step_id = models.IntegerField(help_text=(
        "What time step is this TimeStep for?"))
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,
                                   help_text="The related Experiment model.")
    total_infected = models.IntegerField(help_text=(
        "People who contracted the virus thus far in the experiment."
    ))
    current_infected = models.IntegerField(help_text=(
        "People infected who are still alive in this step of the experiment."
    ))
    vaccinated_population = models.FloatField(help_text=(
        "Percentage of the overall population which is currently vaccinated."
    ))
    dead = models.IntegerField(help_text="People thus far who have succumbed.")
    total_vaccinated = models.IntegerField(help_text=(
        "Amount of individuals who are now vaccinated in the population."
    ))
    alive = models.IntegerField(help_text="People who are currently alive.")
    uninfected = models.IntegerField(help_text=(
        "People who have not had any interaction with the virus."
    ))
    uninteracted = models.IntegerField(help_text=(
        "Alive people in the"
        + " population who are both uninfected, not vaccinated."))
    created = models.DateTimeField(auto_now_add=True,
                                   help_text=("The date and time this TimeStep"
                                              + " was created. Auto-generated "
                                              + "when the model " +
                                              "saves, used for ordering."))

    def __str__(self):
        '''Return a unique phrase identifying the TimeStep.'''
        return f'{self.experiment} Step {self.step_id}'
