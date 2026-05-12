from conexion import *
import pytest
import requests

class Test_paises:

    def setup_class(self):
        self.url = "http://localhost:5084/paises"
        id = "PP"
        nombre = "Pais_Prueba"
        continente = "Asia"
        sql = f"""INSERT INTO paises (idPais,nombre,continente)VALUES ('{id}','{nombre}','{continente}')"""
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        sql = "DELETE FROM paises WHERE idPais='PP'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_paises(self):
        esperado = "paises"
        calculado = requests.get(self.url)
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"id":"SP","nombre":"Nuevo_Pais","continente":"America"},"País agregado con éxito"),
        ({"id":"PP","nombre":"Pais_Prueba","continente":"Asia"},"Id de país ya existe")])

    def test_agregar(self,nuevo_entrada,esperado_entrada):
        calculado = requests.post(self.url,json=nuevo_entrada)
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("PP","País encontrado"),
        ("PR","País no encontrado")
        ]
    )

    def test_busqueda(self,id_entrada,esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        calculado = requests.get(f"{self.url}/{id}")
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    def test_modifica1(self):
        id = "PP"
        nombre = "Pais_Cambiado"
        continente = "Africa"
        nuevo = {"nombre":nombre,"continente":continente}
        esperado = "País modificado con éxito"
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql = f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre == datos[1] and continente == datos[2]
    def test_modifica2(self):
        id = "QP"
        nombre = "Rusia"
        continente = "Europa"
        nuevo = {"nombre":nombre,"continente":continente}
        esperado = "País no existe"
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("SP","País eliminado con éxito"),
        ("PX","País no existe")
        ]
    )

    def test_elimina(self,id_entrada,esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        calculado = requests.delete(f"{self.url}/{id}")
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        mi_db.commit()
        sql = f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos) == 0