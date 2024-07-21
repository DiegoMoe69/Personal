import sys
import json
from PyQt6.QtWidgets import QApplication
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_error import VentanaError, VentanaJuegoMalComprobado, VentanaJuegoBienComprobado
from backend.logica_ventana_inicio import VentanaInicioBackend
from backend.logica_juego import Juego

def hook(type_error, traceback):
    print(type_error)
    print(traceback)

if __name__ == "__main__":
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    # configuracion cliente
    port = int(sys.argv[1])
    with open('config.json') as configuracion:
        config = json.load(configuracion)
    host = config['host']
    ## cambiar al servidor

    ventana_inicio = VentanaInicio()
    logica_inicio = VentanaInicioBackend()
    ventana_juego = VentanaJuego()
    logica_juego = Juego(host, port)

    # funcionamiento de error
    ventana_error = VentanaError()
    logica_inicio.senal_mensaje_error.connect(ventana_error.mostrar_error)
    ventana_error.senal_mostrar_error.connect(ventana_inicio.hide)
    ventana_error.senal_error_cerrado.connect(ventana_inicio.show)

    ventana_comprobar = VentanaJuegoMalComprobado()
    ventana_timeout = VentanaJuegoMalComprobado()
    ventana_comprobado = VentanaJuegoBienComprobado()

    ventana_comprobado.senal_volver_inicio.connect(ventana_juego.reiniciar)
    ventana_comprobado.senal_volver_inicio.connect(ventana_inicio.reiniciar)
    ventana_comprobado.senal_volver_inicio.connect(ventana_inicio.show)
    logica_juego.senal_mensaje_error.connect(ventana_comprobar.mostrar_error)
    ventana_comprobar.senal_mostrar_error.connect(ventana_juego.hide)
    ventana_comprobar.senal_error_cerrado.connect(ventana_juego.show)
    ventana_comprobar.senal_error_cerrado.connect(ventana_juego.resume)

    # Senales victoria
    logica_juego.senal_victoria.connect(ventana_comprobado.mostrar_felicitaciones)

    # verificar usuario y puzzle
    ventana_inicio.senal_revisar_usuario.connect(logica_inicio.verificar_usuario)
    ventana_inicio.senal_verificar_puzzle.connect(logica_inicio.verificar_puzzle)
    logica_inicio.senal_ocultar_inicio.connect(ventana_inicio.hide)

    # senales empezar juego
    logica_inicio.senal_comenzar_juego.connect(ventana_juego.init_ui)
    logica_inicio.senal_logica_iniciar.connect(logica_juego.iniciar_usuario)
    logica_inicio.senal_comenzar_juego.connect(logica_juego.iniciar_juego)

    # señales juego
    ventana_juego.senal_teclas.connect(logica_juego.mover_pepa)
    ventana_juego.pepa_interactuar.connect(logica_juego.interactuar)
    logica_juego.senal_actualizar_casilla.connect(ventana_juego.update_casilla)
    logica_juego.senal_actualizar_pepa.connect(ventana_juego.update_pepa)
    ventana_juego.senal_efecto_sandia.connect(logica_juego.efecto_sandia)

    # sonidos
    logica_juego.senal_emitir_sonido.connect(ventana_juego.sonido)
    ventana_juego.mutear.connect(ventana_inicio.silencio)
    ventana_juego.mutear.connect(ventana_comprobado.silencio)
    ventana_juego.mutear.connect(ventana_comprobar.silencio)
    ventana_juego.mutear.connect(ventana_timeout.silencio)

    # señales comprobar puzzle
    ventana_juego.senal_puntajes_tiempos.connect(logica_juego.revisar_informacion)

    # señales salir
    ventana_inicio.senal_cerrar_todo.connect(ventana_juego.cerrar)
    logica_juego.senal_terminar.connect(ventana_inicio.cerrar)
    logica_juego.senal_terminar.connect(ventana_juego.cerrar)

    # timeout
    ventana_juego.senal_juego_termino.connect(lambda: ventana_timeout.mostrar_error(\
        'Te quedaste sin tiempo para terminar el puzzle'))
    ventana_juego.senal_volver_inicio.connect(lambda: ventana_timeout.mostrar_error(\
        'Regresando al inicio'))
    ventana_timeout.senal_error_cerrado.connect(ventana_inicio.reiniciar)
    ventana_timeout.senal_error_cerrado.connect(ventana_juego.reiniciar)
    ventana_timeout.senal_error_cerrado.connect(ventana_inicio.show)

    sys.exit(app.exec())
