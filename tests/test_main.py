import sys
import types
import importlib
import unittest
from unittest.mock import MagicMock, patch


class TestMain(unittest.TestCase):

    def test_main_success_flow(self):
        fake_service_class = MagicMock()
        fake_translator_class = MagicMock()
        fake_report_class = MagicMock()

        fake_service_instance = MagicMock()
        fake_translator_instance = MagicMock()
        fake_report_instance = MagicMock()

        fake_service_class.return_value = fake_service_instance
        fake_translator_class.return_value = fake_translator_instance
        fake_report_class.return_value = fake_report_instance

        fake_service_instance.get_pokemon_info.return_value = {
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "abilities": [{"ability": {"name": "static"}}],
        }
        fake_translator_instance.translate.return_value = "Pikachu_FR"

        fake_pokemon_service_module = types.ModuleType("pokemon_service")
        fake_pokemon_service_module.PokemonService = fake_service_class

        fake_pokemon_name_translator_module = types.ModuleType("pokemon_name_translator")
        fake_pokemon_name_translator_module.PokemonNameTranslator = fake_translator_class

        fake_pokemon_report_module = types.ModuleType("pokemon_report")
        fake_pokemon_report_module.PokemonReport = fake_report_class

        with patch.dict(sys.modules, {
            "pokemon_service": fake_pokemon_service_module,
            "pokemon_name_translator": fake_pokemon_name_translator_module,
            "pokemon_report": fake_pokemon_report_module,
        }):
            import main
            importlib.reload(main)

            main.main()

        fake_service_instance.get_pokemon_info.assert_called_once_with("pikachu")
        fake_translator_instance.translate.assert_called_once_with("pikachu", target_language="fr")
        fake_report_instance.generate_report.assert_called_once_with(
            {
                "name": "pikachu",
                "height": 4,
                "weight": 60,
                "abilities": [{"ability": {"name": "static"}}],
            },
            "Pikachu_FR",
            "pokemon_report.pdf",
        )

    def test_main_pokemon_not_found(self):
        fake_service_class = MagicMock()
        fake_translator_class = MagicMock()
        fake_report_class = MagicMock()

        fake_service_instance = MagicMock()
        fake_translator_instance = MagicMock()
        fake_report_instance = MagicMock()

        fake_service_class.return_value = fake_service_instance
        fake_translator_class.return_value = fake_translator_instance
        fake_report_class.return_value = fake_report_instance

        fake_service_instance.get_pokemon_info.return_value = None

        fake_pokemon_service_module = types.ModuleType("pokemon_service")
        fake_pokemon_service_module.PokemonService = fake_service_class

        fake_pokemon_name_translator_module = types.ModuleType("pokemon_name_translator")
        fake_pokemon_name_translator_module.PokemonNameTranslator = fake_translator_class

        fake_pokemon_report_module = types.ModuleType("pokemon_report")
        fake_pokemon_report_module.PokemonReport = fake_report_class

        with patch.dict(sys.modules, {
            "pokemon_service": fake_pokemon_service_module,
            "pokemon_name_translator": fake_pokemon_name_translator_module,
            "pokemon_report": fake_pokemon_report_module,
        }):
            with patch("builtins.print") as mock_print:
                import main
                importlib.reload(main)

                main.main()

        fake_service_instance.get_pokemon_info.assert_called_once_with("pikachu")
        fake_translator_instance.translate.assert_not_called()
        fake_report_instance.generate_report.assert_not_called()
        mock_print.assert_called_once_with("Pokemon not found.")