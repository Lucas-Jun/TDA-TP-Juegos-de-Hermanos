import sys

def setValores(txtFile):
    filas = []
    columnas = []
    barcos = []
    lineas_leidas = 0
    with open(txtFile, "r") as file:
        linea = file.readline()
        linea = file.readline()
        linea = file.readline()
        while(linea):
            if(linea == '\n'):
                break
            filas.append(int(linea))
            linea = file.readline()
        linea = file.readline()
        while(linea):
            if(linea == '\n'):
                break
            columnas.append(int(linea))
            linea = file.readline()
        linea = file.readline()
        while(linea):
            if(linea == '\n'):
                break
            barcos.append(int(linea))
            linea = file.readline()
    return (filas, (columnas, barcos))
    
class Tablero:
    def __init__(self, arrayFilas,arrayColumnas):
        self.filas = arrayFilas
        self.columnas = arrayColumnas
        self.matriz = []
        self.demandaCumplida = 0
        self.demandaTotal = sum(arrayFilas) + sum(arrayColumnas)
        self.ubicacionBotes = {}
        for x in range (0,len(arrayColumnas)):
            self.matriz.append([0]*len(arrayFilas))

        
    def printTablero(self):
        for x in range(0,len(self.filas)):
            for y in range(0,len(self.columnas)):
                if(self.matriz[y][x] == "X"):
                    print("\033[1;31;40m{}\033[0m".format(self.matriz[y][x]), end = "|")
                else:
                    print(self.matriz[y][x],end='|')
            print(self.filas[x])
        for prioridadColumna in self.columnas:
            print(prioridadColumna,end='|')
        print("")
        
    #devuelve fila/columna, (demanda, indice)
    def obtenerDimensionConMasDemanda(self):
        dimensionMayor = ('Fila',(-1,-1)  )
        for idx, demandaFila in enumerate(self.filas):
            if demandaFila > dimensionMayor[1][0]:
                dimensionMayor = ('Fila',(demandaFila,idx))
        for idx, demandaColumna in enumerate(self.columnas):
            if demandaColumna > dimensionMayor[1][0]:
                dimensionMayor = ('Columna',(demandaColumna,idx))
        return dimensionMayor
    
    #el numero de fila arranca desde cero contando desde arriba para abajo 
    def posicionarHorizontalmente(self, numeroFila, tamanioBote, numeroBote):
        #nos movemos de izquierda a derecha para ubicar el lugar
        if tamanioBote > self.filas[numeroFila]:
            #print("El bote no entra en la fila :(")
            return False
        for x in range(0,len(self.columnas)-tamanioBote+1):
            listaPosiciones = []
            flagFallo = False
            for y in range (x, x+tamanioBote):
                if (self.columnas[y] == 0):
                    flagFallo = True
                    break
                #revisar si no estan ocupadas
                if(self.espacioEstaOcupado(numeroFila,y)):
                    flagFallo = True
                if(self.hayBarcosAlrededor(numeroFila,y,len(self.filas),len(self.columnas))):
                    flagFallo = True
                    break
                listaPosiciones.append(y)
            if(flagFallo == False):
                if(len(listaPosiciones) > 0):
                    for posicion in listaPosiciones: 
                        self.columnas[posicion]-=1
                        self.matriz[posicion][numeroFila] = "X"
                    self.filas[numeroFila]-=tamanioBote
                    self.demandaCumplida+=(tamanioBote*2)
                    self.ubicacionBotes[numeroBote] = ((numeroFila,listaPosiciones[0]),(numeroFila,listaPosiciones[-1]))                   
                break       
            
    def posicionarVerticalmente(self, numeroColumna, tamanioBote, numeroBote):
        if tamanioBote > self.columnas[numeroColumna]:
            return False
        for x in range(0,len(self.filas)-tamanioBote+1):
            listaPosiciones = []
            flagFallo = False
            for y in range (x, x+tamanioBote):
                if (self.filas[y] == 0):
                    flagFallo = True
                    break
                if(self.espacioEstaOcupado(y,numeroColumna)):
                    flagFallo = True
                if(self.hayBarcosAlrededor(y,numeroColumna,len(self.filas),len(self.columnas))):
                    flagFallo = True
                    break
                listaPosiciones.append(y)
            if(flagFallo == False):
                if(len(listaPosiciones) > 0):
                    for posicion in listaPosiciones: 
                        self.filas[posicion]-=1
                        self.matriz[numeroColumna][posicion] = "X"
                    self.demandaCumplida+=(tamanioBote*2)
                    self.columnas[numeroColumna]-=tamanioBote
                    self.ubicacionBotes[numeroBote] = ((listaPosiciones[0],numeroColumna),(listaPosiciones[-1],numeroColumna))                   
                break
            
            
    def hayBarcosAlrededor(self, fila, columna, numFilas, numColumnas):
        #chequeamos hacia abajo
        print
        if(fila +1 < numFilas):
            if (self.matriz[columna][fila+1] == "X"):
                return True
        #chequeamos hacia arriba
        if(fila-1 >= 0):
            if (self.matriz[columna][fila-1] == "X"):
                return True
        #chequeamos hacia derecha 
        if (columna + 1 < numColumnas):
            if (self.matriz[columna+1][fila] == "X"):
                return True
        #chequeamos hacia izquierda 
        if (columna - 1 >= 0 ):
            if(self.matriz[columna-1][fila] == "X"):
                return True
        #chequeamos diagonalmente derecha arriba
        if (fila-1 >= 0 and columna+1 < numColumnas):
            if(self.matriz[columna+1][fila-1] == "X"):
                return True
        #chequeamos diagonalmente izquierda arriba        
        if (fila-1 >= 0 and columna-1 >= 0):
            if(self.matriz[columna-1][fila-1] == "X"):
                return True
        #chequeamos diagonalmente derecha abajo
        if (fila+1 < numFilas and columna+1 < numColumnas):
            if(self.matriz[columna+1][fila+1] == "X"):
                return True
        #chequeamos diagonalmente izquierda abajo
        if (fila+1 < numFilas and columna-1 >= 0):
            if(self.matriz[columna-1][fila+1] == "X"):
                return True
        return False
        
    def espacioEstaOcupado(self, fila, columna):
        if (self.matriz[columna][fila] == "X"):
            return True
        return False
        
    def obtenerResultados(self):
        print("Demanda cumplida: {}".format(self.demandaCumplida))
        print("Demanda total: {}".format(self.demandaTotal))
     
    def imprimirPosiciones(self ,numeroBarcos):
        print("Posiciones:")
        for x in range(0,numeroBarcos):
            ubicaciones = self.ubicacionBotes.get(x,None)
            if (ubicaciones == None):
                   print("{}: {}".format(x,self.ubicacionBotes.get(x,'None')))
            else:
                print("{}: {}".format(x,ubicaciones))
            
     
        
def main():
    (filas, (columnas,barcos)) = setValores(sys.argv[1])
    barcos.sort(reverse = True)
    tablero = Tablero(filas,columnas)
    botesPuestos = 0
    while(len(barcos)>0):
        largoBarco = barcos.pop(0)
        (dimension,(demanda,indice)) = tablero.obtenerDimensionConMasDemanda()
        if(demanda == 0):
            #No hay mas demanda en el tablero
            break
        if (dimension == "Fila"):
            tablero.posicionarHorizontalmente(indice, largoBarco,botesPuestos)
        else:
            tablero.posicionarVerticalmente(indice, largoBarco, botesPuestos)
        botesPuestos+=1
    #tablero.printTablero()
    tablero.imprimirPosiciones(botesPuestos-1)
    tablero.obtenerResultados()

main()
    