from conexiones import *
from usuarios import mis_usuarios

programa = Flask(__name__)
api = Api(programa)

class ListaUsuarios(Resource):
    def get(self):
        usuarios = mis_usuarios.listar()
        return jsonify(usuarios)
    
    def post(self):
        nuevo=request.json
        mis_usuarios.agregar(nuevo ["id"], nuevo["nom"], nuevo["contra"])
        return jsonify({"mensaje":"Usuario Agregado con exito"})
    

class Usuarios(Resource):
    def get(self,id):
        resultado= mis_usuarios.consultar(id)
        if len(resultado)==0:
            return jsonify({"mensaje":"Usuario no encontrado"})
        else:
            return jsonify({"mensaje":"Usuario encontrado: "+resultado[0][1],"data":resultado[0]})
    

    def put(self,id):
        nuevo=request.json
        resultado = mis_usuarios.consultar(id)
        if len(resultado)==0:
            return jsonify({"mensaje":"Usuario no existe"})
        else:
            mis_usuarios.modificar(nuevo["id"], nuevo["nombre"],nuevo["contrasena"])
            return jsonify({"mensaje":"Usuario Modificado con exito"})
    

    def delete(self,id):
        resultado =  mis_usuarios.consultar(id)
        if len(resultado)==0:
            return jsonify ({"mensajes":"Usuario no existe"})
        else:
            mis_usuarios.eliminar(id)
            return jsonify ({"mensaje":"Usuario eliminado con exito"})
        
    def post(self,id):
        nuevo=request.json
        resultado = mis_usuarios.login(id,nuevo["contra"])
        if resultado["entra"]:
            return jsonify({"mensaje":"Bienvenido"+resultado["nombre"]})
        else:
            return jsonify (resultado)

api.add_resource(ListaUsuarios, "/usuarios")
api.add_resource(Usuarios,"/usuarios/<id>")
if __name__ =="__main__":
    programa.run (host="0.0.0.0", debug= True, port=5080)
