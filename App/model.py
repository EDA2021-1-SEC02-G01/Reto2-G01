﻿"""
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
               'video_tags': None,
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
                'country': video['country'].strip(),
                'tags': video['tags'].strip(),
                'category_id': video['category_id'].strip()}
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], filtrado)
    addVideoCategory(catalog, filtrado)


def addVideoCategory(catalog, video):
    try:
        categories = catalog['categories']
        if (video['category_id'] != ''):
            categoryId = video['category_id']
            categoryId = int(float(categoryId))
        else:
            categoryId = 0
        existyear = mp.contains(categories, categoryId)
        if existyear:
            entry = mp.get(categories, categoryId)
            category = me.getValue(entry)
        else:
            category = newCategory(categoryId, "No category")
            mp.put(categories, categoryId, category)
        lt.addLast(category['videos'], video)
        category['total_videos'] += 1
    except Exception:
        return None


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
    category['name'] = name
    category['category_id'] = id
    category['videos'] = lt.newList("ARRAY_LIST")
    return category


# Funciones de consulta

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
    idVideo = getCategoryIdByName(catalog, categoryName)
    if idVideo != None:
        category = getCategoryById(catalog, idVideo)
        videos = category['videos']
        return videos
    return None


# Funciones utilizadas para comparar elementos dentro de una lista

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


# Funciones de ordenamiento

def sortVideosByViews(videos):
    sorted_list = mg.sort(videos, cmpVideosByViews)
    return sorted_list


def sortCountry(catalog, category_name, country_name):
    videosByCategory = getVideosByCategory(catalog, category_name)
    country_list = lt.newList('ARRAY_LIST')
    if videosByCategory is not None:
        for video in lt.iterator(videosByCategory):
            if country_name.lower() == video['country'].lower():
                lt.addLast(country_list, video)
        return country_list
    return None