"""
ari_inler_bal_icinde: Komut Satırı Arayüzü (CLI)
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
    Kanonik metinleri listeler ve arama yapar.
    """
    kutuphane = KanonikKutuphane()

    if args.arama:
        metinler = kutuphane.serbest_arama(args.arama)
        print(f"\n🔍 '{args.arama}' araması için bulunan metinler ({len(metinler)} sonuç):\n")
    elif args.tema:
        metinler = kutuphane.temaya_gore_ara(args.tema)
        print(f"\n🔍 '{args.tema}' teması için bulunan metinler ({len(metinler)} sonuç):\n")
    else:
        metinler = kutuphane.tum_metinler()
        print(f"\n📚 KANONİK İRFAN KÜTÜPHANESİ ({len(metinler)} Eser):\n")

    for m in metinler:
        print(_renkli(f"◆ {m.muellif} — {m.eser} ({m.donem})", Renk.BOLD + Renk.ALTIN))
        print(f"  Ekol: {m.ekol} | Temalar: {', '.join(m.temalar)}")
        print(_renkli("  \"" + m.orijinal_metin.replace("\n", "\n   ") + "\"", Renk.CYAN))
        print(f"  Şerh: {m.serh}\n")


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
    p_divan = subparsers.add_parser("divan", help="Kanonik irfan edebiyatı kütüphanesini tara")
    p_divan.add_argument("-a", "--arama", type=str, help="Serbest arama terimi")
    p_divan.add_argument("-t", "--tema", type=str, help="Tematik filtre (fail, fena, zar, vuslat vb.)")

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
