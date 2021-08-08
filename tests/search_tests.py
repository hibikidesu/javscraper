import unittest
from javscraper import *


class SearchTests(unittest.TestCase):
    def test_javlibrary(self):
        base = JAVLibrary()

        result = base.search("SDAB-187")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javme5zn6e" in result[0])
        self.assertTrue(result[0].startswith("http"))

        result = base.search("SSIS-001")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javmezzbqu" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_mgstage(self):
        base = MGStage()

        result = base.search("345SIMM-600")
        self.assertTrue(len(result) > 0)
        self.assertTrue("345SIMM-600" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_r18(self):
        base = R18()

        result = base.search("MIDE-805")
        self.assertTrue(len(result) > 0)
        self.assertTrue("mide00805" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_sod(self):
        base = SOD()

        result = base.search("OKS-116")
        self.assertTrue(len(result) > 0)
        self.assertTrue("OKS-116" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_10musume(self):
        base = TenMusume()

        result = base.search("maid")
        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0].startswith("http"))

        base.close()

    def test_ideapocket(self):
        base = IdeaPocket()

        result = base.search("zzzzz")
        self.assertEqual(result, [])

        result = base.search("IPX-445")
        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0].startswith("http"))


if __name__ == '__main__':
    unittest.main()
