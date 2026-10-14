"""
ari_inler_bal_icinde: Varlık Deryası, Arı ve Kudret-Bahane Ontoloji Çekirdeği
"""

from __future__ import annotations

import math
from typing import Generator, List, Optional

from ari_inler_bal_icinde.models import (
    Makam,
    NefsMertebesi,
    SalikDurumu,
    SeyrAdimi,
    TerkMertebesi,
    ZarTecellisi,
)
from ari_inler_bal_icinde.physics import FenaDinamigi


class VarlikDeryasi:
    """
    Mutlak Varlık, Kudret ve Bal Deryası.
    Tek, bölünmez, ebedi ve ezeli olan kaynak.
    """

    def __init__(
        self,
        isim: str = "Mutlak Kudret / Bal",
        viskozite: float = 1.618,
        lezzet_katsayisi: float = 1000.0,
    ) -> None:
        self.isim = isim
        self.viskozite = viskozite
        self.lezzet_katsayisi = lezzet_katsayisi
        self.sonsuz_lezzet: float = float("inf")

    def __repr__(self) -> str:
        return f"<VarlikDeryasi: {self.isim} (Viskozite={self.viskozite})>"


class Ari:
    """
    Kesret âlemindeki bahane ve arayış içindeki sâlik: Arı.
    Görünüşte balı yapan mimar; hakikatte balın içinde erimeye yazgılı zerre.
    """

    def __init__(
        self,
        ad: str = "Derviş / Arı",
        cozulme_hizi: float = 0.28,
    ) -> None:
        self.ad = ad
        self.durum = SalikDurumu(
            kimlik=ad,
            benlik_orani=1.0,
            makam=Makam.TALEP,
            nefs=NefsMertebesi.EMMARE,
            viskozite_direnci=1.0,
            hayret_katsayisi=0.0,
            rezonans_frekansi=440.0,
            ses_karakteri="Kesret Feryadı",
        )
        self.fizik = FenaDinamigi(cozulme_hizi=cozulme_hizi)

    def vuslata_er(
        self,
        kaynak: VarlikDeryasi,
        adim_araligi: float = 0.5,
    ) -> Generator[SeyrAdimi, None, None]:
        """
        Arının bal deryasına dalarak vuslat, hayret ve fenâ mertebelerini
        tecrübe ettiği tekâmül akışı (Seyr-ü Sülûk).
        """
        terkler = [
            (TerkMertebesi.TERK_I_DUNYA, Makam.SEVK, NefsMertebesi.LEVVAME),
            (TerkMertebesi.TERK_I_UKBA, Makam.VUSLAT, NefsMertebesi.MULHIME),
            (TerkMertebesi.TERK_I_HESTI, Makam.HAYRET, NefsMertebesi.MUTMAINNE),
            (TerkMertebesi.TERK_I_TERK, Makam.FENA_FI_EFAL, NefsMertebesi.RAZIYE),
            (None, Makam.FENA_FI_SIFAT, NefsMertebesi.MARZIYE),
            (None, Makam.FENA_FI_ZAT, NefsMertebesi.SAFIYE),
            (None, Makam.BEKABILLAH, NefsMertebesi.SAFIYE),
        ]

        # 0. Başlangıç: Kesret ve Cehalet Hâli
        yield SeyrAdimi(
            adim_no=0,
            zaman=0.0,
            durum=SalikDurumu(
                kimlik=self.ad,
                benlik_orani=1.0,
                makam=Makam.TALEP,
                nefs=NefsMertebesi.EMMARE,
                viskozite_direnci=1.0,
                hayret_katsayisi=0.0,
                rezonans_frekansi=440.0,
                ses_karakteri="Kesret Feryadı",
            ),
            terk=None,
            mesaj=f"[{self.ad}] Balı kendi eseri zanneder. Egonun zirvesindedir.",
            zar_metni="Vızıltı: 'Balı ben yaptım, emek benimdir.'",
            metrikler={"benlik": 1.0, "direnc": 1.0, "hayret": 0.0},
        )

        terk_sayaci = 0
        t = 0.0

        for i, (terk, makam, nefs) in enumerate(terkler, start=1):
            t += adim_araligi
            if terk is not None:
                terk_sayaci += 1

            benlik = self.fizik.benlik_hesapla(t, terk_sayaci)
            # Bekābillâh aşamasında benlik tamamen 0.0'a oturur
            if makam in (Makam.FENA_FI_ZAT, Makam.BEKABILLAH):
                benlik = 0.0

            direnc = self.fizik.viskozite_direnci_hesapla(benlik)
            hayret = self.fizik.hayret_katsayisi_hesapla(benlik, t)
            frekans, harmonikler, ses_karakteri = self.fizik.akustik_zar_modulasyonu(benlik, hayret)

            self.durum.benlik_orani = benlik
            self.durum.makam = makam
            self.durum.nefs = nefs
            self.durum.viskozite_direnci = direnc
            self.durum.hayret_katsayisi = hayret
            self.durum.rezonans_frekansi = frekans
            self.durum.ses_karakteri = ses_karakteri

            mesaj = self._adim_mesaji_olustur(makam, terk)
            zar_metni = self._adim_zari_olustur(makam, benlik, frekans)

            yield SeyrAdimi(
                adim_no=i,
                zaman=t,
                durum=SalikDurumu(**self.durum.__dict__),
                terk=terk,
                mesaj=mesaj,
                zar_metni=zar_metni,
                metrikler={
                    "benlik": benlik,
                    "direnc": direnc,
                    "hayret": hayret,
                    "frekans": frekans,
                },
            )

    def _adim_mesaji_olustur(self, makam: Makam, terk: Optional[TerkMertebesi]) -> str:
        if terk:
            return f"[{self.ad}] {terk.value}. Makam: {makam.value}."
        return f"[{self.ad}] Tecelli derinleşiyor. Makam: {makam.value}."

    def _adim_zari_olustur(self, makam: Makam, benlik: float, frekans: float) -> str:
        if benlik > 0.7:
            return f"Zâr ({frekans:.1f} Hz): Telaş ve sitem. Kanatlar bala saplandı."
        elif benlik > 0.4:
            return f"Zâr ({frekans:.1f} Hz): Hayret başlıyor. Balın lezzeti aklı bastırdı."
        elif benlik > 0.1:
            return f"Zâr ({frekans:.1f} Hz): Ney rezonansı. Şikâyet değil, vecd fısıltısı."
        else:
            return f"Zâr ({frekans:.1f} Hz): 'Dinle imdi âh u zârı / Arı inler bal içinde.' Birlik sırrı."

    def inle(self, kaynak: VarlikDeryasi) -> ZarTecellisi:
        """
        Nihai Fenâ ve Vuslat Tecellisi.
        Arının bal içinde inlemesi:
        Avam acı çığlığı sanır; havas ise sınırsız vuslatın lezzet sarhoşluğu olduğunu bilir.
        """
        if self.durum.hayret_katsayisi <= 0.0:
            self.durum.hayret_katsayisi = self.fizik.hayret_katsayisi_hesapla(
                self.durum.benlik_orani, t=3.0
            )

        frekans, harmonikler, _ = self.fizik.akustik_zar_modulasyonu(
            self.durum.benlik_orani, self.durum.hayret_katsayisi
        )

        vecd = max(0.1, self.durum.hayret_katsayisi * (1.0 + (1.0 - self.durum.benlik_orani)))

        return ZarTecellisi(
            hal=(
                f"'{self.ad}' artık bağımsız bir fail ve münferit bir varlık değildir. "
                f"'{kaynak.isim}' deryasında gark olmuş, katreyken ummâna dönüşmüştür."
            ),
            feryat=(
                "Bu ses; mahrumiyetin ve sürgünün iniltisi değil, sonsuz kudret ve tat karşısında "
                "daralan aklın ve taşan kabın vecd zikridir."
            ),
            hukum="Kudretten verdi balı / Bahanesi oldu arı / Dinle imdi âh u zârı / Arı inler bal içinde.",
            frekans=frekans,
            harmonikler=harmonikler,
            vecd_indeksi=round(vecd, 4),
        )


