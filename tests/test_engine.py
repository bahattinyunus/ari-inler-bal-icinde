import unittest
from ari_inler_bal_icinde.engine import ParadoksSimulasyonu, simule_et

class TestEngine(unittest.TestCase):
    def test_simule_et_helper(self):
        sonuc = simule_et(salik_adi="Test Arı", viskozite=1.5, cozulme_hizi=0.3)
        self.assertEqual(sonuc.salik_adi, "Test Arı")
        self.assertGreater(sonuc.toplam_adim, 0)
        self.assertEqual(sonuc.nihai_durum.benlik_orani, 0.0)
        self.assertIn("Hüküm:", sonuc.ozet)
        self.assertIn("Arı inler bal içinde", sonuc.zar_tecellisi.hukum)

    def test_paradoks_simulasyonu_stream(self):
        motor = ParadoksSimulasyonu(salik_adi="Salik 1")
        stream_adimlar = list(motor.adim_adim_ak())
        self.assertGreaterEqual(len(stream_adimlar), 6)
        
        # Sonuç dict doğrulaması
        sonuc = motor.calistir()
        d = sonuc.to_dict()
        self.assertEqual(d["salik_adi"], "Salik 1")
        self.assertEqual(len(d["adimlar"]), len(stream_adimlar))

if __name__ == "__main__":
    unittest.main()
