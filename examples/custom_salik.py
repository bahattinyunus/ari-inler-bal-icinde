"""
Örnek 4: Özel Sâlik ve Akış Simülasyonu
"""

import sys
from pathlib import Path

# Proje kök dizinini ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ari_inler_bal_icinde import ParadoksSimulasyonu

def main():
    sim = ParadoksSimulasyonu(
        salik_adi="Attâr'ın Kuşu",
        derya_adi="Simurg'un Varlık Ummanı",
        viskozite=2.5,
        cozulme_hizi=0.35,
    )

    print(f"Başlatılıyor: {sim.salik_adi} -> {sim.derya_adi}\n")
    for adim in sim.adim_adim_ak():
        print(
            f"Adım {adim.adim_no:2d} | "
            f"Makam: {adim.durum.makam.name:<15} | "
            f"Kalan Benlik: %{adim.durum.benlik_orani*100:5.1f} | "
            f"Frekans: {adim.durum.rezonans_frekansi:.1f} Hz"
        )

if __name__ == "__main__":
    main()
