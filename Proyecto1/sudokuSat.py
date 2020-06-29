import sys
import os
import subprocess
import re
from solver import Solver

rutaActual = os.getcwd()

# SUDOKU SAT SOLVER

# Moises Gonzalez
# Fabio  Suarez

rutaActual = os.getcwd()
rutaDirTest = rutaActual + "/Tests/"
rutaDirCNF = rutaActual + "/CNFs/"
rutaOutputDimacs = rutaActual + "/outputDimacs/"
rutaReporteZchaff = rutaActual + "/ReporteZchaffRun/"
rutaReporteDPLL = rutaActual + "/ReporteDPLLrun/"
rutaZchaff = rutaActual +"/zchaff.2008.10.12/zchaff/zchaff"
rutaOutputZchaff = rutaActual + "/outputZCHAFF/"

chaffTimes = []  # Arreglo que guarda los tiempos de corrida de los casos de prueba para zchaff

class cnfData:
    def __init__(self, c, var, w):
        self.clauses = c
        self.variables = var
        self.write = w

# Genera un string con la forma del grid con su resultado de un Sudoku
def gridSudoku(m,orden):
    sudok = ""
    counterRow = 1
    counterCol = 1
    
    if orden == 1:
        sudok = str(m[0][0])
    
    elif orden == 2:
        for x in m:
            for y in x:
                if counterCol == 2:
                    sudok = sudok + str(y) + " | "
                
                elif counterCol == 4:
                    sudok = sudok+ str(y) + "\n"
                    counterCol = 0
                
                else:
                    sudok = sudok + str(y) + " "
                counterCol += 1   
            if counterRow == 2:
                sudok = sudok +"---------\n"
            counterRow += 1   

    elif orden == 3:
        for x in m:
            for y in x:
                if counterCol == 3 or counterCol == 6:
                    sudok = sudok + str(y) + " | "
                
                elif counterCol == 9:
                    sudok = sudok+ str(y) + "\n"
                    counterCol = 0
                
                else:
                    sudok = sudok + str(y) + " "
                counterCol += 1   
            if counterRow == 3 or counterRow == 6:
                sudok = sudok +"----------------------\n"
            counterRow += 1                     
    
    return sudok

# Ejecuta el sat solver de zchaff con los archivos CNF DIMACS generados anteriormente
def runZchaff(nombreArchivo, tiempoCorrida):
    rutaEntrada = rutaDirCNF + nombreArchivo # Archivo que se le pasará como entrada a zchaff
    rutaSalida = rutaOutputZchaff + nombreArchivo    # Archivo que devolverá la ejecución de zchaff
    archivoSalida = open(rutaSalida, "w")
    # Crea el archivo f donde se guarda el output de la terminal
    # Por otro lado se guarda la salida de la satisfacibilidad de los valores en el archivo contenido en la variable rutaSalida
    with open(rutaOutputZchaff + nombreArchivo, "w") as f:
        subprocess.call([rutaZchaff, rutaEntrada, " "+ str(tiempoCorrida) ,rutaSalida], stdout = f)

    archivoSalida.close()

def runDPLL(nombreArchivo=None):
    s = Solver()
    s.read(nombreArchivo)
    is_sat = "SAT" if s.solve(0) else "UNSAT"
    output = s.output_dimacs()
    return (s.vars, s.number_clauses, is_sat, output)

# recibe un int y lo convierte en string
def imprimirVariable(lit):
    return str(lit)

# encoding de las variables para sudoku de orden 3
def var3x3(fil, col, value):
    return 81 * (fil - 1) + 9 * (col - 1) + value

# encoding de las variables para sudoku de orden 2
def var2x2(fil, col, value):
    return 16 * (fil - 1) + 4 * (col - 1) + value

# Se guardan en el diccionario los literales 
def dictCheckSudoku9x9(d,fil,col,value):
    # Procedemos a guardar la variable si no se ha creado anteriormente
     if str(var3x3(fil,col,value)) not in d:
         d[str(var3x3(fil,col,value))] = (fil,col,value)

def dictCheckSudoku4x4(d,fil,col,value):
    # Procedemos a guardar la variable si no se ha creado anteriormente
     if str(var2x2(fil,col,value)) not in d:
         d[str(var2x2(fil,col,value))] = (fil,col,value)

