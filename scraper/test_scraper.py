import sys
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest

from scraper import Scraper

class test_scraper(unittest.TestCase):

    def test_scraper(self):
        self.assertTrue(False)

