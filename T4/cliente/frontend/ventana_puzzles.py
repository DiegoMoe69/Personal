from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox
from PyQt6.QtCore import pyqtSignal
import os

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