# Conversion de las restricciones del tablero 9x9 a formato CNF
def cnfSudoku1x1(m):
    
    clauses = [[1]]
    literals = {'1':(0,0,1)}
    dimacs = "1 0"
    head = "p cnf " + "1" + " " + "1" + " \n" + dimacs

    return cnfData(clauses, literals, head)
def cnfSudoku4x4(m):
    
    # Creamos diccionario literals que reciba una variable y guarde la tupla (i,j,v) para luego servir de referencia a la hora de llenar el sudoku con los resultados 
    # y además para la lista de conteo de variables para el formato dimacs
    clauses = []
    literals = {}
    dimacs = ""
    
    # Ambas clausulas a continuacion generan la condicion de que
    # toda casilla del sudoku debe contener exactamente un numero entre [1..9]

    for i in range(1, 5):
        for j in range(1, 5):
            aux_atLeast = []
            for v in range(1, 5):
                
                # Clausula de toda casilla debe tener al menos un numero
                aux_atLeast.append(var2x2(i,j,v))
                dimacs += imprimirVariable(var2x2(i,j,v)) + " "
                
                # Procedemos a guardar la variables verificando que no se repitan
                dictCheckSudoku4x4(literals,i,j,v)

            dimacs += "0 \n"
            clauses.append(aux_atLeast)

    # Clausura de restriccion que en una fila no se repite un numero
    for y in range(1, 5):
        for z in range(1, 5):
            for x in range(1, 4):
                for i in range(x + 1, 5):
                    
                    # Clausula de toda casilla contiene a lo sumo un numero
                    clauses.append([-var2x2(x,y,z),-var2x2(i,y,z)])
                    dimacs += imprimirVariable(-var2x2(x,y,z)) + " " + imprimirVariable(-var2x2(i,y,z)) + " 0 \n"

    # Clausura de restriccion que en una columna no se repite un numero
    for x in range(1, 5):
        for z in range(1, 5):
            for y in range(1, 4):
                for i in range(y + 1, 5):
                    
                    # Clausula de toda casilla contiene a lo sumo un numero
                    clauses.append([-var2x2(x,y,z),-var2x2(x,i,z)])
                    dimacs += imprimirVariable(-var2x2(x,y,z)) + " " + imprimirVariable(-var2x2(x,i,z)) + " 0 \n"
    
    # Clausula de que un numero aparece a lo sumo una vez en una subtabla 3x3
    
    for z in range(1,5):
        for i in range(0,2):
            for j in range(0,2):
                for x in range(1,3):
                    for y in range(1,3):

                        for k in range(y+1,3):
                            clauses.append([-var2x2(2*i+x,2*j+y,z),-var2x2(2*i+x,2*j+k,z)])
                            dimacs += imprimirVariable(-var2x2(2*i+x,2*j+y,z)) + " " + imprimirVariable(-var2x2(2*i+x,2*j+k,z)) + " 0 \n"     
                
                        for k in range(x+1,3):
                            for l in range(1,3):
                                clauses.append([-var2x2(2*i+x,2*j+y,z),-var2x2(2*i+k,2*j+l,z)])
                                dimacs += imprimirVariable(-var2x2(2*i+x,2*j+y,z)) + " " + imprimirVariable(-var2x2(2*i+k,2*j+l,z)) + " 0 \n"
    
    #print("\n EL NUMERO TOTAL DE CLAUSULAS SIN CONTAR LAS INICIALES : " + str(len(clauses)) + "\n")

    # Se proceden a agregar las clausulas relacionadas a los 
    # numeros que ya se encuentran asignados de inicio en el sudoku
    for i in range(0, 4):
        for j in range(0, 4):
            if (m[i][j] != 0):
                clauses.append(var2x2(i+1, j+1, m[i][j]))
                dimacs = imprimirVariable(var2x2(i+1,j+1,m[i][j])) + " 0 \n" + dimacs
                #print(i+1,j+1,m[i][j], var3x3(i+1,j+1,m[i][j]))
    #print("NUMERO DE LITERALES "+ str(len(literals)) + "\n")
    # Creamos el header del Dimacs SAT 
    # p cnf num_vars num_clauses

    head = "p cnf " + imprimirVariable(len(literals)) + " " + imprimirVariable(len(clauses)) + " \n" + dimacs

    #os.system("clear")
    #print(head)

    return cnfData(clauses, literals, head)


