import random
import sys
from person import Person
from logger import Logger
from virus import Virus
import visualizer
random.seed(42)


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when
        file is run.

    Simulates the spread of a virus through a given population.
    The percentage of the population that are vaccinated,
        the size of the population, and the amount of initially
        infected people in a population are all variables that can be set when
        the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of
            population vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected
            with the disease.
        The total infected people is the running total that have been infected
            since the simulation began, including the currently infected people
            who died.
        You will also need to keep track of the number of people that have die
            as a result of the infection.

        All arguments will be passed as command-line arguments when the file is
            run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO:
        # Remember to call the appropriate logger method in the corresponding
        #   parts of the simulation.
        # TODO: Store each newly infected person's ID in newly_infected
        #   attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.population = []  # List of Person objects
        self.pop_size = pop_size  # Int
        self.next_person_id = pop_size  # Int
        self.virus = virus  # Virus object
        self.initial_infected = initial_infected  # Int
        self.total_infected = 0  # Int
        self.vacc_percentage = vacc_percentage  # float between 0 and 1
        self.total_dead = 0  # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
                        self.virus.name, self.pop_size, self.vacc_percentage,
                        self.initial_infected)
        self.logger = Logger(self.file_name)
        self.newly_infected = []
        self.population = self._create_population()
        self.logger.write_metadata(self.pop_size, self.vacc_percentage,
                                   self.virus.name, self.virus.mortality_rate,
                                   self.virus.repro_rate)

    def get_infected(self):
        '''Helper function that returns a list of alive infected people'''
        alive_infected = list()
        for person in self.population:
            if person.infection and person.is_alive:
                alive_infected.append(person)
        return alive_infected

    def get_alive(self, id=-1):
        '''Helper function that returns a list of alive people'''
        alive = list()
        for person in self.population:
            if person.is_alive and not person._id == id:
                alive.append(person)
        return alive

    def random_infected(self, total):
        """Return a list of indices of people to vaccinate."""
        random_infected = [
            total.pop(random.randint(0, len(total)-1)
                      ) for i in range(self.initial_infected)
        ]
        return random_infected

    def _create_population(self):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the
                simulation will begin with.

            Returns:
                population: A list of Person objects.

        '''
        population = list()
        number_vaccinated = round(self.vacc_percentage * self.pop_size)
        total = random.sample(range(self.pop_size), number_vaccinated +
                              self.initial_infected)
        indices_infected = self.random_infected(total)
        indices_vaccinated = total
        self.total_infected += self.initial_infected
        for index in range(self.pop_size):
            if index in indices_vaccinated and index not in indices_infected:
                population.insert(index, Person(index, True))
            elif index not in indices_vaccinated and index in indices_infected:
                population.insert(index, Person(index, False, self.virus))
            else:
                population.insert(index, Person(index, False))
        return population

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: False for simulation should continue, True otherwise.
        '''
        # find the number of people who are both alive and vaccinated
        alive_vacc = 0
        for person in self.population:
            if person.is_alive and person.is_vaccinated:
                alive_vacc += 1
        # make decision
        return (self.total_dead + alive_vacc + self.get_neither() >=
                self.pop_size)

    def get_alive_num(self):
        """Return the number of alive people in the population."""
        alive_num = 0
        for person in self.population:
            if person.is_alive:
                alive_num += 1
        return alive_num

    def get_neither(self):
        """Return the number of alive people who are neither vaccinated nor
           infected."""
        neither = 0
        alive = self.get_alive()
        for person in alive:
            if not person.infection and not person.is_vaccinated:
                neither += 1
        return neither

    def get_dead(self):
        """Return number of dead people."""
        dead = 0
        for person in self.population:
            if not person.is_alive:
                dead += 1
        return dead

    def run(self, visualizer):
        ''' This method should run the simulation until all requirements for
            ending the simulation are met.
            Param: visualizer is Visualizer object
        '''
        time_step_counter = 1
        simulation_should_continue = 0
        should_continue = None

        assert self.population[0]._id == 0
        print(f"Time step 0, Total infected: {self.total_infected}, " +
              f"current infected: {self.current_infected()}, " +
              f"vaccinated percentage: {self.vacc_percentage}, " +
              f"dead: {self.total_dead}")

        while True:
            self.time_step(time_step_counter)
            # create a list of alive persons
            alive = self.get_alive()
            # create a list of vaccinated persons
            vaccinated = []
            for person in self.population:
                if person in alive and person.is_vaccinated:
                    vaccinated.append(person)
            # create a list of uninfected persons
            uninfected = []
            for person in alive:
                if person not in vaccinated and person.infection:
                    uninfected.append(person)
            print(f"Time step: {time_step_counter}, " +
                  f"total infected: {self.total_infected}, " +
                  f"current infected: {self.current_infected()} vaccinated %: "
                  + f"{self.vacc_percentage}, dead: {self.total_dead},  " +
                  f"total vaccinated: {len(vaccinated)}, " +
                  f"alive: {len(alive)}, uninfected: {len(uninfected)} " +
                  f"uninteracted {self.get_neither()}")
            visualizer.bar_graph(time_step_counter,
                                 self.vacc_percentage * self.get_alive_num(),
                                 self.current_infected(),
                                 self.get_dead(),
                                 self.get_neither())
            if self._simulation_should_continue():
                simulation_should_continue += 1
                break

            time_step_counter += 1
        print(f'The simulation has ended after {time_step_counter} turns.',)

    def time_step(self, time_step_counter):
        ''' This method should contain all the logic for computing
            one time step in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected
                person in the population
            2. If the person is dead, grab another random person from
                the population.
                Since we don't interact with dead people, this does not count
                as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        dead_this_step = 0
        for person in self.population:
            if person.infection and person.is_alive:
                sampling = random.sample(self.get_alive(person._id), 100)
                interaction_sample = sampling
                for random_person in interaction_sample:
                    self.interaction(person, random_person)
                did_survive = person.did_survive_infection()
                self.logger.log_infection_survival(person, did_survive)
                if not did_survive:
                    dead_this_step += 1
                    self.total_dead += 1
                # self.current_infected -= 1
        infected_this_step = self._infect_newly_infected()
        self.logger.log_time_step(time_step_counter, infected_this_step,
                                  dead_this_step, self.total_infected,
                                  self.total_dead)

    def current_infected(self):
        inf = 0
        for person in self.population:
            if person.infection and person.is_alive:
                inf += 1
        return inf

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected
            for an interaction. It assumes that only living people are passed
            in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''

        assert person.is_alive is True
        assert random_person.is_alive is True

        if random_person.is_vaccinated:
            self.logger.log_interaction(person, random_person,
                                        random_person_vacc=True)
        elif random_person.infection:
            self.logger.log_interaction(person, random_person,
                                        random_person_sick=True)
        elif (random_person.infection is None and
              not random_person.is_vaccinated):
            num = random.random()
            if num < self.virus.repro_rate:
                random_person.infection = self.virus
                self.newly_infected.append(random_person._id)
                self.total_infected += 1
                # self.current_infected += 1
                self.logger.log_interaction(person, random_person,
                                            did_infect=True)

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in
            self.newly_infected
            and update each Person object with the disease. '''

        infected_this_time = 0
        for people in self.newly_infected:
            self.population[people].infection = self.virus
            infected_this_time += 1
        self.newly_infected = []
        return infected_this_time


if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    repro_rate = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage,  virus, initial_infected)
    graph = visualizer.Visualizer("Number of Survivors",
                                  ("Herd Immunity Defense Against Disease " +
                                   "Spread"))

    sim.run(graph)
