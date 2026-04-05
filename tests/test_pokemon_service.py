import unittest
from unittest.mock import patch, MagicMock

from pokemon_service import PokemonService


class TestPokemonService(unittest.TestCase):

    @patch("pokemon_service.requests.get")
    def test_get_pokemon_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "pikachu", "height": 4}

        mock_get.return_value = mock_response

        service = PokemonService()
        result = service.get_pokemon_info("pikachu")

        mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/pikachu")
        self.assertEqual(result, {"name": "pikachu", "height": 4})

    @patch("pokemon_service.requests.get")
    def test_get_pokemon_info_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404

        mock_get.return_value = mock_response

        service = PokemonService()
        result = service.get_pokemon_info("unknown")

        mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/unknown")
        self.assertIsNone(result)