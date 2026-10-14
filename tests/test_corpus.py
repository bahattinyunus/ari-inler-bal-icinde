import unittest
from ari_inler_bal_icinde.corpus import KanonikKutuphane, KARSILASTIRMA_MATRISI

class TestCorpus(unittest.TestCase):
    def setUp(self):
        self.kutuphane = KanonikKutuphane()

    def test_metin_sayisi(self):
        metinler = self.kutuphane.tum_metinler()
        self.assertGreaterEqual(len(metinler), 8)

    def test_id_ile_getir(self):
        pir = self.kutuphane.id_ile_getir("pir-sultan-abdal")
        self.assertIsNotNone(pir)
        self.assertEqual(pir.muellif, "Pir Sultan Abdal")
        self.assertIn("Kudretten verdi balı", pir.orijinal_metin)

    def test_muellife_gore_ara(self):
        yunus = self.kutuphane.muellife_gore_ara("Yunus")
        self.assertGreaterEqual(len(yunus), 1)
        self.assertEqual(yunus[0].muellif, "Yunus Emre")

    def test_temaya_gore_ara(self):
        fena_metinleri = self.kutuphane.temaya_gore_ara("fena")
        self.assertGreaterEqual(len(fena_metinleri), 2)

    def test_serbest_arama(self):
        sonuclar = self.kutuphane.serbest_arama("Simurg")
        self.assertGreaterEqual(len(sonuclar), 1)
        self.assertEqual(sonuclar[0].muellif, "Ferîdüddîn Attâr")

    def test_matris_getir(self):
        matris = self.kutuphane.matris_getir()
        self.assertEqual(len(matris), len(KARSILASTIRMA_MATRISI))
        for item in matris:
            self.assertIn("parametre", item)
            self.assertIn("zahir", item)
            self.assertIn("batin", item)
            self.assertIn("temel", item)

if __name__ == "__main__":
    unittest.main()
