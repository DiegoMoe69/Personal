import time
import random
import parametros as p
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QVBoxLayout, \
    QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal, QUrl, Qt,  QSize, QTimer, QThread
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtGui import QPixmap, QIcon


class VentanaJuego(QWidget):

    senal_teclas = pyqtSignal(dict)
    empezar_senal_frontend = pyqtSignal()
    senal_juego_termino = pyqtSignal()
    senal_volver_inicio = pyqtSignal()
    pepa_interactuar = pyqtSignal()
    senal_puntajes_tiempos = pyqtSignal(int)
    senal_efecto_sandia = pyqtSignal(list)
    mutear = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.threads = []
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.timer = None
        self.sandias_timer = None
        self.sonidos = True
        self.inf = True
        
        self.estado_m = False
        self.estado_u = False
        self.estado_t = False
        self.estado_i = False
        self.estado_n = False

    def init_ui(self, info_puzzle):
        self.info_puzzle = info_puzzle
        self.setWindowTitle("DCCome lechuga")
        self.setGeometry(100, 100, 250 + info_puzzle[0] * 30, 130 + info_puzzle[0] * 30)

        self.layout_general = QHBoxLayout()

        contenedor = QWidget()
        layout_estadisticas = QVBoxLayout()

        # layout derecha
        self.minutos = p.TIEMPO_JUEGO // 60
        self.segundos = p.TIEMPO_JUEGO % 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.estado_timer = True
        self.timer_label = QLabel(f'{self.minutos}:{self.segundos}', self)
        layout_estadisticas.addWidget(self.timer_label)

        btn_comprobar = QPushButton("Comprobar", self)
        btn_comprobar.clicked.connect(self.comprobadorinador)
        layout_estadisticas.addWidget(btn_comprobar)

        self.btn_pausar = QPushButton("Pausar", self)
        self.btn_pausar.clicked.connect(self.pausar_juego)
        layout_estadisticas.addWidget(self.btn_pausar)

        btn_salir = QPushButton("Salir", self)
        btn_salir.clicked.connect(self.senal_volver_inicio.emit)
        btn_salir.clicked.connect(self.reiniciar)
        layout_estadisticas.addWidget(btn_salir)

        contenedor.setLayout(layout_estadisticas)

        ## GRILLA
        self.grilla = QTableWidget(self)
        self.grilla.setColumnCount(info_puzzle[0])
        self.grilla.setRowCount(info_puzzle[0])
        for i, label in enumerate(info_puzzle[1]):
            header_item = QTableWidgetItem()
            header_item.setText("\n".join(label.split(",")))
            self.grilla.setHorizontalHeaderItem(i, header_item)
        for i, label in enumerate(info_puzzle[2]):
            header_item = QTableWidgetItem()
            header_item.setText(" ".join(label.split(",")))
            self.grilla.setVerticalHeaderItem(i, header_item)
        cell_size = 30
        for i in range(info_puzzle[0]):
            self.grilla.setColumnWidth(i, cell_size)
            self.grilla.setRowHeight(i, cell_size)
        pixmap = QPixmap('assets/sprites/lechuga.png').scaled(30, 30)
        for x in range(info_puzzle[0]):
            for y in range(info_puzzle[0]):
                lechuga = QLabel(self)
                lechuga.setPixmap(pixmap)
                self.grilla.setCellWidget(x, y, lechuga)
        
        ## PEPA
        self.update_pepa([0,0])

        ## sandias
        self.sandias_timer = QTimer(self)
        self.sandias_timer.timeout.connect(self.update_sandias)
        self.sandias_timer.start(p.TIEMPO_APARICION * 1000)

        self.layout_general.addWidget(self.grilla)
        self.layout_general.addWidget(contenedor)
        self.setLayout(self.layout_general)
        self.show()

    def update_timer(self):
        if self.inf:
            if self.segundos > 0:
                self.segundos -= 1
                self.timer_label.setText(f'{self.minutos}:{self.segundos}')
            elif self.segundos == 0 and self.minutos > 0:
                self.minutos -= 1
                self.segundos = 59
                self.timer_label.setText(f'{self.minutos}:{self.segundos}')
            else:
                self.senal_juego_termino.emit()

    def update_sandias(self):
        eje_x = random.randint(0, self.info_puzzle[0] - 1)
        eje_y = random.randint(0, self.info_puzzle[0] - 1)
        self.update_casilla([3, eje_x, eje_y])

    def pausar_juego(self):
        if self.inf:
            if self.estado_timer:
                self.timer.stop()
                self.sandias_timer.stop()
                self.grilla.hide()
                self.btn_pausar.setText('Reanudar')
            else:
                self.timer.start(1000)
                self.sandias_timer.start(p.TIEMPO_APARICION * 1000)
                self.grilla.show()
                self.btn_pausar.setText('Pausar')
            self.estado_timer = not self.estado_timer

    def update_casilla(self, info_previa):
        if info_previa[0] == 0:
            self.grilla.removeCellWidget(info_previa[1], info_previa[2])
        elif info_previa[0] == 1:
            self.grilla.removeCellWidget(info_previa[1], info_previa[2])
            lechuga = QLabel(self)
            lechuga.setPixmap(QPixmap('assets/sprites/lechuga.png').scaled(30, 30))
            self.grilla.setCellWidget(info_previa[1], info_previa[2], lechuga)
        elif info_previa[0] == 2:
            caca_thread = Caca(p.TIEMPO_TRANSICION, info_previa[1], info_previa[2])
            caca_thread.finished.connect(\
                lambda x: self.senal_efecto_sandia.emit([info_previa[1], info_previa[2]]))
            self.threads.append(caca_thread)
            caca_thread.start()
            self.grilla.removeCellWidget(info_previa[1], info_previa[2])
            caca = QLabel(self)
            caca.setPixmap(QPixmap('assets/sprites/poop.png').scaled(30, 30))
            self.grilla.setCellWidget(info_previa[1], info_previa[2], caca)
        elif info_previa[0] == 3:
            sandia_thread = Caca(p.TIEMPO_DURACION, info_previa[1], info_previa[2])
            sandia_thread.finished.connect(\
                lambda x: self.senal_efecto_sandia.emit([info_previa[1], info_previa[2]]))
            self.threads.append(sandia_thread)
            sandia_thread.start()
            self.grilla.removeCellWidget(info_previa[1], info_previa[2])
            sandia = QPushButton(self)
            icono_sandia = QIcon('assets/sprites/sandia.png')
            sandia.setIcon(icono_sandia)
            sandia.setIconSize(QSize(30, 30))
            sandia.clicked.connect(lambda x: self.sandia_efecto(info_previa[1],\
                                                    info_previa[2]))
            self.grilla.setCellWidget(info_previa[1], info_previa[2], sandia)
        
    def update_pepa(self, info_pepa):
        self.grilla.removeCellWidget(info_pepa[0], info_pepa[1])
        pepa = QLabel(self)
        pepa.setPixmap(QPixmap('assets/sprites/pepa/down_0.png').scaled(30, 30))
        self.grilla.setCellWidget(info_pepa[0], info_pepa[1], pepa)
        
    def sandia_efecto(self, eje_x, eje_y):
        self.senal_efecto_sandia.emit([eje_x, eje_y])
        self.minutos += p.TIEMPO_ADICIONAL // 60
        self.segundos += p.TIEMPO_ADICIONAL % 60
        if self.sonidos:
            sonido = QSoundEffect(self)
            sonido.setSource(QUrl.fromLocalFile('assets/sonidos/obtener_sandia.wav'))
            sonido.play()
        if self.segundos > 59:
            self.segundos -= 59
            self.minutos += 1

    def comprobadorinador(self):
        if self.inf:
            self.timer.stop()
            self.sandias_timer.stop()
            self.grilla.hide()
        if self.inf:
            self.senal_puntajes_tiempos.emit(self.minutos * 60 + self.segundos)
        else:
            self.senal_puntajes_tiempos.emit(0)

    def resume(self):
        if self.timer is not None:
            self.timer.start(1000)
            self.sandias_timer.start(p.TIEMPO_APARICION * 1000)
            self.grilla.show()

    def sonido(self, efecto):
        if self.sonidos:
            if efecto == 'comer':
                sonido = QSoundEffect(self)
                sonido.setSource(QUrl.fromLocalFile('assets/sonidos/comer.wav'))
                sonido.play()
            elif efecto == 'caca':
                sonido = QSoundEffect(self)
                sonido.setSource(QUrl.fromLocalFile('assets/sonidos/poop.wav'))
                sonido.play()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            self.senal_teclas.emit({'direccion': 'up'})
        if event.key() == Qt.Key.Key_A:
            self.senal_teclas.emit({'direccion': 'left'})
        if event.key() == Qt.Key.Key_S:
            self.senal_teclas.emit({'direccion': 'down'})
        if event.key() == Qt.Key.Key_D:
            self.senal_teclas.emit({'direccion': 'right'})
        if event.key() == Qt.Key.Key_G:
            self.pepa_interactuar.emit()
        ## MUTE
        if event.key() == Qt.Key.Key_M:
            self.estado_m = True
        if event.key() == Qt.Key.Key_U and self.estado_m:
            self.estado_u = True
        if event.key() == Qt.Key.Key_T and self.estado_u:
            self.estado_t = True
        if event.key() == Qt.Key.Key_E and self.estado_t:
            self.sonidos = False
            self.mutear.emit()
        ## INF
        if event.key() == Qt.Key.Key_I:
            self.estado_i = True
        if event.key() == Qt.Key.Key_N and self.estado_i:
            self.estado_n = True
        if event.key() == Qt.Key.Key_F and self.estado_n:
            self.timer_label.setText('infinito')
            self.timer.stop()
            self.sandias_timer.stop()
            self.inf = False
            self.btn_pausar.setText('Cheater')
            
        
    def reiniciar(self):
        self.hide()
        self.timer.stop()
        if self.sandias_timer is not None:
            self.sandias_timer.stop()
        if self.layout_general is not None:
            for i in reversed(range(self.layout_general.count())):
                widget = self.layout_general.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)
            self.layout_general.deleteLater()
        self.layout_general = None

    def cerrar(self):
        self.close()



class Caca(QThread):

    finished = pyqtSignal(list)

    def __init__(self, tiempo, eje_x, eje_y):
        super().__init__()
        self.tiempo = tiempo
        self.eje_x = eje_x
        self.eje_y = eje_y

    def run(self):
        time.sleep(self.tiempo)
        self.finished.emit([self.eje_x, self.eje_y])