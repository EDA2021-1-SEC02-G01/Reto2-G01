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
 """

import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del Catálogo de libros

def initCatalog(LoadFactor, TypeMap):
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog(LoadFactor, TypeMap)
    return catalog


# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el proceso para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    categoryId(catalog)
    loadVideos(catalog)

    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el proceso para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory


def loadVideos(catalog):
    """
    Carga los videos del archivo.
    """
    videosfile = cf.data_dir + 'videos/videos-large.csv'
    input_file = csv.DictReader(open(videosfile, encoding="utf-8"))
    for video in input_file:
        model.addVideo(catalog, video)


def categoryId(catalog):
    """
    Carga todas categorias del archivo y los agrega a la lista de categorias
    """
    video_category_id = cf.data_dir + 'videos/category-id.csv'
    input_file = csv.DictReader(open(video_category_id, encoding='utf-8'),
                                delimiter="\t")
    for category in input_file:
        model.addCategory(catalog, category)


# Funciones de ordenamiento

def sortVideosByViews(videos):
    return model.sortVideosByViews(videos)


def sortCountry(catalog, category_name, country_name):
    return model.sortCountry(catalog, category_name, country_name)


def videoUniques(videos):
    return model.videoUniques(videos)


# Funciones de consulta sobre el catálogo

def getCategoryById(catalog, categoryId):
    return model.getCategoryById(catalog, categoryId)


def getCategoryByName(catalog, categoryName):
    return model.getCategoryByName(catalog, categoryName)


def getTrendVidByCountry(catalog, country_name):
    """
    Busca el video que más días ha sido tendencia
    para un pais especifico
    """
    return model.getTrendVidByCountry(catalog, country_name)


def getTrendVidByCategory(catalog, category_name):
    """
    Busca el video que más días ha sido tendencia
    para una categoria especifica
    """
    return model.getTrendVidByCategory(catalog, category_name)


def getVidsByCountry(catalog, country_name):
    """
    Retorn una lista con todos los videos del pais
    que se busca
    """
    return model.getVidsByCountry(catalog, country_name)


def filterByCountry(videoList, country_name):
    """
    Filtra la lista que contiene el pais buscado
    """
    return model.filterByCountry(videoList, country_name)


def getVidsByTag(videosList, tag_name):
    """
    Filtra los videos que contengan un tag especifico
    """
    return model.getVidsByTag(videosList, tag_name)


def sortVideosByLikes(videosList):
    """
    Ordena la lista de videos por likes
    """
    return model.sortVideosByLikes(videosList)


# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
