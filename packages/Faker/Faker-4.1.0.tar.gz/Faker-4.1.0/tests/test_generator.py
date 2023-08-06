import unittest

from unittest.mock import patch

from faker import Generator


class GeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.generator = Generator()

    @patch('random.getstate')
    def test_get_random(self, mock_system_random):
        random_instance = self.generator.random
        random_instance.getstate()
        assert not mock_system_random.called

    @patch('random.seed')
    def test_random_seed_doesnt_seed_system_random(self, mock_system_random):
        self.generator.seed(0)
        assert not mock_system_random.called
