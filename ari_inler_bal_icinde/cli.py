"""
ari_inler_bal_icinde: Komut Satırı Arayüzü (CLI) - Genişletilmiş Külliyat ve Karşılaştırma
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Optional

from ari_inler_bal_icinde.corpus import KanonikKutuphane
from ari_inler_bal_icinde.engine import ParadoksSimulasyonu
from ari_inler_bal_icinde.physics import FenaDinamigi

# Windows ve genel konsol UTF-8 uyumluluğu
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# Basit ANSI Renk Kodları
class Renk:
    ALTIN = "\033[38;2;255;191;0m"
    KEHRIBAR = "\033[38;2;255;127;0m"
    YESIL = "\033[32m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    KIRMIZI = "\033[31m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def _renkli(metin: str, renk_kodu: str) -> str:
    return f"{renk_kodu}{metin}{Renk.RESET}"


def komut_simule(args: argparse.Namespace) -> None:
    """
    Sâlikin bal deryasındaki seyrini konsolda adım adım simüle eder.
    """
    print(_renkli("\n=======================================================", Renk.ALTIN))
    print(_renkli("  🍯 ARİ İNLER BAL İÇİNDE - VUSLAT VE FENÂ SİMÜLASYONU  ", Renk.BOLD + Renk.ALTIN))
    print(_renkli("=======================================================\n", Renk.ALTIN))

    sim = ParadoksSimulasyonu(
        salik_adi=args.salik,
        viskozite=args.viskozite,
        cozulme_hizi=args.hiz,
    )

    print(f"Sâlik: {_renkli(args.salik, Renk.CYAN)}")
    print(f"Viskozite Katsayısı: {_renkli(str(args.viskozite), Renk.KEHRIBAR)}")
    print(f"Çözülme Sürati: {_renkli(str(args.hiz), Renk.KEHRIBAR)}\n")

    for adim in sim.adim_adim_ak(adim_araligi=0.5):
        benlik = adim.durum.benlik_orani
        bar_dolu = int((1.0 - benlik) * 20)
        bar_bos = 20 - bar_dolu
        fena_bar = "█" * bar_dolu + "░" * bar_bos

        print(
            f"Adım {adim.adim_no} | "
            f"Fenâ: [{_renkli(fena_bar, Renk.ALTIN)}] "
            f"%{int((1.0 - benlik) * 100):3d} | "
            f"Frekans: {_renkli(f'{adim.durum.rezonans_frekansi:.1f} Hz', Renk.CYAN)}"
        )
        print(f"  └─ Makam: {_renkli(adim.durum.makam.value, Renk.BOLD)}")
        print(f"  └─ Nefs : {adim.durum.nefs.value}")
        print(f"  └─ Seda : {_renkli(adim.zar_metni, Renk.DIM)}")
        print()

        if not args.hizli:
            time.sleep(args.bekleme)

    sonuc = sim.calistir()
    print(_renkli("-" * 55, Renk.ALTIN))
    print(_renkli(">>> NİHAİ ZÂR VE VECİD TECELLEİSİ <<<", Renk.BOLD + Renk.ALTIN))
    print(f"Hâl   : {sonuc.zar_tecellisi.hal}")
    print(f"Feryat: {sonuc.zar_tecellisi.feryat}")
    print(f"Hüküm : {_renkli(sonuc.zar_tecellisi.hukum, Renk.BOLD + Renk.KEHRIBAR)}")
    print(_renkli("-" * 55, Renk.ALTIN) + "\n")


def komut_matris(args: argparse.Namespace) -> None:
    """
    Zâhir ile Bâtın karşılaştırma matrisini yazdırır.
    """
    kutuphane = KanonikKutuphane()
    matris = kutuphane.matris_getir()

    print(_renkli("\n📊 SURET (ZÂHİR / AVAM) İLE HAKİKAT (BÂTIN / HAVAS) MATRİSİ\n", Renk.BOLD + Renk.ALTIN))

    for idx, satir in enumerate(matris, start=1):
        print(f"{_renkli(f'[{idx}] ' + satir['parametre'], Renk.BOLD + Renk.CYAN)}")
        print(f"  ├─ Zâhirî Bakış (Avam)  : {satir['zahir']}")
        print(f"  ├─ Bâtınî Bakış (Havas) : {_renkli(satir['batin'], Renk.ALTIN)}")
        print(f"  └─ Kanonik Temel        : {_renkli(satir['temel'], Renk.DIM)}\n")


def komut_divan(args: argparse.Namespace) -> None:
    """
    Kanonik metinleri listeler ve gelenek, motif veya serbest arama yapar.
    """
    kutuphane = KanonikKutuphane()

    if args.arama:
        metinler = kutuphane.serbest_arama(args.arama)
        baslik = f"🔍 '{args.arama}' araması için bulunan metinler"
    elif args.tema:
        metinler = kutuphane.temaya_gore_ara(args.tema)
        baslik = f"🏷️ '{args.tema}' teması için bulunan metinler"
    elif args.gelenek:
        metinler = kutuphane.gelenege_gore_ara(args.gelenek)
        baslik = f"🏛️ '{args.gelenek}' geleneği için metinler"
    elif args.motif:
        metinler = kutuphane.motife_gore_ara(args.motif)
        baslik = f"🕊️ '{args.motif}' motifi için metinler"
    else:
        metinler = kutuphane.tum_metinler()
        baslik = "📚 KANONİK İRFAN KÜLLİYATI"

    print(_renkli(f"\n{baslik} ({len(metinler)} Eser):\n", Renk.BOLD + Renk.ALTIN))

    for m in metinler:
        print(_renkli(f"◆ {m.muellif} — {m.eser} ({m.donem})", Renk.BOLD + Renk.ALTIN))
        print(f"  Gelenek: {_renkli(m.gelenek, Renk.CYAN)} | Ekol: {m.ekol} | Motif: {_renkli(m.motif, Renk.KEHRIBAR)}")
        print(f"  Temalar: {', '.join(m.temalar)}")
        print(_renkli("  \"" + m.orijinal_metin.replace("\n", "\n   ") + "\"", Renk.BOLD))
        print(_renkli(f"  Tefsir/Şerh: {m.serh}", Renk.DIM))
        print()


def komut_kesfet(args: argparse.Namespace) -> None:
    """
    Rastgele bir irfani tecelli ve tefekkür alıntısı getirir.
    """
    kutuphane = KanonikKutuphane()
    m = kutuphane.rastgele_getir()

    print(_renkli("\n✨ GÜNÜN HİKMETİ VE TEFEKKÜR TECELLEİSİ\n", Renk.BOLD + Renk.ALTIN))
    print(_renkli(f"Ârif   : {m.muellif} ({m.donem})", Renk.BOLD + Renk.CYAN))
    print(f"Eser   : {m.eser} [{m.gelenek}]")
    print(f"Motif  : {_renkli(m.motif, Renk.KEHRIBAR)}\n")
    print(_renkli("──────────────── ALINTI ────────────────", Renk.ALTIN))
    print(_renkli(m.orijinal_metin, Renk.BOLD + Renk.ALTIN))
    print(_renkli("─────────────────────────────────────────", Renk.ALTIN))
    print(f"\nİngilizce: \"{m.ingilizce_ceviri}\"")
    print(f"\n💡 Ana Fikir: {m.ana_fikir}")
    print(f"\n📖 İrfani Şerh:\n{m.serh}\n")


def komut_karsilastir(args: argparse.Namespace) -> None:
    """
    İki arifi veya eseri yan yana ontolojik analize tabi tutar.
    """
    kutuphane = KanonikKutuphane()
    id1 = args.id1
    id2 = args.id2

    try:
        sonuc = kutuphane.karsilastir(id1, id2)
    except Exception as e:
        print(_renkli(f"\nHata: {e}", Renk.KIRMIZI))
        return

    m1 = sonuc["metin_1"]
    m2 = sonuc["metin_2"]

    print(_renkli("\n⚖️ KARŞILAŞTIRMALI İRFAN VE MİSTİSİZM ANALİZİ", Renk.BOLD + Renk.ALTIN))
    print(_renkli("=" * 60, Renk.ALTIN))
    print(f"1. Ârif: {_renkli(m1['muellif'], Renk.CYAN)} ({m1['gelenek']}) — Motif: {m1['motif']}")
    print(f"2. Ârif: {_renkli(m2['muellif'], Renk.KEHRIBAR)} ({m2['gelenek']}) — Motif: {m2['motif']}")
    print(_renkli("-" * 60, Renk.ALTIN))
    print(f"Ortak Temalar: {_renkli(', '.join(sonuc['ortak_temalar']) or 'Yok', Renk.BOLD)}")
    print(f"Motif Aynılığı: {'Evet' if sonuc['motif_ortakligi'] else 'Farklı ama Tamamlayıcı'}\n")
    print(_renkli(">>> KARŞILAŞTIRMALI SENTEZ <<<", Renk.BOLD + Renk.ALTIN))
    print(sonuc["sentez"])
    print(_renkli("=" * 60, Renk.ALTIN) + "\n")


def komut_antoloji(args: argparse.Namespace) -> None:
    """
    Külliyatın gelenek ve motif bazlı antoloji raporunu sunar.
    """
    kutuphane = KanonikKutuphane()
    rapor = kutuphane.antoloji_raporu()

    print(_renkli("\n📜 KÜLLİYAT ANTOLOJİ RAPORU VE İSTATİSTİKLER", Renk.BOLD + Renk.ALTIN))
    print(_renkli("=" * 55, Renk.ALTIN))
    print(f"Toplam Kayıtlı Kanonik Eser: {_renkli(str(rapor['toplam_eser_sayisi']), Renk.BOLD + Renk.CYAN)}\n")

    print(_renkli("🏛️ Gelenekler Dağılımı:", Renk.BOLD))
    for gel, sayi in rapor["gelenek_dagilimi"].items():
        print(f"  • {gel:<35}: {_renkli(str(sayi), Renk.ALTIN)} eser")

    print(_renkli("\n🕊️ Sembolik Motif Dağılımı:", Renk.BOLD))
    for mot, sayi in rapor["motif_dagilimi"].items():
        print(f"  • {mot:<35}: {_renkli(str(sayi), Renk.KEHRIBAR)} eser")

    print(_renkli("\nÂrifler Listesi:", Renk.BOLD))
    print(", ".join(rapor["muellifler"][:10]) + f"... ve diğerleri (Toplam {len(rapor['muellifler'])})")
    print(_renkli("=" * 55, Renk.ALTIN) + "\n")


def komut_zar(args: argparse.Namespace) -> None:
    """
    Belirli bir benlik oranındaki Zâr frekansını ve harmoniklerini hesaplar.
    """
    fizik = FenaDinamigi()
    benlik = max(0.0, min(1.0, args.benlik))
    hayret = fizik.hayret_katsayisi_hesapla(benlik, t=3.0)
    frekans, harmonikler, karakter = fizik.akustik_zar_modulasyonu(benlik, hayret)

    print(_renkli("\n🎵 AKUSTİK ZÂR VE FREKANS ANALİZİ", Renk.BOLD + Renk.ALTIN))
    print(f"Benlik Oranı: {_renkli(f'%{benlik * 100:.1f}', Renk.CYAN)}")
    print(f"Hayret Katsayısı: {hayret:.3f}")
    print(f"Temel Frekans: {_renkli(f'{frekans:.2f} Hz', Renk.KEHRIBAR)}")
    print(f"Ses Karakteri: {_renkli(karakter, Renk.BOLD)}")
    print("Harmonikler (Altın Oran & Mistik Aralıklar):")
    for i, h in enumerate(harmonikler, start=1):
        print(f"  H{i}: {h:.2f} Hz")
    print()


def komut_web(args: argparse.Namespace) -> None:
    """
    Web arayüzünü ve REST API'yi ayağa kaldırır.
    """
    from ari_inler_bal_icinde.web_server import sunucuyu_baslat
    import webbrowser

    url = f"http://{args.host}:{args.port}"
    print(_renkli(f"\n🍯 Web Sunucusu Başlatılıyor: {url}", Renk.BOLD + Renk.ALTIN))
    print("Durdurmak için Ctrl+C tuşlarına basınız.\n")

    if args.tarayici:
        webbrowser.open(url)

    sunucu = sunucuyu_baslat(host=args.host, port=args.port)
    try:
        sunucu.serve_forever()
    except KeyboardInterrupt:
        print(_renkli("\nSunucu kapatıldı.", Renk.DIM))
        sunucu.server_close()


def komut_manifesto(args: argparse.Namespace) -> None:
    """
    Manifestoyu ekrana basar.
    """
    manifesto = """
