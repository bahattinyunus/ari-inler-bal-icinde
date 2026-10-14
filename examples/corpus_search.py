"""
Örnek 2: Kanonik İrfan Kütüphanesi, Motifler ve Karşılaştırmalı Analiz
"""

import sys
from pathlib import Path

# Proje kök dizinini ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

# UTF-8 konsol desteği
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ari_inler_bal_icinde import KanonikKutuphane

def main():
    kutuphane = KanonikKutuphane()
    rapor = kutuphane.antoloji_raporu()
    print(f"Toplam Yüklü Eser Sayısı: {rapor['toplam_eser_sayisi']}\n")

    print("--- 1. Gelenekler ve Eser Sayıları ---")
    for gelenek, sayi in rapor["gelenek_dagilimi"].items():
        print(f"  • {gelenek}: {sayi} eser")

    print("\n--- 2. Sembolik Motifler ve Eser Sayıları ---")
    for motif, sayi in rapor["motif_dagilimi"].items():
        print(f"  • {motif}: {sayi} eser")

    print("\n--- 3. Karşılaştırmalı Analiz: Pir Sultan Abdal vs Sri Ramakrishna ---")
    karsilastirma = kutuphane.karsilastir("pir-sultan-abdal", "ramakrishna-tuz-bebek")
    print(f"1. Metin: {karsilastirma['metin_1']['muellif']} ({karsilastirma['metin_1']['motif']})")
    print(f"2. Metin: {karsilastirma['metin_2']['muellif']} ({karsilastirma['metin_2']['motif']})")
    print(f"\nSentez:\n{karsilastirma['sentez']}")

    print("\n--- 4. Rastgele Tefekkür Alıntısı ---")
    tefekkur = kutuphane.rastgele_getir(tohum=100)
    print(f"[{tefekkur.muellif} - {tefekkur.eser}]:")
    print(f"\"{tefekkur.orijinal_metin.replace(chr(10), ' / ')}\"")
    print(f"Şerh: {tefekkur.serh}")

if __name__ == "__main__":
    main()
