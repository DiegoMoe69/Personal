from abc import ABC, abstractmethod

from parametros import CANSANCIO, PROB_CAB, RED_CAB, ATQ_CAB,PROB_MAG, RED_MAG, ATQ_MAG,\
PROB_PAL, AUM_PAL, PROB_MDB, DEF_MDB, PROB_CAR, AUM_CAR

from random import randint


class Ejercito:
    def __init__(self, oro):
        self.combatientes = []
        self.oro = oro
    
    def combatir(self, gato_chico):
        while True:
            dano_1 = self.combatientes[0].atacar(gato_chico.combatientes[0])
            dano_2 = gato_chico.combatientes[0].atacar(self.combatientes[0])
            self.combatientes[0].actualizar_stats(dano_2)
            gato_chico.combatientes[0].actualizar_stats(dano_1)
            if self.combatientes[0].vida == 0:
                self.combatientes.pop(0)
            if gato_chico.combatientes[0].vida == 0:
                gato_chico.combatientes.pop(0)
            if len(self.combatientes) == 0:
                return False
            elif len(gato_chico.combatientes) == 0:
                return True
    
    def posicion(self, n_nombre, nombre):
        contador_nombre = 1
        contador_posicion = 0
        for gato in self.combatientes:
            if gato.nombre == nombre and contador_nombre == n_nombre:
                return contador_posicion
            elif gato.nombre == nombre:
                contador_nombre += 1
                if gato.tipo not in ['Mago', 'Caballero', 'Guerrero']:
                    contador_nombre -= 1
            contador_posicion += 1

    def __str__(self):
        print('*** Este es tu Ejército Actual ***')
        print('      Clase      Nombre')
        n = 1
        for gato in self.combatientes:
            print(f'[{n}] Gato {gato.tipo} {gato.nombre}')
            n += 1
        print(f'Te quedan {len(self.combatientes)} combatientes. ¡Éxito, Guerrero!')
        return ''


class Item:
    def __init__(self, tipo):
        self.tipo = tipo
        self.lista = []
    
    @property
    def lista(self):
        return self._lista
    
    @lista.setter
    def lista(self,nueva_lista):
        if self.tipo == 'pergamino':
            self._lista = ['CAB','GUE']
        elif self.tipo == 'armadura':
            self._lista = ['MAG','GUE']
        else:
            self._lista = ['MAG','CAB']


class Combatiente(ABC):
    def __init__(self,
                nombre: str,
                vida_max: int,
                poder: int,
                defensa: int,
                agilidad: int,
                resistencia: int,
                **kwargs):
        self.nombre = nombre
        self.vida_max = vida_max
        self.vida = vida_max
        self.poder = poder
        self.defensa = defensa
        self.agilidad = agilidad
        self.resistencia = resistencia
    
    @property
    def vida(self) -> int:
        return self._vida

    @vida.setter
    def vida(self, nueva_vida):
        if nueva_vida >= self.vida_max:
            self._vida = self.vida_max
        elif nueva_vida < 0 :
            self._vida = 0
        else:
            self._vida = nueva_vida


    #por cansancio
    @property
    def agilidad(self):
        return self._agilidad
    
    @agilidad.setter
    def agilidad(self, nueva_agilidad):
        if nueva_agilidad > 10:
            self._agilidad = 10
        elif nueva_agilidad < 1:
            self._agilidad = 1
        else:
            self._agilidad = nueva_agilidad
    
    
    @property
    def ataque(self):
        return round((self.poder + self.agilidad + self.resistencia)\
                    * 2 * self.vida / self.vida_max) 


    #por el debuff de caballero
    @property
    def poder(self):
        return self._poder
    
    @poder.setter
    def poder(self, nuevo_poder):
        if nuevo_poder > 10:
            self._poder = 10
        elif nuevo_poder < 1:
            self._poder = 1
        else:
            self._poder = nuevo_poder


    #por el buff de paladin
    @property
    def resistencia(self):
        return self._resistencia
    
    @resistencia.setter
    def resistencia(self, nueva_resistencia):
        if nueva_resistencia > 10:
            self._resistencia = 10
        elif nueva_resistencia < 1:
            self._resistencia = 1
        else:
            self._resistencia = nueva_resistencia


    #por el buff de mago de batalla
    @property
    def defensa(self):
        return self._defensa
    
    @defensa.setter
    def defensa(self, nueva_defensa):
        if nueva_defensa > 20:
            self._defensa = 20
        elif nueva_defensa < 1:
            self._defensa = 1
        else:
            self._defensa = nueva_defensa


    @abstractmethod
    def atacar(self):
        pass
    
    def curarse(self, cura):
            self.vida += cura
    
    @abstractmethod
    def evolucionar(self):
        pass
    
    def actualizar_stats(self, info: tuple):
        self.vida -= info[0]
        if info[1][0] == False:
            return
        else:
            if 'poder' in info[1][1]:
                self.poder += info[1][2]

    def __str__(self):
        return f'¡Hola! Soy {self.nombre}, un Gato # con {self.vida} / {self.vida_max} \
        de vida, {self.ataque} de ataque y {self.defensa} de defensa.'


