import unittest
from javscraper import *


class SearchTests(unittest.TestCase):
    def test_javlibrary(self):
        base = JAVLibrary()

        result = base.search("SDAB-187")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javme5zn6e" in result[0])

        result = base.search("SSIS-001")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javmezzbqu" in result[0])

    def test_mgstage(self):
        base = MGStage()

        result = base.search("345SIMM-600")
        self.assertTrue(len(result) > 0)
        self.assertTrue("345SIMM-600" in result[0])

    def test_r18(self):
        base = R18()

        result = base.search("MIDE-805")
        self.assertTrue(len(result) > 0)
        self.assertTrue("mide00805" in result[0])

    def test_sod(self):
        base = SOD()

        result = base.search("OKS-116")
        print(result)
        self.assertTrue(len(result) > 0)
        self.assertTrue("OKS-116" in result[0])


if __name__ == '__main__':
    unittest.main()
