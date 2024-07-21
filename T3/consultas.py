from typing import Generator

from utilidades import Animales, Candidatos, Distritos, Locales, Votos, Ponderador

from momasos_diego import ordenar_data, transformar_generador,\
cambio_edad_humana, mas_edad, iniciador_dict_votos_por_especie, id_especies_votos_por_especie,\
cuenta_votos_por_especie, iniciador_dict_comunas_locales, iniciador_dict_distritos_locales,\
cuenta_distritos_mas_locales, inicializador_dict_interespecie, iniciador_dic_votante_votado,\
misma_especie_True, misma_especie_False, iniciador_dic_candidato_votos, actualizar_dic,\
iniciador_dic_animal_especie, actualizar_dic_2, iniciador_dic_candidato_votos_2,\
iniciador_dicc_especie_ponderador, iniciador_dicc_distritos_comunas, \
iniciador_dicc_comunas_locales

from functools import reduce

from itertools import combinations, tee

from collections import Counter
# ----------------------------------------------------------------------
# CARGA DE DATOS

def cargar_datos(tipo_generator: str, tamano: str) -> Generator:
    with open('data/' + tamano + '/' + tipo_generator  + '.csv', 'r', encoding = 'latin-1') as file:
        data = file.readline() ## primera linea
        seguir = True
        while seguir:
            data = file.readline()
            if data == '':
                seguir = False
            else:
                data = data.split(',')
                data[-1] = data[-1].strip('\n')
                if tipo_generator == 'animales':
                    yield Animales(int(data[0]), data[1], data[2], int(data[3]), float(data[4]),\
                                int(data[5]), data[6])
                elif tipo_generator == 'candidatos':
                    yield Candidatos(int(data[0]), data[1], int(data[2]), data[3])
                
                elif tipo_generator == 'distritos':
                    yield Distritos(int(data[0]), data[1], int(data[2]), data[3], data[4])
                
                elif tipo_generator == 'locales':
                    data = ordenar_data(data)
                    yield Locales(int(data[0]), data[1], int(data[2]), data[3])
                
                elif tipo_generator == 'ponderadores':
                    yield Ponderador(str(data[0]), float(data[1]))
                
                elif tipo_generator == 'votos':
                    yield Votos(int(data[0]), int(data[1]), int(data[2]), int(data[3]))

# 1 GENERADOR

def animales_segun_edad(generador_animales: Generator,
    comparador: str, edad: int) -> Generator:
    if comparador == '<':
        filtro = filter(lambda x: x.edad < edad, generador_animales)
    elif comparador == '>':
        filtro = filter(lambda x: x.edad > edad, generador_animales)
    elif comparador == '=':
        filtro = filter(lambda x: x.edad == edad, generador_animales)
    return map(lambda x: x.nombre, filtro)


def animales_que_votaron_por(generador_votos: Generator,
    id_candidato: int) -> Generator:   
    filtro = filter(lambda x: x.id_candidato == id_candidato, generador_votos)
    return map(lambda x: x.id_animal_votante, filtro)


def cantidad_votos_candidato(generador_votos: Generator,
    id_candidato: int) -> int:
    filtro = filter(lambda x: x.id_candidato == id_candidato, generador_votos)
    return reduce(lambda x, y: x + 1, filtro, 0)


def ciudades_distritos(generador_distritos: Generator) -> Generator:
    provincias = map(lambda x: x.provincia, generador_distritos)
    nombres = reduce(lambda x, y: x.union({y}), provincias, set())
    return map(lambda x: x, nombres)


def especies_postulantes(generador_candidatos: Generator,
    postulantes: int) -> Generator:
    especies = map(lambda x: x.especie, generador_candidatos)
    especies = Counter(especies)
    filtro = filter(lambda x: especies[x] >= postulantes, especies)
    return transformar_generador(filtro)


def pares_candidatos(generador_candidatos: Generator) -> Generator:
    nombres = map(lambda x: x.nombre, generador_candidatos)
    return transformar_generador(combinations(nombres, 2))


def votos_alcalde_en_local(generador_votos: Generator, candidato: int,
    local: int) -> Generator:
    generador = filter(lambda x: x.id_candidato == candidato and x.id_local == local,\
                    generador_votos)
    return generador


def locales_mas_votos_comuna (generador_locales: Generator,
    cantidad_minima_votantes: int, id_comuna: int) -> Generator:
    generador = filter(lambda x: x.id_comuna == id_comuna, generador_locales)
    filtro = filter(lambda x: len(x.id_votantes) >= cantidad_minima_votantes, generador)
    return map(lambda x: x.id_local, filtro)


