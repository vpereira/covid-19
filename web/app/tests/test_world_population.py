import os
import unittest

from covid19.expogo.dataset import WorldPopulation


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.world_population = WorldPopulation(
            'datasets/world_population.csv')

    def test_population_by_country(self):
        self.assertEqual(
            self.world_population.population_by_country('Angola'), 30809762)
