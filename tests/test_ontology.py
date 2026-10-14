import unittest
from ari_inler_bal_icinde.ontology import VarlikDeryasi, Ari, KudretVeBahaneMotoru
from ari_inler_bal_icinde.models import Makam, NefsMertebesi

class TestOntology(unittest.TestCase):
    def test_varlik_deryasi(self):
        derya = VarlikDeryasi(isim="Kudret Deryası", viskozite=2.0)
        self.assertEqual(derya.isim, "Kudret Deryası")
        self.assertEqual(derya.viskozite, 2.0)
        self.assertEqual(derya.sonsuz_lezzet, float("inf"))
        self.assertIn("Kudret Deryası", repr(derya))

    def test_ari_vuslata_er(self):
        derya = VarlikDeryasi()
        ari = Ari(ad="Salik Arı", cozulme_hizi=0.3)
        adimlar = list(ari.vuslata_er(derya))

        self.assertGreater(len(adimlar), 5)
        # İlk adım (t=0) kesret
        self.assertEqual(adimlar[0].adim_no, 0)
        self.assertEqual(adimlar[0].durum.benlik_orani, 1.0)
        self.assertEqual(adimlar[0].durum.makam, Makam.TALEP)

        # Son adım bekābillâh / fenâfillâh
        son_adim = adimlar[-1]
        self.assertEqual(son_adim.durum.benlik_orani, 0.0)
        self.assertEqual(son_adim.durum.makam, Makam.BEKABILLAH)
        self.assertEqual(son_adim.durum.nefs, NefsMertebesi.SAFIYE)

    def test_ari_inle(self):
        derya = VarlikDeryasi()
        ari = Ari(ad="Derviş")
        ari.durum.benlik_orani = 0.0
        zar = ari.inle(derya)
        self.assertIn("Derviş", zar.hal)
        self.assertIn("Arı inler bal içinde", zar.hukum)
        self.assertGreater(zar.vecd_indeksi, 0)

    def test_kudret_ve_bahane_motoru(self):
        t1 = KudretVeBahaneMotoru.tahlil_et(benlik_orani=0.95)
        self.assertIn("Kesret", t1["ontolojik_seviye"])
        self.assertIn("Zahiren Arı", t1["hakiki_fail"])

        t2 = KudretVeBahaneMotoru.tahlil_et(benlik_orani=0.0)
        self.assertIn("Tevhid-i Tâmm", t2["ontolojik_seviye"])
        self.assertIn("Mutlak Kudret", t2["hakiki_fail"])
        self.assertEqual(t2["vahdet_idraki"], 100.0)

if __name__ == "__main__":
    unittest.main()
