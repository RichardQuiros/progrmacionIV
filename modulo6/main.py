import requests

#Hay un problema con swapi que es que nos da un numero limitado de resultados, y necesitamos todos para para pode compar
#esta fucion devolvera todo los resultados, iterando de pagina en pagina
def obtenerTodo(url):
    next = url
    data = []
    #la logica seria algo asi: mientras la respuesta contiene next url entonces dame el resultado y pasa a la siguiente pagina 
    while next:
        res = requests.get(next)
        res = res.json()
        next = res['next'
        #este for se debe a que el resulatado de cadad pagina queda alojado dentro de un array y esto provoca con no padramos iterar por
        #todo los valores; esta for devueleve cada item y lo aloja en un array en commun
        for item in res['results']:
            data.append(item)
    return data

#una vez ya se pude obtener todo pues ya solo es cuestion de iterar y verificar
def obtenerPlanetsPorClima(url,clima):
    planets = obtenerTodo(url)
    data = []
    for item in planets:
        if item['climate'] == clima:
            data.append(item)
    return data

#en este caso no solo basta con iterar si no tambien parsear el resultado en numeros(float), en este caso los numeros desde swapi pueden
#tener coma pero no parsear numeros con coma asi que lo cambiamos con nada ','->'' asi si se puede parsear
def obtenerNaveMasGrande(url):
    waves = obtenerTodo(url)
    data = waves[0]
    for item in waves:
        print(item['length']+ ' > ' +data['length'])
        print(float(item['length'].replace(',', '')) > float(data['length'].replace(',', '')))
        if float(item['length'].replace(',', '')) > float(data['length'].replace(',', '')):
            data = item
    return data


#En este caso necesitaremos obtener primero todos los personajes de la pelicula y despues obtener la espcecie de cada personaje para finalmente verificar si concide con la especie
#que se esta buscando
def apracionDeEspeciePorPelicula(pelicula,especie):
    especie = especie
    req = requests.get(pelicula)
    req = req.json()
    peliculaPersonajes = req['characters']
    res = []
    for item in peliculaPersonajes:
        reqNameSpecie = requests.get(item).json()
        nameSpecie = reqNameSpecie['species']
        try:
            print(item+'-'+str(especie))
            if especie == nameSpecie[0]:
                print('si es de esta especie AGREGADO')
                res.append(item)
        except:
            pass
        
    return res
    
#print(obtenerPlanetsPorClima('https://swapi.dev/api/planets/','arid'))
#print(len(apracionDeEspeciePorPelicula('https://swapi.dev/api/films/6/','http://swapi.dev/api/species/3/')))
#print(obtenerNaveMasGrande('https://swapi.dev/api/starships/'))