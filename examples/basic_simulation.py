"""
Örnek 1: Temel Simülasyon Çalıştırması
"""

import sys
from pathlib import Path

# Proje kök dizinini ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ari_inler_bal_icinde import simule_et

def main():
    print("--- Arı İnler Bal İçinde: Temel Simülasyon ---")
    sonuc = simule_et(salik_adi="Yunus", viskozite=1.618, cozulme_hizi=0.30)
    
    print(f"Toplam Adım: {sonuc.toplam_adim}")
    print(f"Sâlik: {sonuc.salik_adi}")
    print(f"Kaynak: {sonuc.kaynak_adi}")
    print("\n--- Özet Rapor ---")
    print(sonuc.ozet)
    print("\n--- Hüküm ---")
    print(sonuc.zar_tecellisi.hukum)

if __name__ == "__main__":
    main()
