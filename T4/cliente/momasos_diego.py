import os

def cargar_puntajes() -> list:
    try:
        puntajes = []
        with open('puntaje.txt', 'r') as data:
            lineas = data.readlines()
        for linea in lineas:
            linea = linea.strip('\n')
            nombre, puntaje = linea.split(',')
            puntajes.append([nombre, puntaje])
        return puntajes[:3]
    except FileNotFoundError:
        return []

def ingresar_puntaje(nombre_nuevo, puntaje_nuevo):
    try:
        with open('puntaje.txt', 'r') as file:
            lineas = file.readlines()
        puntajes = []
        for linea in lineas:
            nombre, puntaje = linea.strip().split(',')
            puntajes.append((nombre, int(puntaje)))
        puntajes.append((nombre_nuevo, int(puntaje_nuevo)))
        # orden
        puntajes_ordenados = sorted(puntajes, key=lambda x: x[1], reverse=True)
        with open('puntaje.txt', 'w') as file:
            for nombre, puntaje in puntajes_ordenados:
                file.write(f'{nombre},{puntaje}\n')
    except FileNotFoundError:
        with open('puntaje.txt', 'w') as file:
            file.write(f'{nombre_nuevo},{puntaje_nuevo}\n')

def cargar_puzzle(nombre_archivo):
    with open(os.path.join('assets', 'base_puzzles', nombre_archivo)) as file:
        file = file.readlines()
    lineas_X = file[0].strip().split(';')
    lineas_Y = file[1].strip().split(';')
    n_casillas = len(lineas_X)
    eje_x = []
    eje_y =[]
    for info in lineas_X:
        eje_x.append(info)
    for info in lineas_Y:
        eje_y.append(info)
    return (n_casillas, eje_x, eje_y)