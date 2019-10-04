import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus

class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: 
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.population = [] # Dictionary of Person objects
        self.pop_size = pop_size # Int
        self.next_person_id = pop_size # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = self.initial_infected # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            self.virus.name, self.pop_size, self.vacc_percentage, self.initial_infected)
        self.logger = Logger(self.file_name)
        self.newly_infected = []
        self.population = self._create_population(initial_infected)
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        population = []
        number_vaccinated = round(self.vacc_percentage * self.pop_size)
        total = random.sample(range(self.pop_size), number_vaccinated + self.initial_infected)
        indices_infected = [total.pop(random.randint(0, len(total)-1)) for _ in range(self.initial_infected)]
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
        return self.current_infected > 0

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 1
        should_continue = None

        assert self.population[0]._id == 0
        while self._simulation_should_continue():
            vaccinated = [person for person in self.population if person.is_vaccinated and person.is_alive ]
            uninfected = [person for person in self.population if not person.is_vaccinated and person.is_alive and not person.infection]
            # print(f"infected: {self.total_infected}, current infected: {self.current_infected} vaccinated %: {self.vacc_percentage}, dead: {self.total_dead},  total vaccinated: {len(vaccinated)}, uninfected: {len(uninfected)}")
            self.time_step(time_step_counter)
            time_step_counter += 1
        # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.
        print(f'The simulation has ended after {time_step_counter-1} turns.', )


    def kill_or_vaccinate(self):
        '''function that kills infected people based on Virus' mortality rate'''
        infected_ids = [person._id for person in self.population if person.infection and person.is_alive]
        total_vaccinated = 0
        alive = 0
        dead = 0
        for person in self.get_infected():
            num = random.random()
            if num < self.virus.mortality_rate: #kill
                self.population[person._id].is_alive = False
                self.total_dead += 1
                dead += 1
                self.current_infected -= 1
                self.logger.log_infection_survival(person, True)
            else:
                self.population[person._id].is_vaccinated = True
                self.population[person._id].infection = None
                self.current_infected -= 1
                self.logger.log_infection_survival(person, False)

        for person in self.population:
            if person.is_vaccinated and person.is_alive:
                total_vaccinated += 1
            if person.is_alive:
                alive+= 1

        self.vacc_percentage = total_vaccinated/alive
        return dead

    def get_infected(self):
        '''Helper function that returns a list of alive infected people'''
        return [person for person in self.population if person.infection and person.is_alive]
    
    def get_alive(self, id=-1):
        '''Helper function that returns a list of alive people'''
        return [person for person in self.population if person.is_alive and person._id != id]

    def time_step(self, time_step_counter):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        for person in self.get_infected():
            interaction_sample = random.sample(self.get_alive(person._id), 100)
            for random_person in interaction_sample:
                self.interaction(person, random_person)
        infected_this_step = self._infect_newly_infected()
        dead_this_step = self.kill_or_vaccinate()
        self.logger.log_time_step(time_step_counter, infected_this_step, dead_this_step, self.total_infected, self.total_dead) #more arguments?

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated:
            self.logger.log_interaction(person, random_person, random_person_vacc= True)
        elif random_person.infection:
            self.logger.log_interaction(person, random_person, random_person_sick=True)
        elif not random_person.infection and not random_person.is_vaccinated:
            num = random.random()
            if num < self.virus.repro_rate:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, did_infect= True)


        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''

        infected_this_time = 0
        print(f"infecting {len(self.newly_infected)}")
        for people in self.newly_infected:
            self.population[people].infection = self.virus
            self.current_infected += 1
            self.total_infected += 1
            infected_this_time += 1
        self.newly_infected = []
        return infected_this_time


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_rate = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage,  virus, initial_infected)

    sim.run()