# Conversion de las restricciones del tablero 9x9 a formato CNF
def cnfSudoku9x9(m):
    
    # Creamos diccionario literals que reciba una variable y guarde la tupla (i,j,v) para luego servir de referencia a la hora de llenar el sudoku con los resultados 
    # y además para la lista de conteo de variables para el formato dimacs
    clauses = []
    literals = {}
    dimacs = ""
    
    # Ambas clausulas a continuacion generan la condicion de que
    # toda casilla del sudoku debe contener exactamente un numero entre [1..9]

    for i in range(1, 10):
        for j in range(1, 10):
            aux_atLeast = []
            for v in range(1, 10):
                
                # Clausula de toda casilla debe tener al menos un numero
                aux_atLeast.append(var3x3(i,j,v))
                dimacs += imprimirVariable(var3x3(i,j,v)) + " "
                
                # Procedemos a guardar la variables verificando que no se repitan
                dictCheckSudoku9x9(literals,i,j,v)

            dimacs += "0 \n"
            clauses.append(aux_atLeast)

    # Clausura de restriccion que en una fila no se repite un numero
    for y in range(1, 10):
        for z in range(1, 10):
            for x in range(1, 9):
                for i in range(x + 1, 10):
                    
                    # Clausula de toda casilla contiene a lo sumo un numero
                    clauses.append([-var3x3(x,y,z),-var3x3(i,y,z)])
                    dimacs += imprimirVariable(-var3x3(x,y,z)) + " " + imprimirVariable(-var3x3(i,y,z)) + " 0 \n"

    # Clausura de restriccion que en una columna no se repite un numero
    for x in range(1, 10):
        for z in range(1, 10):
            for y in range(1, 9):
                for i in range(y + 1, 10):
                    
                    # Clausula de toda casilla contiene a lo sumo un numero
                    clauses.append([-var3x3(x,y,z),-var3x3(x,i,z)])
                    dimacs += imprimirVariable(-var3x3(x,y,z)) + " " + imprimirVariable(-var3x3(x,i,z)) + " 0 \n"
    
    # Clausula de que un numero aparece a lo sumo una vez en una subtabla 3x3
    
    for z in range(1,10):
        for i in range(0,3):
            for j in range(0,3):
                for x in range(1,4):
                    for y in range(1,4):

                        for k in range(y+1,4):
                            clauses.append([-var3x3(3*i+x,3*j+y,z),-var3x3(3*i+x,3*j+k,z)])
                            dimacs += imprimirVariable(-var3x3(3*i+x,3*j+y,z)) + " " + imprimirVariable(-var3x3(3*i+x,3*j+k,z)) + " 0 \n"     
                
                        for k in range(x+1,4):
                            for l in range(1,4):
                                clauses.append([-var3x3(3*i+x,3*j+y,z),-var3x3(3*i+k,3*j+l,z)])
                                dimacs += imprimirVariable(-var3x3(3*i+x,3*j+y,z)) + " " + imprimirVariable(-var3x3(3*i+k,3*j+l,z)) + " 0 \n"
    
    #print("\n EL NUMERO TOTAL DE CLAUSULAS SIN CONTAR LAS INICIALES : " + str(len(clauses)) + "\n")

    # Se proceden a agregar las clausulas relacionadas a los 
    # numeros que ya se encuentran asignados de inicio en el sudoku
    for i in range(0, 9):
        for j in range(0, 9):
            if (m[i][j] != 0):
                clauses.append(var3x3(i+1, j+1, m[i][j]))
                dimacs = imprimirVariable(var3x3(i+1,j+1,m[i][j])) + " 0 \n" + dimacs
                #print(i+1,j+1,m[i][j], var3x3(i+1,j+1,m[i][j]))
    #print("NUMERO DE LITERALES "+ str(len(literals)) + "\n")
    # Creamos el header del Dimacs SAT 
    # p cnf num_vars num_clauses

    head = "p cnf " + imprimirVariable(len(literals)) + " " + imprimirVariable(len(clauses)) + " \n" + dimacs

    #os.system("clear")
    #print(head)

    return cnfData(clauses, literals, head)


########################################################################
#                            MAIN
#
########################################################################