🍯 ARİ İNLER BAL İÇİNDE: MANİFESTO

"Kudretten verdi balı / Bahanesi oldu arı / Dinle imdi âh u zârı / Arı inler bal içinde."

1. İLLÜZYONUN YIKILIŞI (Kudret vs. Bahane)
   Eserin, fiilin ve nizamın faili arı değil, bizzat Hakk'ın kudretidir.
   Arı balı yaptım sandıkça ayrılıktadır; balın bahanesi olduğunu anladığında tevhide erer.

2. FENÂ VE VİSKOZİTE (Eriyen Kimlik)
   Balın içine düşen arının kanatları yapışır. Bu tutsaklık değil,
   bireysel iradenin küllî irade deryasında eriyişidir (Fenâfillâh).

3. HAYRET MAKAMI (Taşan Kap Prensibi)
   Arının iniltisi elemden değil; sonsuz lezzet ve sınırsız güzellik karşısında
   daralan aklın feryadıdır. Şikâyet değil, vecdin ta kendisidir.

4. EVRENSEL NON-DUALİZM (Damla, Tuz, Şeker ve Bal)
   Anadolu ozanlarının balı, Upanishadlar'ın tuz bebeği, Meister Eckhart'ın şarabı
   ve Spinoza'nın tek tözü aynı hakikati haykırır: "Varlık birdir; ikilik dildeki perdedir."
