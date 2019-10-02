import unittest
import logger


class TestLogger(unittest.TestCase):
    def test__init__(self):
        """Check to make sure Logger object instantiation works properly."""
        log_file = logger.Logger("my_file.txt")

        assert log_file.file_name == "my_file.txt"

    def test_write_metadata(self):
        pass

    def test_log_interaction(self):
        pass

    def test_log_infection_survival(self):
        pass

    def test_log_time_step(self):
        pass