if len(sys.argv) == 3 or len(sys.argv) == 4:
    archivo = sys.argv[1]

    # si pasan 0 por consola como 2do parametro se corre Zchaff solver
    # si pasan 1 por consola como 2do parametro se corre nuestra implementacion
    method = -1
    option = int(sys.argv[2])
    tiempoCorrida = 0

    if len(sys.argv) == 3:
        tiempoCorrida = str(200)
    else:
        tiempoCorrida = str(sys.argv[3])

    if(option == 0):
        method = 0 
    
    elif(option == 1):
        method = 1
    
    else:
        print("\n Opcion 0 - > ZChaff solver ")
        print("\n Opcion 1 - > DPLL. \n Seleccione entre alguna de las opciones dadas como 3er parametro por consola \n")
        sys.exit()

    # En el caso de que sea necesario que el archivo termine en .txt
    if archivo.endswith('.txt'):
        # Caso de la linea
        numLinea = 1
        with open(rutaDirTest+str(archivo)) as f:            
            for line in f:
                #Creamos la matriz de acuerdo al tamaño del sudoku 
                # info: contiene en la posicion 0 el numero de orden del sudoku 
                #       y en la posicion 1 la instancia inicial del tablero.
                info = line.split()
                #comentar print(info)
                #print(info)
                m = 0
                num = 0
                if (int(info[0]) == 1):
                    # Verificamos que el caso de prueba no tenga
                    # mas numeros de lo que deberia tener para un 
                    # sudoku de orden 1
                    if (len(info[1]) != 1):
                        print("\nEl caso de prueba no contiene la misma cantidad de digitos que casillas asociados al orden del sudoku en el archivo: " + archivo + " en la linea " + str(numLinea))
                        sys.exit()

                    m = [[0]]
                    num = 1
                
                elif (int(info[0]) == 2):
                    # Verificamos que el caso de prueba no tenga
                    # mas numeros de lo que deberia tener para un 
                    # sudoku de orden 2
                    if (len(info[1]) != 16):
                        print("\nEl caso de prueba no contiene la misma cantidad de digitos que casillas asociados al orden del sudoku en el archivo: " + archivo + " en la linea " + str(numLinea))
                        sys.exit()

                    m = [[0 for col in range(4)] for row in range(4)]
                    num = 4
                
                elif (int(info[0]) == 3):
                    # Verificamos que el caso de prueba no tenga
                    # mas numeros de lo que deberia tener para un 
                    # sudoku de orden 1
                    if (len(info[1]) != 81):
                        print("\nEl caso de prueba no contiene la misma cantidad de digitos que casillas asociados al orden del sudoku en el archivo: " + archivo + " en la linea " + str(numLinea))
                        sys.exit()

                    m = [[0 for col in range(9)] for row in range(9)]
                    num = 9

                else:
                    # 
                    print("\n El orden de los tableros solo pueden ser 1, 2 o 3 \n")
                    sys.exit()

                i = 0
                j = 0
                for elem in info[1]:
                    m[i][j] = int(elem)
                    #print(elem)
                    j += 1

                    if(j == num):
                        j = 0
                        i += 1
                #print(m)

                # Procedemos a escribir la teoria SAT del sudoku en formato CNF Dimacs 

                # Orden 1 Sudoku (ponemos 1 de una o ponemos la clausula p(fil,col,1) )
                if (int(info[0]) == 1):
                    cnf_data = cnfSudoku1x1(m)
                
                # Orden 2 Sudoku
                elif (int(info[0]) == 2):
                    cnf_data = cnfSudoku4x4(m)

                # Orden 3 Sudoku
                elif (int(info[0]) == 3):
                    cnf_data = cnfSudoku9x9(m)


                # se pasa el formato cnf dimacs a un txt para luego llamar a zchaff
                
                writeCNF = "c "+ "caso seleccionado del archivo: " + archivo + "\nc "+ "caso de prueba de la linea "+ imprimirVariable(numLinea)+ " \n" + cnf_data.write
                #print(writeCNF)

                # Se escribe la teoria SAT en un txt para luego llamar al solver correspondiente

                
                # Creamos el archivo en la carpeta CNFs
                arc = archivo.split(".txt")
                solcFile = arc[0]+"-Linea"+str(numLinea)+".txt"
                f = open(rutaDirCNF+solcFile, "w")
                f.write(writeCNF)
                f.close()


                # Hacer script que haga make o poner como requerimiento
                literals = cnf_data.variables
                clauses = cnf_data.clauses        
                
                
                # Se ejecuta el CNF con zchaff o solver propio (opcion 0 / 1)
                if method == 1:
                    ruta="./CNFs/sudo4x4-Linea1.txt"
                    time = 0
                    ( satValues, num_clauses, is_sat, output) = runDPLL(ruta)

                    for x,y in enumerate(satValues):
                        if y == 1:
                            tupla = cnf_data.variables[str(x+1)]
                            m[tupla[0]-1][tupla[1]-1] = tupla[2] 

                    sudok = gridSudoku(m,int(info[0]))                   

                    cnf_sol = "c solucion de la formula CNF del archivo {}\n".format(ruta)
                    cnf_sol += "c RESULT: {}\n".format(is_sat)
                    cnf_sol += "c Total Run Time: {}\n".format(time)
                    cnf_sol += output
                    grid_out = is_sat
                    grid_out += "\n\nTotal Run Time {}\n\n".format(time)
                    grid_out += "{}".format(sudok)

                    # with open(rutaReporteDPLL)

                    print(grid_out)



                if (method == 0):
                    runZchaff(solcFile, tiempoCorrida)
                    h1 = "s cnf " + imprimirVariable(len(literals)) + " " + imprimirVariable(len(clauses)) + " \n"


                    with open(rutaOutputZchaff+solcFile) as f:
                        #Creamos un archivo que reporte cada caso de prueba en un nuevo txt con el formato final
                        # El cual es una impresion de la matriz tipo grid con su solucion
                        reportChaff = open(rutaReporteZchaff+ "SOLUCION_" +solcFile,"w")

                        #print("\n NUMERO DE LINEA " + str(numLinea))
                        #print()
                        # se toma el reporte de zchaff y se selecciona 
                        # la informacion de interes
                        lines = [line for line in f.readlines()]
                        #print(lines)
                        #print(lines[5])
                        patternSAT = re.search("\tSAT", lines[-1])
                        patternUNSAT = re.search("\tUNSAT",lines[-1])

                        if(bool(patternSAT)):
                            # Tomamos el tiempo, y la lista de valores de los literales
                            satValues = lines[5].split()
                            result = lines[-1]
                            time = lines[-2]
                            chaffTimes.append(str(time.split()[3]))
                            h1 = "c " + result + "c " + time + h1

                            for x in satValues:
                                if (x == "Random"):
                                    break

                                #Buscamos las variables que sean True
                                if (0 < int(x)):
                                    #if int(x) in cnf_data.variables:
                                    tupla = cnf_data.variables[str(x)]
                                    m[tupla[0]-1][tupla[1]-1] = tupla[2] 

                                    # Procedemos a guardar h2 y agregar al reporte                              
                                
                                # se guarda la matriz en el reporte 
                                # con el tiempo que se tardó en conseguir la solucion



                                h1 = h1 + "v " + str(x) + "\n"
                            # h1 es el header para el caso de zchaffOutputDimacs
                            h1 = "c solucion de la formula CNF del archivo " + archivo + " linea " + str(numLinea) + "\n" + h1
                            # Guardamos el archivo en su respectiva carpeta
                            f = open(rutaOutputDimacs +solcFile, "w")
                            f.write(h1)
                            f.close()
                            
                            # Generamos un string con el grid y la solucion final de la instancia del sudoku
                            sudok = gridSudoku(m,int(info[0]))                   

                            #print(sudok)
                            #Matriz solucion
                            #print(m)
                            #print(solcFile)

                            reportChaff.write("SAT\n\n"+ time + "\n" + sudok)
                            reportChaff.close()                     
                                                   
                        elif(bool(patternUNSAT)):
                            # procedemos a crear el output con la palabra UNSAT
                            result = lines[-1]
                            h1 = result + h1
                            # h2 es el header para el caso del reporte final
                            h2 = "c solucion de la formula CNF del archivo " + archivo + " linea " + str(numLinea) + "\n" + "c UNSAT \n"
                            
                            # h1 es el header para el caso de zchaffOutputDimacs
                            h1 = "c solucion de la formula CNF del archivo " + archivo + " linea " + str(numLinea) + "\n" + h1

                            reportChaff.write("UNSAT\n")
                            reportChaff.close()
                        else:
                            #print(" TIME OUT \n" + " El problema no pudo ser resuelto en el tiempo establecido \n")
                            msg = " TIME OUT \n" + " El problema no pudo ser resuelto en el tiempo establecido \n"
                            reportChaff.write(msg)
                            reportChaff.close()
                        
                        h1 = "c solucion de la formula CNF del archivo " + archivo + " linea " + str(numLinea) + "\n" + h1
                
                # CASO en el que hay que correr con el DPLL solver

                numLinea += 1

    else:
        print("\n El archivo de casos de prueba debe tener la extension txt \n Ejemplo: prueba.txt")
        sys.exit()             
