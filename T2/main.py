import sys

from clases import Ejercito, Item

from parametros import PRECIO_MAG, PRECIO_GUE, PRECIO_CAB, PRECIO_ARMADURA,\
PRECIO_PERGAMINO, PRECIO_LANZA, PRECIO_CURA, ORO_INICIAL, CURAR_VIDA, ORO_GANADO

from funciones_diego import archivos_validos, instanciar, instanciar_rondas, menu_gatos

from random import randint

if __name__ == "__main__":
    dificultad = sys.argv[1]
    if dificultad not in ['facil', 'intermedio', 'dificil']:
        loop_menu = False
        print('dificultad no valida')
    elif archivos_validos():
        loop_menu = True
        persona = Ejercito(ORO_INICIAL)
        with open('data/' + dificultad + '.txt') as file:
            file = ''.join(file.readlines()).split('\n')
            ronda_1 = file[0].split(';')
            ronda_2 = file[1].split(';')
            ronda_3 = file[2].split(';')
            ronda_act = 1
            gato_chico = instanciar_rondas(ronda_1, ronda_2, ronda_3)
            #gato_chico es una lista de ejercitos
    else:
        loop_menu = False
        print('error en los archivos')
    while loop_menu == True: # menu inicio
        print(f'*** Menú de inicio ***\n\
Dinero disponible: {persona.oro}\n\
Ronda actual: {ronda_act}\n\
[1] Tienda\n\
[2] Ejercito\n\
[3] Combatir\n\
[0] Salir del programa\n\
Indique su opción:')
        menu = input()
        if menu not in '0123':
            print('input invalido')
        elif menu == '1':
            loop_tienda = True
            while loop_tienda:
                print(f'*** Tienda ***\n\
Dinero disponible: {persona.oro}\n\
Producto               Precio\n\
[1] Gato Mago          {PRECIO_MAG}\n\
[2] Gato Guerrero      {PRECIO_GUE}\n\
[3] Gato Caballero     {PRECIO_CAB}\n\
[4] Ítem Armadura      {PRECIO_ARMADURA}\n\
[5] Ítem Pergamino     {PRECIO_PERGAMINO}\n\
[6] Ítem Lanza         {PRECIO_LANZA}\n\
[7] Curar Ejército     {PRECIO_CURA}\n\
[0] Volver al Menú de inicio\n\
Indique su opción:')
                tienda = input()
                unidades = []
                with open('data/unidades.txt') as file:
                    file = ''.join(file.readlines()).split('\n')
                    for data_gato in file:
                        unidades.append(data_gato.split(','))
                posibles = []
                if tienda == '0':
                    loop_tienda = False
                    print('volviendo al menu de inicio')
                elif tienda == '1':
                    if persona.oro >= PRECIO_MAG:
                        persona.oro -= PRECIO_MAG
                        for unidad in unidades:
                            if unidad[1] == 'MAG':
                                posibles.append(','.join(unidad))
                        persona.combatientes.append(\
                            instanciar(posibles[randint(0, len(posibles) - 1)]))
                elif tienda == '2':
                    if persona.oro >= PRECIO_GUE:
                        persona.oro -= PRECIO_GUE
                        for unidad in unidades:
                            if unidad[1] == 'GUE':
                                posibles.append(','.join(unidad))
                        persona.combatientes.append(\
                            instanciar(posibles[randint(0, len(posibles) - 1)]))
                elif tienda == '3':
                    if persona.oro >= PRECIO_CAB:
                        persona.oro -= PRECIO_CAB
                        for unidad in unidades:
                            if unidad[1] == 'CAB':
                                posibles.append(','.join(unidad))
                        persona.combatientes.append(\
                            instanciar(posibles[randint(0, len(posibles) - 1)]))
                elif tienda == '4':
                    if persona.oro >= PRECIO_ARMADURA:
                        persona.oro -= PRECIO_ARMADURA
                        item = Item('armadura')
                        for gato in persona.combatientes:
                            if gato.tipo in ['Mago', 'Guerrero']:
                                posibles.append(gato)
                        if len(posibles) == 0:
                            print('no hay gatos combatientes compatibles con el item')
                            persona.oro += PRECIO_ARMADURA
                        else:
                            posicion = menu_gatos(posibles)
                            posicion = persona.posicion(posicion[0], posicion[1])
                            evolucionado = persona.combatientes[posicion]
                            evolucionado = evolucionado.evolucionar(item)
                            persona.combatientes[posicion] = evolucionado
                elif tienda == '5':
                    if persona.oro >= PRECIO_PERGAMINO:
                        persona.oro -= PRECIO_PERGAMINO
                        item = Item('pergamino')
                        for gato in persona.combatientes:
                            if gato.tipo in ['Caballero', 'Guerrero']:
                                posibles.append(gato)
                        if len(posibles) == 0:
                            print('no hay gatos combatientes compatibles con el item')
                            persona.oro += PRECIO_PERGAMINO
                        else:
                            posicion = menu_gatos(posibles)
                            posicion = persona.posicion(posicion[0], posicion[1])
                            evolucionado = persona.combatientes[posicion]
                            evolucionado = evolucionado.evolucionar(item)
                            persona.combatientes[posicion] = evolucionado
                elif tienda == '6':
                    if persona.oro >= PRECIO_LANZA:
                        persona.oro -= PRECIO_LANZA
                        item = Item('lanza')
                        for gato in persona.combatientes:
                            if gato.tipo in ['Caballero', 'Mago']:
                                posibles.append(gato)
                        if len(posibles) == 0:
                            print('no hay gatos combatientes compatibles con el item')
                            persona.oro += PRECIO_PERGAMINO
                        else:
                            posicion = menu_gatos(posibles)
                            posicion = persona.posicion(posicion[0], posicion[1])
                            evolucionado = persona.combatientes[posicion]
                            evolucionado = evolucionado.evolucionar(item)
                            persona.combatientes[posicion] = evolucionado
                elif tienda == '7':
                    if persona.oro >= PRECIO_CURA:
                        for combatiente in persona.combatientes:
                            combatiente.curarse(CURAR_VIDA)
                        persona.oro -= PRECIO_CURA
                else:
                    print('input invalido')
        elif menu == '2':
            print(persona)
        elif menu == '3':
            pelea = persona.combatir(gato_chico[ronda_act - 1])
            if pelea:
                ronda_act += 1
                persona.oro += ORO_GANADO
                if ronda_act == 4:
                    print('FELICIDADES DERROTASTE A GATO CHICO')
                    print('Despidete de los combatientes que sobrevivieron a tan ardua batalla')
                    print(persona)
                    print('cerrando el programa')
                    loop_menu = False
            else:
                ronda_act = 1
                gato_chico = instanciar_rondas(ronda_1, ronda_2, ronda_3)
                persona.oro = ORO_INICIAL
                print('Fuiste derrotado, pero te dare otra oportunidad')
        elif menu == '0':
            print('cerrando el programa')
            loop_menu = False