"""
    print(_renkli(manifesto, Renk.ALTIN))


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ari-inler-bal-icinde",
        description="🍯 Anadolu İrfanı ve Doğu Mistisizminde Vuslat Paradoksu Simülatörü",
    )
    subparsers = parser.add_subparsers(dest="komut", help="Alt komutlar")

    # simule
    p_simule = subparsers.add_parser("simule", help="Seyr-ü sülûk simülasyonunu çalıştır")
    p_simule.add_argument("--salik", type=str, default="Derviş / Arı", help="Sâlikin ismi")
    p_simule.add_argument("--viskozite", type=float, default=1.618, help="Bal viskozitesi")
    p_simule.add_argument("--hiz", type=float, default=0.28, help="Çözülme sürati")
    p_simule.add_argument("--bekleme", type=float, default=0.4, help="Adım bekleme süresi (sn)")
    p_simule.add_argument("--hizli", action="store_true", help="Beklemeden hızlı çalıştır")

    # matris
    subparsers.add_parser("matris", help="Suret ve Hakikat karşılaştırma matrisini göster")

    # divan
    p_divan = subparsers.add_parser("divan", help="Kanonik irfan edebiyatı külliyatını tara")
    p_divan.add_argument("-a", "--arama", type=str, help="Serbest arama terimi")
    p_divan.add_argument("-t", "--tema", type=str, help="Tematik filtre")
    p_divan.add_argument("-g", "--gelenek", type=str, help="Gelenek filtresi (Anadolu İrfanı, Mevlevî, vb.)")
    p_divan.add_argument("-m", "--motif", type=str, help="Motif filtresi (ari-ve-bal, damla-ve-umman, vb.)")

    # kesfet
    subparsers.add_parser("kesfet", help="Rastgele irfani tecelli ve tefekkür alıntısı getir")

    # karsilastir
    p_kar = subparsers.add_parser("karsilastir", help="İki arifi yan yana karşılaştır")
    p_kar.add_argument("--id1", type=str, default="pir-sultan-abdal", help="1. Metin ID'si")
    p_kar.add_argument("--id2", type=str, default="ramakrishna-tuz-bebek", help="2. Metin ID'si")

    # antoloji
    subparsers.add_parser("antoloji", help="Külliyat istatistik ve antoloji dökümünü göster")

    # zar
    p_zar = subparsers.add_parser("zar", help="Akustik zâr ve frekans analizi yap")
    p_zar.add_argument("--benlik", type=float, default=0.2, help="Benlik oranı (0.0 - 1.0)")

    # web
    p_web = subparsers.add_parser("web", help="İnteraktif Web UI ve REST API sunucusunu başlat")
    p_web.add_argument("--port", type=int, default=8080, help="Port numarası")
    p_web.add_argument("--host", type=str, default="127.0.0.1", help="Host adresi")
    p_web.add_argument("--tarayici", action="store_true", help="Tarayıcıda otomatik aç")

    # manifesto
    subparsers.add_parser("manifesto", help="Ontolojik manifestoyu görüntüle")

    parsed_args = parser.parse_args(argv)

    if not parsed_args.komut:
        parser.print_help()
        return 0

    komutlar = {
        "simule": komut_simule,
        "matris": komut_matris,
        "divan": komut_divan,
        "kesfet": komut_kesfet,
        "karsilastir": komut_karsilastir,
        "antoloji": komut_antoloji,
        "zar": komut_zar,
        "web": komut_web,
        "manifesto": komut_manifesto,
    }

    fonk = komutlar.get(parsed_args.komut)
    if fonk:
        fonk(parsed_args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
