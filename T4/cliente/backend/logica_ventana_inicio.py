import re

from PyQt6.QtCore import pyqtSignal, QObject, QUrl
from PyQt6.QtMultimedia import QSoundEffect


class VentanaInicioBackend(QObject):

    senal_mensaje_error = pyqtSignal(str)
    senal_ocultar_inicio = pyqtSignal()
    senal_comenzar_juego = pyqtSignal(list)
    senal_logica_iniciar = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.puzzle_valido = False
        self.usuario_valido = False
        self.start()
    
    def verificar_usuario(self, usuario: str):
        if not usuario:
            self.senal_mensaje_error.emit('Falta ingresar un nombre de usuario')
        elif not usuario.isalnum():
            self.senal_mensaje_error.emit('El nombre de usuario no es alfanumerico')
        elif not re.search(r'[A-Z]', usuario):
            self.senal_mensaje_error.emit('Falta una mayuscula en el nombre de usuario')
        elif not re.search(r'[0-9]', usuario):
            self.senal_mensaje_error.emit('Falta un numero en el nombre de usuario')
        else:
            self.usuario = usuario
            self.usuario_valido = True

    def verificar_puzzle(self, puzzle, dificultad):
        self.dificultad = dificultad
        if puzzle == []:
            self.senal_mensaje_error.emit('Falta seleccionar un puzzle')
        else:
            self.puzzle_valido = True
            if self.usuario_valido:
                self.senal_ocultar_inicio.emit()
                self.senal_comenzar_juego.emit(puzzle)
                self.senal_logica_iniciar.emit([dificultad, self.usuario])

    def start(self):
        pass



class Musica(QObject):

    def __init__(self, ruta_cancion):
        super().__init__()
        self.ruta_cancion = ruta_cancion
        self.media_player_wav = QSoundEffect(self)
        file_url = QUrl.fromLocalFile(self.ruta_cancion)
        self.media_player_wav.setSource(file_url)
        self.media_player_wav.setVolume(0.3)  # Opcional

    def comenzar(self):
        try:
            self.media_player_wav.play()
        except Exception as error:
            print('No se pudo iniciar la canción', error)