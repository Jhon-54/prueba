import requests
from conexion import *
import pytest

class Test_editoriales:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5083/editoriales"

        sql = "INSERT IGNORE INTO paises (idPais,nombre) VALUES ('VZ','Venezuela')"
        mi_cursor.execute(sql)
        sql = "INSERT IGNORE INTO paises (idPais,nombre) VALUES ('CO','Colombia')"
        mi_cursor.execute(sql)

        id = "Col2"
        nombre = "test3"
        idPais = "VZ"
        sql = f"INSERT INTO editoriales (idEditorial,nombre,idPais) VALUES ('{id}','{nombre}','{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        sql = "DELETE FROM editoriales WHERE idEditorial IN ('Col2', 'Col3')"
        mi_cursor.execute(sql)
        mi_db.commit()
    
    def test_lista_editoriales(self):
        esperado = "editoriales"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"]==esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"idEditorial":"Col3", "nombre":"test4","idPais":"CO"},"Editorial agregada con éxito"),
        ({"idEditorial":"Col2", "nombre":"test3","idPais":"VZ"},"Id de editorial ya existe")]
    )
    
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url,json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]
    
    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("Col2","Editorial encontrada"),
        ("Col4","Editorial no encontrada")]
    )
    
    def test_busqueda(self,id_entrada,esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    # Para cuando el usuario existe y se modifica con éxito
    def test_modifica1(self):
        id = "Col2"
        nombre = "pablito"
        idPais = "VZ"
        nuevo = {"nombre":nombre, "idPais":idPais}
        esperado = "Editorial modificada con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql =f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre==datos[1] and idPais ==datos[2]

    # Para cuando el usuario no existe
    def test_modifica2(self):
        id = "Ven2"
        nombre = "test5"
        idPais = "VZ"
        nuevo = {"nombre":nombre, "idPais":idPais}
        esperado = "Editorial no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("Col2","Editorial eliminada con éxito!"),
        ("Col4","Editorial no existe")]
    )
    def test_elimina(self,id_entrada, esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.delete(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        mi_db.commit()
        sql =f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos)==0        