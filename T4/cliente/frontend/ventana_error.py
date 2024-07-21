from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, QUrl
from PyQt6.QtMultimedia import QSoundEffect

class VentanaError(QWidget):
    senal_mostrar_error = pyqtSignal()
    senal_error_cerrado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Error')
        self.setGeometry(150, 150, 400, 100)
        layout = QVBoxLayout()

        self.etiqueta_error = QLabel(self)
        layout.addWidget(self.etiqueta_error)

        boton_cerrar = QPushButton('Cerrar', self)
        boton_cerrar.clicked.connect(self.hide)
        boton_cerrar.clicked.connect(self.senal_error_cerrado.emit)
        layout.addWidget(boton_cerrar)

        self.setLayout(layout)
    
    def mostrar_error(self, mensaje_error):
        self.etiqueta_error.setText(mensaje_error)
        self.senal_mostrar_error.emit()
        self.show()


class VentanaJuegoMalComprobado(QWidget):
    senal_mostrar_error = pyqtSignal()
    senal_error_cerrado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.sonidos = True

    def initUI(self):
        self.setWindowTitle('El puzzle no esta correcto')
        self.setGeometry(150, 150, 400, 100)
        layout = QVBoxLayout()

        self.etiqueta_error = QLabel(self)
        layout.addWidget(self.etiqueta_error)

        boton_cerrar = QPushButton('Cerrar', self)
        boton_cerrar.clicked.connect(self.hide)
        boton_cerrar.clicked.connect(self.senal_error_cerrado.emit)
        layout.addWidget(boton_cerrar)

        self.setLayout(layout)
    
    def mostrar_error(self, mensaje_error):
        self.etiqueta_error.setText(mensaje_error)
        if mensaje_error == 'Te quedaste sin tiempo para terminar el puzzle':
            if self.sonidos:
                sonido = QSoundEffect(self)
                sonido.setSource(QUrl.fromLocalFile('assets/sonidos/juego_perdido.wav'))
                sonido.play()
        self.senal_mostrar_error.emit()
        self.show()
    
    def silencio(self):
        self.sonidos = False


class VentanaJuegoBienComprobado(QWidget):
    senal_volver_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.sonidos = True

    def initUI(self):
        self.setWindowTitle('Felicidades')
        self.setGeometry(150, 150, 300, 100)
        layout = QVBoxLayout()

        self.etiqueta_error = QLabel(self)
        layout.addWidget(self.etiqueta_error)

        boton_cerrar = QPushButton('Cerrar', self)
        boton_cerrar.clicked.connect(self.hide)
        boton_cerrar.clicked.connect(self.senal_volver_inicio.emit)
        layout.addWidget(boton_cerrar)

        self.setLayout(layout)
    
    def mostrar_felicitaciones(self, puntaje):
        if self.sonidos:
            sonido = QSoundEffect(self)
            sonido.setSource(QUrl.fromLocalFile('assets/sonidos/juego_ganado.wav'))
            sonido.play()
        self.etiqueta_error.setText(f'Tu puntaje fue {puntaje}')
        self.show()
    
    def silencio(self):
        self.sonidos = False