def votos_candidato_mas_votado(generador_votos: Generator) -> Generator:
    copias = tee(generador_votos, 2)
    copia_1 = copias[0]
    copia_2 = copias[1]
    candidatos = map(lambda x: x.id_candidato, copia_1)
    candidatos = Counter(candidatos)
    mas_votado = reduce(lambda x, y: x if x > candidatos[y] else candidatos[y], candidatos, 0)
    los_mas_votados = filter(lambda x: candidatos[x] == mas_votado, candidatos)
    id_mas_votado = reduce(lambda x, y: x if x > y else y, los_mas_votados, 0)
    filtro = filter(lambda x: x.id_candidato == id_mas_votado, copia_2)
    return map(lambda x: x.id_voto, filtro)

# 2 GENERADORES

def animales_segun_edad_humana(generador_animales: Generator,
    generador_ponderadores: Generator, comparador: str,
    edad: int) -> Generator:
    ponderadores = {p.especie: p.ponderador for p in generador_ponderadores}
    animales_actualizados = map(lambda x: cambio_edad_humana(x, ponderadores), generador_animales)
    return animales_segun_edad(animales_actualizados, comparador, edad)


def animal_mas_viejo_edad_humana(generador_animales: Generator,
    generador_ponderadores: Generator) -> Generator:
    ponderadores = {p.especie: p.ponderador for p in generador_ponderadores}
    animales_actualizados = map(lambda x: cambio_edad_humana(x, ponderadores), generador_animales)
    copias = tee(animales_actualizados, 2)
    copia_1 = copias[0]
    copia_2 = copias[1]
    mas_viejo = reduce(mas_edad, copia_1)
    return transformar_generador(animales_segun_edad(copia_2, '=', mas_viejo.edad))


