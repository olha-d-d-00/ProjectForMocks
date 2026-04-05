import unittest
from unittest.mock import patch, mock_open
import importlib


class TestPokemonReport(unittest.TestCase):

    def setUp(self):
        self.pokemon_info = {
            "height": 4,
            "weight": 60,
            "abilities": [
                {"ability": {"name": "static"}},
                {"ability": {"name": "lightning-rod"}},
            ],
        }

    @patch("pdfkit.configuration")
    def test_create_html_report(self, mock_configuration):
        import pokemon_report
        importlib.reload(pokemon_report)

        report = pokemon_report.PokemonReport()

        with patch("builtins.open", mock_open()) as mocked_file:
            result = report.create_html_report(self.pokemon_info, "Pikachu_FR")

        self.assertEqual(result, "report_template.html")
        mocked_file.assert_called_once_with("report_template.html", "w", encoding="utf-8")

        handle = mocked_file()
        written_html = "".join(call.args[0] for call in handle.write.call_args_list)

        self.assertIn("Pikachu_FR", written_html)
        self.assertIn("4 decimetres", written_html)
        self.assertIn("60 hectograms", written_html)
        self.assertIn("static, lightning-rod", written_html)

    @patch("pdfkit.configuration")
    def test_generate_report_calls_pdfkit_from_file(self, mock_configuration):
        import pokemon_report
        importlib.reload(pokemon_report)

        report = pokemon_report.PokemonReport()

        with patch.object(report, "create_html_report", return_value="report_template.html") as mock_create_html:
            with patch("pokemon_report.pdfkit.from_file") as mock_from_file:
                report.generate_report(self.pokemon_info, "Pikachu_FR", "pokemon_report.pdf")

        mock_create_html.assert_called_once_with(self.pokemon_info, "Pikachu_FR")
        mock_from_file.assert_called_once_with(
            "report_template.html",
            "pokemon_report.pdf",
            configuration=pokemon_report.config,
        )