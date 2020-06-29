<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h2 align="center"> Proyecto I SAT </h2>

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

  <p>Descripción: Se desea crear la teoría SAT asociada a problemas de sudoku de orden 1, 2 y 3 en formato CNF para luego proceder a buscar una solución  
  mediante la prueba de si dicha teoría creada es satisfacible. Para esto se  procede a probar la satisfacibilidad con el solver de Zchaff de la universidad  
  de Princeton y a su vez con una implementación del algoritmo DPLL (Davis-Putnam-Logemann-Loveland) hecho por el equipo. Luego de obtener los resultados se procede 
  a verificar y crear un reporte que muestre el estado final del problema, es decir, SAT si existe una solución además de brindar el tiempo de corrida y la configuración final 
  de la matriz. Para el otro caso si no es satisfacible devolver UNSAT y si el tiempo no fue suficiente para resolver, devolver un mensaje que notifique en el reporte  
  asociado al problema que dicha solución no pudo ser encontrada en el tiempo dado. </p>

### Implementado Con
	
	- Python3 
	- zchaff 

### Implementacion

#### Lectura

<p> Para esta parte se procede a leer el archivo según las especificaciones del enunciado y se verifica que el número de orden sea consistente con el número de casillas que son pasadas como segundo parametro en cada caso de prueba.</p>


#### Codificación Teoría SAT CNF Dimacs

Para la codificación del problema del sudoku se realizó un encoding para las variables personalizado al caso:

<p>- 1x1: No tiene una codificación especial, ya que solo existe la posibilidad de una sola variable para este caso. </p>

<p>- 4x4: Se hizo una función que mapeara para 64 valores distintos tomando como parámetros la fila, columna y valor que representaba dicha variable al problema. 
Las 64 variables vienen al problema dado que cada casilla puede tener 4 valores posible y existen un total de 16 casillas por lo que el número de variables es 16*4.</p>

<p>- 9x9: Para este caso se creó una función que mapeara para 729 valores dado que el problema contiene 9 posibles valores para cada casilla y en total son 81 por lo que el 
número de variables está restringido a 81*9 = 729 variables proposicionales.</p>

	
<p> A continuación se describirán las reglas que fueron utilizadas para hacer la codificación del problema en formato CNF, para esta parte se realizará la descripción específica solamente
	para el sudoku de orden 3, pero cabe destacar que para el caso de orden 2 es analogo, pero ajustado a los rangos asociados a dicha instancia del problema. </p>

	
<p>Las reglas utilizadas para la formulación en formato CNF del sudoku de orden 3 son las siguientes:  </p>

	1) Existe al menos un número una entrada de los números del 1 al 9 en cada casilla. 
	2) Cada número del 1 al 9 aparece a lo sumo una vez en cada fila. 
	3) Cada número del 1 al 9 aparece a lo sumo una vez en cada columna. 
	4) Cada número del 1 al 9 aparece a lo sumo una vez en cada sub-grid 3x3 
	5) Se agregan todas las restricciones unitarias de los valores fijados de inicio en el tablero. 

<p> Este encoding sin contar las clausulas generadas por la regla (5) para el caso del sudoku de orden 3 nos creará 8829 clausulas de las cuales solamente 81 son clausulas que contienen  
9 literales y el resto de las 8748 van a ser clausulas binarias, ya que solo poseen 2 literales por clausula. El resto de las clausulas que se agregarán después por la regla (5) serán todas unitarias. </p>

<p>Este encoding implementado provee varias ventajas para la resolución de dicho problema, ya que en principio genera un conjunto  minimal de reglas, lo cual es importante para la resolución pero no suficiente si estas reglas no minimizan el número de literales para cada clausula. Para este caso este tipo encoding permite minimizar el número de clausulas de 9 literales y maximizar el número de clausulas binarias lo cual es vital para poseer una mejor corrida con los algoritmos de resolución, ya que les permite realizar una buena inferencia de manera más rápida sobre el espacio de búsqueda. Por lo que un punto importante para resolver este tipo de problemas es conseguir una buena codificación a formato CNF. </p>


<p>Por último cabe destacar que para este problema se guardan en un diccionario cada una de las variables creadas como clave y se almacena una 3-tupla (fila,columna,valor) 
la cual nos permitirá más adelante después de resolver la satisfacibilidad del problema saber cuales son los valores que representan en el grid cada una de las variables True de la instancia del sudoku resuelta. </p>

#### DPLL Solver

