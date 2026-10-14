import unittest
from ari_inler_bal_icinde.models import (
    Makam,
    NefsMertebesi,
    TerkMertebesi,
    SalikDurumu,
    ZarTecellisi,
    SeyrAdimi,
    SimulasyonSonucu,
)

class TestModels(unittest.TestCase):
    def test_enums(self):
        self.assertIn("Talep", Makam.TALEP.value)
        self.assertIn("Fenâfillâh", Makam.FENA_FI_ZAT.value)
        self.assertIn("Bekābillâh", Makam.BEKABILLAH.value)

        self.assertIn("Emmâre", NefsMertebesi.EMMARE.value)
        self.assertIn("Sâfiye", NefsMertebesi.SAFIYE.value)

        self.assertIn("Terk-i Dünya", TerkMertebesi.TERK_I_DUNYA.value)
        self.assertIn("Terk-i Terk", TerkMertebesi.TERK_I_TERK.value)

    def test_salik_durumu_to_dict(self):
        durum = SalikDurumu(
            kimlik="Derviş",
            benlik_orani=0.75,
            makam=Makam.SEVK,
            nefs=NefsMertebesi.LEVVAME,
            viskozite_direnci=0.8,
            hayret_katsayisi=1.2,
            rezonans_frekansi=380.0,
            ses_karakteri="Şaşkın Çırpınış",
        )
        d = durum.to_dict()
        self.assertEqual(d["kimlik"], "Derviş")
        self.assertEqual(d["benlik_orani"], 0.75)
        self.assertIn("Şevk", d["makam"])
        self.assertEqual(d["rezonans_frekansi"], 380.0)

    def test_zar_tecellisi_to_dict(self):
        zar = ZarTecellisi(
            hal="Gark oldu",
            feryat="Vecd fısıltısı",
            hukum="Arı inler bal içinde",
            frekans=136.1,
            harmonikler=[136.1, 220.2],
            vecd_indeksi=3.5,
        )
        d = zar.to_dict()
        self.assertEqual(d["frekans"], 136.1)
        self.assertEqual(d["hukum"], "Arı inler bal içinde")
        self.assertEqual(len(d["harmonikler"]), 2)

    def test_simulasyon_sonucu_to_dict(self):
        durum = SalikDurumu(kimlik="Arı", benlik_orani=0.0)
        zar = ZarTecellisi(hal="Fenâ", feryat="Zâr", hukum="Hüküm", frekans=136.1)
        sonuc = SimulasyonSonucu(
            salik_adi="Arı",
            kaynak_adi="Bal",
            toplam_adim=1,
            adimlar=[],
            nihai_durum=durum,
            zar_tecellisi=zar,
            ozet="Özet rapor",
        )
        d = sonuc.to_dict()
        self.assertEqual(d["salik_adi"], "Arı")
        self.assertEqual(d["nihai_durum"]["benlik_orani"], 0.0)

if __name__ == "__main__":
    unittest.main()
