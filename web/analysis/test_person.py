from .virus import Virus
from .person import Person
import unittest


''' These are simple tests to ensure that
    you are instantiating your Person class correctly.
'''


class TestPerson:
    def test_vacc_person_instantiation(self):
        # create some people to test if our init method works as expected
        person = Person(1, True)
        assert person._id == 1
        assert person.is_alive is True
        assert person.is_vaccinated is True
        assert person.infection is None

    def test_not_vacc_person_instantiation(self):
        person = Person(2, False)
        # test the values at each attribute
        assert person._id == 2
        assert person.is_alive is True
        assert person.is_vaccinated is False
        assert person.infection is None

    def test_sick_person_instantiation(self):
        # Create a Virus object to give a Person object an infection
        virus = Virus("Ebola", 0.7, 0.23)
        # Create a Person object and give them the virus infection
        person = Person(3, False, virus)
        # test the values at each attribute
        assert person._id == 3
        assert person.is_vaccinated is False
        assert person.is_alive is True
        assert person.infection is virus

    def test_did_survive_infection(self):
        # Create a Virus object to give a Person object an infection
        virus = Virus("Smallpox", 0.17, 0.59)
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
            # test the values of each attribute for a Person who died
            assert person_sam._id == 4
            assert person_sam.is_vaccinated is False
            assert person_sam.infection is virus


if __name__ == '__main__':
    unittest.main()