class Guerrero(Combatiente):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'Guerrero'
    
    def evolucionar(self, item: Item):
        if 'pergamino' == item.tipo:
            return Mago_de_Batalla(nombre = self.nombre,
                vida_max = self.vida_max,
                poder = self.poder,
                defensa = self.defensa,
                agilidad = self.agilidad,
                resistencia = self.resistencia)
        elif 'armadura' == item.tipo:
            return Paladin(nombre = self.nombre,
                vida_max = self.vida_max,
                poder = self.poder,
                defensa = self.defensa,
                agilidad = self.agilidad,
                resistencia = self.resistencia)
    
    def atacar(self, enemigo):
        ataque = self.ataque
        self.agilidad -= self.agilidad * CANSANCIO / 100
        ataque = round(ataque - enemigo.defensa)
        if ataque < 1:
            return (1, (False, 0, 0))
        return (ataque, (False, 0, 0))


class Caballero(Combatiente):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'Caballero'
    
    def evolucionar(self, item: Item):
        if 'pergamino' == item.tipo:
            return Caballero_Arcano(nombre = self.nombre,
                vida_max = self.vida_max,
                poder = self.poder,
                defensa = self.defensa,
                agilidad = self.agilidad,
                resistencia = self.resistencia)
        elif 'lanza' == item.tipo:
            return Paladin(nombre = self.nombre,
                vida_max = self.vida_max,
                poder = self.poder,
                defensa = self.defensa,
                agilidad = self.agilidad,
                resistencia = self.resistencia)
    
    def atacar(self, enemigo):
        if randint(0, 100) <= PROB_CAB:
            ataque = self.ataque
            ataque = round((ataque * ATQ_CAB / 100) - enemigo.defensa)
            debufs = (True, 'poder', - enemigo.poder * RED_CAB / 100)
        else:
            ataque = self.ataque
            debufs = (False, 0, 0)
            ataque = round(ataque - enemigo.defensa)
        self.resistencia -= self.resistencia * CANSANCIO / 100
        if ataque < 1:
            return (1, debufs)
        return (ataque, debufs)


class Mago(Combatiente):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'Mago'
    
    def evolucionar(self, item: Item):
        if 'lanza' == item.tipo:
            return Mago_de_Batalla(nombre = self.nombre,
                vida_max = self.vida_max,
                poder = self.poder,
                defensa = self.defensa,
                agilidad = self.agilidad,
                resistencia = self.resistencia)
        elif 'armadura' == item.tipo:
            return Caballero_Arcano(nombre = self.nombre,
                vida_max = self.vida_max,
                poder = self.poder,
                defensa = self.defensa,
                agilidad = self.agilidad,
                resistencia = self.resistencia)
    
    def atacar(self, enemigo):
        if randint(0, 100) <= PROB_MAG:
            ataque = self.ataque
            ataque = round((ataque * ATQ_MAG / 100) - enemigo.defensa * (100 - RED_MAG) / 100)
            debufs = (False, 0, 0)
        else:
            ataque = self.ataque
            debufs = (False, 0, 0)
            ataque = round(ataque - enemigo.defensa)
        self.agilidad -= self.agilidad * CANSANCIO / 100
        self.resistencia -= self.resistencia * CANSANCIO / 100
        if ataque < 1:
            return (1, debufs)
        return (ataque, debufs)


class Paladin(Guerrero, Caballero):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'Paladin'
    
    def atacar(self, enemigo):
        if randint(0, 100) <= PROB_PAL:
            ataque = self.ataque
            ataque = round((ataque * ATQ_CAB / 100) - enemigo.defensa)
            debufs = (True, 'poder', - enemigo.poder * RED_CAB / 100)
        else:
            ataque = self.ataque
            debufs = (False, 0, 0)
            ataque = round(ataque - enemigo.defensa)
        self.resistencia += self.resistencia * AUM_PAL
        if ataque < 1:
            return (1, debufs)
        return (ataque, debufs)


class Mago_de_Batalla(Guerrero, Mago):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'Mago de batalla'

    #para que el incremento de defensa se aplique despues de atacar
    #este se aplicara al recibir daño
    def actualizar_stats(self, info: tuple):
        self.vida -= info[0]
        self.defensa += self.defensa * DEF_MDB / 100
        if info[1][0] == False:
            return
        else:
            if 'poder' in info[1][1]:
                self.poder += info[1][2]
    
    def atacar(self, enemigo):
        if randint(0, 100) <= PROB_MDB:
            ataque = self.ataque
            ataque = round((ataque * ATQ_MAG / 100) - enemigo.defensa * (100 - RED_MAG) / 100)
            debufs = (False, 0, 0)
        else:
            ataque = self.ataque
            debufs = (False, 0, 0)
            ataque = round(ataque - enemigo.defensa)
        self.agilidad -= self.agilidad * CANSANCIO / 100
        if ataque < 1:
            return (1, debufs)
        return (ataque, debufs)


class Caballero_Arcano(Caballero, Mago):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'Caballero arcano'
    
    def atacar(self, enemigo):
        if randint(0, 100) < PROB_CAR:
            ataque = self.ataque
            ataque = round((ataque * ATQ_CAB / 100) - enemigo.defensa)
            debufs = (True, 'poder', - enemigo.poder * RED_CAB / 100)
        else:
            ataque = self.ataque
            ataque = round((ataque * ATQ_MAG / 100) - enemigo.defensa * (100 - RED_MAG) / 100)
            debufs = (False, 0, 0)
        self.poder += self.agilidad * AUM_CAR / 100
        self.agilidad += self.defensa * AUM_CAR / 100
        self.resistencia -= self.resistencia * CANSANCIO / 100
        if ataque < 1:
            return (1, debufs)
        return (ataque, debufs)