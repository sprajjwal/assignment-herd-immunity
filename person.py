from virus import Virus
import random
random.seed(42)


class Person(object):
    ''' Person objects will populate the simulation. '''

    def __init__(self, _id, is_vaccinated, infection=None):
        '''
        We start out with is_alive = True,
        because we don't make vampires or zombies.
        All other values will be set by the simulation
        when it makes each Person object.

        If person is chosen to be infected when the population is created,
        the simulation
        should instantiate a Virus object and set it as the value
        self.infection. Otherwise, self.infection should be set to None.
        '''
        self._id = _id  # int
        self.is_alive = True  # boolean
        self.is_vaccinated = is_vaccinated  # boolean
        self.infection = infection  # Virus object or None

    def did_survive_infection(self):
        '''
        Generate a random number and compare to virus's mortality_rate.
        If random number is smaller, person dies from the disease.
        If Person survives, they become vaccinated and they have no infection.
        Return a boolean value indicating whether they survived the infection.
        '''
        immunity_strength = random.uniform(0, 1)

        if immunity_strength < self.infection.mortality_rate:
            self.is_alive = False
        else:
            self.is_vaccinated = True
            self.infection = None
        return self.is_alive
        # Only called if infection attribute is not None.


''' These are simple tests to ensure that
    you are instantiating your Person class correctly.
'''


def test_vacc_person_instantiation():
    # create some people to test if our init method works as expected
    person = Person(1, True)
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False)
    # test the values at each attribute
    assert person._id == 2
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection is None


def test_sick_person_instantiation():
    # Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
    # Create a Person object and give them the virus infection
    person = Person(3, False, virus)
    # test the values at each attribute
    assert person._id == 3
    assert person.is_vaccinated is False
    assert person.is_alive is True
    assert person.infection is virus


def test_did_survive_infection():
    # Create a Virus object to give a Person object an infection
    virus = Virus("Smallpox", 0.6, 0.17)
    # Create a Person object and give them the virus infection
    person_sam = Person(4, False, virus)

    # Resolve whether the Person survives the infection or not
    survived = person_sam.did_survive_infection()
    # Check if the Person survived or not
    if survived:
        assert person_sam.is_alive is True
        # test the values of each attribute for a Person who survived
        assert person_sam._id == 4
        assert person_sam.is_vaccinated is True
        assert person_sam.infection is None
    else:
        assert person_sam.is_alive is False
        # test the values of each attribute for a Person who did not survive
        assert person_sam._id == 4
        assert person_sam.is_vaccinated is False
        assert person_sam.infection is virus
