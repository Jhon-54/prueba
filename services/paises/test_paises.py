from conexion import *
import pytest
import requests

class Test_paises:

    def setup_method(self):
        # Limpiar la tabla antes de cada test
        mi_cursor.execute("DELETE FROM paises")
        mi_db.commit()
        self.url = "http://localhost:5084/paises"

    def teardown_method(self):
        # Limpiar la tabla después de cada test
        mi_cursor.execute("DELETE FROM paises")
        mi_db.commit()

    def test_lista_paises(self):
        esperado = "paises"
        respuesta = requests.get(self.url)
        assert respuesta.status_code == 200
        assert respuesta.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            ({"id": "SP", "nombre": "Nuevo_Pais", "continente": "America"}, "País agregado con éxito"),
            ({"id": "PP", "nombre": "Pais_Prueba", "continente": "Asia"}, "Id de país ya existe"),
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        # Insertar PP antes de probar el caso de duplicado
        if nuevo_entrada["id"] == "PP":
            requests.post(self.url, json={"id": "PP", "nombre": "Pais_Prueba", "continente": "Asia"})
        respuesta = requests.post(self.url, json=nuevo_entrada)
        assert respuesta.status_code == 200
        assert esperado_entrada == respuesta.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [("PP", "País encontrado"), ("PR", "País no encontrado")]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        # Insertar PP para que exista
        requests.post(self.url, json={"id": "PP", "nombre": "Pais_Prueba", "continente": "Asia"})
        respuesta = requests.get(f"{self.url}/{id_entrada}")
        assert respuesta.status_code == 200
        assert esperado_entrada in respuesta.json()["mensaje"]

    def test_modifica1(self):
        # Insertar PP para poder modificarlo
        requests.post(self.url, json={"id": "PP", "nombre": "Pais_Prueba", "continente": "Asia"})
        nuevo = {"nombre": "Pais_Cambiado", "continente": "Africa"}
        respuesta = requests.put(f"{self.url}/PP", json=nuevo)
        assert respuesta.status_code == 200
        assert "País modificado con éxito" in respuesta.json()["mensaje"]

    def test_modifica2(self):
        # No insertamos QP, así que no existe
        nuevo = {"nombre": "Rusia", "continente": "Europa"}
        respuesta = requests.put(f"{self.url}/QP", json=nuevo)
        assert respuesta.status_code == 200
        assert "País no existe" in respuesta.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [("SP", "País eliminado con éxito!"), ("PX", "País no existe")]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        # Insertar SP para poder eliminarlo
        if id_entrada == "SP":
            requests.post(self.url, json={"id": "SP", "nombre": "Nuevo_Pais", "continente": "America"})
        respuesta = requests.delete(f"{self.url}/{id_entrada}")
        assert respuesta.status_code == 200
        assert esperado_entrada in respuesta.json()["mensaje"]