class KudretVeBahaneMotoru:
    """
    Sebep (Bahane) ile Müsebbip (Kudret) arasındaki metafizik perdeyi
    çözen ve Tevhid-i Ef'âl hakikatini değerlendiren motor.
    """

    @staticmethod
    def tahlil_et(benlik_orani: float) -> dict:
        zahir_hakimiyet = max(0.0, min(1.0, benlik_orani))
        batin_idrak = 1.0 - zahir_hakimiyet

        if zahir_hakimiyet > 0.7:
            seviye = "Kesret Perdesi (Arı kendini usta ve fail sanıyor)"
            fail = "Zahiren Arı (Gaflet Hâli)"
        elif zahir_hakimiyet > 0.3:
            seviye = "Tahayyür Eşiği (Arı kudretin büyüklüğünü fark ediyor)"
            fail = "Müşterek Zannı (Araf Hâli)"
        else:
            seviye = "Tevhid-i Tâmm (Bahane kalktı, fail yalnızca Kudrettir)"
            fail = "Mutlak Kudret (Vahdet Hâli)"

        return {
            "kesret_yanilsamasi": round(zahir_hakimiyet * 100, 1),
            "vahdet_idraki": round(batin_idrak * 100, 1),
            "ontolojik_seviye": seviye,
            "hakiki_fail": fail,
        }
