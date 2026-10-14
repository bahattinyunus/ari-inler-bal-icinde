"""
Örnek 2: Kanonik İrfan Kütüphanesi ve Matris Taraması
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
    print(f"Toplam Yüklü Eser Sayısı: {len(kutuphane.tum_metinler())}\n")

    print("--- 1. 'zar' Temalı Eserler ---")
    zar_metinleri = kutuphane.temaya_gore_ara("zar")
    for m in zar_metinleri:
        print(f"[{m.muellif}] - {m.eser}:")
        print(f"  \"{m.orijinal_metin.replace(chr(10), ' / ')}\"")
        print(f"  Ana Fikir: {m.ana_fikir}\n")

    print("--- 2. Suret vs Hakikat Karşılaştırma Matrisi ---")
    for row in kutuphane.matris_getir():
        print(f"Parametre: {row['parametre']}")
        print(f"  Zâhir : {row['zahir']}")
        print(f"  Bâtın : {row['batin']}\n")

if __name__ == "__main__":
    main()
