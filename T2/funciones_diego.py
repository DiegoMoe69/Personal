from clases import Mago, Caballero, Guerrero, Paladin, Mago_de_Batalla, Caballero_Arcano, Ejercito


def archivos_validos() -> bool:
    data_facil = open('data/facil.txt')
    data_intermedio = open('data/intermedio.txt')
    data_dificil = open('data/dificil.txt')
    data_unidades = open('data/unidades.txt')
    info_facil = unir(data_facil.readlines())
    info_intermedio = unir(data_intermedio.readlines())
    info_dificil = unir(data_dificil.readlines())
    info_unidades = unir(data_unidades.readlines())
    data_facil.close()
    data_intermedio.close()
    data_dificil.close()
    data_unidades.close()
    for ronda in info_facil + info_intermedio + info_dificil:
        ronda = ronda.split(';')
        for unidad in ronda:
            if not chequear(unidad, True):
                return False
    for ronda in info_unidades:
        ronda = ronda.split(';')
        for unidad in ronda:
            if not chequear(unidad, False):
                return False
    return True

def chequear(unidad: list, dificultad: bool) -> bool:
    if dificultad:
        tipos = ['MAG', 'CAB', 'GUE', 'CAR', 'PAL', 'MDB']
    else:
        tipos = ['MAG', 'CAB', 'GUE']
    unidad = unidad.split(',')
    if len(unidad) != 7:
        return False
    elif unidad[1] not in tipos:
        return False
    elif int(unidad[2]) > 100 or int(unidad[2]) < 1:
        return False
    elif int(unidad[3]) > 20 or int(unidad[3]) < 1:
        return False
    elif int(unidad[4]) > 10 or int(unidad[4]) < 1:
        return False
    elif int(unidad[5]) > 10 or int(unidad[5]) < 1:
        return False
    elif int(unidad[6]) > 10 or int(unidad[6]) < 1:
        return False
    return True

def unir(rondas: list):
    rondas = ''.join(rondas)
    rondas = rondas.split('\n')
    return rondas

def instanciar(personaje: str):
    personaje = personaje.split(',')
    if personaje[1] == 'MAG':
        return Mago(nombre = personaje[0],\
                    vida_max = int(personaje[2]),\
                    poder = int(personaje[3]),\
                    defensa = int(personaje[4]), \
                    agilidad = int(personaje[5]),\
                    resistencia = int(personaje[6]))
    elif personaje[1] == 'CAB':
        return Caballero(nombre = personaje[0],\
                    vida_max = int(personaje[2]),\
                    poder = int(personaje[3]),\
                    defensa = int(personaje[4]), \
                    agilidad = int(personaje[5]),\
                    resistencia = int(personaje[6]))
    elif personaje[1] == 'GUE':
        return Guerrero(nombre = personaje[0],\
                    vida_max = int(personaje[2]),\
                    poder = int(personaje[3]),\
                    defensa = int(personaje[4]), \
                    agilidad = int(personaje[5]),\
                    resistencia = int(personaje[6]))
    elif personaje[1] == 'CAR':
        return Caballero_Arcano(nombre = personaje[0],\
                    vida_max = int(personaje[2]),\
                    poder = int(personaje[3]),\
                    defensa = int(personaje[4]), \
                    agilidad = int(personaje[5]),\
                    resistencia = int(personaje[6]))
    elif personaje[1] == 'PAL':
        return Paladin(nombre = personaje[0],\
                    vida_max = int(personaje[2]),\
                    poder = int(personaje[3]),\
                    defensa = int(personaje[4]), \
                    agilidad = int(personaje[5]),\
                    resistencia = int(personaje[6]))
    elif personaje[1] == 'MDB':
        return Mago_de_Batalla(nombre = personaje[0],\
                    vida_max = int(personaje[2]),\
                    poder = int(personaje[3]),\
                    defensa = int(personaje[4]), \
                    agilidad = int(personaje[5]),\
                    resistencia = int(personaje[6]))

def instanciar_rondas(ronda_1, ronda_2, ronda_3):
    enemigos_1 = Ejercito(0)
    enemigos_2 = Ejercito(0)
    enemigos_3 = Ejercito(0)
    for enemigo in ronda_1:
        enemigos_1.combatientes.append(instanciar(enemigo))
    for enemigo in ronda_2:
        enemigos_2.combatientes.append(instanciar(enemigo))
    for enemigo in ronda_3:
        enemigos_3.combatientes.append(instanciar(enemigo))
    return [enemigos_1, enemigos_2, enemigos_3]

#posibles es una lista de combatientes basicos
def menu_gatos(posibles: list) -> tuple:
    loop = True
    while loop:
        print('*** Selecciona un gato ***')
        print('      Clase      Nombre')
        n = 1
        for gato in posibles:
            print(f'[{n}] Gato {gato.tipo} {gato.nombre}')
            n += 1
        posicion = int(input('Indique su opción:'))
        if posicion > 0 and posicion <= len(posibles):
            nombre = posibles[posicion - 1].nombre
            contador_posicion = 1
            contador_nombres = 0
            for gato in posibles:
                if contador_posicion <= posicion and gato.nombre == nombre:
                    contador_nombres += 1
                contador_posicion += 1
            return (contador_nombres, nombre)
        else:
            print('input invalido')
