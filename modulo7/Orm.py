
#1- instala sqlalchemy en la consola $ pip install SQLAlchemy
#Nota: La unica diferencia del orm del modulo anterior es que ahora en vez de imprimir resultado los retorno
#importar lo que usaremos
from sqlalchemy import create_engine,MetaData,Column, String,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base() 

class PalabraModel (Base,SerializerMixin):
    __tablename__= "myTableName"
    palabra = Column(String,primary_key=True)
    definicion = Column(String)
    def __init__(self,palabra,definicion):
        self.palabra = palabra
        self.definicion = definicion

def createTable(engine): 
    meta = MetaData()
    mydb = Table(
    'myTableName',meta,
    Column('palabra',String(1000),primary_key=True),
    Column('definicion',String(1000)))
    meta.create_all(engine)


class ORM():
    def __init__(self,nameTable,dialect): 
        self.nameTable = nameTable+'.db' 
        self.dialect = dialect+self.nameTable +'?check_same_thread=False' 
        self.engine = create_engine(self.dialect)  
        if not database_exists(self.engine.url): 
            create_database(self.engine.url)
            createTable(self.engine)
        self.session = sessionmaker(bind = self.engine)() 

    def agregarPalabra(self,palabra,definicion):
        self.session.add(PalabraModel(palabra,definicion))
        self.session.commit()
    
    def obtenerPalabra(self,palabra):
        try:
            resultado = self.session.query(PalabraModel).filter(PalabraModel.palabra == palabra).one()
            return resultado
        except:
            pass
       
    
    def obtenerTodo(self):
        resultado = self.session.query(PalabraModel).all()
        return resultado
    
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
    
#dialectoSQLITE = 'sqlite:///'
#sql = ORM('MyTableName',dialectoSQLITE)
#DIALECTO PARA MARIADB
#sql = ORM('MyTableName',dialectoMARIADB)
#Estos son algunos ejemplo de lo que puedes hacer
#sql.agregarPalabra('newPalabra','newDefinicion')
#sql.editarPalbra('palabra','palabraEditada')
#sql.editarDefinicion('palabra','definicionEditada')
#sql.obtenerTodo()
#sql.borrarPalabra('palabra')