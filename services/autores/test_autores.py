import requests
from conexion import *
import pytest

class Test_autores:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5082/autores"
        sql = """INSERT INTO paises (idPais,nombre,continente) VALUES('VZ','Venezuela','America'),('CO','Colombia','America')"""
        mi_cursor.execute(sql)
        mi_db.commit()

        id = "01"
        nombre = "pablo"
        email = "pablitogod@gmail.com"
        idPais = "VZ"
        sql = f"INSERT INTO autores (idAutor,nombre,email, idPais) VALUES ('{id}','{nombre}','{email}', '{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        #Limpia la base de datos
        
        sql = "DELETE FROM autores"
        mi_cursor.execute(sql)

        sql = "DELETE FROM paises WHERE idPais IN ('VZ','CO')"
        mi_cursor.execute(sql)
        mi_db.commit()
    
    def test_lista_autores(self):
        esperado = "autores"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"]==esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"idAutor":"02", "nombre":"Usuario Pruebas","email":"6666@gmail.com","idPais":"CO"},"Autor agregado con éxito"),
        ({"idAutor":"01", "nombre":"pablo","email":"pablitogod@gmail.com","idPais":"VZ"},"Id de autor ya existe")]
    )
    
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url,json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]
    
    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("01","Autor encontrado"),
        ("03","Autor no encontrado")]
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
        id = "01"
        nombre = "pablito"
        email = "pablocrak@gmail.com"
        idPais = "CO"
        nuevo = {"nombre":nombre, "email":email, "idPais":idPais}
        esperado = "Autor modificado con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql =f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre==datos[1] and email==datos[2] and idPais ==datos[3]

    # Para cuando el usuario no existe
    def test_modifica2(self):
        id = "000"
        nombre = "Juan"
        email = "Juanitopro@gmail.com"
        idPais = "VZ"
        nuevo = {"nombre":nombre, "email":email, "idPais":idPais}
        esperado = "Autor no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("02","Autor eliminado con éxito!"),
        ("03","Autor no existe")]
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
        sql =f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos)==0