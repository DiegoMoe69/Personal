# Tarea 2: DCCombatientes 🐈⚔️


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

La tarea realiza los combates de la manera solicitada, con bastantes usos de menu. Se definieron varios modulos para poder tener mas claridad de donde ocurrian los errores durante el desarrollo. Lo que presenta problemas la tarea es al evolucionar muchos gatos, a veces, se agregan elementos None al ejercito y provoca error al realizar algunos chequeos y no tener atributos correspondientes. Esto especificamente ocurre al añadir muchos gatos y evolucionar al que sea ultimo gato en el minuto aproximadamente 3 veces, honestamente no se porque se produce este error y no se en que parte mencionarlo, pero por eso es lo primero que esta puesto.

A medida que desarrolle la tarea se me ocurrio definir algunas funciones como menu pero no todos los menus funcionan mediante el llamado de una funcion ya que en el caso de la tienda ya la habia hecho antes de esta idea.

Hay algunos inputs que podrian provocar errores, pero estan casi todos los posibles errores cubiertos.

Los calculos de probabilidades y la adquisicion de gatos random se realizo con el comando randint de la libreria random, al usarse un randint el uso de probabilidades implica que poner probabilidades con decimales como 36,5% (en parametros) no tiene ningun sentido, osea las probablididades se trabajan con enteros del 0 al 100.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos: 12 pts (10%)
##### ✅ Definición de clases, herencia y *properties*: se definieron las clases solicitadas con las interacciones solicitadas y algunos metodos extra (actualizar_stats), hay herencia, clases abstractas, uso de properties (que casi todos los atributos terminaron siendo properties) e incluso use overriding para la subclase Mago_de_Batalla.

#### Preparación del programa: 10 pts (8%)
##### ✅ Inicio de la partida: El programa empieza correctamente, cerrandose si hay cualquier problema en los archivos de la carpeta data o si es que la dificultad no es valida.

#### Entidades: 56 pts (47%)
##### ✅ Ejército: Funciona completamente e implemente un metodo que se llama posicion que sirve para el tema de la evolucion ya que al evolucionar muchos gatos estos ya no salen en los posibles a evolucionar pero siguen estando en el ejercito y dificultaba el hecho de identificarlos, el metodo combatir se aplica a el jugador principal, retornando True si este es el vencedor o False en el caso opuesto y simulando la batalla donde se calcula el daño que realizarian los gatos que estan peleando y luego se aplica mas los debuffs y los buffs respectivos, para que estos no afecten el calculo del daño.
##### ✅ Combatientes: Funcionan correctamente, Combatiente es una clase abstracta donde estan las properties de sus atributos que van variando por debuffs y buffs para que no se salgan de los parametros establecidos en el enunciado, esto tambien podria estar en parametros, como un valor maximo por default y que eventualmente por buffs llegaso a otro maximo pero asumi que no era necesario. Luegos los combatientes que heredan de Combatiente tienen su respectivo metodo evolucionar que retorna el gato evolucionado dependiendo del item con el que interactua y teniendo las mismas estadisticas, un detalle es que al evolucionar al combatiente este se cura ya que se vuelve a instanciar, asumi que no era necesario que tubiese la vida anterior porque no estaba especificado y en el contexto de un juego creo que seria mejor asi. Por ultimo los gatos evolucionados heredan de los que son 'combinacion' y el caso excepcion es el Mago_de_Batalla que hace overriding del metodo actualizar_stats() ya que este sube su defensa, la cual podria afectar al calculo del daño, con este cambio lo que pasa es que se calculan ambos daños en un combate y luego al ser restados de la vida se aplica el buff a la defenza para que al proximo ataque este buff sea considerado.
##### ✅ Ítems: Clase implementada correctamente, aunque la verdad es bastante dispensable, intente usar herramientas que permiten reutilizar codigo como properties, pero la verdad instanciar cada item con la informacion seria mas eficiente.