def votos_por_especie(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    copias = tee(generador_candidatos, 2)
    copia_1 = copias[0]
    copia_2 = copias[1]
    especies = reduce(lambda x, y: x.union({y.especie}), copia_1, set())
    dict_candidatos = reduce(iniciador_dict_votos_por_especie, especies, {})
    dict_candidatos = reduce(id_especies_votos_por_especie, copia_2, dict_candidatos)
    dict_candidatos = reduce(cuenta_votos_por_especie, generador_votos, dict_candidatos)
    return map(lambda x: (x, int(dict_candidatos[x][0])), dict_candidatos)


def hallar_region(generador_distritos: Generator,
    generador_locales: Generator, id_animal: int) -> str:
    local = next((x for x in generador_locales if id_animal in x.id_votantes))
    distrito = next((x for x in generador_distritos if local.id_comuna == x.id_comuna))
    return distrito.region


def max_locales_distrito(generador_distritos: Generator,
    generador_locales: Generator) -> Generator:
    dict_id_comunas_locales = reduce(lambda x, y: iniciador_dict_comunas_locales(x, y.id_comuna)\
                                , generador_locales, {})
    dict_distritos_locales = reduce(lambda x, y: iniciador_dict_distritos_locales(x, y, dict_id_comunas_locales),\
                                    generador_distritos, {})

    mas_locales = reduce(lambda x, y: cuenta_distritos_mas_locales(x, y,\
                                dict_distritos_locales), dict_distritos_locales, 0)
    distritos = filter(lambda x: dict_distritos_locales[x] == mas_locales, dict_distritos_locales)
    return transformar_generador(distritos)


def votaron_por_si_mismos(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    id_votaron_por_ellos = filter(lambda x: x.id_candidato == x.id_animal_votante, generador_votos)
    id_votaron_por_ellos = reduce(lambda x, y: x.union({y.id_candidato}), id_votaron_por_ellos, set())
    votaron_por_ellos = filter(lambda x: x.id_candidato in id_votaron_por_ellos, generador_candidatos)
    return transformar_generador(map(lambda x: x.nombre, votaron_por_ellos))


def ganadores_por_distrito(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    # COMPLETAR
    pass

# 3 o MAS GENERADORES

def mismo_mes_candidato(generador_animales: Generator,
    generador_candidatos: Generator, generador_votos: Generator,
    id_candidato: str) -> Generator:
    copias = tee(generador_animales, 2)
    copia_1 = copias[0]
    copia_2 = copias[1]
    candidato_info = next((x for x in copia_1 if id_candidato == x.id), None)
    if candidato_info == None:
        return transformar_generador(x for x in generador_candidatos if id_candidato == x.id_candidato)
    id_votaron_por = animales_que_votaron_por(generador_votos, candidato_info.id)
    id_votaron_por = reduce(lambda x, y: x.union({y}), id_votaron_por, set())
    animales_votaron_por = filter(lambda x: x.id in id_votaron_por, copia_2)
    animales_mismo_mes = filter(lambda x:\
            x.fecha_nacimiento[:4] == candidato_info.fecha_nacimiento[:4] or \
            x.fecha_nacimiento[5:] == candidato_info.fecha_nacimiento[5:], animales_votaron_por)
    return transformar_generador(map(lambda x: x.id, animales_mismo_mes))


def edad_promedio_humana_voto_comuna(generador_animales: Generator,
    generador_ponderadores: Generator, generador_votos: Generator,
    id_candidato: int, id_comuna:int ) -> float:
    ids_votaron_por = animales_que_votaron_por(generador_votos, id_candidato)
    ids_votaron_por = reduce(lambda x, y: x.union({y}), ids_votaron_por, set())
    animales_votaron_por = filter(lambda x: x.id in ids_votaron_por and x.id_comuna == id_comuna\
                                  , generador_animales)
    ponderadores = {p.especie: p.ponderador for p in generador_ponderadores}
    animales_votaron_por = map(lambda x: cambio_edad_humana(x, ponderadores), animales_votaron_por)
    edades = reduce(lambda x, y: x.union({y.edad}), animales_votaron_por, set())
    if sum(edades) == 0:
        return 0
    return sum(edades)/len(edades)


def votos_interespecie(generador_animales: Generator,
    generador_votos: Generator, generador_candidatos: Generator,
    misma_especie: bool = False) -> Generator:
    dic_especie_ids_candidatos = reduce(inicializador_dict_interespecie, generador_candidatos, {})
    dic_votante_votado = reduce(iniciador_dic_votante_votado, generador_votos, {})
    if misma_especie == True:
        return transformar_generador(filter(lambda x: misma_especie_True(x, dic_votante_votado,\
                                dic_especie_ids_candidatos), generador_animales))
    else:
        return transformar_generador(filter(lambda x: misma_especie_False(x, dic_votante_votado,\
                                dic_especie_ids_candidatos), generador_animales))


def porcentaje_apoyo_especie(generador_animales: Generator,
    generador_candidatos: Generator, generador_votos: Generator) -> Generator:
    copias = tee(generador_animales, 2)
    copia_1 = copias[0]
    copia_2 = copias[1]
    copias = tee(generador_candidatos, 2)
    candidato_1 = copias[0]
    candidato_2 = copias[1]
    # asumiendo que todos los animales votan
    especies = map(lambda x: x.especie, copia_1)
    especies = Counter(especies)
    dic_id_candidato_voto = reduce(iniciador_dic_candidato_votos, candidato_1, {})
    dic_id_candidato_voto = reduce(iniciador_dic_candidato_votos_2, generador_votos, dic_id_candidato_voto)
    dic_id_candidato_voto = reduce(actualizar_dic, candidato_2, dic_id_candidato_voto)
    dic_animal_especie = reduce(iniciador_dic_animal_especie, copia_2, {})
    dic_id_candidato_voto = reduce(lambda x, y: actualizar_dic_2(x, y, dic_animal_especie),\
                                dic_id_candidato_voto, dic_id_candidato_voto)
    return map(lambda x: (x, 0) if especies[dic_id_candidato_voto[x][1]] == 0 else\
            (x, round(int(dic_id_candidato_voto[x][0]) * 100 / especies[dic_id_candidato_voto[x][1]])),\
            dic_id_candidato_voto)


def votos_validos(generador_animales: Generator,
    generador_votos: Generator, generador_ponderadores) -> int:
    dicc_especie_ponderador = reduce(iniciador_dicc_especie_ponderador, generador_ponderadores, {})
    votos = {voto.id_animal_votante for voto in generador_votos}
    animales_votan = filter(lambda x: x.id in votos, generador_animales)
    edad_transformadas = map(lambda x: dicc_especie_ponderador[x.especie] * x.edad, animales_votan)
    return reduce(lambda x, y: x + 1 , filter(lambda z: z >= 18, edad_transformadas), 0)


def cantidad_votos_especie_entre_edades(generador_animales: Generator,
    generador_votos: Generator, generador_ponderador: Generator,
    especie: str, edad_minima: int, edad_maxima: int) -> str:
    ponderador = next(filter(lambda x: x.especie == especie, generador_ponderador), None)
    votos = {voto.id_animal_votante for voto in generador_votos}
    set_animales_especie_votaron = reduce(lambda x, y: x.union({y}), \
            filter(lambda z: z.especie == especie and z.id in votos, generador_animales), set())
    edades = map(lambda x: ponderador.ponderador * x.edad, set_animales_especie_votaron)
    cantidad_votos = reduce(lambda x, y: x + 1 , filter(lambda z: z > edad_minima and\
                                                                z < edad_maxima, edades), 0)
    return f'Hubo {cantidad_votos} votos emitidos por animales entre {edad_minima} y \
{edad_maxima} años de la especie {especie}.'   


def distrito_mas_votos_especie_bisiesto(generador_animales: Generator,
    generador_votos: Generator, generador_distritos: Generator,
    especie: str) -> str:
    animales = filter(lambda x: x.especie == especie and \
                    int(x.fecha_nacimiento[:4]) % 4 == 0, generador_animales)
    votos = {voto.id_animal_votante for voto in generador_votos}
    animales = map(lambda y: y.id_comuna, filter(lambda x: x.id in votos, animales))
    comunas = Counter(animales)
    dicc_distritos_comunas = reduce(iniciador_dicc_distritos_comunas, generador_distritos, {})
    distrito_mas_votos = reduce(lambda x, y: x if \
            sum(comunas[id_comuna] for id_comuna in dicc_distritos_comunas[x]) >\
            sum(comunas[id_comuna] for id_comuna in dicc_distritos_comunas[y])\
            or (sum(comunas[id_comuna] for id_comuna in dicc_distritos_comunas[x]) ==\
            sum(comunas[id_comuna] for id_comuna in dicc_distritos_comunas[y]) \
            and int(x[9:]) < int(y[9:])) else y, dicc_distritos_comunas)
    return f'El distrito {distrito_mas_votos[9:]} fue el que tuvo más votos emitidos por\
 animales de la especie {especie} nacidos en año bisiesto.'


def votos_validos_local(generador_animales: Generator,
    generador_votos: Generator, generador_ponderadores: Generator,
    id_local: int) -> Generator:
    votos = filter(lambda x: x.id_local == id_local, generador_votos)
    ponderadores = {p.especie: p.ponderador for p in generador_ponderadores}
    copia = tee(votos)
    copia_1 = copia[0]
    copia_2 = copia[1]
    animales = map(lambda x: cambio_edad_humana(x, ponderadores), generador_animales)
    votos = {voto.id_animal_votante for voto in copia_1}
    ids_animales_validos = {animal.id for animal in \
                filter(lambda x: x.id in votos and x.edad >= 18, animales)}
    return map(lambda x: x.id_voto, filter(lambda x: x.id_animal_votante\
                                        in ids_animales_validos, copia_2))


def votantes_validos_por_distritos(generador_animales: Generator,
    generador_distritos: Generator, generador_locales: Generator,
    generador_votos: Generator, generador_ponderadores: Generator) -> Generator:
    copia = tee(generador_animales)
    copia_1 = copia[0]
    animales_original = copia[1]
    ponderadores = {p.especie: p.ponderador for p in generador_ponderadores}
    animales = map(lambda x: cambio_edad_humana(x, ponderadores), copia_1)
    ids_votantes_validos = {animal.id for animal in filter(lambda x: x.edad >= 18, animales)}
    votos = filter(lambda x: x.id_animal_votante in ids_votantes_validos, generador_votos)
    # tenemos los votos validos
    ids_locales = map(lambda y: y.id_local, votos)
    ids_locales = Counter(ids_locales)
    # cada voto valido por local
    dicc_distritos_comunas = reduce(iniciador_dicc_distritos_comunas, generador_distritos, {})
    dicc_comunas_locales = reduce(iniciador_dicc_comunas_locales, generador_locales, {})
    # diccionarios
    distrito_mas_votos = reduce(lambda x, y: x if \
        sum(sum(ids_locales[local] for local in dicc_comunas_locales[comuna]) \
            for comuna in dicc_distritos_comunas[x]) >\
        sum(sum(ids_locales[local] for local in dicc_comunas_locales[comuna]) \
            for comuna in dicc_distritos_comunas[y])\
            or\
        (sum(sum(ids_locales[local] for local in dicc_comunas_locales[comuna]) \
            for comuna in dicc_distritos_comunas[x]) ==\
        sum(sum(ids_locales[local] for local in dicc_comunas_locales[comuna]) \
            for comuna in dicc_distritos_comunas[y]) \
            and int(x[9:]) < int(y[9:])) else y,\
            dicc_distritos_comunas)
    return filter(lambda x: x.id_comuna in dicc_distritos_comunas[distrito_mas_votos], animales_original)
    