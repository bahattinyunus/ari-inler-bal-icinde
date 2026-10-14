"""
ari_inler_bal_icinde: Ontolojik ve Tasavvufi Durum Modelleri
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Makam(str, Enum):
    """Sâlikin seyr-ü sülûk yolculuğundaki manevi durakları."""
    TALEP = "Talep (Arayış ve İstek)"
    SEVK = "Şevk (Cezbe ve Hızlanma)"
    VUSLAT = "Vuslat (Kaynağa Ulaşma)"
    HAYRET = "Hayret (Tahayyür / Aşk Şaşkınlığı)"
    FENA_FI_EFAL = "Fenâ fi'l-Ef'âl (Fiillerin Birliği)"
    FENA_FI_SIFAT = "Fenâ fi's-Sıfât (Sıfatların Birliği)"
    FENA_FI_ZAT = "Fenâfillâh (Mutlak Fenâ / Varlıkta Eriyip Yok Oluş)"
    BEKABILLAH = "Bekābillâh (Hakk ile Bâkî Kalış)"

    def __str__(self) -> str:
        return self.value


class NefsMertebesi(str, Enum):
    """Nefsin yedi basamağı (Etvâr-ı Seb'a)."""
    EMMARE = "Nefs-i Emmâre (Benlik ve Şehvet Kulu)"
    LEVVAME = "Nefs-i Levvâme (Kendini Kınayan Bilinç)"
    MULHIME = "Nefs-i Mülhime (İlhama Mazhar Olan Kalp)"
    MUTMAINNE = "Nefs-i Mutmainne (Huzura Kavuşmuş Ruh)"
    RAZIYE = "Nefs-i Râziye (Kaderden Hoşnut Olan)"
    MARZIYE = "Nefs-i Marziye (Hakk'ın Rızasını Kazanmış)"
    SAFIYE = "Nefs-i Sâfiye / Kâmile (Saf, Katıksız Birlik)"

    def __str__(self) -> str:
        return self.value


class TerkMertebesi(str, Enum):
    """Dört Terk Doktrini (Çehâr Terk)."""
    TERK_I_DUNYA = "Terk-i Dünya (Maddi kaygı ve nesnelerin terk edilmesi)"
    TERK_I_UKBA = "Terk-i Ukbâ (Ahiret mükâfatı ve cennet arzusunun terk edilmesi)"
    TERK_I_HESTI = "Terk-i Hestî (Bizzat kendi varlığının ve egosunun terk edilmesi)"
    TERK_I_TERK = "Terk-i Terk (Terk ettiğinin dahi unutulması; mutlak hiçlik)"

    def __str__(self) -> str:
        return self.value


@dataclass
class SalikDurumu:
    """
    Sâlikin (veya bal deryasına dalan Arı'nın) anlık ontolojik durumu.
    """
    kimlik: str
    benlik_orani: float = 1.0          # 1.0 = Kesret (Saf Ego), 0.0 = Fenâfillâh
    makam: Makam = Makam.TALEP
    nefs: NefsMertebesi = NefsMertebesi.EMMARE
    viskozite_direnci: float = 1.0     # 1.0 = Akışa tam direnç, 0.0 = Tam teslimiyet
    hayret_katsayisi: float = 0.0      # Bilinç kapasitesinin aşılma oranı
    rezonans_frekansi: float = 432.0   # Akustik vecd frekansı (Hz)
    ses_karakteri: str = "Kesret Vızıltısı"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kimlik": self.kimlik,
            "benlik_orani": round(self.benlik_orani, 4),
            "makam": str(self.makam),
            "nefs": str(self.nefs),
            "viskozite_direnci": round(self.viskozite_direnci, 4),
            "hayret_katsayisi": round(self.hayret_katsayisi, 4),
            "rezonans_frekansi": round(self.rezonans_frekansi, 2),
            "ses_karakteri": self.ses_karakteri,
        }


@dataclass
class ZarTecellisi:
    """
    Arının bal içindeki iniltisinin tecellisi ve vecd yankısı.
    """
    hal: str
    feryat: str
    hukum: str
    frekans: float
    harmonikler: List[float] = field(default_factory=list)
    vecd_indeksi: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hal": self.hal,
            "feryat": self.feryat,
            "hukum": self.hukum,
            "frekans": round(self.frekans, 2),
            "harmonikler": [round(h, 2) for h in self.harmonikler],
            "vecd_indeksi": round(self.vecd_indeksi, 4),
        }


@dataclass
class SeyrAdimi:
    """
    Seyr-ü sülûk simülasyonunun tekil bir tekâmül adımı.
    """
    adim_no: int
    zaman: float
    durum: SalikDurumu
    terk: Optional[TerkMertebesi]
    mesaj: str
    zar_metni: str
    metrikler: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "adim_no": self.adim_no,
            "zaman": round(self.zaman, 3),
            "durum": self.durum.to_dict(),
            "terk": str(self.terk) if self.terk else None,
            "mesaj": self.mesaj,
            "zar_metni": self.zar_metni,
            "metrikler": {k: round(v, 4) for k, v in self.metrikler.items()},
        }


@dataclass
class SimulasyonSonucu:
    """
    Tüm simülasyonun tam dökümü ve nihai fenâ tespiti.
    """
    salik_adi: str
    kaynak_adi: str
    toplam_adim: int
    adimlar: List[SeyrAdimi]
    nihai_durum: SalikDurumu
    zar_tecellisi: ZarTecellisi
    ozet: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "salik_adi": self.salik_adi,
            "kaynak_adi": self.kaynak_adi,
            "toplam_adim": self.toplam_adim,
            "adimlar": [a.to_dict() for a in self.adimlar],
            "nihai_durum": self.nihai_durum.to_dict(),
            "zar_tecellisi": self.zar_tecellisi.to_dict(),
            "ozet": self.ozet,
        }
