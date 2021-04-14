﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- (REQ 1) Los n videos con más LIKES en un pais" +
          " una categoría específica")
    print("2- (REQ 2) El video que mas ha sido trending un" + 
          "pais especifico")
    print("3- (REQ 3) El video que mas ha sido trending en" +
          " una categoría especifica")
    print("4- (REQ 4) Los n videos con mas LIEKS dado un pais" +
          " y un tag especifico")
    print("5- Salir")


def initCatalog(LoadFactor, TypeMap):
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog(LoadFactor, TypeMap)


def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    categorias = controller.loadData(catalog)
    return categorias


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        LoadFactor = float(input("Ingrese el factor de carga con " +
                                 "el que quiere cargar los videos: "))
        TypeMap = input("Ingrese el tipo de mapa con el que quiere " +
                        "cargar los datos: ").upper()
        catalog = initCatalog(LoadFactor, TypeMap)
        answer = loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorias cargadas: ' + str(lt.size(catalog['categories'])))
        print('lista categorias: ' + str(lt.size(catalog['category_ids'])))
        print('Paises cargados: ' + str(lt.size(catalog['countries'])))
        first_video = lt.firstElement(catalog['videos'])
        print('Titulo: ' + first_video['title'] +
              ', Canal: ' + first_video['channel_title'] +
              ', Dia de trending: ' + first_video['trending_date'] +
              ', Pais: ' + first_video['country'] +
              ', Vistas: ' + first_video['views'] +
              ', Me gusta: ' + first_video['likes'] +
              ', No me gusta: ' + first_video['dislikes']
              )
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
        print("\n")
    elif int(inputs[0]) == 1:
        category_name = input("Ingrese el nombre de la categoria: ").title()
        country_name = input("Ingrese el nombre del pais: ").title()
        nVideos = int(input("Ingrese el top de videos que desea: "))
        listCountryCat = controller.sortCountry(catalog,
                                                category_name,
                                                country_name)
        if listCountryCat is None:
            print(f"El pais {country_name} no existe")
        else:
            sortedVids = controller.sortVideosByViews(listCountryCat)
            i = 1
            while i <= nVideos:
                video = lt.getElement(sortedVids, i)
                print("#" + str(i))
                print('Titulo: ' + video['title'] +
                      ', Canal: ' + video['channel_title'] +
                      ', Id de categoria: ' + video['category_id'] +
                      ', Dia de trending: ' + video['trending_date'] +
                      ', Pais: ' + video['country'] +
                      ', Vistas: ' + video['views'] +
                      ', Me gusta: ' + video['likes'] +
                      ', No me gusta: ' + video['dislikes']
                      )
                print("\n")
                i += 1
    elif int(inputs[0]) == 2:
        country_name = input("Ingrese el nombre del pais: ").title()
        trendVid = controller.getTrendVidByCountry(catalog,
                                                   country_name).title()
        trendInfo = trendVid['info']
        cuenta = trendVid['cuenta']
        print("Title: " + trendInfo['title'])
        print("Channel Title" + trendInfo['channel_title'])
        print("Country: " + trendInfo['country'])
        print("Numero de dias en tendencia: " + str(cuenta))
    elif int(inputs[0]) == 3:
        category_name = input("Ingrese el nombre de la categoria: ").title()
        trendVid = controller.getTrendVidByCategory(catalog, category_name)
        if trendVid is not None:
            trendInfo = trendVid['info']
            cuenta = trendVid['cuenta']
            print("Title: " + trendInfo['title'])
            print("Channel Title" + trendInfo['channel_title'])
            print("Country: " + trendInfo['category_id'])
            print("Numero de dias en tendencia: " + str(cuenta))
        else:
            print(f"La categoria {category_name}" +
                  " no se encontró en el catálogo")
    elif int(inputs[0]) == 4:
        tag_name = input("Ingrese el nombre del 'tag': ")
        country_name = input("Ingrese el nombre del pais: ")
        n_videos =  int(input("Ingrese el numero top de videos que desea: "))
        videosByCountry = controller.getVidsByCountry(catalog, country_name)
        if videosByCountry is not None:
            videosByTag = controller.getVidsByTag(videosByCountry, tag_name)
            videosByViews = controller.sortVideosByLikes(videosByTag)
            counter = 1
        while counter <= n_videos:
            video = lt.getElement(videosByViews, counter)
            print('\n' +
                  'title: ' + video['title'],
                  'channel_title: ' + video['channel_title'],
                  'publish_time: ' + video['publish_time'],
                  'views: ' + video['views'],
                  'likes: ' + video['likes'],
                  'dislikes: ' + video['dislikes'],
                  'tags: ' + video['tags'] + '/n'
                  )
            counter += 1
    else:
        sys.exit(0)
sys.exit(0)