#### Flujo del programa: 30 pts (25%)
##### ✅ Menú de Inicio: Este funciona con un loop directamente en main.py y recibe el input y abre el loop de tienda o imprime el ejercito o comienza el combate o termina el loop de tienda cerrando el programa.
##### ✅ Menú Tienda: Este menu tambien funciona como un loop directamente en el main.py y al realizar las compras descuenta instantaneamete el oro del jugador y en el caso de los items al revisar si hay gatos validos, devuelve el valor del objeto por lo que es como si no se hubiese comprado. Las compra de gatos, si es que hay el dinero disponible, se instancia con la funcion instanciar() uun gato random que cumpla con el tipo solicitado. La opcion de curar, literalmente cura a cada gato y la opcion de cerrar el menu termina el loop de la tienda volviendo al loop del menu de inicio.
##### ✅ Selección de gato: Este menu funciona mediante una funcion menu_gatos que recibe una lista de gatos que cumplen las caracteristicas solicitadas, por ejemplo al comprar el item armadura no se muestran los gatos que no pueden recibir este item, esta funcion retorna una tupla con la informacion necesaria para que el metodo posicion de Ejercito pueda identificar al gato seleccionado de entre todos los gatos del ejercito.
##### ✅ Fin del Juego: Al ganar la 3era ronda se imprime un mensaje felicitando al jugador y imprimiendo una ultima vez al ejercito para ver lo gatos que sobrevivieron y luego se cierra el programa, supuse que para jugar denuevo hay que volver a empezar el programa. Al perder durante cualquier ronda se reinicia el oro, el jugador ya no tiene combatientes y se vuelven a cargar las rondas del archivos de dificultad correspondiente, y vuelve al menu de inicio.
##### 🟠 Robustez: El menu de gatos debe ser un int porque si no, no puede realizar las comparaciones necesarias, todos los otros menus pueden recibir cualquier tipo de input y funcionar aunque puede ser que me este equivocando.

#### Archivos: 12 pts (10%)
##### ✅ Archivos .txt: El chequeo de los archivos se realiza con la funcion archivos_validos(), y se revisan de manera diferente los archivos de dificultad y de unidades, se va revisando por 'unidad', asumiendo que una unidad tiene la siguiente forma 'nombre,tipo,vida_max,defensa,poder,agilidad,resistencia'.
##### ✅ parametros.py: Estan todos los parametros en este archivo y de este son importados para su respectivo uso, no tenia muy claro cuando poder informacion constante ahi ya que eventualmente podria poner el numero de las opciones de los menus y muchos datos ahi pero sentia que no era necesario.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```unidades.txt```, ```facil.txt```, ```intermedio.txt``` y ```dificil.txt``` en ```data```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```librería_1```: ```randint() / random```
2. ```librería_2```: ```argv() / sys```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```clases.py```: Contiene a ```Ejercito```, ```Item```, ```Combatientes```. En general las solicitadas, todas las clases estan aqui.
2. ```funciones_diego```: Hecha para simplificar el codigo y contiene procesos que suelen usar muchas variables y contadores, para no confundir estas variables auxiliares y para poder identificar rapidamente errores. Por ejemplo aqui se usan directamente las clases en una funcion que se llama instanciar para instanciar correctamente a un gato, todo para que el programa sea mas claro y legible. En general son bastante auto explicativas, y cuando devuelven mucha informacion estas funciones devuelven tuplas. Especifico todas las funciones en ***EXTRA***

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Evolucion de gatos restaura la vida, esto por que en el contexto del juego no tendria mucho sentido evolucionar ya que tras analizar las opciones de la tienda no es rentable a menos que fuese muy barato evolucionarlos, ademas que curar al ejercito es extremadamente caro considerando que el unico gato que recbe daño es el primero.
2. Para volver a jugar hay que volver a iniciar el programa, no se especifica que hay que poner una opcion para volver a iniciar el juego dentro del juego.

PD: La manera para calcular los daños, los buffs y debuffs es iq 200 y seria muy facil implementar mas efectos.
PD2: Despues me di cuenta de varios detalles de notacion incluso en el readme pero para la proxima va a estar prolijo y formal.

**EXTRA** 

La funcion archivos_validos revisa TODOS los archivos y devuelve False ante cualquier error.
La funcion chequear sirve para la revision de archivos de la funcion anterior, ahorra un poco de codigo.
La funcion unir tambien sirve para un proceso que realiza archivos_validos.
La funcion instanciar instancia un gato recibiendo el formato en el que esta en los archivos y devolviendo un combatiente de la clase especifica solicitada.
La funcion instanciar_rondas genera una lista de ejercitos correspondiente a las rondas del juego.
La funcion menu_gatos realiza todo lo que haria un menu y devuelve el gato elegido mas las coordenadas. (Estas son usadas por el metodo posicion de la clase Ejercito)

## Referencias de código externo :book:

Para realizar mi tarea no saqué código de ninguna parte.

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).