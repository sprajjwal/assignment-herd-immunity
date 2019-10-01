import unittest


class Virus(object):
    '''Properties and attributes of the virus used in Simulation.'''

    def __init__(self, name, repro_rate, mortality_rate):
        err_msg = "Rates are too high!"
        assert repro_rate <= 1 or mortality_rate <= 1, err_msg

        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate


class TestVirus(unittest.TestCase):
    def test_virus_instantiation(self):
        # TODO: Create your own test that models the virus you are working with
        '''Check to make sure that the virus instantiator is working.'''
        virus = Virus("HIV", 0.8, 0.3)
        another_virus = Virus("Polio", 0.2, 0.6)
        third_virus = Virus("Tubercolosis", 0.65, 0.55)

        # assert statements
        assert virus.name == "HIV"
        assert virus.repro_rate == 0.8
        assert virus.mortality_rate == 0.3
        assert another_virus.name == "Polio"
        assert third_virus.name == "Tubercolosis"
        assert another_virus.repro_rate == 0.2
        assert third_virus.mortality_rate == 0.55

    def test_insufficient_args(self):
        '''
        Credit to
        https://stackoverflow.com/questions/88325/how-do-i-unit-test-an-init-method-of-a-python-class-with-assertraises
        for inspiring this test.
        '''
        name = "HIV"
        repro_rate = 1.2
        mortality_rate = 2.9
        self.assertRaises(AssertionError,
                          Virus, name, repro_rate, mortality_rate)


if __name__ == '__main__':
    unittest.main()
    test_virus_instantiation()
