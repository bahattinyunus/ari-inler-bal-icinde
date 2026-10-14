"""
ari_inler_bal_icinde: Fenâ Dinamiği, Viskozite ve Akustik Rezonans Modeli
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple


# Evrensel ve Metafizik Sabitler
ALTIN_ORAN: float = (1.0 + math.sqrt(5.0)) / 2.0  # 1.6180339887...
NEY_TEMEL_FREKANSI: float = 136.1                 # Meditatif OM / Ney derya tonu (Hz)
KESRET_VIZILTI_FREKANSI: float = 440.0             # Ayrılıktaki telaşlı sâlik vızıltısı (Hz)


class FenaDinamigi:
    """
    Sâlikin bal deryasında benliğini eritme sürecinin matematiksel ve
    metafizik modellemesi.
    """

    def __init__(
        self,
        viskozite: float = 1.618,
        cozulme_hizi: float = 0.28,
        kudret_yogunlugu: float = 10.0,
    ) -> None:
        """
        :param viskozite: İlahi cezbenin yoğunluğu ve akış direnci (Bal viskozitesi).
        :param cozulme_hizi: Benlik kabuğunun çözünme katsayısı (Lambda).
        :param kudret_yogunlugu: Tecellinin sınırsızlık katsayısı (Omega).
        """
        self.viskozite = max(0.1, viskozite)
        self.cozulme_hizi = max(0.01, cozulme_hizi)
        self.kudret_yogunlugu = max(1.0, kudret_yogunlugu)

    def benlik_hesapla(self, t: float, terk_sayisi: int = 0) -> float:
        """
        Zaman ve terk makamlarına bağlı olarak kalan benlik oranını (1.0 -> 0.0) hesaplar.
        E(t) = E0 * exp(-lambda * t) - (0.15 * terk_sayisi)
        """
        temel_erime = math.exp(-self.cozulme_hizi * t)
        terk_bonusu = terk_sayisi * 0.12
        benlik = max(0.0, min(1.0, temel_erime - terk_bonusu))
        return benlik

    def viskozite_direnci_hesapla(self, benlik_orani: float) -> float:
        """
        Benlik direnci; sâlik benliğini korumaya çalıştıkça viskoziteye direnir.
        Benlik sıfırlandığında direnç de sıfıra iner (tam teslimiyet).
        """
        return max(0.0, min(1.0, math.pow(benlik_orani, 1.2)))

    def hayret_katsayisi_hesapla(self, benlik_orani: float, t: float) -> float:
        """
        Taşan Kap Prensibi:
        Sâlikin akli idrak kabı sonludur; içine dökülen tecelli sonsuzdur.
        Benlik azaldıkça tecelli doğrudan idrake vurur ve hayret patlar.
        """
        kap_kapasitesi = max(0.05, benlik_orani + 0.1)
        tecelli_akisi = self.kudret_yogunlugu * (1.0 - math.exp(-0.35 * t))
        tasan_miktar = tecelli_akisi / kap_kapasitesi
        # Hayret logaritmik olarak genişler
        return round(math.log1p(tasan_miktar) * 1.5, 4)

    def akustik_zar_modulasyonu(
        self,
        benlik_orani: float,
        hayret: float,
    ) -> Tuple[float, List[float], str]:
        """
        İniltinin (Zâr) frekans spektrumunu modeller:
        - Kesrette: 440 Hz civarında tiz, telaşlı, ayrılık acısı içeren feryat.
        - Fenâda: 136.1 Hz derinliğine oturan, altın oran harmonikleriyle zenginleşen vecd.
        """
        alfa = 1.0 - benlik_orani  # Fenâlaşma oranı (0.0 -> 1.0)

        # Temel frekans enterpolasyonu (Kesret -> Ney Tonu)
        frekans = (KESRET_VIZILTI_FREKANSI * (1.0 - alfa)) + (NEY_TEMEL_FREKANSI * alfa)

        # Hayret titremesi: hayret arttıkça mikrotonal zikir salınımı eklenir
        salinim = math.sin(hayret * math.pi) * (2.5 * (1.0 - alfa))
        anlik_frekans = max(50.0, frekans + salinim)

        # Harmonikler (Doğu mistik makam aralıkları ve altın oran)
        harmonikler = [
            anlik_frekans,
            anlik_frekans * ALTIN_ORAN,
            anlik_frekans * 2.0,
            anlik_frekans * 3.0,
            anlik_frekans * (ALTIN_ORAN * 2.0),
        ]

        # Ses Karakteri İsimlendirmesi
        if benlik_orani > 0.8:
            karakter = "Kesret Feryadı (Ayrılık ve Sitem Vızıltısı)"
        elif benlik_orani > 0.5:
            karakter = "Viskozite Direnci (Şaşkın Çırpınış ve Zâr)"
        elif benlik_orani > 0.2:
            karakter = "Ney Sedası (Cezbe ve Aşk Uğultusu)"
        elif benlik_orani > 0.05:
            karakter = "Hayret Zikri (Eriyerek Kaybolan İnilti)"
        else:
            karakter = "Vahdet Sükûtu (Bâkî Derya Rezonansı)"

        return anlik_frekans, harmonikler, karakter

    def anlik_adim_hesapla(
        self,
        t: float,
        terk_sayisi: int = 0,
    ) -> Dict[str, float]:
        """
        Bütün fiziksel metrikleri tek bir anda hesaplar.
        """
        benlik = self.benlik_hesapla(t, terk_sayisi)
        direnc = self.viskozite_direnci_hesapla(benlik)
        hayret = self.hayret_katsayisi_hesapla(benlik, t)
        frekans, _, _ = self.akustik_zar_modulasyonu(benlik, hayret)

        return {
            "zaman": t,
            "benlik_orani": benlik,
            "viskozite_direnci": direnc,
            "hayret_katsayisi": hayret,
            "frekans": frekans,
        }
