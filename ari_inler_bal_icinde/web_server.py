"""
ari_inler_bal_icinde: Dahili Web Sunucusu ve Genişletilmiş REST API
"""

from __future__ import annotations

import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from ari_inler_bal_icinde.corpus import KanonikKutuphane
from ari_inler_bal_icinde.engine import ParadoksSimulasyonu


WEB_DIR = Path(__file__).parent.parent / "web"


class AriApiHandler(BaseHTTPRequestHandler):
    """
    Hem statik web arayüzünü hem de ontolojik simülasyon ve antoloji API'sini
    harici bağımlılık gerektirmeden sunan HTTP işleyicisi.
    """

    kutuphane = KanonikKutuphane()

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        # API Yolları
        if path == "/api/status":
            self._json_cevap({
                "status": "ok",
                "versiyon": "0.2.0",
                "sistem": "ari-inler-bal-icinde",
                "toplam_eser": len(self.kutuphane.tum_metinler()),
            })
            return

        elif path == "/api/simulate":
            salik = query.get("salik", ["Derviş / Arı"])[0]
            try:
                viskozite = float(query.get("viskozite", [1.618])[0])
            except ValueError:
                viskozite = 1.618

            try:
                hiz = float(query.get("hiz", [0.28])[0])
            except ValueError:
                hiz = 0.28

            sim = ParadoksSimulasyonu(salik_adi=salik, viskozite=viskozite, cozulme_hizi=hiz)
            sonuc = sim.calistir()
            self._json_cevap(sonuc.to_dict())
            return

        elif path == "/api/corpus":
            aranan = query.get("q", [None])[0]
            tema = query.get("tema", [None])[0]
            gelenek = query.get("gelenek", [None])[0]
            motif = query.get("motif", [None])[0]

            if aranan:
                metinler = self.kutuphane.serbest_arama(aranan)
            elif tema:
                metinler = self.kutuphane.temaya_gore_ara(tema)
            elif gelenek:
                metinler = self.kutuphane.gelenege_gore_ara(gelenek)
            elif motif:
                metinler = self.kutuphane.motife_gore_ara(motif)
            else:
                metinler = self.kutuphane.tum_metinler()
            self._json_cevap([m.to_dict() for m in metinler])
            return

        elif path == "/api/random":
            metin = self.kutuphane.rastgele_getir()
            self._json_cevap(metin.to_dict())
            return

        elif path == "/api/compare":
            id1 = query.get("id1", ["pir-sultan-abdal"])[0]
            id2 = query.get("id2", ["ramakrishna-tuz-bebek"])[0]
            try:
                karsilastirma = self.kutuphane.karsilastir(id1, id2)
                self._json_cevap(karsilastirma)
            except Exception as e:
                self._json_cevap({"error": str(e)}, kod=400)
            return

        elif path == "/api/report":
            rapor = self.kutuphane.antoloji_raporu()
            self._json_cevap(rapor)
            return

        elif path == "/api/matrix":
            matris = self.kutuphane.matris_getir()
            self._json_cevap(matris)
            return

        # Statik Dosya Sunumu
        self._statik_dosya_sun(path)

    def _statik_dosya_sun(self, path: str) -> None:
        if path == "/" or not path:
            path = "/index.html"

        # Güvenlik kontrolü (Path traversal önleme)
        rel_path = path.lstrip("/\\")
        hedef_dosya = (WEB_DIR / rel_path).resolve()

        if not str(hedef_dosya).startswith(str(WEB_DIR.resolve())):
            self.send_error(HTTPStatus.FORBIDDEN, "Erişim engellendi.")
            return

        if not hedef_dosya.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Dosya bulunamadı.")
            return

        mime_tipi, _ = mimetypes.guess_type(str(hedef_dosya))
        mime_tipi = mime_tipi or "application/octet-stream"

        try:
            with open(hedef_dosya, "rb") as f:
                icerik = f.read()

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", f"{mime_tipi}; charset=utf-8")
            self.send_header("Content-Length", str(len(icerik)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(icerik)
        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))

    def _json_cevap(self, veri: object, kod: int = 200) -> None:
        govde = json.dumps(veri, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(kod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(govde)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(govde)

    def log_message(self, format: str, *args: object) -> None:
        pass


def sunucuyu_baslat(host: str = "127.0.0.1", port: int = 8080) -> HTTPServer:
    """
    Web sunucusunu başlatır.
    """
    sunucu = HTTPServer((host, port), AriApiHandler)
    return sunucu


if __name__ == "__main__":
    import argparse
    import webbrowser

    parser = argparse.ArgumentParser(description="ari-inler-bal-icinde Web Sunucusu")
    parser.add_argument("--port", type=int, default=8080, help="Sunucu portu (Varsayılan: 8080)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Sunucu hostu")
    parser.add_argument("--open", action="store_true", help="Tarayıcıyı otomatik aç")

    args = parser.parse_args()
    url = f"http://{args.host}:{args.port}"
    print(f"🍯 ari-inler-bal-icinde Web Sunucusu çalışıyor: {url}")

    if args.open:
        webbrowser.open(url)

    sunucu = sunucuyu_baslat(host=args.host, port=args.port)
    try:
        sunucu.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...")
        sunucu.server_close()
