import socket
import parametros as p
from momasos_diego import ingresar_puntaje
from codificacion import codificar, decodificacion
from PyQt6.QtCore import pyqtSignal, QObject, QThread


class Juego(QObject):

    senal_terminar = pyqtSignal()
    senal_actualizar_casilla = pyqtSignal(list)
    senal_actualizar_pepa = pyqtSignal(list)
    senal_solicitar_tiempo = pyqtSignal()
    senal_mensaje_error = pyqtSignal(str)
    senal_victoria = pyqtSignal(int)
    senal_emitir_sonido = pyqtSignal(str)
    
    def __init__(self, host, port):
        super().__init__()
        self.cliente_thread = ClienteThread(host, port)
        self.cliente_thread.senal_mensaje.connect(self.recibir_mensaje)
        self.cliente_thread.senal_desconexion.connect(self.desconexion)
        self.cliente_thread.start()

    def desconexion(self, error):
        self.senal_mensaje_error.emit(error)
        self.senal_terminar.emit()

    def iniciar_usuario(self, lista):
        self.posicion = [0,0]
        self.dificultad = lista[0]
        self.usuario = lista[1]

    def iniciar_juego(self, info_puzzle):
        self.puzzle = []
        self.largo = info_puzzle[0]
        for y in range(self.largo):
            columna = []
            for x in range(self.largo):
                columna.append(1)
            self.puzzle.append(columna)

    def mover_pepa(self, event):
        direccion = event['direccion']
        dict_dirrecion = {'left': (0, -1), 'right': (0, 1), 'up': (-1, 0), 'down': (1, 0)}
        
        if dict_dirrecion[direccion][0] + self.posicion[0] < 0:
            return
        if dict_dirrecion[direccion][0] + self.posicion[0] > self.largo - 1:
            return
        if dict_dirrecion[direccion][1] + self.posicion[1] < 0:
            return
        if dict_dirrecion[direccion][1] + self.posicion[1] > self.largo - 1:
            return
        self.senal_actualizar_casilla.emit([self.puzzle[self.posicion[0]][self.posicion[1]],\
                                        self.posicion[0], self.posicion[1]])
        self.posicion[0] += dict_dirrecion[direccion][0]
        self.posicion[1] += dict_dirrecion[direccion][1]
        self.senal_actualizar_pepa.emit([self.posicion[0], self.posicion[1]])
        
    def interactuar(self):
        if self.puzzle[self.posicion[0]][self.posicion[1]] == 1 or\
        self.puzzle[self.posicion[0]][self.posicion[1]] == 2:
            self.senal_emitir_sonido.emit('comer')
            self.puzzle[self.posicion[0]][self.posicion[1]] = 0
        
        elif self.puzzle[self.posicion[0]][self.posicion[1]] == 0:
            self.senal_emitir_sonido.emit('caca')
            self.puzzle[self.posicion[0]][self.posicion[1]] = 2

    def revisar_informacion(self, tiempos):
        self.tiempo = tiempos
        respuesta = ''
        for linea in self.puzzle:
            for casilla in linea:
                if casilla == 2 or casilla == 1:
                    respuesta += '1'
                elif casilla == 0:
                    respuesta += '0'
            respuesta += '\n'
        respuesta = f'{self.dificultad};' + respuesta[:-1]
        self.cliente_thread.send_message(respuesta)

    def recibir_mensaje(self, mensaje: str):
        if mensaje == 'valido':
            puntaje = round((self.tiempo * len(self.puzzle) * len(self.puzzle) * p.CONSTANTE_PUNTAJE)\
                /(p.TIEMPO_JUEGO - self.tiempo))
            if puntaje == 0:
                ingresar_puntaje(self.usuario, p.PUNTAJE_INF)
                self.senal_victoria.emit(p.PUNTAJE_INF)
            else:
                ingresar_puntaje(self.usuario, puntaje)
                self.senal_victoria.emit(puntaje)
        elif mensaje == 'invalido':
            self.senal_mensaje_error.emit('Aun falta para completar el puzzle')

    def efecto_sandia(self, posicion):
        if self.puzzle[posicion[0]][posicion[1]] == 2:
            self.puzzle[posicion[0]][posicion[1]] = 1
        self.senal_actualizar_casilla.emit([self.puzzle[posicion[0]][posicion[1]],\
                                        posicion[0], posicion[1]])
    


class ClienteThread(QThread):
    senal_mensaje = pyqtSignal(str)
    senal_desconexion = pyqtSignal(str)
    
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def run(self):
        self.sock.connect((self.host, self.port))
        while self.running:
            try:
                mensaje = decodificacion(self.sock.recv(10000))
                if mensaje:
                    self.senal_mensaje.emit(mensaje)
            except ConnectionResetError:
                self.senal_desconexion.emit('Se desconecto el servidor')
                self.running = False
                self.sock.close()
                break

    def send_message(self, mensaje):
        self.sock.sendall(codificar(mensaje))