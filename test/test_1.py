
import unittest

from helper.common import *

class TestScrape(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def testCheckKw(self):
        k1 = kw1.split(",")
        k1 = [x.strip() for x in k1]
        l1=len(k1)
        k2 = kw2.split(",")
        k2 = [x.strip() for x in k2]    
        l2=len(k2)
        print(f"l1={l1}, l2={l2}")