<p> El algoritmo implementado es DPLL el cual es un algoritmo de búsqueda más inferencia que permite resolver la teoría asociada a un problema de satisfacibilidad. Por otro lado se tuvo que implementar el algoritmo de propagación unitaria, ya que este es el núcleo que le permite realizar la inferencia al DPLL y a su vez también depende de este algoritmo que tan efectiva va a ser la ejecución del DPLL.</p>

La implementación de dichos algoritmos se de la siguiente forma... 


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

	- outputDimacs: Esta carpeta posee los archivos en formato Dimacs del resultado del satSolver seleccionado solamente cuando es satisfacible la respuesta. 
					Siguiendo el formato del enunciado.
	
	- outputZCHAFF: En esta carpeta cada archivo posee las estadísticas que devuelve zchaff por la terminal para su caso especifico determinado por el nombre del archivo.
	
	- outputDPLL: Esta carpeta guarda el reporte específico para cada caso corrido con el solver DPLL
	
	- outputZchaffRun: Esta carpeta guarda el reporte especifíco para cada caso corrido con el zchaff solver

<p>Para tanto la carpetas outputDPLL y outputZchaffRun es el siguiente: </p>

	- La primera linea posee SAT en caso de existir un resultado que satisfaga las restricciones o UNSAT en caso contrario. 
	
	- La segunda linea impresa contiene el tiempo que tomo la corrida de esa instancia del problema en saco de ser satisfacible.
	
	- Por último se imprime el tablero con el resultado en caso de ser satisfacible.  
	
	- En caso de no poderse resolver en el tiempo estipulado por el usuario o por defecto, se procede a escribir en el archivo un TIMEOUT  


### Prerequisitos

 - Python 3 debe estar instalado para el funcionamiento 

 - Utilizar la versión de zchaff provisto en el repositorio. 

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


<p>Una vez realizada esta configuración para el zchaff, se procede a devolverse a la dirección principal del repositorio que es donde se encuentra el script sudokuSat.py, 
es necesario que a ese mismo nivel del filesystem se encuentren los archivos de texto con los casos de prueba y que dicho archivo tenga extension txt.  </p>

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

Para ver los resultados devueltos por el solver ir a la carpeta outputZchaffRun en caso de ejecutar el metodo zchaff o a la carpeta outputDPLL en caso de correr DPLL 
Con el fin de ver la información detallada de la distribución de los archivos ir a la sección de "Salida" en este readme </p>

### Resultados




### Conclusion

<p>Se pudo observar que a pesar de trabajar con instancias de sudoku de ordenes pequeñas la gran exploción combinatoria que tiene este tipo de problemas es alta por lo que el proceso de buscar una solución satisfacible o no crece rápidamente a medida que crece el orden del sudoku ya que las posibilidades combinatorias crecen. Esto se pudo constatar al ver como crece el número de literales y clausulas a medida que se aumenta el orden del sudoku. Por ejemplo para el caso de orden 2 se obtuvieron 64 literales y 304 clausulas, por otro lado para el caso de orden 3 se obtuvieron 729 literales y 8829 clausulas en ambos casos sin contar las clausulas unitarias que se agregan dependiendo de cuantos valores iniciales distintos de cero tenga la instancia de prueba. 
	
Por otro lado trabajar con este tipo de aproximación para atacar problemas combinatorios como lo es el caso de un sudoku se puede observar que este tipo de enfoque permite conseguir una solución bastantemente rápida comparada con otros métodos alternativos como podría ser construir una implementación alterna con A* que posea una buena heurística admisible y consistente, además que el costo en memoria es sustancialmente menor, lo cual hace esta alternativa de SAT solvings un mejor enfoque.

El tiempo de ejecución de un SAT solver depende principalmente de que tan rápido sea su mecanismo para propagar restricciones booleanas ya que esto es lo que hace que dicho problema se pueda resolver más rápido, esto último se pudo verificar mediante las comparaciones entre una implementación simple de propagación unitaria que tiene nuestra implementación comparada a la de los watched literals que lleva zchaff además de utilizar otras técnicas avanzadas. 

Por último también pudo observarse que una buena implementación de restricciones en las clausulas en CNF puede hacer una buena diferencia a la hora de atacar el problema, dado a que dependiendo del enfoque al bajar el número de literales que se genera en cada clausula facilita a la propagación unitaria a que pueda hacer una mejor inferencia sobre la satisfacibilidad del problema. Esto se pudo observar dado a que al desarrollar la forma CNF en el proyecto probamos 2 implementaciones distintas. Al final se colocó en el proyecto la mejor implementación entre las dos que realizamos.</p>
	
 
	 

<!-- Integrants -->
## Integrantes

		Moisés González - 11-10406
		Fabio  Suárez   - 12-10578 

