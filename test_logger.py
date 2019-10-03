import unittest
from logger import *
from person import *
import os


class TestLogger(unittest.TestCase):
    def test__init__(self):
        """Check to make sure Logger object instantiation works properly."""
        log_file = Logger('file.txt')
        assert log_file.file_name == 'file.txt'

    def test_write_metadata(self):
        file_name = 'file.txt'
        assert os.path.isfile(file_name) == False
        log_file = Logger(file_name)
        log_file.write_metadata(100, 0.5, 'HIV', 0.4, 0.8)
        f = open(file_name, 'r')
        assert os.path.isfile(file_name) 
        line = f.readline()
        f.close()
        os.remove(file_name)
        test = "Population size: 100\tVaccination percentage: 0.5\tVirus name: HIV\tMortality rate: 0.4\tBasic reproduction number: 0.8\n"
        assert line == test

    def test_log_interaction(self):
        file_name = 'test_log_interaction.txt'
        open(file_name, 'a').close()
        # setup
        infector = Person(0, False)
        person1 = Person(1, False) 
        person2 = Person(2, False)
        person3 = Person(3, True)
        log_file = Logger(file_name)

        f = open(file_name, 'r')
        log_file.log_interaction(infector, person1, False, False, True)
        log_file.log_interaction(infector, person2, False, True, False)
        log_file.log_interaction(infector, person3, True, False, False)

        lines = f.readlines()
        f.close()
        os.remove(file_name)

        # tests
        assert lines[0] == "0 infects 1\n"
        assert lines[1] == "0 didn't infect 2 because they are already vaccinated\n"
        assert lines[2] == "0 didn't infect 3 because they are already sick\n"

    # def test_log_infection_survival(self):
    #     pass

    # def test_log_time_step(self):
    #     pass

if __name__ == '__main__':
    unittest.main()
    test_virus_instantiation()
