from services.editores.conexion import *
from usuarios import mis_usuarios
import pytest
import requests

class Test_usuarios:
    def setup_class(self):
        # Preparación de la prueba
        self.url= "http://localhost:5080/usuarios"
        id = "test2026"
        nombre= "Usuario Pruebas"
        contra= "test"
        cifrada= hashlib.sha512(contra.encode("UTF-8")).hexdigest()
        sql = f"INSERT INTO usuarios (idUsuarios,nombre,contrasena) VALUES ('{id}','{nombre}','{cifrada}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpiar la base de datos
        sql= "DELETE FROM usuarios WHERE idUsuarios='test2026'"
        mi_cursor.execute(sql)
        mi_db.commit()

    @pytest.mark.parametrize(
            ["id_entrada","contra_entrada","esperado_entrada"],
            [("test2026","test","BienvenidoUsuario Pruebas"),
            ("test2026","text","credenciales invalidas"),
            ("test226","text","credenciales invalidas")]
    )

    def test_login(self,id_entrada,contra_entrada,esperado_entrada):
        # Ejecución de caso de prueba 
        id = id_entrada
        contra= contra_entrada
        esperado = esperado_entrada
        cifrada= hashlib.sha512(contra.encode("UTF-8")).hexdigest()
        usuario= {"id": id, "contra":cifrada}
        respuesta= requests.post(f"{self.url}/{id}",json=usuario)
        # Verificacion del caso de prueba
        assert respuesta.status_code==200
        assert respuesta.json()["mensaje"]==esperado

    @pytest.mark.parametrize(
            ["id_entrada","esperado_entrada"],
            [("test2026", "Usuario encontrado: Usuario Pruebas"),
            ("test226", "Usuario no encontrado")]
    )

    def test_consulta(self, id_entrada, esperado_entrada): 
        #La ejecucion de caso de prueba 2
        id = id_entrada
        esperado = esperado_entrada
        respuesta = requests.get(f"{self.url}/{id}")
        #Verificacion del caso de prueba
        assert respuesta.status_code==200
        assert respuesta.json()["mensaje"]==esperado
    
    @pytest.mark.parametrize(
            ["id_entrada","nuevo_entrada","esperado_entrada"],
            [("test2026",{"id":"test2026", "nombre":"Pruebas 2026", "contrasena":"test"}, "Usuario Modificado con exito"),
            ("test226", {"id":"test226", "nombre":"nn","contrasena":"ps"},"Usuario no existe")]
    )

    def test_modifica(self, id_entrada,nuevo_entrada, esperado_entrada): 
        #La ejecucion de caso de prueba 2
        id = id_entrada
        nuevo =nuevo_entrada
        esperado = esperado_entrada
        cifrada= hashlib.sha512(nuevo["contrasena"].encode("UTF-8")).hexdigest()
        nuevo["contrasena"] = cifrada
        respuesta = requests.put(f"{self.url}/{id}",json = nuevo)
        #Verificacion del caso de prueba
        assert respuesta.status_code==200
        assert respuesta.json()["mensaje"]==esperado
        sql = f"SELECT nombre from usuarios WHERE idUsuarios ='{id}'"
        mi_cursor.execute(sql)
        nombre = mi_cursor.fetchall()
        if len (nombre) > 0:
            assert nombre[0][0]=="Pruebas 2026"










"""
def test_login1(self):
        # Ejecución de caso de prueba 1
        id = "test2026"
        contra= "test"
        cifrada= hashlib.sha512(contra.encode("UTF-8")).hexdigest()
        usuario= {"id": id, "contra":cifrada}
        respuesta= requests.post(f"{self.url}/{id}",json=usuario)
        # Verificacion del caso de prueba
        assert respuesta.status_code==200
        assert respuesta.json()["mensaje"]=="Bienvenido Usuario Pruebas"

    def test_login2(self):
        # Ejecución de caso de prueba 1
        id = "test2026"
        contra= "text"
        cifrada= hashlib.sha512(contra.encode("UTF-8")).hexdigest()
        usuario= {"id": id, "contra":cifrada}
        respuesta= requests.post(f"{self.url}/{id}",json=usuario)
        # Verificacion del caso de prueba
        assert respuesta.status_code==200
        assert respuesta.json()["mensaje"]=="Credenciales invalidas"
    
    def test_login3(self):
        # Ejecución de caso de prueba 1
        id = "test226"
        contra= "text"
        cifrada= hashlib.sha512(contra.encode("UTF-8")).hexdigest()
        usuario= {"id": id, "contra":cifrada}
        respuesta= requests.post(f"{self.url}/{id}",json=usuario)
        # Verificacion del caso de prueba
        assert respuesta.status_code==200
        assert respuesta.json()["mensaje"]=="Credenciales invalidas"

"""

