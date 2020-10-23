from flask import Flask,jsonify,render_template,request
from flask_restful import Api, Resource, reqparse
from marshmallow import Schema, fields
from Orm import ORM

class PalabraModel(Schema):
    palabra = fields.Str()
    definicion = fields.Str()

app = Flask(__name__)
api = Api(app)

Palabras = [{'id':1,'title':'mtitle'}]

class Palabra(Resource):
     dialectoSQLITE = 'sqlite:///'
     orm = ORM('MyTableName',dialectoSQLITE)
     def get(self, palabra=''): 
         if palabra == '':
            return PalabraModel(many=True).dump(self.orm.obtenerTodo()), 200
         
         if PalabraModel().dump(self.orm.obtenerPalabra(palabra)):
             return PalabraModel().dump(self.orm.obtenerPalabra(palabra))
         else:
             return "No hay resultado", 404

     def post(self, palabra):
        parser = reqparse.RequestParser()
        parser.add_argument("definicion")
        params = parser.parse_args()
        try:
            self.orm.agregarPalabra(palabra,params['definicion'])
            return palabra, 201
        except:
            return f"la palabra {palabra} ya existe", 400
        

     def put(self, palabra):
        parser = reqparse.RequestParser()
        parser.add_argument("definicion")
        parser.add_argument("nuevaPalabra")
        params = parser.parse_args()
        try:
            self.orm.editarDefinicion(palabra,params['definicion'])
            self.orm.editarPalbra(palabra,params['nuevaPalabra'])
            return 'cambio exitoso', 200
        except:
            return f"la palabra {palabra} no  existe", 400

     def delete(self, palabra):
      try:
         self.orm.borrarPalabra(palabra)
         return f"la palabra {palabra} ha sido borrado", 200 
      except:
          return f"la palabra {palabra} no existe", 400
      

api.add_resource(Palabra, "/palabra", "/palabra/", "/palabra/<string:palabra>")

@app.route('/',methods=['GET','POST'])
def index():
    dialectoSQLITE = 'sqlite:///'
    orm = ORM('MyTableName',dialectoSQLITE) 
    tabla = orm.obtenerTodo()
    if 'refrescar' in request.form:
        try:
            orm = ORM('MyTableName',dialectoSQLITE)
            tabla = orm.obtenerTodo()
        except:
            pass
    return render_template('index.html',tabla=tabla)

if __name__ == '__main__':
    app.run(debug=True)
