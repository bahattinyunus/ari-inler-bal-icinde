"""
ari_inler_bal_icinde: Simülasyon Motoru ve Orkestrasyon Katmanı
"""

from __future__ import annotations

from typing import Generator, List, Optional

from ari_inler_bal_icinde.corpus import KanonikKutuphane
from ari_inler_bal_icinde.models import (
    SalikDurumu,
    SeyrAdimi,
    SimulasyonSonucu,
    ZarTecellisi,
)
from ari_inler_bal_icinde.ontology import Ari, KudretVeBahaneMotoru, VarlikDeryasi


class ParadoksSimulasyonu:
    """
    Arının bal deryasına dalışını ve inleme paradoksunu baştan sona
    yöneten simülasyon orkestratörü.
    """

    def __init__(
        self,
        salik_adi: str = "Derviş / Arı",
        derya_adi: str = "Mutlak Kudret / Bal",
        viskozite: float = 1.618,
        cozulme_hizi: float = 0.28,
        kudret_yogunlugu: float = 10.0,
    ) -> None:
        self.salik_adi = salik_adi
        self.derya_adi = derya_adi
        self.derya = VarlikDeryasi(isim=derya_adi, viskozite=viskozite)
        self.ari = Ari(ad=salik_adi, cozulme_hizi=cozulme_hizi)
        self.ari.fizik.viskozite = viskozite
        self.ari.fizik.kudret_yogunlugu = kudret_yogunlugu
        self.kutuphane = KanonikKutuphane()

    def adim_adim_ak(
        self,
        adim_araligi: float = 0.5,
    ) -> Generator[SeyrAdimi, None, None]:
        """
        Sâlikin seyr-ü sülûk adımlarını gerçek zamanlı veya döngüsel olarak
        akıtır.
        """
        yield from self.ari.vuslata_er(self.derya, adim_araligi=adim_araligi)

    def calistir(self) -> SimulasyonSonucu:
        """
        Tüm süreci yürütür ve nihai simülasyon sonucunu döner.
        """
        adimlar: List[SeyrAdimi] = []
        for adim in self.adim_adim_ak():
            adimlar.append(adim)

        nihai_durum = self.ari.durum
        zar_tecellisi = self.ari.inle(self.derya)
        tahlil = KudretVeBahaneMotoru.tahlil_et(nihai_durum.benlik_orani)

        ozet = (
            f"=== {self.salik_adi} Vuslat ve Fenâ Raporu ===\n"
            f"Makam: {nihai_durum.makam.value}\n"
            f"Nefs Basamağı: {nihai_durum.nefs.value}\n"
            f"Kalan Benlik: %{nihai_durum.benlik_orani * 100:.1f}\n"
            f"Viskozite Direnci: {nihai_durum.viskozite_direnci:.3f}\n"
            f"Hayret Katsayısı: {nihai_durum.hayret_katsayisi:.3f}\n"
            f"Akustik Zâr Frekansı: {nihai_durum.rezonans_frekansi:.1f} Hz ({nihai_durum.ses_karakteri})\n"
            f"Hakiki Fail İdrakı: {tahlil['hakiki_fail']} (Vahdet İdraki: %{tahlil['vahdet_idraki']})\n"
            f"Hüküm: {zar_tecellisi.hukum}"
        )

        return SimulasyonSonucu(
            salik_adi=self.salik_adi,
            kaynak_adi=self.derya_adi,
            toplam_adim=len(adimlar),
            adimlar=adimlar,
            nihai_durum=nihai_durum,
            zar_tecellisi=zar_tecellisi,
            ozet=ozet,
        )


def simule_et(
    salik_adi: str = "Derviş / Arı",
    viskozite: float = 1.618,
    cozulme_hizi: float = 0.28,
) -> SimulasyonSonucu:
    """
    Hızlı çalıştırma için yardımcı fonksiyon.
    """
    motor = ParadoksSimulasyonu(
        salik_adi=salik_adi,
        viskozite=viskozite,
        cozulme_hizi=cozulme_hizi,
    )
    return motor.calistir()
