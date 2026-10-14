"""
ari_inler_bal_icinde: Kanonik İrfan Literatürü, Karşılaştırma Matrisi ve Külliyat
"""

from __future__ import annotations

import json
import random
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
    gelenek: str = "Anadolu İrfanı"
    motif: str = "ari-ve-bal"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "muellif": self.muellif,
            "donem": self.donem,
            "ekol": self.ekol,
            "eser": self.eser,
            "gelenek": self.gelenek,
            "motif": self.motif,
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
        "temel": "Enfâl 17 / Pir Sultan Abdal (Tevhid-i Ef'âl) / Spinoza",
    },
    {
        "parametre": "İnlemenin Sebebi",
        "zahir": "Arı yapışkan bala batmış, kanatları kilitlenmiş, çaresizce acı çekmektedir.",
        "batin": "Sonsuz vuslatın lezzetinden sarhoş olmuş, ilahi nefesin vecdiyle mesttir.",
        "temel": "Fuzûlî / Mevlânâ (Mesnevî 1-3) / San Juan de la Cruz",
    },
    {
        "parametre": "Varlık İlişkisi",
        "zahir": "Arı ayrı bir özne, bal ayrı bir nesnedir (Dualizm / Kesret).",
        "batin": "Arı balın içinde erimiş, ikilik perdesi yırtılmıştır (Vahdet-i Vücûd / Non-Dualizm).",
        "temel": "Niyâzî-i Mısrî (Katrenin Ummân Oluşu) / Chandogya Upanishad (Tat Tvam Asi)",
    },
    {
        "parametre": "Sesin Anlamı",
        "zahir": "Şikâyet, sızlanma, ölüm korkusu ve acı çığlığı.",
        "batin": "Zikir, vecd, hayret ve sonlu kabın taşmasından doğan sır nidası.",
        "temel": "İbnü'l-Arabî (Tahayyür) / Şeyh Galip / Meister Eckhart",
    },
    {
        "parametre": "Bitiş Noktası",
        "zahir": "Yok oluş bir felaket, hezimet ve trajedidir.",
        "batin": "Fenâ, ebedi dirilişin (Bekābillâh / Samadhi) yegâne eşiğidir.",
        "temel": "Hallâc-ı Mansûr / Ferîdüddîn Attâr (Simurg) / Sri Ramakrishna (Tuz Bebek)",
    },
]


class KanonikKutuphane:
    """
    Genişletilmiş kanonik metin havuzunu yöneten, arama, filtreleme,
    tematik eşleştirme ve karşılaştırmalı analiz motoru.
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

    def gelenege_gore_ara(self, gelenek: str) -> List[KanonikMetin]:
        gelenek = gelenek.lower()
        return [m for m in self.metinler if gelenek in m.gelenek.lower()]

    def motife_gore_ara(self, motif: str) -> List[KanonikMetin]:
        motif = motif.lower()
        return [m for m in self.metinler if motif in m.motif.lower()]

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
                or terim in m.gelenek.lower()
                or terim in m.motif.lower()
            ):
                sonuclar.append(m)
        return sonuclar

    def tum_gelenekler(self) -> List[str]:
        return sorted(list({m.gelenek for m in self.metinler}))

    def tum_motifler(self) -> List[str]:
        return sorted(list({m.motif for m in self.metinler}))

    def rastgele_getir(self, tohum: Optional[int] = None) -> KanonikMetin:
        if tohum is not None:
            r = random.Random(tohum)
            return r.choice(self.metinler)
        return random.choice(self.metinler)

    def karsilastir(self, id1: str, id2: str) -> Dict[str, Any]:
        """
        İki farklı arif veya geleneği ontolojik olarak yan yana karşılaştırır.
        """
        m1 = self.id_ile_getir(id1)
        m2 = self.id_ile_getir(id2)

        if not m1 or not m2:
            raise ValueError(f"Karşılaştırılacak metin bulunamadı: {id1} veya {id2}")

        ortak_temalar = list(set(m1.temalar) & set(m2.temalar))
        motif_ortak = m1.motif == m2.motif

        sentez = (
            f"'{m1.muellif}' ({m1.gelenek}) ile '{m2.muellif}' ({m2.gelenek}) "
            f"farklı coğrafya ve asırlarda yaşamış olmalarına rağmen, "
            f"benliğin Mutlak Varlık karşısındaki erimesini ve vuslat sarhoşluğunu "
            f"{'aynı motif (' + m1.motif + ')' if motif_ortak else 'tamamlayıcı semboller (' + m1.motif + ' ve ' + m2.motif + ')'} "
            f"ekseninde ifade etmektedirler. "
            f"Her iki irfani tecelli de egonun tasfiyesini ve hakiki failin keşfini merkeze alır."
        )

        return {
            "metin_1": m1.to_dict(),
            "metin_2": m2.to_dict(),
            "ortak_temalar": ortak_temalar,
            "motif_ortakligi": motif_ortak,
            "sentez": sentez,
        }

    def antoloji_raporu(self) -> Dict[str, Any]:
        """
        Külliyatın gelenek ve motif bazlı istatistiksel dökümünü üretir.
        """
        gelenek_sayilari: Dict[str, int] = {}
        motif_sayilari: Dict[str, int] = {}

        for m in self.metinler:
            gelenek_sayilari[m.gelenek] = gelenek_sayilari.get(m.gelenek, 0) + 1
            motif_sayilari[m.motif] = motif_sayilari.get(m.motif, 0) + 1

        return {
            "toplam_eser_sayisi": len(self.metinler),
            "gelenek_dagilimi": gelenek_sayilari,
            "motif_dagilimi": motif_sayilari,
            "muellifler": [m.muellif for m in self.metinler],
        }

    def matris_getir(self) -> List[Dict[str, str]]:
        return list(KARSILASTIRMA_MATRISI)
