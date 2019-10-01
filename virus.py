class Virus(object):
    '''Properties and attributes of the virus used in Simulation.'''

    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate


def test_virus_instantiation():
    # TODO: Create your own test that models the virus you are working with
    '''Check to make sure that the virus instantiator is working.'''
    virus = Virus("HIV", 0.8, 0.3)

    # another test Virus instance
    another_virus = Virus("Smallpox", 0.95, 0.25)

    # assert statements
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3

    assert another_virus.name == "Smallpox"
    assert another_virus.repro_rate == 0.95
    assert another_virus.mortality_rate == 0.25
