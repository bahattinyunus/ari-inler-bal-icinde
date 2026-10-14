import unittest
from ari_inler_bal_icinde.physics import (
    FenaDinamigi,
    ALTIN_ORAN,
    NEY_TEMEL_FREKANSI,
    KESRET_VIZILTI_FREKANSI,
)

class TestPhysics(unittest.TestCase):
    def setUp(self):
        self.fizik = FenaDinamigi(viskozite=1.618, cozulme_hizi=0.28)

    def test_benlik_decay(self):
        b0 = self.fizik.benlik_hesapla(t=0.0, terk_sayisi=0)
        self.assertAlmostEqual(b0, 1.0, places=4)

        b1 = self.fizik.benlik_hesapla(t=2.0, terk_sayisi=1)
        self.assertLess(b1, b0)

        b_son = self.fizik.benlik_hesapla(t=20.0, terk_sayisi=4)
        self.assertEqual(b_son, 0.0)

    def test_viskozite_direnci_bounds(self):
        d_full = self.fizik.viskozite_direnci_hesapla(1.0)
        self.assertAlmostEqual(d_full, 1.0, places=4)

        d_zero = self.fizik.viskozite_direnci_hesapla(0.0)
        self.assertAlmostEqual(d_zero, 0.0, places=4)

        d_mid = self.fizik.viskozite_direnci_hesapla(0.5)
        self.assertGreater(d_mid, 0.0)
        self.assertLess(d_mid, 1.0)

    def test_hayret_katsayisi_monotonic(self):
        h0 = self.fizik.hayret_katsayisi_hesapla(benlik_orani=1.0, t=0.5)
        h_fena = self.fizik.hayret_katsayisi_hesapla(benlik_orani=0.05, t=3.0)
        self.assertGreater(h_fena, h0)

    def test_akustik_modulasyon(self):
        # Kesret hâli
        f_kesret, harm_kesret, char_kesret = self.fizik.akustik_zar_modulasyonu(1.0, 0.0)
        self.assertAlmostEqual(f_kesret, KESRET_VIZILTI_FREKANSI, delta=5.0)
        self.assertIn("Kesret", char_kesret)

        # Fenâ hâli
        f_fena, harm_fena, char_fena = self.fizik.akustik_zar_modulasyonu(0.0, 5.0)
        self.assertAlmostEqual(f_fena, NEY_TEMEL_FREKANSI, delta=5.0)
        self.assertIn("Vahdet", char_fena)

        # Altın oran harmonikleri kontrolü
        self.assertEqual(len(harm_fena), 5)
        self.assertAlmostEqual(harm_fena[1], f_fena * ALTIN_ORAN, delta=2.0)

    def test_anlik_adim_hesapla(self):
        adim = self.fizik.anlik_adim_hesapla(t=1.5, terk_sayisi=2)
        self.assertIn("benlik_orani", adim)
        self.assertIn("viskozite_direnci", adim)
        self.assertIn("hayret_katsayisi", adim)
        self.assertIn("frekans", adim)

if __name__ == "__main__":
    unittest.main()
