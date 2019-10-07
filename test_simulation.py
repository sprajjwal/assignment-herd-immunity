import unittest
import random
import sys
from person import Person
from logger import Logger
from virus import Virus
from simulation import *

random.seed(42)


class TestSimulation(unittest.TestCase):
    def test__init__(self):
        """Test values passed into Simulation instance properties at
           instantiation."""
        # test virus
        virus = Virus("HIV", 0.8, 0.3)
        # test instances with and without args for initial infected
        sim_no_arg = Simulation(1000, 0.05, virus)
        sim_yes_arg = Simulation(1000, 0.05, virus, 10)

        assert sim_no_arg.pop_size == sim_yes_arg.pop_size == 1000
        assert sim_no_arg.vacc_percentage == sim_yes_arg.vacc_percentage == .05
        assert sim_no_arg.initial_infected == 1
        assert sim_yes_arg.initial_infected == 10
        assert sim_no_arg.virus == sim_yes_arg.virus == virus
        # self.population cannot be tested, because assigned using random
        assert sim_no_arg.file_name == ("HIV_simulation_pop_1000_vp_0.05_" +
                                        "infected_1.txt")
        assert sim_yes_arg.file_name == ("HIV_simulation_pop_1000_vp_0.05_" +
                                         "infected_10.txt")
        test_file_no_arg = open(sim_no_arg.file_name, "r")
        assert test_file_no_arg.read() == ("Population size: 1000" +
                                           "\tVaccination percentage: 0.05	" +
                                           "Virus name: HIV	Mortality rate: " +
                                           "0.3	Basic reproduction " +
                                           "number: 0.8\n")
        test_file_no_arg.close()

    def test_get_infected(self):
        """Test list returned by get_infected to ensure it only contains
           people who are both alive and infected."""
        virus = Virus("HIV", 0.8, 0.3)
        sim = Simulation(1000, 0.05, virus)
        alive_infected = sim.get_infected()  # stores value returned by method

        num_alive_infected = 0
        for person in alive_infected:
            if person.infection and person.is_alive:
                num_alive_infected += 1
        assert num_alive_infected == len(alive_infected)

    def test_get_alive(self):
        """Test output of get_alive to ensure only contains alive people."""
        virus = Virus("HIV", 0.8, 0.3)
        sim = Simulation(1000, 0.05, virus)
        alive = sim.get_alive()

        num_alive = 0
        for person in alive:
            if person.is_alive:
                num_alive += 1
        assert num_alive == len(alive)

    def test_random_infected(self):
        """Test output of random_infected to ensure all elements in
           list are integer values."""
        virus = Virus("HIV", 0.8, 0.3)
        sim = Simulation(1000, 0.05, virus)
        number_vaccinated = round(sim.vacc_percentage * sim.pop_size)
        total = random.sample(range(sim.pop_size), number_vaccinated +
                              sim.initial_infected)
        random_infected = sim.random_infected(total)

        num_infected = 0
        for index in random_infected:
            if type(index) is int:
                num_infected += 1
        assert num_infected == len(random_infected)

    def test_create_population(self):
        """Test to be sure:
          1. the appropiate amount of people in population are vaccinated,
          2. infected,
          3. the rest are neither,
          4. and all are alive,
          5. and the population is the right size.
        """
        virus = Virus("HIV", 0.8, 0.3)
        sim = Simulation(1000, 0.05, virus)

        sim_population = sim.population
        # bools to store that each condition is being met
        pop_size_condition = False
        alive_size = False
        vacc_size = False
        infect_size = False
        neither = False
        # decisions that can change bools to True
        if len(sim_population) == sim.pop_size:
            pop_size_condition = True

        alive_list = sim.get_alive()
        if len(alive_list) == len(sim_population):
            alive_size = True

        vacc_num = 0
        for person in sim_population:
            if person.is_vaccinated:
                vacc_num += 1
        if vacc_num == sim.vacc_percentage * len(sim_population):
            vacc_size = True

        infected_num = 0
        for person in sim_population:
            if person.infection:
                infected_num += 1
        if len(sim.get_infected()) == infected_num:
            infect_size = True

        neither_count = 0
        for person in sim_population:
            if not person.infection and not person.is_vaccinated:
                neither_count += 1
        if neither_count == (len(sim_population) - infected_num - vacc_num):
            neither = True

        # asserting that bools came out True
        assert pop_size_condition is True
        assert alive_size is True
        assert vacc_size is True
        assert infect_size is True
        assert neither is True

    def test_simulation_should_continue(self):
        """Test decision returned by _simulation_should_continue."""
        # Test scenarios that should cause simulation to continue
        # Scenario 1: just after 1 time step with HIV virus
        virus = Virus("HIV", 0.8, 0.3)
        sim = Simulation(200, 0.05, virus)
        sim.run()
        assert sim.run()[0] == sim.run()[1]

        # Test scenarios that should cause simulation to end
        # Scenario 1: kill everyone
        for person in sim.population:
            person.is_alive = False
            sim.total_dead += 1
            person.is_vaccinated = False
        assert sim._simulation_should_continue() is True

        # Scenario 2: vaccinate everyone
        for person in sim.population:
            person.is_alive = True
            person.infection = None
            person.is_vaccinated = True
        sim.total_dead = 0
        assert sim._simulation_should_continue() is True


if __name__ == "__main__":
    unittest.main()
