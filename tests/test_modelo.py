import unittest
from models.datos_model import normalizar_registro


class TestNormalizarRegistro(unittest.TestCase):
    def setUp(self):
        self.registro = {
            "cod_eve": "210",
            "nombre": "Dengue",
            "ano": "2018",
            "semana": "1",
            "cod_dpto_o": "8",
            "nom_mun": "Barranquilla",
            "cod_mun_o": "8001",
            "conteo_casos": "15",
        }

    def test_mapea_campos_de_sivigila(self):
        id_api, campos, original = normalizar_registro(self.registro)
        self.assertEqual(len(id_api), 64)
        self.assertEqual(campos["nombre"], "Dengue")
        self.assertEqual(campos["ano"], 2018)
        self.assertEqual(campos["conteo_casos"], 15)
        self.assertIn('"nom_mun":"Barranquilla"', original)

    def test_hash_estable_para_mismo_registro(self):
        primera = normalizar_registro(self.registro)[0]
        segunda = normalizar_registro(dict(self.registro))[0]
        self.assertEqual(primera, segunda)

    def test_falla_si_campo_numerico_no_es_entero(self):
        registro = dict(self.registro)
        registro["semana"] = "primera"
        with self.assertRaises(ValueError):
            normalizar_registro(registro)


if __name__ == "__main__":
    unittest.main()
