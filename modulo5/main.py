#1- intalar flask $ pip install flask

#nota: en este modulo usaremos mucho el request post, para la interaccion entre la web
#y el servidor 
#render_templates se utiliza para renderizar html,request para manejar peticiones
#INICIAR SERVIDOR solo ejecuta esta codigo y te dara el enlace generalmente es http://127.0.0.1:5000/

#COMO FUNCIONA Aunque se vea mucho texto es bastante simple y repetitivo la idea principal es que el servidor haga una funcion dependiendo de que petcion recibe de la web
#estas peticiones alteraran el valor de la variable tabla y esa variable se envia ala pagina web. la tabla obtiene su valor desde el orm con dialecto sqlite
from flask import Flask,render_template, request
from Orm import ORM

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    dialectoSQLITE = 'sqlite:///'
    orm = ORM('MyTableName',dialectoSQLITE) 
    tabla = orm.obtenerTodo()
    value = ''
    if 'refrescar' in request.form:
        try:
            orm = ORM('MyTableName',dialectoSQLITE)
            tabla = orm.obtenerTodo()
        except:
            pass
    elif 'obtener' in request.form:
        try:
            orm = ORM('MyTableName',dialectoSQLITE)
            tabla = orm.obtenerPalabra(request.form.to_dict().get("obtener"))
            if not (isinstance(tabla,list)):
                tabla = [tabla]
        except:
            pass
    elif 'agregar' in request.form:
        try:
            value = request.form.to_dict()
            orm = ORM('MyTableName',dialectoSQLITE)
            orm.agregarPalabra(request.form.to_dict().get("palabra"),request.form.to_dict().get("definicion"))
        except:
            pass
    elif 'editarPalabra' in request.form:
        try:
            orm = ORM('MyTableName',dialectoSQLITE)
            orm.editarPalbra(request.form.to_dict().get("palabra"),request.form.to_dict().get("editarPalabra"))
        except:
            pass
    elif 'editarDefinicion' in request.form:
            orm = ORM('MyTableName',dialectoSQLITE)
            orm.editarDefinicion(request.form.to_dict().get("palabra"),request.form.to_dict().get("definicion"))
    elif 'borrar' in request.form:
        try:
            orm = ORM('MyTableName',dialectoSQLITE)
            orm.borrarPalabra(request.form.to_dict().get("palabra"))
        except:
            pass

    return render_template('index.html',tabla=tabla,value=value)

if __name__ == '__main__':
    app.run(debug=True)
    