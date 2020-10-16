#sqlite3 1- haces conexion con una tabla 2- creas un cursor 3- creas una funcion de crear/actulizar/borrar etc 4-si lo requiere commit 5-cerrar la conexion

import sqlite3
tableName= 'myTabla.db'

#crear tabla
def crearTabla():
    sql = sqlite3.connect(tableName)
    cursor = sql.cursor()
    cursor.execute("CREATE TABLE TableName(palabra text,definicion text)")
    print('La tabla se ha creado')
    sql.close()

#obtener palabra 
def obtenerTodasLasPalabra():
    sql = sqlite3.connect(tableName)
    cursor = sql.cursor()
    cursor.execute("SELECT * FROM TableName")
    print("Lista de palabras \n")
    for listpalabras in cursor.fetchall():
        print(listpalabras[0]+"\n")
    sql.close()

#obtener todas las palabra 
def obtenerPalabra(palabra):
    sql = sqlite3.connect(tableName)
    cursor = sql.cursor()
    cursor.execute("SELECT * FROM TableName WHERE palabra=:palabra",{'palabra':palabra})
    print(cursor.fetchone())
    sql.close()

#agregar Palabra
def agregarPalabra(palabra,definicion):
    sql = sqlite3.connect(tableName)
    cursor = sql.cursor()
    cursor.execute("INSERT INTO TableName  VALUES (:palabra,:definicion)",{'palabra':palabra,'definicion':definicion})
    sql.commit()
    sql.close()
    print('se a posteado exitosamente')

#editar Palabra
def editarPalabra(palabra,nuevaPalabra):
    sql = sqlite3.connect(tableName)
    cursor = sql.cursor()
    cursor.execute("UPDATE TableName SET palabra=:nuevaPalabra WHERE palabra=:palabra",{'palabra':palabra,'nuevaPalabra':nuevaPalabra})
    sql.commit()
    sql.close()
    print('palabra actualizada')

#editar definicion
def editarDefinicion(palabra,definicion):
    sql = sqlite3.connect(tableName)
    cursor = sql.cursor()
    cursor.execute("UPDATE TableName SET definicion=:definicion WHERE palabra=:palabra",{'palabra':palabra,'definicion':definicion})
    sql.commit()
    sql.close()
    print('definicion actualizada')

#delete Palabra
def deletePalabra(palabra):
    sql = sqlite3.connect(tableName)
    cursor = sql.cursor()
    cursor.execute("DELETE FROM TableName WHERE palabra=:palabra",{'palabra':palabra})
    sql.commit()
    sql.close()
    print('palabra eliminada')

# Definicion de la funcion y sus requirimiento
# <Ejemplo de la funcion>

#para crear tabla
#crearTabla()

#agregar palbra requiere <palabara> <definicion>
#agregarPalabra('myPalabra','myDefinicion')

#editar palabra requiere <palabra> <nuevaPalabra>
#editarPalabra('myPalabra','PalabraEdiatada')

#editar definicion palabra requiere <palabra> <nuevaDefinicion>
#editarDefinicion('PalabraEdiatada','definicionEditada')

#obtener palabra requiere <palabra>
#obtenerPalabra('PalabraEdiatada')

#obtener todas las palabras
#obtenerTodasLasPalabra()

#borrar palabra requiere <palabra>
#deletePalabra('PalabraEdiatada')