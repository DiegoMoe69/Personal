import dcciudad

class RedMetro:
    def __init__(self, red: list, estaciones: list) -> None:
        self.red = red
        self.estaciones = estaciones
        self.resumen = self.informacion_red()
        self.nombre = ''

    def informacion_red(self) -> list:
        cantidad_estaciones = len(self.estaciones)
        cantidad_tuneles = []
        for info in self.red:
            tuneles = 0
            for tunel in info:
                if tunel == 1:
                    tuneles += 1
            cantidad_tuneles.append(tuneles)
        return [cantidad_estaciones, cantidad_tuneles]

    def agregar_tunel(self, inicio: str, destino: str) -> int:
        estacion_inicio = self.estaciones.index(inicio)
        estacion_destino = self.estaciones.index(destino)
        if self.red[estacion_inicio][estacion_destino] == 0:
            self.red[estacion_inicio][estacion_destino] = 1
            self.resumen = self.informacion_red()
            #actualizamos la informacion de self.resumen
            return self.resumen[1][estacion_inicio]
        else:
            return -1
    
    def tapar_tunel(self, inicio: str, destino: str) -> int:
        estacion_inicio = self.estaciones.index(inicio)
        estacion_destino = self.estaciones.index(destino)
        if self.red[estacion_inicio][estacion_destino] == 1:
            self.red[estacion_inicio][estacion_destino] = 0
            self.resumen = self.informacion_red()
            #actualizamos la informacion de self.resumen
            return self.resumen[1][estacion_inicio]
        else:
            return -1

    def invertir_tunel(self, estacion_1: str, estacion_2: str) -> bool:
        estacion_1_posicion = self.estaciones.index(estacion_1)
        estacion_2_posicion = self.estaciones.index(estacion_2)
        tunel_1_2 = self.red[estacion_1_posicion][estacion_2_posicion]
        tunel_2_1 = self.red[estacion_2_posicion][estacion_1_posicion]
        if tunel_1_2 == 1 and tunel_2_1 == 1:
            return True
        elif tunel_1_2 == 1 and tunel_2_1 == 0:
            self.tapar_tunel(estacion_1,estacion_2)
            self.agregar_tunel(estacion_2,estacion_1)
            return True
        elif tunel_1_2 == 0 and tunel_2_1 == 1:
            self.tapar_tunel(estacion_2,estacion_1)
            self.agregar_tunel(estacion_1,estacion_2)
            return True
        else:
            return False

    def nivel_conexiones(self, inicio: str, destino: str) -> str:
        posicion_1 = self.estaciones.index(inicio)
        posicion_2 = self.estaciones.index(destino)
        alcanzable = dcciudad.alcanzable(self.red, posicion_1, posicion_2)
        if alcanzable == False:
            return 'no hay ruta'
        #no hubiese usado esto pero el test especificaba el uso de la funcion
        posible = self.rutas_posibles(inicio, destino, 1)
        distancia = 1
        while posible == 0:
            distancia += 1
            posible = self.rutas_posibles(inicio, destino, distancia)
        if distancia == 1:
            return 'túnel directo'
        elif distancia == 2:
            return 'estación intermedia'
        else:
            return 'muy lejos'

    def rutas_posibles(self, inicio: str, destino: str, p_intermedias: int) -> int:
        if p_intermedias == 0:
            return 0
        posicion_1 = self.estaciones.index(inicio)
        posicion_2 = self.estaciones.index(destino)
        mapa = dcciudad.elevar_matriz(self.red, p_intermedias)
        return mapa[posicion_1][posicion_2]

    def ciclo_mas_corto(self, estacion: str) -> int:
        posicion = self.estaciones.index(estacion)
        for paradas in range(self.resumen[0]):
            red_temporal = dcciudad.elevar_matriz(self.red, paradas + 1)
            if red_temporal[posicion][posicion] > 0:
                return paradas
        return -1

    def estaciones_intermedias(self, inicio: str, destino: str) -> list:
        posicion_1 = self.estaciones.index(inicio)
        posicion_2 = self.estaciones.index(destino)
        estaciones_salen_1 = []
        estaciones_entran_2 = []
        for tunel in range(self.resumen[0]):
            if self.red[posicion_1][tunel] == 1:
                estaciones_salen_1.append(self.estaciones[tunel])
            if self.red[tunel][posicion_2] == 1:
                estaciones_entran_2.append(self.estaciones[tunel])
        estaciones_intermedias = []
        for estacion in estaciones_salen_1:
            if estacion in estaciones_entran_2:
                estaciones_intermedias.append(estacion)
        return estaciones_intermedias

    def estaciones_intermedias_avanzado(self, inicio: str, destino: str) -> list:
        #Voy a reutilizar gran parte de estaciones_intermedias()
        posicion_1 = self.estaciones.index(inicio)
        posicion_2 = self.estaciones.index(destino)
        estaciones_salen_1 = []
        estaciones_entran_2 = []
        for tunel in range(self.resumen[0]):
            if self.red[posicion_1][tunel] == 1:
                estaciones_salen_1.append(self.estaciones[tunel])
            if self.red[tunel][posicion_2] == 1:
                estaciones_entran_2.append(self.estaciones[tunel])
        estaciones_intermedias = []
        for estacion_inicio in estaciones_salen_1:
            for estacion_destino in estaciones_entran_2:
                if self.nivel_conexiones(estacion_inicio, 
                                         estacion_destino) == 'túnel directo':
                    estaciones_intermedias.append([estacion_inicio, 
                                                   estacion_destino])
        return estaciones_intermedias

    def cambiar_planos(self, nombre_archivo: str) -> bool:    
        try:
            with open('data/' + nombre_archivo) as file:
                info = file.readlines()
                info = ''.join(info).split('\n')
                estaciones = []
                red = []
                red_info = info[int(info[0]) + 1]
                red_info = red_info.split(',')
                for estacion in range(int(info[0])):
                    estaciones.append(info[estacion + 1])
                    red_temporal = []
                    for tunel in range(int(info[0])):
                        red_temporal.append(int(red_info[tunel + estacion * int(info[0])]))
                    red.append(red_temporal)
                self.estaciones = estaciones
                self.red = red
                return True
        except FileNotFoundError:
            return False

    def asegurar_ruta(self, inicio: str, destino: str, p_intermedias: int) -> list:
        if self.rutas_posibles(inicio, destino, p_intermedias + 1) > 0:
            ruta = []
            siguiente = (inicio)
            paradas_faltan = p_intermedias + 1
            for parada in range(p_intermedias + 1):
                ruta.append(siguiente)
                siguiente = self.estacion_siguiente(siguiente, destino, paradas_faltan)
                paradas_faltan -= 1
            #tenemos la ruta
            ruta.append(siguiente)
            if destino in ruta[1:len(ruta) - 1]:
                return []
            red = []
            tuneles = []
            for estaciones in range(self.resumen[0]):
                tuneles.append(0)
            for estaciones in range(self.resumen[0]):
                red.append(tuneles[:])
            for paso in range(p_intermedias + 1):
                posicion_1 = self.estaciones.index(ruta[paso])
                posicion_2 = self.estaciones.index(ruta[paso + 1])
                red[posicion_1][posicion_2] = 1
            return red
        else:
            return []

    def estacion_siguiente(self, inicio: str, destino: str, p_intermedias: int) -> str:
        if p_intermedias == 1:
            return destino
        else:
            posibles_estaciones = []
            posicion = self.estaciones.index(inicio)
            n_estacion = 0
            for estacion_siguiente in self.red[posicion]:
                if estacion_siguiente == 1:
                    posibles_estaciones.append(self.estaciones[n_estacion])
                n_estacion += 1
            #aqui tenemos la lista de posibles estaciones a donde podemos ir desde el inicio
            #ahora hay q ver si es posible desde estas estaciones llegar al destino en 
            for estacion in posibles_estaciones:
                if self.rutas_posibles(estacion, destino, p_intermedias - 1) >= 1:
                    return estacion