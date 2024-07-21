from typing import Generator

from utilidades import Animales, Votos

from functools import reduce


def ordenar_data(data: list) -> list:
    data_limpia = []
    lista = []
    data_limpia.append(data[0])
    data_limpia.append(data[1])
    data_limpia.append(data[2])
    data.pop(0)
    data.pop(0)
    data.pop(0)
    data = ','.join(data)
    data = data.strip('[]')
    if data == '':
        data_limpia.append([])
        return data_limpia
    data = data.split(',')
    for info in data:
        lista.append(int(info))
    data_limpia.append(lista)
    return data_limpia


def transformar_generador(generador) -> Generator:
    for dato in generador:
        yield dato

    
## animales_segun_edad_humana
def cambio_edad_humana(animal, ponderadores: set) -> Animales:
    edad_nueva = animal.edad * ponderadores[animal.especie]
    return Animales(animal.id, animal.nombre, animal.especie, animal.id_comuna, animal.peso_kg,\
                    edad_nueva, animal.fecha_nacimiento)

## animal_mas_viejo_edad_humana
def mas_edad(animal_x, animal_y ):
    if animal_x.edad > animal_y.edad:
        return animal_x
    else:
        return animal_y

## votos_por_especie
def iniciador_dict_votos_por_especie(dicc: dict, especie: str):
    dicc[especie] = ['0']
    return dicc


def id_especies_votos_por_especie(dicc: dict, candidato):
    lista = dicc[candidato.especie]
    lista = lista + [candidato.id_candidato]
    dicc[candidato.especie] = lista
    return dicc


def cuenta_votos_por_especie(dicc: dict, voto: Votos):
    especie = next((x for x in dicc if voto.id_candidato in dicc[x]))
    info = dicc[especie]
    info[0] = int(info[0]) + 1
    info[0] = str(info[0])
    dicc[especie] = info
    return dicc
    
## max_locales_distrito
def iniciador_dict_comunas_locales(dicc: dict, id_comuna: int):
    if dicc.get(id_comuna) == None:
        dicc[id_comuna] = 1
    else:
        info = dicc[id_comuna] + 1
        dicc[id_comuna] = info
    return dicc


def iniciador_dict_distritos_locales(dicc, distrito, dict_id_comunas_locales):
    if dicc.get(distrito.nombre) == None:
        dicc[distrito.nombre] = dict_id_comunas_locales[distrito.id_comuna]
    else:
        info = dicc[distrito.nombre] + dict_id_comunas_locales[distrito.id_comuna]
        dicc[distrito.nombre] = info
    return dicc


def cuenta_distritos_mas_locales(x, key, dicc):
    if dicc[key] > x:
        return dicc[key]
    else:
        return x

## votos inter especie
def inicializador_dict_interespecie(dicc, candidato):
    if dicc.get(candidato.especie) == None:
        dicc[candidato.especie] = []
    info = dicc[candidato.especie] + [candidato.id_candidato]
    dicc[candidato.especie] = info
    return dicc

def iniciador_dic_votante_votado(dicc, voto):
    dicc[voto.id_animal_votante] = voto.id_candidato
    return dicc

def misma_especie_True(animal, dic_votante_votado, dic_especie_ids_candidatos) -> bool:
    if dic_votante_votado.get(animal.id) == None:
        return False
    elif dic_especie_ids_candidatos.get(animal.especie) == None:
        return False
    elif dic_votante_votado[animal.id] in dic_especie_ids_candidatos[animal.especie]:
        return True
    return False

def misma_especie_False(animal, dic_votante_votado, dic_especie_ids_candidatos) -> bool:
    if dic_votante_votado.get(animal.id) == None:
        return False
    elif dic_especie_ids_candidatos.get(animal.especie) == None:
        return True
    elif dic_votante_votado[animal.id] not in dic_especie_ids_candidatos[animal.especie]:
        return True
    return False

## porcentaje_apoyo_especie
def iniciador_dic_candidato_votos(dicc, candidato):
    dicc[candidato.id_candidato] = ['0'] + ['especie']
    return dicc

def iniciador_dic_candidato_votos_2(dicc, voto):
    if dicc.get(voto.id_candidato) == None:
        return dicc
    dicc[voto.id_candidato] += [voto.id_animal_votante]
    return dicc

def actualizar_dic(dicc, candidato):
    dicc[candidato.id_candidato][1] = candidato.especie
    return dicc

def iniciador_dic_animal_especie(dicc, animal):
    dicc[animal.id] = animal.especie
    return dicc

def actualizar_dic_2(dic_candidato_votos, key_candidato_votos, dic_animal_especie):
    votantes = dic_candidato_votos[key_candidato_votos][2:]
    votos_especie = reduce(lambda x, y: x + 1, filter(lambda x: dic_animal_especie[x] ==\
                    dic_candidato_votos[key_candidato_votos][1], votantes), 0)
    dic_candidato_votos[key_candidato_votos][0] = f'{votos_especie}'
    return dic_candidato_votos

## votos_validos
def iniciador_dicc_especie_ponderador(dicc, ponderador):
    dicc[ponderador.especie] = ponderador.ponderador
    return dicc

## distrito_mas_votos_especie_bisiesto
def iniciador_dicc_distritos_comunas(dicc, distrito):
    if dicc.get(distrito.nombre) == None:
        dicc[distrito.nombre] = []
    dicc[distrito.nombre] += [distrito.id_comuna]
    return dicc

## votantes_validos_por_distritos
def iniciador_dicc_comunas_locales(dicc, local):
    if dicc.get(local.id_comuna) == None:
        dicc[local.id_comuna] = []
    dicc[local.id_comuna] += [local.id_local]
    return dicc




