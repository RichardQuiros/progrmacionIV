#Antes que nada y si te pasa como ami que sale muchos errores en session, no te preocupes creo que es un error de el editor de texto por que esta funcional


#1- instala sqlalchemy en la consola $ pip install SQLAlchemy
#2- descarga y instala mariadb https://mariadb.org/download/
#3- abre HeidiSQL que se instala al instalar mariadb
#3- crea un nuevo proyecto con su usuario y contraseña *IMPORTANTE: establece permisos para que pueda interactuar con la tabla, requiere reinicio de el programa

#importar lo que usaremos
from sqlalchemy import create_engine,MetaData,Column, String,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

#declara la "base/modelo/tabla" esto lo utiliza para taransformar esa clase a una tabla sql 
Base = declarative_base() 

#crearemos una clase que sera el modelo de la tabla palabra, con el  podemos llamar a todas la colummna y valores de la tabla
class PalabraModel (Base):
    __tablename__= "myTableName"
    palabra = Column(String,primary_key=True)
    definicion = Column(String)
    def __init__(self,palabra,definicion):
        self.palabra = palabra
        self.definicion = definicion

#esta es una funcion que al llamarlo junto al engine nos creara la tabla 
def createTable(engine): 
    meta = MetaData()
    mydb = Table(
    'myTableName',meta,
    Column('palabra',String(1000),primary_key=True),
    Column('definicion',String(1000)))
    meta.create_all(engine)

#crearemos una clase para poder usar mas facil sqlalchemy se llamara ORM
class ORM():
    # requiere el nombre de la tabla y el dialegto de la base de datos, hay muchas pero usaremos el dialecto de mariadb que esta basado en mysql
    def __init__(self,nameTable,dialect): 
        # concatenamos .db alo que el usuario introduzca, lo requerimos para el dialecto
        self.nameTable = nameTable+'.db' 
        #Esto concatenara el dialecto introducido mas el nombre de la tabla <Dialecto+MyTableName>
        #necesitamos el dialecto para que el engine sepa manejar las tablas con su respectivo sql; es como decir motor trabaja con disel
        self.dialect = dialect+self.nameTable
        #inicializamos/encendemos el motor pasandole el parametro dialecto
        self.engine = create_engine(self.dialect)  

        #este es un simple verificador que crea la base de datos si no existe; utiliza la funcion creada anteriormente
        if not database_exists(self.engine.url): 
            create_database(self.engine.url)
            createTable(self.engine)
           

        self.session = sessionmaker(bind = self.engine)() # iniciamos session con el engine para manejar la base de datos

    # Estas funciones utilizaran la session para realizar distintas operaciones sql

    def agregarPalabra(self,palabra,definicion):
        self.session.add(PalabraModel(palabra,definicion))
        self.session.commit()
    
    def obtenerPalabra(self,palabra):
        resultado = self.session.query(PalabraModel).filter(PalabraModel.palabra == palabra).one()
        print('Palabra:'+resultado.palabra+' Definicion:'+resultado.definicion)
    
    def obtenerTodo(self):
        resultado = self.session.query(PalabraModel).all()
        for informacion in resultado:
            print('Palabra:'+informacion.palabra+' Definicion:'+informacion.definicion+'\n')
    
    def editarPalbra(self,palabra,newPalabra):
        resultado = self.session.query(PalabraModel).filter(PalabraModel.palabra == palabra).one()
        resultado.palabra = newPalabra
        self.session.add(resultado)
        self.session.commit()
    
    def editarDefinicion(self,palabra,definicion):
        resultado = self.session.query(PalabraModel).filter(PalabraModel.palabra == palabra).one()
        resultado.definicion = definicion
        self.session.add(resultado)
        self.session.commit()
    
    def borrarPalabra(self,palabra):
        resultado = self.session.query(PalabraModel).filter(PalabraModel.palabra == palabra).one()
        self.session.delete(resultado)
        self.session.commit()

#este es el dialecto para mariadb requiere <nombredeUsuario><password> es importante que este usuario tenga permisos para trabajar con la tabla
dialectoMARIADB = 'mysql+pymysql://myUserName:mypass@localhost/'
dialectoSQLITE = 'sqlite:///'
#sql sera nuestro manager de orm
#DIALECTO PARA SQLITE
#sql = ORM('MyTableName',dialectoSQLITE)
#DIALECTO PARA MARIADB
sql = ORM('MyTableName',dialectoMARIADB)
#Estos son algunos ejemplo de lo que puedes hacer
#sql.agregarPalabra('newPalabra','newDefinicion')
#sql.editarPalbra('palabra','palabraEditada')
#sql.editarDefinicion('palabra','definicionEditada')
#sql.obtenerTodo()
#sql.borrarPalabra('palabra')

#RESUMEN
#En resumen los ORM es una especie de traductor de Sintaxis de lenguaje sql, o lo puedes visaulizar como una motor que transforma un modelo
#a una tabla sql

#NOTA: esto es un ejemplo practico si quieres saber mas de aspectos tecnicos y ver las buenas practicas; ver la documentacion oficial  