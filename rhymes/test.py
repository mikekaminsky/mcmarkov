import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest

from rhymes import approx_nsyl
from rhymes import nsyl
from rhymes import rhymesyls
