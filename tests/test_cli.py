import io
import unittest
from contextlib import redirect_stdout
from ari_inler_bal_icinde.cli import main

class TestCLI(unittest.TestCase):
    def test_cli_simule(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            kod = main(["simule", "--salik", "TestSalik", "--hizli"])
        self.assertEqual(kod, 0)
        cikis = buf.getvalue()
        self.assertIn("ARİ İNLER BAL İÇİNDE", cikis)
        self.assertIn("TestSalik", cikis)
        self.assertIn("ZÂR VE VECİD TECELLEİSİ", cikis)

    def test_cli_matris(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            kod = main(["matris"])
        self.assertEqual(kod, 0)
        cikis = buf.getvalue()
        self.assertIn("SURET (ZÂHİR / AVAM) İLE HAKİKAT", cikis)
        self.assertIn("Fail Kimdir?", cikis)

    def test_cli_divan(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            kod = main(["divan", "-a", "Pir Sultan"])
        self.assertEqual(kod, 0)
        cikis = buf.getvalue()
        self.assertIn("Pir Sultan Abdal", cikis)

    def test_cli_zar(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            kod = main(["zar", "--benlik", "0.1"])
        self.assertEqual(kod, 0)
        cikis = buf.getvalue()
        self.assertIn("AKUSTİK ZÂR VE FREKANS ANALİZİ", cikis)
        self.assertIn("Harmonikler", cikis)

    def test_cli_manifesto(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            kod = main(["manifesto"])
        self.assertEqual(kod, 0)
        cikis = buf.getvalue()
        self.assertIn("İLLÜZYONUN YIKILIŞI", cikis)
        self.assertIn("HAYRET MAKAMI", cikis)

    def test_cli_help_no_args(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            kod = main([])
        self.assertEqual(kod, 0)
        self.assertIn("usage", buf.getvalue().lower())

if __name__ == "__main__":
    unittest.main()
