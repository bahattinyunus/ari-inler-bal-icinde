import unittest
from ari_inler_bal_icinde.corpus import KanonikKutuphane, KARSILASTIRMA_MATRISI

class TestCorpus(unittest.TestCase):
    def setUp(self):
        self.kutuphane = KanonikKutuphane()

    def test_metin_sayisi(self):
        metinler = self.kutuphane.tum_metinler()
        self.assertGreaterEqual(len(metinler), 25)

    def test_id_ile_getir(self):
        pir = self.kutuphane.id_ile_getir("pir-sultan-abdal")
        self.assertIsNotNone(pir)
        self.assertEqual(pir.muellif, "Pir Sultan Abdal")
        self.assertIn("Kuduretten verdi balı", pir.orijinal_metin)

    def test_muellife_gore_ara(self):
        yunus = self.kutuphane.muellife_gore_ara("Yunus")
        self.assertGreaterEqual(len(yunus), 2)
        self.assertEqual(yunus[0].muellif, "Yunus Emre")

    def test_temaya_gore_ara(self):
        fena_metinleri = self.kutuphane.temaya_gore_ara("fena")
        self.assertGreaterEqual(len(fena_metinleri), 5)

    def test_gelenege_gore_ara(self):
        anadolu = self.kutuphane.gelenege_gore_ara("Anadolu İrfanı")
        self.assertGreaterEqual(len(anadolu), 8)

        felsefe = self.kutuphane.gelenege_gore_ara("Evrensel Mistisizm")
        self.assertGreaterEqual(len(felsefe), 4)

    def test_motife_gore_ara(self):
        ari_bal = self.kutuphane.motife_gore_ara("ari-ve-bal")
        self.assertGreaterEqual(len(ari_bal), 5)

        tuz_deniz = self.kutuphane.motife_gore_ara("tuz-ve-deniz")
        self.assertGreaterEqual(len(tuz_deniz), 2)

    def test_tum_gelenekler_ve_motifler(self):
        gelenekler = self.kutuphane.tum_gelenekler()
        self.assertIn("Anadolu İrfanı", gelenekler)
        self.assertIn("Evrensel Mistisizm & Felsefe", gelenekler)

        motifler = self.kutuphane.tum_motifler()
        self.assertIn("ari-ve-bal", motifler)
        self.assertIn("damla-ve-umman", motifler)
        self.assertIn("tuz-ve-deniz", motifler)

    def test_rastgele_getir(self):
        m1 = self.kutuphane.rastgele_getir(tohum=42)
        m2 = self.kutuphane.rastgele_getir(tohum=42)
        self.assertEqual(m1.id, m2.id)

    def test_karsilastir(self):
        analiz = self.kutuphane.karsilastir("pir-sultan-abdal", "ramakrishna-tuz-bebek")
        self.assertIn("metin_1", analiz)
        self.assertIn("metin_2", analiz)
        self.assertIn("sentez", analiz)
        self.assertEqual(analiz["metin_1"]["muellif"], "Pir Sultan Abdal")
        self.assertEqual(analiz["metin_2"]["muellif"], "Sri Ramakrishna Paramahamsa")

    def test_karsilastir_hata(self):
        with self.assertRaises(ValueError):
            self.kutuphane.karsilastir("gecersiz-id", "pir-sultan-abdal")

    def test_antoloji_raporu(self):
        rapor = self.kutuphane.antoloji_raporu()
        self.assertGreaterEqual(rapor["toplam_eser_sayisi"], 25)
        self.assertIn("gelenek_dagilimi", rapor)
        self.assertIn("motif_dagilimi", rapor)

    def test_serbest_arama(self):
        sonuclar = self.kutuphane.serbest_arama("Spinoza")
        self.assertGreaterEqual(len(sonuclar), 1)
        self.assertEqual(sonuclar[0].muellif, "Baruch Spinoza")

    def test_matris_getir(self):
        matris = self.kutuphane.matris_getir()
        self.assertEqual(len(matris), len(KARSILASTIRMA_MATRISI))

if __name__ == "__main__":
    unittest.main()
