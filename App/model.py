"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mg
assert cf


# Construccion de modelos
def newCatalog(LoadFactor, TypeMap):
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'categories': None,
               'countries': None,
               'tags': None,
               'category_ids': None}

    catalog['videos'] = lt.newList('ARRAY_LIST')
    """
    Este indice crea un map cuya llave es la categoria del video
    """
    catalog['categories'] = mp.newMap(67,
                                      maptype=TypeMap,
                                      loadfactor=LoadFactor,
                                      comparefunction=cmpCategoriesById)
    """
    Este indice crea un map cuya llave es el nombre de la categoria
    del video y su valor es el id del video
    """
    catalog['category_ids'] = mp.newMap(67,
                                        maptype=TypeMap,
                                        loadfactor=LoadFactor,
                                        comparefunction=cmpCategoriesByName)
    """
    Este indice crea un map cuya llave es el pais del video
    """
    catalog['countries'] = mp.newMap(22,
                                     maptype=TypeMap,
                                     loadfactor=LoadFactor,
                                     comparefunction=cmpCategoriesByName)

    return catalog


# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    # Filtramos la informacion del video con lo que necesitamos
    filtrado = {'video_id': video['video_id'].strip(),
                'trending_date': video['trending_date'].strip(),
                'title': video['title'].strip(),
                'channel_title': video['channel_title'].strip(),
                'publish_time': video['publish_time'].strip(),
                'views': video['views'],
                'likes': video['likes'].strip(),
                'dislikes': video['dislikes'].strip(),
                'country': video['country'].strip().title(),
                'tags': video['tags'].strip().lower(),
                'category_id': video['category_id'].strip()}
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], filtrado)
    addVideoCategory(catalog, filtrado)
    country_name = video['country'].strip().title()
    addVideoCountry(catalog, country_name, filtrado)


def addVideoCategory(catalog, video):
    try:
        categories = catalog['categories']
        if (video['category_id'] != ''):
            categoryId = int(float(video['category_id']))
        else:
            categoryId = 0
        categoryExists = mp.contains(categories, categoryId)
        if categoryExists:
            entry = mp.get(categories, categoryId)
            category = me.getValue(entry)
        else:
            category = newCategory(categoryId, "No category")
            mp.put(categories, categoryId, category)
        lt.addLast(category['videos'], video)
        category['total_videos'] += 1
    except Exception:
        return None


def addVideoCountry(catalog, country_name, video):
    """
    Adiciona un pais al map de paises, el cual guarda referencias
    a los videos que tienen ese pais
    """
    countries = catalog['countries']
    existscountry = mp.contains(countries, country_name)
    if not existscountry:
        countryVidLst = lt.newList('ARRAY_LIST')
        mp.put(countries, country_name, countryVidLst)
    entry = mp.get(countries, country_name)
    videolst = me.getValue(entry)
    lt.addLast(videolst, video)


def addCategory(catalog, category):
    """
    Adiciona una categoría a la lista de categorías
    """
    categories = catalog['categories']
    category_ids = catalog['category_ids']
    categoryName = category['name'].strip()
    categoryId = int(category['id'])
    existCategory = mp.contains(categories, categoryId)
    if not existCategory:
        c = newCategory(categoryId, categoryName)
        mp.put(categories, categoryId, c)
        mp.put(category_ids, categoryName, categoryId)


# Funciones para creacion de datos

def newCategory(id, name):
    """
    Esta estructura crea las categorías utilizadas para marcar videos.
    """
    category = {'name': '',
                'category_id': '',
                'total_videos': 0,
                'videos': None}
    category['name'] = name.title()
    category['category_id'] = id
    category['videos'] = lt.newList("ARRAY_LIST")
    return category


# Funciones de consulta

def getTrendVidByCountry(catalog, country_name):
    countries = catalog['countries']
    existsCountry = mp.contains(countries, country_name)
    if existsCountry:
        entry = mp.get(countries, country_name)
        videoList = me.getValue(entry)
        trendVids = mp.newMap(comparefunction=compareVideoName2)
        for video in lt.iterator(videoList):
            vidTitle = video['title']
            existVid = mp.contains(trendVids, vidTitle)
            if existVid:
                entry = mp.get(trendVids, vidTitle)
                videoUnique = me.getValue(entry)
                videoUnique['cuenta'] += 1
            else:
                mp.put(trendVids, vidTitle, {"info": video, "cuenta": 1})
        trendVidList = mp.valueSet(trendVids)
        mayorVideo = None
        cuentaMayor = 0
        for video in lt.iterator(trendVidList):
            cuenta = video["cuenta"]
            if cuenta > cuentaMayor:
                mayorVideo = video["info"]
                cuentaMayor = cuenta

        return mayorVideo, cuentaMayor
    return None


