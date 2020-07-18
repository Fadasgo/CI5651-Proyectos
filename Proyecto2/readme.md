
<br />
<p align="center">

  <h2 align="center"> Proyecto II SAT solver </h2>

<!-- TABLE OF CONTENTS -->
## Tabla de Contenidos

* [Acerca del Proyecto](#acerca-del-proyecto)
  * [Implementado Con](#implementado-con)
  * [Implementacion](#implementacion)
  * [Prerequisitos](#prerequisitos)
* [Como se Usa](#como-se-usa)
* [Integrantes](#contacto)



<!-- Acerca del Proyecto -->
## Acerca del Proyecto

  <p>Descripción: Se desea realizar una mejora a la implementación del SAT solver de la primera entrega, para ello se propone en el enunciado utilizar la propagación unitaria para poder hacer la evaluación de satisfacibilidad de manera más eficiente y por otro lado se proponen otras mejoras opcionales. </p>

### Implementado Con
	
	- Python3 
	- zchaff 

### Implementacion

#### DPLL Solver 

La estructura de datos principales es una lista para lo que se conoce como
__watched literals__.
La idea consiste en que cada cláusula lleva seguimiento
de dos literales, al momento de una asignación debemos asegurarnos de que sus
valores no sean falso (es decir, verdadero o indeterminado).
Mantener esta restricción es lo que nos permite identificar rápidamente
las cláusulas unitarias, cuando deja de cumplirse todos los literales
excepto uno son falsos y la asignación es inmediata.
Este proceso lo repetimos recursivamente y de esta forma logramos la
propagación unitaria.

Para implementar los watched literals utilizamos una lista de listas,
los indices de la lista se corresponden con cada literal posible.
Las sublistas son las cláusulas que están siendo observadas por cada literal.
Para inicializarlas simplemente tomamos los dos primeros literales de
cada cláusula y los ponemos a observarla.

Una vez tenemos implementada la propagación unitaria, debemos
implementar el backtracking, puesto que utilizaremos una versión
iterativa del DPLL.
La idea general es tener un ciclo en el cual iremos asignando variables
y propagándolas hasta que no existan variables sin asignar.
Para esto necesitaremos una pila de variables por asignar,
una pila de eventos y una lista donde guardar las asignaciones de la 
propagación.
Cada vez que tomemos una decisión manualmente creamos debemos realizar
la propagación.
Si la propagación es exitosa entonces creamos un nuevo nivel de decisión.
En este nivel guardaremos la variable que asignamos manualmente junto con
las asignaciones. También es importante quitar de la pila de variables
por asignar las variables que asignó la propagación.
Si la propagación no es exitosa restauramos la asignación de la propagación,
asignamos manualmente el otro valor posible y repetimos el proceso anterior.
Si intentamos ambos valores manualmente y encontramos conflictos en ambos
debemos hacer backtracking. Para saber cuales intentos llevamos tenemos un
arreglo de estados para cada variable con valores entre 0 y 3, el 0 se corresponde
con ningún intento, el 1 con true, el 2 con false y el 3 con ambos.
Para hacer backtracking reiniciamos el estado de la variable actual a 0, la
desasignamos y la incluimos de vuelta en la pila de variables por asignar.
Desempilamos el nivel de decisión anterior, deshacemos la propagación que
tomo lugar en ese nivel, agregamos las variables de esa propagación a la pila
de variables por asignar y finalmente añadimos la variable del nivel anterior
al tope de la pila de variables por asignar.

Si queremos hacer backtracking y la pila de eventos esta vacía entonces
el problema es UNSAT, por otro lado, si la pila de variables esta vacía
entonces el encontramos una solución.


#### Traducción SAT a Sudoku
	
<p>Para esta parte una vez que ya se resolvió la satisfacibilidad de la teoría SAT del problema asociado se procede a verificar en caso de que sea el resultado satisfacible cuáles son 
las variables que evaluaron a True y a medida que se van obteniendo, se procede a buscar en el diccionario creado anteriormente cual es la tupla de fila, columna y valor asociado a dicha variable para proceder a llenar el tablero de sudoku </p>

#### Salida

<p>Los outputs de este proyecto se encuentran en distintos archivos que se  explicaran a continuación y su distribución entre las distintas carpetas creadas. 
	
Para los archivos de salida todos los nombres están formados de la siguiente forma nombreDelArchivo-LineaNumeroLinea.txt 

Donde el nombreDelArchivo es el archivo de donde originalmente se extrajo el caso de prueba y el numeroLinea es como su nombre lo expresa el número de linea del 
archivo nombreDelArchivo donde se extrajo el caso de prueba.  Cada archivo va a tener el formato correspondiente al de la carpeta en la que se encuentre.</p>

 Ahora se procederá a explicar la distribución de las distintas carpetas y su contenido:

	- CNFs: Esta carpeta posee los archivos en formato CNF DIMACS como se encuentran especificado en el enunciado.

	- outputDimacs: Esta carpeta posee los archivos en formato Dimacs del resultado del satSolver seleccionado.Siguiendo la especificación del enunciado.
	
	- outputZCHAFF: En esta carpeta cada archivo posee las estadísticas que devuelve zchaff por la terminal para su caso especifico determinado por el nombre del archivo.
	
	- outputDPLL: Esta carpeta guarda el reporte específico para cada caso corrido con el solver DPLL
	
	- outputZchaffRun: Esta carpeta guarda el reporte especifíco para cada caso corrido con el zchaff solver
	
	- Tests: En dicha carpeta se encuentran todos los casos de prueba a correr por sudokuSat.py

<p>Para tanto la carpetas outputDPLL y outputZchaffRun es el siguiente: </p>

	- La primera linea posee SAT en caso de existir un resultado que satisfaga las restricciones o UNSAT en caso contrario. 
	
	- La segunda linea impresa contiene el tiempo que tomo la corrida de esa instancia del problema en saco de ser satisfacible.
	
	- Por último se imprime el tablero con el resultado en caso de ser satisfacible.  
	
	- En caso de no poderse resolver en el tiempo estipulado por el usuario o por defecto, se procede a escribir en el archivo un TIMEOUT  


### Prerequisitos

 - Python 3 debe estar instalado para el funcionamiento 

 - Utilizar la versión de zchaff provisto en el repositorio. 
 
 - Compilar haciendo "make" o "make all" el archivo de zchaff, para poder ejecutar el script (se procede a explicar más adelante)

Dicha version de zchaff es la zchaff.2008.10.12 

<!-- USAGE EXAMPLES -->
## Como se Usa

<p>Una vez en la ruta principal de la carpeta del repositorio se descomprimime el zip del zchaff que se encuentra en el repositorio y  se procede a entrar 
a las carpetas siguientes zchaff.2008.10.12/zchaff para luego abrir la terminal en dicha ruta y aplicar cualquiera de los siguientes dos comandos: </p>

```sh
	make all
```
```sh
	make
```

estos pasos anteriores son necesarios para poder compilar zchaff y poder ejecutar esta funcionalidad para sudokuSat.py .

<p>Una vez realizada esta configuración para el zchaff, se procede a devolverse a la dirección principal del repositorio que es donde se encuentra el script sudokuSat.py </p>

<p>El comando para correr los solvers es el siguiente: </p>

```sh
python3 sudokuSat.py archivoLectura.txt solverMethod tiempo
```

	Parámetros:

		archivoLectura.txt:Como su nombre lo representa dicho parametro es el nombre del archivo el cual debe tener extension txt 
	
		solverMethod:colocar el número cero en caso de querer ejecutar la solución con zchaff o 1 en caso de ser con nuestro DPLL solver 
	
		tiempo: este parámetro es opcional y se coloca un número en caso de no querer usar el tiempo predeterminado que es 200

<p>Después de ejecutar dicho comando el script se encargará de solucionar los casos de pruebas pasados en el archivo con el método elegido y hará la distribución 
de los archivos a sus respectivas carpetas.

Para ver los resultados devueltos por el solver ir a la carpeta outputZchaffRun en caso de ejecutar el método zchaff (0) o a la carpeta outputDPLL en caso de correr DPLL (1)
Con el fin de ver la información detallada de la distribución de los archivos ir a la sección de "Salida" en este readme </p>

### Resultados

| Caso | zchaff (tiempo en segundos) | DPLL solver entrega 1  (tiempo en segundos) | DPLL solver entrega 2  (tiempo en segundos) |
|------|-----------------------------|---------------------------------------------|---------------------------------------------|
| 1    | 0.000161                    | 43.2131028175354                            | 0.0325469970703125                          |
| 2    | 0.000149                    | 626.6806128025055                           | 0.03179574012756348                         |
| 3    | 0.000158                    | 3220.3500497341156                          | 0.03406095504760742                         |
| 4    | 0.00016                     | 3073.1158742904663                          | 0.2751278877258301                          |
| 5    | 0.000144                    |                                             | 0.03142666816711426                         |
| 6    | 0.000192                    |                                             | 0.031447649002075195                        |
| 7    | 0.000217                    |                                             | 0.032824039459228516                        |
| 8    | 0.00062                     |                                             | 0.06815552711486816                         |
| 9    | 0.000168                    |                                             | 4.262210130691528                           |
| 10   | 0.00022                     |                                             | 0.03124523162841797                         |
| 11   | 0.000218                    |                                             | 25.02929973602295                           |
| 12   | 0.000158                    |                                             | 0.03038763999938965                         |
| 13   | 0.000455                    |                                             | 0.03967738151550293                         |
| 14   | 0.000524                    |                                             | 0.051631927490234375                        |
| 15   | 0.000293                    |                                             | 0.5710747241973877                          |
| 16   | 0.000173                    |                                             | 0.03084278106689453                         |
| 17   | 0.00016                     |                                             | 0.03157806396484375                         |
| 18   | 0.000176                    |                                             | 0.03385567665100098                         |
| 19   | 0.000156                    |                                             | 0.03203845024108887                         |
| 20   | 0.000179                    |                                             | 0.030948162078857422                        |
| 21   | 0.001582                    |                                             |                                             |
| 22   | 0.000268                    |                                             |                                             |
| 23   | 0.00014                     |                                             |                                             |
| 24   | 0.000319                    |                                             |                                             |
| 25   | 0.003369                    |                                             |                                             |
| 26   | 0.000291                    |                                             |                                             |
| 27   | 0.000262                    |                                             |                                             |
| 28   | 0.000146                    |                                             |                                             |
| 29   | 0.000141                    |                                             |                                             |
| 30   | 0.00014                     |                                             |                                             |
| 31   | 0.000192                    |                                             |                                             |
| 32   | 0.000434                    |                                             |                                             |
| 33   | 0.000507                    |                                             |                                             |
| 34   | 0.002273                    |                                             |                                             |
| 35   | 0.000383                    |                                             |                                             |
| 36   | 0.006141                    |                                             |                                             |
| 37   | 0.000172                    |                                             |                                             |
| 38   | 0.000161                    |                                             |                                             |
| 39   | 0.000141                    |                                             |                                             |
| 40   | 0.000235                    |                                             |                                             |
| 41   | 0.000258                    |                                             |                                             |
| 42   | 0.000206                    |                                             |                                             |
| 43   | 0.001099                    |                                             |                                             |
| 44   | 0.000998                    |                                             |                                             |
| 45   | 0.010589                    |                                             |                                             |
| 46   | 0.000269                    |                                             |                                             |

### Conclusion

<p>La propagación unitaria (UP) es vital para un buen desempeño de un SAT solver ya que dicha implementación hace la diferencia en la ejecución de un 90% o más en el tiempo de corrida  por lo que una buena implementación es crucial para obtener un desempeño efectivo. Para esta entrega se hicieron mejoras en la implementación de UP, se le agregó la estructura de datos watched literals que fue explicada anteriormente, la integración de dicha estructura permitió una mejora sustancial en los resultados obtenidos para esta fase. Entre los resultados
obtenidos que se encuentran en el archivo soluciones.txt, se puede observar que
para el caso 3 el tiempo de solución con zchaff fue de 0.000167 segundos por otro
lado con la implementación del primer proyecto este caso se pudo resolver en 
3220.3500497341156 segundos y para esta entrega se obtuvo una mejora sustancial con la cual se pudo resolver en 0.03406095504760742 segundos, además permitió resolver las primeras 20 instancias en 30 segundos.

Para las otras instancias en el tiempo de ejecución realizado no se lograron obtener algún resultado, para ello haría falta implementar las opciones complementarias propuestas en el enunciado del proyecto 2 entre las cuales están el backtracking no cronológico, el aprendizaje de implicantes y la heurística de bifurcación en especifico VSIDS que es la que usa zchaff, todo esto sería necesario para poder dar un resultado más cercano a lo que hace dicha implementación y poder completar de manera eficiente y efectiva los resultados de las corridas.
 </p>

El archivo soluciones.txt en la carpeta principal del proyecto 2 también provee los resultados obtenidos durante la ejecución. Cabe destacar que el tiempo es en segundos.

<!-- Integrants -->
## Integrantes

		Moisés González - 11-10406
		Fabio  Suárez   - 12-10578 


