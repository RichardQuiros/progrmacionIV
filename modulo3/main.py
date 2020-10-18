#-1 instalar pymongo  en consola $ pip install pymongo
#-2 descargar y instalar MongoDB  https://www.mongodb.com/try/download/community hay una configuracion adicional para windowns https://www.youtube.com/watch?v=2KMQdqDk9e8
#-3 en cualquiera consola ejecutar $ mongod
#importamos lo que usaremos
from pymongo import MongoClient

# Crearemos una clase para hacer mas facil la interaccion
class MONGO():
    def __init__(self,nombreDB,host,port=None,user=None,password=None):
        #Hay dos formas en que le usuario puede acceder asu database una es con credenciales de usurio y la otra sin ellas
        #esto verifica cual de las dos formas el usuario quiere ingresar y asigna esos parametros
        if(user != None and user != ''):
            self.mongoUser = MongoClient(host,int(port),user,password)
        else:
            self.mongoUser = MongoClient(host,int(port))
        #solo falta inicializar el usuario para que pueda interactuar con la base de datos
        self.db = self.mongoUser[nombreDB]
        self.database = self.db.myTableName

    #las siguientes son funciones donde se utiliza db para interactuar con la base de datos
    def agregarPalabra(self,palabra,definicion):
        data = {'palabra':palabra,'definicion':definicion}
        self.database.insert_one(data)
    
    def obtenerPalabra(self,palabra):
        data = {'palabra':palabra}
        resultado = self.database.find_one(data)
        print('palabra:'+resultado['palabra']+' definicion:'+resultado['definicion'])
    
    def obtenerTodo(self):
        resultado = self.database.find()
        print('Lista de palabras')
        for informacion in resultado:
            print(informacion['palabra']+'\n')
    
    def editarPalabra(self,palabra,newPalabra):
        data = {'palabra':palabra}
        newData = {'palabra':newPalabra}
        self.database.update_one(data,{"$set":newData})

    def editarDefinicion(self,palabra,newDefinicion):
        data = {'palabra':palabra}
        newData = {'definicion':newDefinicion}
        self.database.update_one(data,{"$set":newData})

    def borrarPalabra(self,palabra):
        data = {'palabra':palabra}
        self.database.delete_many(data)

#Algunos ejemplos de uso 
#Antes debes inicializar el server de mongo desde el shell escribiendo $ mongod 
#en shell dice todos los parametros que usaremos por lo general el de abajo funciona bien
db = MONGO('myTableName','localhost',27017,'')
#db.agregarPalabra('myPalabra','myDefinicion')
#db.editarPalabra('myPalabra','newPalabra')
#db.editarDefinicion('myPalabra','newDefinicion')
#db.obtenerPalabra('myPalabra')
#db.obtenerTodo()
#db.borrarPalabra('myPalabra')

#RESUMEN 
#Las base de datos no sql generalmente se organiza DATBASE ---> COLLECCION ---> DOCUMENTO; en donde database guarda las colleciones
#las colleciones guardan documentos y los documentos guardan los datos en un formato json; el cual es muy parecido a un boletin de notas
#en donde el nombre a quien le pertenece es el nombre del documento, el nombre de la materia es la llave y la calificacion es el valor;

#NOTA: esto es un ejemplo practico si quieres saber mas de aspectos tecnicos y ver las buenas practicas; ver la documentacion oficial  