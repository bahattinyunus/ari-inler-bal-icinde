"""
Örnek 3: Akustik Zâr ve Frekans Salınımı
"""

import sys
from pathlib import Path

# Proje kök dizinini ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ari_inler_bal_icinde import FenaDinamigi

def main():
    fizik = FenaDinamigi()
    print("--- Benlik Çözülürken Zâr Frekansının Dönüşümü ---")
    print(f"{'Benlik':<10} | {'Frekans':<12} | {'Hayret':<10} | {'Ses Karakteri'}")
    print("-" * 65)

    for oran in [1.0, 0.8, 0.6, 0.4, 0.2, 0.05, 0.0]:
        hayret = fizik.hayret_katsayisi_hesapla(oran, t=3.0)
        frekans, harmonikler, karakter = fizik.akustik_zar_modulasyonu(oran, hayret)
        print(f"%{oran*100:6.1f}   | {frekans:7.2f} Hz   | {hayret:8.3f}   | {karakter}")

if __name__ == "__main__":
    main()
