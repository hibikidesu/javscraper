import unittest
from javscraper import *


class SearchTests(unittest.TestCase):
    def test_javlibrary_en(self):
        base = JAVLibrary()

        result = base.search("SDAB-187")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javme5zn6e" in result[0])
        self.assertTrue(result[0].startswith("http"))

        result = base.search("SSIS-001")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javmezzbqu" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_javlibrary_ja(self):
        base = JAVLibrary("ja")

        result = base.search("SDAB-187")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javme5zn6e" in result[0])
        self.assertTrue(result[0].startswith("http"))

        result = base.search("SSIS-001")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javmezzbqu" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_javlibrary_tw(self):
        base = JAVLibrary("tw")

        result = base.search("SDAB-187")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javme5zn6e" in result[0])
        self.assertTrue(result[0].startswith("http"))

        result = base.search("SSIS-001")
        self.assertTrue(len(result) > 0)
        self.assertTrue("javmezzbqu" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_javlibrary_cn(self):
        base = JAVLibrary("cn")

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

        result = base.search("345SIMM")
        self.assertTrue(len(result) > 5)

    def test_r18(self):
        base = R18()

        result = base.search("MIDE-805")
        self.assertTrue(len(result) > 0)
        self.assertTrue("mide00805" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_sod(self):
        base = SOD()

        result = base.search("zzzzzzzz")
        self.assertEqual(result, [])

        result = base.search("OKS-116")
        self.assertTrue(len(result) > 0)
        self.assertTrue("OKS-116" in result[0])
        self.assertTrue(result[0].startswith("http"))

    # def test_10musume(self):
    #     base = TenMusume()
    #
    #     result = base.search("maid")
    #     self.assertTrue(len(result) > 0)
    #     self.assertTrue(result[0].startswith("http"))

    def test_ideapocket(self):
        base = IdeaPocket()

        result = base.search("zzzzz")
        self.assertEqual(result, [])

        result = base.search("IPX-445")
        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0].startswith("http"))

    def test_caribbeancom_ja(self):
        base = Caribbeancom()

        result = base.search("aaaaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("溺れた白ビキニちゃんを助けたお礼に中出し恩返し")
        self.assertTrue(len(result) == 1)
        self.assertTrue("080621-001" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_caribbeancom_en(self):
        base = Caribbeancom("en")

        result = base.search("aaaaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("White bikini woman did creampie gratitude for saved life from drown")
        self.assertTrue(len(result) > 0)
        self.assertTrue("080621-001" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_caribbeancom_cn(self):
        base = Caribbeancom("cn")

        result = base.search("aaaaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("White bikini woman did creampie gratitude for saved life from drown")
        self.assertTrue(len(result) > 0)
        self.assertTrue("080621-001" in result[0])
        self.assertTrue(result[0].startswith("http"))

    def test_s1(self):
        base = S1()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("sex")
        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0].startswith("http"))

    def test_kmproduce(self):
        base = KMProduce()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("bazx-304")
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("works/bazx-304" in result[0])

    def test_max_a(self):
        base = MaxA()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("xvsr-604")
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("c71b1ae644015b8651a9edac601b2768" in result[0])

    def test_air_control(self):
        base = AirControl()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("ome-401")
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("/detail/ome401/" in result[0])

    def test_alicejapan(self):
        base = AliceJapan()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("DVAJ-528")
        self.assertTrue(len(result) == 2)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("d82ab7c815ac7ad271a23fa4182797eb" in result[0])

    def test_aroma(self):
        base = Aroma()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("sex")
        self.assertTrue(len(result) == 16)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("arm863" in result[0])

    def test_attackers(self):
        base = Attackers()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("ADN-330")
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("adn330" in result[0])

    def test_auroraproject(self):
        base = AuroraProject()

        result = base.search("APKH-185")
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("APKH-185" in result[0])

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

    def test_befree(self):
        base = BeFree()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("BF-640")
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("bf640" in result[0])

    def test_bi(self):
        base = Bi()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("CJOD-307")
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("cjod307" in result[0])

    def test_bigmorkal(self):
        base = BigMorkal()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("BDSR-459")
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("bdsr-459" in result[0])

    def test_deeps(self):
        base = Deeps()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("DVDMS-699")
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0].startswith("http"))
        self.assertTrue("dvdms-699" in result[0])

    def test_dmm(self):
        base = DMM()

        result = base.search("aaaaaaaaa")
        self.assertEqual(result, [])

        result = base.search("JUFE-202")
        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0].startswith("http"))


if __name__ == '__main__':
    unittest.main()