def getTrendVidByCategory(catalog, category_name):
    videoList = getVideosByCategory(catalog, category_name)
    if videoList is not None:
        trendVids = mp.newMap(comparefunction=compareVideoName2)
        for video in lt.iterator(videoList):
            vidTitle = video['title']
            existVid = mp.contains(trendVids, vidTitle)
            if existVid:
                entry = mp.get(trendVids, vidTitle)
                videoUnique = me.getValue(entry)
                videoUnique['cuenta'] += 1
            else:
                mp.put(trendVids, vidTitle, {"info": video, "cuenta": 1})
        trendVidList = mp.valueSet(trendVids)
        mayorVideo = None
        cuentaMayor = 0
        for video in lt.iterator(trendVidList):
            cuenta = video["cuenta"]
            if cuenta > cuentaMayor:
                mayorVideo = video["info"]
                cuentaMayor = cuenta

        return mayorVideo, cuentaMayor
    return None


def filterByCountry(videoList, country_name):
    country_list = lt.newList('ARRAY_LIST')
    for video in lt.iterator(videoList):
        if country_name.lower() == video['country'].lower():
            lt.addLast(country_list, video)
    return country_list


def getCategoryById(catalog, categoryId):
    categoryExists = mp.contains(catalog["categories"], categoryId)
    if categoryExists:
        entry = mp.get(catalog["categories"], categoryId)
        category = me.getValue(entry)
    else:
        category = None
    return category


def getCategoryIdByName(catalog, categoryName):
    categoryExists = mp.contains(catalog['category_ids'], categoryName)
    if categoryExists:
        entry = mp.get(catalog["category_ids"], categoryName)
        categoryId = me.getValue(entry)
    else:
        categoryId = None
    return categoryId


def getVideosByCategory(catalog, categoryName):
    categoryId = getCategoryIdByName(catalog, categoryName)
    if categoryId is not None:
        category = getCategoryById(catalog, categoryId)
        videos = category['videos']
        return videos
    return None


def getVidsByCountry(catalog, country_name):
    entry = mp.get(catalog['countries'], country_name)
    country_list = me.getValue(entry)
    return country_list


def getVidsByTag(country_list, tag_name):
    tag_list = lt.newList('ARRAY_LIST')
    for video in lt.iterator(country_list):
        lista = video['tags'].lower()
        if tag_name.lower() in lista:
            lt.addLast(tag_list, video)
    return tag_list


# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByDays(video1, video2):
    """
    Devuelve True si los dias que estuvo en trend el video 1 son mayores
    que los del video2
    """
    return video1['cuenta'] > video2['cuenta']


def compareVideoName1(videoname1, video):
    if (videoname1.lower() in video['value']['title'].lower()):
        return 0
    return -1


def compareVideoName2(videoname1, video):
    if (videoname1.lower() in video['value']['info']['title'].lower()):
        return 0
    return -1


def comparecountries(countryname1, country):
    if (countryname1.lower() in country['name'].lower()):
        return 0
    return -1


def cmpCategoriesById(categoryId, category):
    if int(categoryId) == int(category['value']['category_id']):
        return 0
    return -1


def cmpCategoriesByName(categoryName, categoryEntry):
    if categoryName.lower() == categoryEntry['key'].lower():
        return 0
    return -1


def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero (True) si los 'views' de video1
    son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'views'
    video2: informacion del segundo video que incluye su valor 'views'
    """
    return int(video1['views']) > int(video2['views'])


def cmpVideosByTitle(video1, video2):
    return video1['title'] < video2['title']


def cmpTags(video1, video2):
    return video1['tags'] < video2['tags']


def cmpLikes(video1, video2):
    return int(video1['likes']) > int(video2['likes'])


# Funciones de ordenamiento

def sortVideosByViews(videos):
    sorted_list = mg.sort(videos, cmpVideosByViews)
    return sorted_list


def sortVideosByLikes(videos):
    sorted_list = mg.sort(videos, cmpLikes)
    return sorted_list


def sortCountry(catalog, category_name, country_name):
    """
    Req. 1
    """
    videosByCategory = getVideosByCategory(catalog, category_name)
    country_list = lt.newList('ARRAY_LIST')
    if videosByCategory is not None:
        for video in lt.iterator(videosByCategory):
            if country_name.lower() == video['country'].lower():
                lt.addLast(country_list, video)
        return country_list
    return None


def videoUniques(videos):
    uniqueVideos = mp.newMap(comparefunction=compareVideoName1)
    for video in lt.iterator(videos):
        vidTitle = video['title']
        existVid = mp.contains(uniqueVideos, vidTitle)
        if existVid:
            entry = mp.get(uniqueVideos, vidTitle)
            videoUnique = me.getValue(entry)
            if int(video['likes']) > int(videoUnique['likes']):
                mp.put(uniqueVideos, vidTitle, video)
        else:
            mp.put(uniqueVideos, vidTitle, video)
    uniqueVideosList = mp.valueSet(uniqueVideos)
    return uniqueVideosList
