import sys
import types
import importlib
import unittest
from unittest.mock import MagicMock, patch


class TestPokemonNameTranslator(unittest.TestCase):

    def test_translate_returns_translated_text(self):
        fake_translate_module = types.ModuleType("translate")
        fake_client_class = MagicMock()
        fake_translate_module.TranslationServiceClient = fake_client_class

        fake_google_module = types.ModuleType("google")
        fake_cloud_module = types.ModuleType("google.cloud")
        fake_cloud_module.translate = fake_translate_module
        fake_google_module.cloud = fake_cloud_module

        with patch.dict(sys.modules, {
            "google": fake_google_module,
            "google.cloud": fake_cloud_module,
            "google.cloud.translate": fake_translate_module,
        }):
            import pokemon_name_translator
            importlib.reload(pokemon_name_translator)

            mock_client = MagicMock()
            fake_client_class.return_value = mock_client

            mock_client.location_path.return_value = "projects/your-project-id/locations/global"

            mock_translation = MagicMock()
            mock_translation.translated_text = "Pikachu_FR"

            mock_response = MagicMock()
            mock_response.translations = [mock_translation]
            mock_client.translate_text.return_value = mock_response

            translator = pokemon_name_translator.PokemonNameTranslator()
            result = translator.translate("pikachu", target_language="fr")

            mock_client.location_path.assert_called_once_with("your-project-id", "global")
            mock_client.translate_text.assert_called_once_with(
                parent="projects/your-project-id/locations/global",
                contents=["pikachu"],
                target_language_code="fr",
            )
            self.assertEqual(result, "Pikachu_FR")