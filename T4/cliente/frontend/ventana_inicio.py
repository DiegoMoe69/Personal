import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout\
, QTableWidget, QTableWidgetItem, QComboBox

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from momasos_diego import cargar_puzzle, cargar_puntajes

class VentanaInicio(QWidget):

    senal_revisar_usuario = pyqtSignal(str)
    senal_verificar_puzzle = pyqtSignal(list, str)
    senal_cerrar_todo = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.info_puzzle = []
        self.dificultad = None
        self.sonidos = True
        self.musica_fondo = ['assets/sonidos/musica_1.wav',\
                             'assets/sonidos/musica_2.wav']
        self.musica_indice = 0
        self.musica = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.musica.setAudioOutput(self.audio)
        self.musica.mediaStatusChanged.connect(self.cambio_cancion)
        self.musica.setSource(QUrl.fromLocalFile(\
                    self.musica_fondo[self.musica_indice]))
        self.musica.play()
        
    def initUI(self):
        # Layout principal
        layout = QHBoxLayout()
        contenedor = QWidget()
        layout_izquierda = QVBoxLayout()
        
        # Logo
        logo = QLabel(self)
        pixmap = QPixmap('assets/sprites/logo.png')
        pixmap = pixmap.scaled(400, 400)
        logo.setPixmap(pixmap)
        layout.addWidget(logo)

        # Salon de la fama
        self.puntajes = cargar_puntajes()
        self.tabla_puntajes = QTableWidget(self)
        self.tabla_puntajes.setColumnCount(2)
        self.tabla_puntajes.setHorizontalHeaderLabels(['Usuario', 'Puntaje'])
        self.tabla_puntajes.setRowCount(len(self.puntajes))
        for ranking in range(len(self.puntajes)):
            self.tabla_puntajes.setItem(ranking, 0, QTableWidgetItem(str(self.puntajes[ranking][0])))
            self.tabla_puntajes.setItem(ranking, 1, QTableWidgetItem(str(self.puntajes[ranking][1])))
        self.tabla_puntajes.setFixedSize(220, 120)
        layout_izquierda.addWidget(self.tabla_puntajes)
        
        # Selector puzzle
        selector_puzzle = QPushButton('Seleccionar Puzzle', self)
        selector_puzzle.clicked.connect(self.abrir_selector_puzzle)
        layout_izquierda.addWidget(selector_puzzle)

        # Campo de nombre de usuario
        self.nombre_usuario = QLineEdit(self)
        self.nombre_usuario.setPlaceholderText('Ingresa tu nombre de usuario')
        layout_izquierda.addWidget(self.nombre_usuario)
        
        # Botón para iniciar el juego
        btn_iniciar = QPushButton('Iniciar Juego', self)
        btn_iniciar.clicked.connect(self.verificar_usuario)
        btn_iniciar.clicked.connect(self.verificar_puzzle)
        layout_izquierda.addWidget(btn_iniciar)
        
        # Botón para cerrar el juego
        btn_cerrar = QPushButton('Salir', self)
        btn_cerrar.clicked.connect(self.senal_cerrar_todo.emit)
        btn_cerrar.clicked.connect(self.close)
        layout_izquierda.addWidget(btn_cerrar)

        # Configurar layout principal
        contenedor.setLayout(layout_izquierda)
        layout.addWidget(contenedor)
        self.setLayout(layout)
        self.setWindowTitle('Ventana de Inicio')
        self.show()

    
    def abrir_selector_puzzle(self):
        self.hide()
        self.selector_puzzle = VentanaSelectorPuzzle()
        self.selector_puzzle.puzzle_seleccionado.connect(self.puzzle_seleccionado)
        self.selector_puzzle.show()

    def puzzle_seleccionado(self, seleccionado):
        self.selector_puzzle.close()
        self.show()
        self.dificultad = seleccionado
        self.info_puzzle = cargar_puzzle(seleccionado)

    def verificar_puzzle(self):
        self.senal_verificar_puzzle.emit(self.info_puzzle, self.dificultad)

    def verificar_usuario(self):
        usuario = self.nombre_usuario.text()
        self.senal_revisar_usuario.emit(usuario)

    def cambio_cancion(self, estado):
        if estado == QMediaPlayer.MediaStatus.EndOfMedia and self.sonidos:
            if self.musica_indice == 0:
                self.musica_indice = 1
                self.musica = QMediaPlayer(self)
                self.audio = QAudioOutput(self)
                self.musica.setAudioOutput(self.audio)
                self.musica.mediaStatusChanged.connect(self.cambio_cancion)
                self.musica.setSource(QUrl.fromLocalFile(\
                            self.musica_fondo[self.musica_indice]))
                self.musica.play()
            elif self.musica_indice == 1:
                self.musica_indice = 0
                self.musica = QMediaPlayer(self)
                self.audio = QAudioOutput(self)
                self.musica.setAudioOutput(self.audio)
                self.musica.mediaStatusChanged.connect(self.cambio_cancion)
                self.musica.setSource(QUrl.fromLocalFile(\
                            self.musica_fondo[self.musica_indice]))
                self.musica.play()
        
    def silencio(self):
        self.musica.stop()
        self.sonidos = False

    def reiniciar(self):
        self.nombre_usuario.setText('')
        self.nombre_usuario.setPlaceholderText('Ingresa tu nombre de usuario')
        self.info_puzzle = None
        self.dificultad = None
        for persona in range(len(self.puntajes)):
            for i in [0, 1]:
                self.tabla_puntajes.removeCellWidget(persona, i)
        self.puntajes = cargar_puntajes()
        self.tabla_puntajes.setRowCount(len(self.puntajes))
        for ranking in range(len(self.puntajes)):
            self.tabla_puntajes.setItem(ranking, 0, QTableWidgetItem(str(self.puntajes[ranking][0])))
            self.tabla_puntajes.setItem(ranking, 1, QTableWidgetItem(str(self.puntajes[ranking][1])))
    
    def cerrar(self):
        self.senal_cerrar_todo.emit()
        self.close()


class VentanaSelectorPuzzle(QWidget):
    puzzle_seleccionado = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Selector de Puzzle')
        self.resize(300, 200)
        layout = QVBoxLayout()

        self.combo_box = QComboBox(self)
        self.cargar_puzzles()
        layout.addWidget(self.combo_box)

        btn_seleccionar = QPushButton('Seleccionar', self)
        btn_seleccionar.clicked.connect(self.seleccionar_puzzle)
        layout.addWidget(btn_seleccionar)

        self.setLayout(layout)

    def cargar_puzzles(self):
        ruta_base_puzzles = os.path.join('assets', 'base_puzzles')
        lista_de_puzzles = os.listdir(ruta_base_puzzles)
        for archivo in lista_de_puzzles:
            self.combo_box.addItem(archivo.strip())

    def seleccionar_puzzle(self):
        puzzle = self.combo_box.currentText()
        self.puzzle_seleccionado.emit(puzzle)