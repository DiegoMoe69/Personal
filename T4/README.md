# Tarea 4: DCCome Lechuga 🐢🍉🥬

## Consideraciones generales :octocat:

La tarea hace la mayoria de cosas que solicitan, siendo en general un juego funcional a prueba de los errores comunes.
Al pasar de la ventana de inicio a la ventana de juego hay que tocar (con el mouse) la ventana para que empieze a interactuar con esa pestaña.
El movimiento de pepa por el tablero es discreto, pero no es continuo, ni fluido, ni animado.
La ventana de inicio la modifique un poco solo por estetica, y el salon de la fama muestra los mejores 3 puntajes solamente por un tema solamente de estetica, pero quedan guardados los puntajes en el archivo puntajes.txt.
La ventana de juego es un muy grande con puzzles muy grandes y para computadores con la pantalla chica (como en el que programo) se vuelve complejo la visualizacion, pero al poner la pantalla completa se vuelve mas facil ver todo.
Los cheatcodes se tienen que hacer desde la ventana de juego ya que esta tiene el strong focus y en la ventana de inicio no realizan sus efectos.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Entidades: Hecho completo a excepcion de la animacion solicitada de pepa.
    * Pepa 🟠 1.1: La animacion no existe, pero el movimiento si es discreto
    * Sandias ✅ 1.2: Hecha completa
* Interfaz grafica: Hecha completa, con algunos alcances.
    * Ventana Inicio ✅ 2.1: Hecha completa, pero por temas esteticos se muestran los mejores 3 puntajes, pero si se mantiene resgistro de todos los puntajes.
    * Ventana Juego ✅ 2.2: Hecha completa, ahora me estoy dando cuenta que el boton de salir deberia cerrar el programa, pero ya esta hecho para volver al inicio y poder empezar otra partida sin tener que volver a iniciar el programa. Otro alcance es que en esta ventana el frontend realiza el efecto de las sandias, tanto la aparicion aleatoria como su efecto en el tiempo extra.
    * Ventana fin de puzzle ✅ 2.3: Hecha completa. De manera analoga a la ventana de juego lo programe para poder empezar otra partida en vez de cerrar el programa, pero realiza todo lo solicitado (no pide que cierre el programa).
* Interaccion 3: Hecho completo
    * Cheatcodes ✅ 3.1: Hecho completo
    * Sonidos ✅ 3.2: Hecho completo.
* Networking 4: Hecha casi completo
    * Arquitectura ✅ 4.1: Hecho completo. Como si fueran programas independientes
    * Networking ✅ 4.2: Hecho completo.
    * Codificacion y decodificacion ✅ 4.3: Hecho completo.
* Archivos 5: Hecho casi completo
    * Sprites 🟠 4.1: No se usaron todas las animaciones de pepa, pero los sprites basicos estan implementados.
    * Puzzle ✅ 4.2: Hecho completo.
    * JSON ✅ 4.3: Hecho completo.
    * Parametros ✅ 4.3: Hecho completo.

## Ejecución :computer:
El módulo principal del Servidor a ejecutar es  ```main.py``` y para su correcto funcionamiento es necesario es necesario el archivo config.json y el modulo codificacion.py (sin considerar los assets ignorados por el gitignore).

El módulo principal del Cliente a ejecutar es  ```main.py``` y para su correcto funcionamiento es necesario es necesario el archivo config.json, el modulo codificacion.py, el modulo momasos_diego.py y parametros.py (sin considerar los assets ignorados por el gitignore). (Solo notar que si no existe el archivo puntajes.txt una funcion lo crea)

## Librerías :books:
### Librerías externas utilizadas
No use librerias externas.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```codificacion```: Contiene exlusivamente 2 funciones que codifican y decodifican de la manera solicitada los mensajes entre cliente y servidor.
2. ```momasos_diego```: Hecha para contener funciones que trabajan con archivos como puntajes.txt y cargar los puzzles de los assets.
3. Las librerias del frontend y el backend que contienen las ventanas y la logica de juego y de inicio

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. El supuesto de que basta con mostrar los mejores 3 puntajes en el salon de la fama solamente.

PD: Quiero recalcar que el movimiento de pepa si bien no es animado si es discreto (como para que no sean 0 puntos)

## Referencias de código externo :book:

Para realizar mi tarea no saqué código de ninguna parte.