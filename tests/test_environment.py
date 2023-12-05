import unittest
from unittest.mock import patch
from datetime import datetime
from environment import (
    keys,
    agora,
    almoco,
    jantar,
    dia_da_semana,
    cardapio,
    restaurantes,
)


class TestEnvironmentModule(unittest.TestCase):
    def test_keys_exist(self):
        self.assertTrue(keys["CONSUMER_KEY"])
        self.assertTrue(keys["CONSUMER_SECRET"])
        self.assertTrue(keys["ACCESS_KEY"])
        self.assertTrue(keys["ACCESS_SECRET"])

    def test_temporal_information(self):
        now = datetime.now()
        self.assertEqual(almoco, now.hour <= 14 and now.weekday() < 5)
        self.assertEqual(jantar, now.hour > 14 or now.weekday() >= 5)
        self.assertIn(dia_da_semana, range(7))

    def test_cardapio_structure(self):
        expected_keys = [
            "proteina_1",
            "proteina_2",
            "proteina_3",
            "guarnicao",
            "acompanhamento_1",
            "acompanhamento_2",
            "acompanhamento_3",
            "entrada_1",
            "entrada_2",
            "entrada_3",
            "sobremesa_1",
            "sobremesa_2",
            "refresco",
            "molho_salada",
        ]
        self.assertEqual(list(cardapio.keys()), expected_keys)

    def test_restaurantes_structure(self):
        expected_restaurantes_keys = [
            "RU_SETORIAL_I",
            "RU_SETORIAL_II",
            "RU_SAUDE_E_DIREITO",
            "RU_ICA",
        ]
        self.assertEqual(list(restaurantes.keys()), expected_restaurantes_keys)


if __name__ == "__main__":
    unittest.main()
