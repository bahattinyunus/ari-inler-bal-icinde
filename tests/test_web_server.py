import json
import threading
import unittest
import urllib.request
from http.server import HTTPServer
from ari_inler_bal_icinde.web_server import AriApiHandler

class TestWebServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), AriApiHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_status_endpoint(self):
        url = f"{self.base_url}/api/status"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["status"], "ok")
            self.assertGreaterEqual(data["toplam_eser"], 25)

    def test_simulate_endpoint(self):
        url = f"{self.base_url}/api/simulate?salik=TestApiSalik&viskozite=2.0"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["salik_adi"], "TestApiSalik")
            self.assertIn("adimlar", data)
            self.assertIn("zar_tecellisi", data)

    def test_corpus_endpoint(self):
        url = f"{self.base_url}/api/corpus"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertIsInstance(data, list)
            self.assertGreaterEqual(len(data), 25)

    def test_corpus_filter_endpoint(self):
        url = f"{self.base_url}/api/corpus?motif=ari-ve-bal"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertGreaterEqual(len(data), 5)

    def test_random_endpoint(self):
        url = f"{self.base_url}/api/random"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertIn("muellif", data)
            self.assertIn("orijinal_metin", data)

    def test_compare_endpoint(self):
        url = f"{self.base_url}/api/compare?id1=pir-sultan-abdal&id2=ramakrishna-tuz-bebek"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertIn("sentez", data)
            self.assertIn("metin_1", data)
            self.assertIn("metin_2", data)

    def test_report_endpoint(self):
        url = f"{self.base_url}/api/report"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertIn("toplam_eser_sayisi", data)
            self.assertIn("gelenek_dagilimi", data)

    def test_matrix_endpoint(self):
        url = f"{self.base_url}/api/matrix"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertIsInstance(data, list)
            self.assertGreaterEqual(len(data), 5)

    def test_static_index(self):
        url = f"{self.base_url}/"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            content = response.read().decode("utf-8")
            self.assertIn("Arı İnler Bal İçinde", content)

if __name__ == "__main__":
    unittest.main()
