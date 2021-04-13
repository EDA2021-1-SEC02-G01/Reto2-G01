"""
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
    print("1- Cargar información en el catálogo")
    print("2- los n videos con más LIKES para el" +
          " nombre de una categoría específica")


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
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        LoadFactor = float(input("Ingrese el factor de carga con el que quiere cargar los videos: "))
        TypeMap = input("Ingrese el tipo de mapa con el que quiere cargar los datos: ")
        catalog = initCatalog(LoadFactor, TypeMap)
        answer = loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorias cargadas: ' + str(lt.size(catalog['categories'])))
        print('lista categorias: ' + str(lt.size(catalog['category_ids'])))
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
    elif int(inputs[0]) == 2:
        categoryName = input("Ingrese el nombre de la categoria: ").title()
        nVideos = int(input("Ingrese el top de videos que desea: "))
        categoryId = controller.getCategoryByName(catalog, categoryName)
        if categoryId is None:
            print(f"La categoria {categoryName} no existe")
        else:
            category = controller.getCategoryById(catalog, categoryId)
            sortedVids = controller.sortVideosByViews(category["videos"])
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
    else:
        sys.exit(0)
sys.exit(0)
