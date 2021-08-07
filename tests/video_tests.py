import unittest
from javscraper import *


class VideoTests(unittest.TestCase):
    def test_javlibrary(self):
        base = JAVLibrary()

        result = base.get_video("abcdefghijklm")
        self.assertIsNone(result)

        result = base.get_video("SDAB-187")
        self.assertIsNotNone(result)
        self.assertEqual(result.code, "SDAB-187")
        self.assertEqual(result.studio, "SOD Create")
        self.assertTrue(len(result.actresses), 1)
        self.assertEqual(result.actresses[0], "Kamon Non")
        self.assertIsNone(result.sample_video)
        self.assertTrue(result.image.startswith("http"))

    def test_mgstage(self):
        base = MGStage()

        result = base.get_video("345SIMM_600")
        self.assertIsNone(result)

        result = base.get_video("345SIMM-600")
        self.assertIsNotNone(result)
        self.assertEqual(result.code, "345SIMM-600")
        self.assertEqual(result.studio, "しろうとまんまん")
        self.assertTrue(result.image.startswith("http"))
        self.assertTrue(len(result.actresses), 1)
        self.assertEqual(result.actresses[0], "りなちゃん")
        self.assertIsNotNone(result.sample_video)
        self.assertIsNotNone(result.description)
        self.assertTrue(result.sample_video.startswith("http"))

    def test_r18(self):
        base = R18()

        result = base.get_video("MIDE_805")
        self.assertIsNone(result)

        result = base.get_video("MIDE-805")
        self.assertIsNotNone(result)
        self.assertEqual(result.code, "MIDE-805")
        self.assertEqual(result.studio, "MOODYZ")
        self.assertTrue(result.image.startswith("https"))
        self.assertTrue(len(result.actresses), 1)
        self.assertEqual(result.actresses[0], "Shoko Takahashi")
        self.assertIsNotNone(result.sample_video)
        self.assertIsNotNone(result.description)
        self.assertTrue(result.sample_video.startswith("http"))

    def test_s1(self):
        base = S1()

        result = base.get_video("SSIS_140")
        self.assertIsNone(result)

        result = base.get_video("SSIS-140")
        self.assertIsNotNone(result)
        self.assertEqual(result.code, "SSIS140")
        self.assertTrue(result.image.startswith("https"))
        self.assertTrue(len(result.actresses), 1)
        self.assertEqual(result.actresses[0], "藤田こずえ")
        self.assertIsNotNone(result.sample_video)
        self.assertIsNotNone(result.description)
        self.assertTrue(result.sample_video.startswith("http"))

    def test_sod(self):
        base = SOD()

        result = base.get_video("OKS_116")
        self.assertIsNone(result)

        result = base.get_video("OKS-116")
        self.assertIsNotNone(result)
        self.assertEqual(result.code, "OKS-116")
        self.assertEqual(result.studio, "親父の個撮")
        self.assertTrue(result.image.startswith("https"))
        self.assertTrue(len(result.actresses), 1)
        self.assertEqual(result.actresses[0], "宮崎リン")
        self.assertIsNotNone(result.description)
        self.assertIsNone(result.sample_video)


if __name__ == '__main__':
    unittest.main()
