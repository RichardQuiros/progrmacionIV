#1- instala redis $ pip install redis
#2- descarga y instala redis *WINDOWS https://github.com/MicrosoftArchive/redis/releases VIDEO https://youtu.be/gmcfZYA47_8
#3- inicializa tu servidor redis y tu cliente  *WINDOWN redis-cli
import redis

#Crearemos unca clase para facilitar su uso
#como constructor agregamos los paremotros que necesita para poder conectarse a su servidor de redis
class REDIS():
    def __init__(self,host,port,db):
        self.host = host
        self.port = port
        self.db = db
        #inicicaliza redis
        self.redisdb = redis.Redis(host=self.host,port=self.port,db=self.db)
    
    #Algunas funciones consumiendo redis
    #Redis a diferencia de mongo no posee collection ni documento es decir que puedes acceder a cualquier valor sabiendo su solo su key gracias a esta cualidad es muy utilizado
    #en cache ademas como mongo el codifica su contenido sus datos para que sea mas rapido por eso al obtener datos te lo dara codificado y lo puedes descodificar usando .decode('utf-8') 

    #los comando de redis que comienzan con h hace referencia a Hashes que estos almacenan datos a igual que un diccionario o json
    #es decir que hmset quiere decir hashes multi ser,hgetall:hashes get all etc..
    def agregarPalabra(self,palabra,definicion):
        data = {'palabra':palabra,'definicion':definicion}
        self.redisdb.hmset('Palabras:'+palabra,data)

    def obtenerPalabra(self,palabra):
        resultado = self.redisdb.hgetall('Palabras:'+palabra)
        return {list(resultado.keys())[0].decode('utf-8'):resultado[list(resultado.keys())[0]].decode('utf-8'),list(resultado.keys())[1].decode('utf-8'):resultado[list(resultado.keys())[1]].decode('utf-8')}


    def obtenerTodo(self):
        res = self.redisdb.keys('Palabras:*')
        data = []
        for info in res:
            data.append(info.decode('utf-8'))
        result=[]
        for info in data:
            result.append(self.getByKey(info))
        return result

    def editarPalabra(self,palabra,newPalabra):
        data = {'palabra':newPalabra}
        self.redisdb.hmset('Palabras:'+palabra,data)

    def editarDefinicion(self,palabra,definicion):
        data = {'definicion':definicion}
        self.redisdb.hmset('Palabras:'+palabra,data)

    def borrarPalabra(self,palabra):
        self.redisdb.delete('Palabras:'+palabra)
    
    #esta funcion soluciona un problema al intentar pedir todo los valores de todas mis hashes;devuelve todas los nombres de mis hashes asi es mas facil hacer un bucle y pedir el valor uno por uno en un loop
    def getByKey(self,key):
        res = self.redisdb.hgetall(key)
        value = {id:key}
        for k,v in res.items():
            value[k.decode('utf-8')]=v.decode('utf-8')
        res = value
        return res
    def obtenerLlaves(self):
        res = self.redisdb.keys('Palabras:*')
        val = []
        for item in res:
            data = item.decode('utf-8') 
            val.append(data[9:len(data)]) 
        return val

#RedisDB = REDIS('localhost',6379,0)
#RedisDB.agregarPalabra('myPalabra','myDefinicion')
#RedisDB.editarPalabra('myPalabra','newPalbra')
#RedisDB.editarDefinicion('myPalabra','newDefinicion')
#RedisDB.obtenerPalabra('myPalabra')
#RedisDB.obtenerTodo()
#RedisDB.borrarPalabra('myPalabra')
        
#RESUMEN
#Redis es bastante rapido acceder a valores gracias a como esta estructurado 