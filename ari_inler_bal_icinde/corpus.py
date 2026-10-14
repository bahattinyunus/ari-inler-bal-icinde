"""
ari_inler_bal_icinde: Kanonik İrfan Literatürü ve Karşılaştırma Matrisi
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


DATA_FILE = Path(__file__).parent / "data" / "canonical_texts.json"


@dataclass
class KanonikMetin:
    id: str
    muellif: str
    donem: str
    ekol: str
    eser: str
    orijinal_metin: str
    ingilizce_ceviri: str
    ana_fikir: str
    temalar: List[str]
    serh: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "muellif": self.muellif,
            "donem": self.donem,
            "ekol": self.ekol,
            "eser": self.eser,
            "orijinal_metin": self.orijinal_metin,
            "ingilizce_ceviri": self.ingilizce_ceviri,
            "ana_fikir": self.ana_fikir,
            "temalar": self.temalar,
            "serh": self.serh,
        }


# Zâhir (Suret / Avam) ve Bâtın (Hakikat / Havas) Karşılaştırma Matrisi
KARSILASTIRMA_MATRISI: List[Dict[str, str]] = [
    {
        "parametre": "Fail Kimdir?",
        "zahir": "Balı arı yapar; emek, maharet ve mülkiyet arınındır.",
        "batin": "Bal ilahi kudrettendir; arı yalnızca tecelli tezgâhı ve perdedir.",
        "temel": "Enfâl 17 / Pir Sultan Abdal (Tevhid-i Ef'âl)",
    },
    {
        "parametre": "İnlemenin Sebebi",
        "zahir": "Arı yapışkan bala batmış, kanatları kilitlenmiş, çaresizce acı çekmektedir.",
        "batin": "Sonsuz vuslatın lezzetinden sarhoş olmuş, ilahi nefesin vecdiyle mesttir.",
        "temel": "Fuzûlî / Mevlânâ (Mesnevî 1-3)",
    },
    {
        "parametre": "Varlık İlişkisi",
        "zahir": "Arı ayrı bir özne, bal ayrı bir nesnedir (Dualizm / Kesret).",
        "batin": "Arı balın içinde erimiş, ikilik perdesi yırtılmıştır (Vahdet-i Vücûd).",
        "temel": "Niyâzî-i Mısrî (Katrenin Ummân Oluşu)",
    },
    {
        "parametre": "Sesin Anlamı",
        "zahir": "Şikâyet, sızlanma, ölüm korkusu ve acı çığlığı.",
        "batin": "Zikir, vecd, hayret ve sonlu kabın taşmasından doğan sır nidası.",
        "temel": "İbnü'l-Arabî (Tahayyür) / Şeyh Galip",
    },
    {
        "parametre": "Bitiş Noktası",
        "zahir": "Yok oluş bir felaket, hezimet ve trajedidir.",
        "batin": "Fenâ, ebedi dirilişin (Bekābillâh) yegâne eşiğidir.",
        "temel": "Hallâc-ı Mansûr / Ferîdüddîn Attâr (Simurg)",
    },
]


class KanonikKutuphane:
    """
    Kanonik metin havuzunu yöneten, arama ve filtreleme motoru.
    """

    def __init__(self, veri_yolu: Optional[Path] = None) -> None:
        yol = veri_yolu or DATA_FILE
        self.metinler: List[KanonikMetin] = []
        if yol.exists():
            with open(yol, "r", encoding="utf-8") as f:
                ham = json.load(f)
                for item in ham:
                    self.metinler.append(KanonikMetin(**item))

    def tum_metinler(self) -> List[KanonikMetin]:
        return list(self.metinler)

    def id_ile_getir(self, metin_id: str) -> Optional[KanonikMetin]:
        for m in self.metinler:
            if m.id.lower() == metin_id.lower():
                return m
        return None

    def muellife_gore_ara(self, aranan: str) -> List[KanonikMetin]:
        aranan = aranan.lower()
        return [m for m in self.metinler if aranan in m.muellif.lower()]

    def temaya_gore_ara(self, tema: str) -> List[KanonikMetin]:
        tema = tema.lower()
        return [m for m in self.metinler if any(tema in t.lower() for t in m.temalar)]

    def serbest_arama(self, terim: str) -> List[KanonikMetin]:
        terim = terim.lower()
        sonuclar = []
        for m in self.metinler:
            if (
                terim in m.muellif.lower()
                or terim in m.eser.lower()
                or terim in m.orijinal_metin.lower()
                or terim in m.ana_fikir.lower()
                or terim in m.serh.lower()
            ):
                sonuclar.append(m)
        return sonuclar

    def matris_getir(self) -> List[Dict[str, str]]:
        return list(KARSILASTIRMA_MATRISI)
