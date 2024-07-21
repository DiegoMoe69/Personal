import red

import sys

import dcciudad

if __name__ == "__main__":
    archivo = sys.argv[1]
    estacion_actual = str(sys.argv[2])
    start = True
    try:
        with open('data/' + archivo) as file:
            info = file.readlines()
            info = ''.join(info).split('\n')
            estaciones = []
            red_data = []
            red_info = info[int(info[0]) + 1]
            red_info = red_info.split(',')
            #lista de numeros que correndponden a los valores de la matriz de incidencia
            for estacion in range(int(info[0])):
                estaciones.append(info[estacion + 1])
                red_temporal = []
                for tunel in range(int(info[0])):
                    red_temporal.append(int(red_info[tunel + estacion * int(info[0])]))
                red_data.append(red_temporal)
            metro = red.RedMetro(red_data, estaciones)
            metro.nombre = archivo
            if estacion_actual not in metro.estaciones:
                print(metro.estaciones)
                print(estacion)
                print('La estacion indicada no existe')
                start = False
    except FileNotFoundError:
        print('La red indicada no existe')
        start = False
    if start == True:
        print('Se cargo la red ' + metro.nombre)
        print('Usted se encuentra en ' + estacion_actual)
        while start:
            print('Menu de acciones')
            print('1- Mostrar red')
            print('2- Encontrar ciclo mas corto')
            print('3- Asegurar ruta')
            print('4- Salir del programa :(')
            accion = int(input('Ingrese la accion que quiere realizar: '))
            if accion == 1:
                dcciudad.imprimir_red(metro.red, metro.estaciones)
                input()
            elif accion == 2:
                print(metro.ciclo_mas_corto(estacion_actual))
                input()
            elif accion == 3:
                print('Recuerda escribir bien tu destino :)')
                destino_invalido = True
                while destino_invalido:
                    destino = input('Ingrese la estacion a la que quieres asegurar tu ruta: ')
                    if destino in metro.estaciones:
                        destino_invalido = False
                    else:
                        print('Por favor ingrese un destino valido')
                p_intermedias = int(input('Ingrese la cantidad de paradas intermedias: '))
                print(metro.asegurar_ruta(estacion_actual, destino, p_intermedias))
                input()
            elif accion == 4:
                print('cerrando el programa')
                start = False
            else:
                print('Accion invalida, usted sera redirijid@ al menu de acciones')
                input()