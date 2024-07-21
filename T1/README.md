# Tarea 1: DCCiudad

## Items de la pauta
* RedMetro<sub>1</sub>: Hecho completo
    * informacion_red<sub>1.1</sub>: Hecha completa 
    * agregar_tunel<sub>1.2</sub>: Hecha completa 
    * tapar_tunel<sub>1.3</sub>: Hecha completa 
    * invertir_tunel<sub>1.4</sub>: Hecha completa 
    * nivel_conexiones<sub>1.5</sub>: Hecha completa
    * rutas_posibles<sub>1.6</sub>: Hecha completa 
    * ciclo_mas_corto<sub>1.7</sub>: Hecha completa 
    * estaciones_intermedias<sub>1.8</sub>: Hecha completa
    * estaciones_intermedias_avanzado<sub>1.9</sub>: Hecha completa 
    * cambiar_planos<sub>1.10</sub>: Hecha completa 
    * asegurar_ruta<sub>1.11</sub>: Hecha completa (Revisar los supuestos)
* Menú<sub>2</sub>: Hecho completo (revisar PD en los supuestos)
    * Consola<sub>2.1</sub>: Hecha completa 
    * Menú de acción<sub>2.2</sub>: Hecha completa
* Aspectos Generales<sub>3</sub>: Segun yo hecho completo
    * Modularizacion<sub>3.1</sub>: Hecha completa 
    * PEP8<sub>3.2</sub>: Hecha completa 

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```red.py``` y el programa se ejecuta exactamente igual que como decia en la pauta, en la terminal ```py main.py *nombre_archivo.txt* *estacion*``` considerar que el nombre del archivo no necesariamente tiene q terminar en .txt pero debe estar en la carpeta data en la misma carpeta donde esta el main.py y el red.py (y dcciudad.pyc)

## Librerías :books:
### Librerías externas utilizadas
No use librerias externas.

### Librerías propias
No cree librerias propias. Pero cree un nuevo metodo en la clase RedMetro que se llama estacion_siguiente y le agrege 2 atributos a la clase que son resumen (que daba informacion util) y nombre (que corresponde al nombre del archivo)

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <En asegurar_ruta en vez de copiar la red del metro la hice de puros 0 y luego de tener la ruta la plasmaba en la matriz de incidencia vacia, considere que era mas facil que ir tapando los tuneles (aunque podia haberlo hecho), ya que una vez teniendo la ruta que ibamos a seguir para llegar al destino, era equivalente tapar el resto de los tuneles a traducir la ruta en una matriz vacia> 

PD: En el menu de acciones puse algunos inputs vacios para que el programa no fuese tan rapido pero con presionar enter uno ya vuelve al menu de acciones.

PD2: A mi criterio las variables que use son bien auto-explicativas pero puede ser que me equivoque, soy nuevo en esto de usar PEP8

## Referencias de código externo :book:

No use referencias de codigo externo