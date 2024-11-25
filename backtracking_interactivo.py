import os
import sys
import time
# ----------------------------------- imprimir por pantalla --------------
TIEMPO_ENTRE_MSG = 0.3 #  Tiempo Entre prints que hara por pantalla


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')



def mostrar_intento_temporal(tablero, fila, col, largo, orientacion):
    # Creamos una copia del tablero
    tablero_temporal = [fila.copy() for fila in tablero]
    
    # Marcar el barco con un número 2 para distinguirlo del 1 (barcos confirmados)
    if orientacion == "H":
        for c in range(col, min(col + largo, len(tablero[0]))):
            tablero_temporal[fila][c] = 2
    else:  # Vertical
        for f in range(fila, min(fila + largo, len(tablero))):
            tablero_temporal[f][col] = 2
            
    return tablero_temporal

def mostrar_tablero(tablero, demanda_filas, demanda_columnas, paso=None, motivo_rechazo=None):
    limpiar_pantalla()
    
    if paso is not None:
        print(f"\nPaso: {paso}\n")
    
    # Mostrar demandas de columnas
    print("    ", end="")
    for dem in demanda_columnas:
        print(f"[{dem}]", end="")
    print("\n")
    
    # Mostrar tablero con demandas de filas
    for i, fila in enumerate(tablero):
        print(f"{i:2} ", end="") 
        for casilla in fila:
            if casilla == 0:
                print(" · ", end="")
            elif casilla == 1:
                print(" █ ", end="")
            elif casilla == 2:
                print(" ▒ ", end="")
        
        print(f"  [{demanda_filas[i]}]")
    
    print("    ", end="")
    for j in range(len(tablero[0])):
        print(f"{j:2} ", end="")
    print("\n")
    
    print("Leyenda:")
    print("· : Casilla vacía")
    print("█ : Barco confirmado")
    print("▒ : Intento actual")
    
    if motivo_rechazo:
        print("\nMotivo de rechazo:", motivo_rechazo)
    print()

# ------------------- solucion del algoritmo------------------------------------------------

def verifica_adyacencia(tablero, fila, col, largo, orientacion):
    if orientacion == "H":
        if fila > 0:
            # superior y sus diagonales
            for c in range(max(0, col-1), min(len(tablero[0]), col + largo + 1)):
                if tablero[fila - 1][c] == 1:
                    return False      
        if fila < len(tablero) - 1:
            # inferior y sus diagonales
            for c in range(max(0, col-1), min(len(tablero[0]), col + largo + 1)):
                if tablero[fila + 1][c] == 1:
                    return False
                    
        # izquierda y derecha
        if col > 0 and tablero[fila][col - 1] == 1:
            return False
        if col + largo < len(tablero[0]) and tablero[fila][col + largo] == 1:
            return False

    elif orientacion == "V":
        if col > 0:
            # izquierda y sus diagonales
            for f in range(max(0, fila-1), min(len(tablero), fila + largo + 1)):
                if tablero[f][col - 1] == 1:
                    return False
                    
        if col < len(tablero[0]) - 1:
            #  derecha y sus diagonales
            for f in range(max(0, fila-1), min(len(tablero), fila + largo + 1)):
                if tablero[f][col + 1] == 1:
                    return False
                    
        # arriba y abajo
        if fila > 0 and tablero[fila - 1][col] == 1:
            return False
        if fila + largo < len(tablero) and tablero[fila + largo][col] == 1:
            return False

    return True


def verifica_superposicion(tablero, fila, col, largo, orientacion):
    if orientacion == "H":
        return all(tablero[fila][c] == 0 for c in range(col, col + largo))
    elif orientacion == "V":
        return all(tablero[f][col] == 0 for f in range(fila, fila + largo))
    return False


def verifica_columa_demanda(col, largo, orientacion, demanda_columnas):    
    if orientacion == "H":
        # Verificar cada columna afectada
        for c in range(col, col + largo):
            if demanda_columnas[c] <= 0:
                return False
    else:
        # Para vertical, solo afecta una columna
        if demanda_columnas[col] < largo:
            return False
    
    return True

def verifica_fila_demanda(fila, largo, demanda_filas, orientacion):
    if orientacion == "H":
        # Para horizontal, solo afecta una fila
        if demanda_filas[fila] < largo:
            return False
    else:
        # Verificar cada fila afectada
        for f in range(fila, fila + largo):
            if demanda_filas[f] <= 0:
                return False
    return True

# Esta funcion verifica que haya espacio en las demandas de las columnas para 
# poder colocar el barco, por ejemplo si el barco tiene 3 de largo, almenos tendra que
# haber 3 columnas de seguido que tiengan una demanda mayor a 1
def verificar_espacio_en_columnas(tablero, barco, demanda_columnas):
    m = len(tablero[0])
    contador = 0
    for col in range(m):
        if demanda_columnas[col] > 0:
            contador += 1
            if contador >= barco:
                return True
        else:
            contador = 0
    return False


# Verificar si se salio del tablero
def salio_limite_fila(tablero, fila, largo):
    return fila + largo > len(tablero)

def salio_limite_columna(tablero,col, largo):
    return col + largo > len(tablero[0])



def ubicar_barcos(barcos, tablero, demanda_filas, demanda_columnas, paso=0):
    if not barcos:
        mostrar_tablero(tablero, demanda_filas, demanda_columnas, paso)
        return True
    
    barco = barcos.pop()
    hay_espacio_en_columnas = True

    for fila in range(len(tablero)):
        primera_vez = True
        
        for orientacion in ["H", "V"]:
            
            # Si el barco tiene largo 1 no tiene sentido chequearlo horizontal y vertical
            # Por eso me salteo una
            # TODO cambiar la estructura para evitar hacer esta comprobacion
            if primera_vez and barco == 1:
                primera_vez = False
                continue
            
            
            if orientacion == "V" and  salio_limite_fila(tablero, fila, barco):
                continue
            
            if not verifica_fila_demanda(fila, barco, demanda_filas, orientacion):
                # Mostramos el tablero si no verifica demanda de filas
                tablero_temporal = mostrar_intento_temporal(tablero, fila, 0, barco, orientacion)
                mostrar_tablero(tablero_temporal, demanda_filas, demanda_columnas, paso,
                                  "Rechazado: Excede la demanda")
                time.sleep(TIEMPO_ENTRE_MSG)
                continue

            if hay_espacio_en_columnas:
                # Buscamos si hay espacio en las demandas de las columnas para colocar el barco
                hay_espacio_en_columnas = verificar_espacio_en_columnas(tablero, barco, demanda_columnas)

            if orientacion == "H" and not hay_espacio_en_columnas:
                continue

            for col in range(len(tablero[0])):
                # Si se salio del limite cortamos
                if (orientacion == "H" and salio_limite_columna(tablero, col, barco)):
                    break


                # Mostrar el intento antes de validar
                tablero_temporal = mostrar_intento_temporal(tablero, fila, col, barco, orientacion)
                mostrar_tablero(tablero_temporal, demanda_filas, demanda_columnas, paso,
                              f"Evaluando barco {barco} en ({fila},{col}) {orientacion}")
                time.sleep(TIEMPO_ENTRE_MSG)

                #TODO verificar si esta comprobacion es necesaria
                if not verifica_columa_demanda(col, barco, orientacion, demanda_columnas):
                    mostrar_tablero(tablero_temporal, demanda_filas, demanda_columnas, paso,
                                  "Rechazado: Excede la demanda")
                    time.sleep(TIEMPO_ENTRE_MSG)
                    continue

                    
                if not verifica_superposicion(tablero, fila, col, barco, orientacion):
                    mostrar_tablero(tablero_temporal, demanda_filas, demanda_columnas, paso,
                                  "Rechazado: Superposición con otro barco")
                    time.sleep(TIEMPO_ENTRE_MSG)
                    continue
                    
                if not verifica_adyacencia(tablero, fila, col, barco, orientacion):
                    mostrar_tablero(tablero_temporal, demanda_filas, demanda_columnas, paso,
                                  "Rechazado: Adyacente a otro barco")
                    time.sleep(TIEMPO_ENTRE_MSG)
                    continue
                
                # Colocar el barco
                if orientacion == "H":
                    for c in range(col, col + barco):
                        tablero[fila][c] = 1
                        demanda_filas[fila] -= 1
                        demanda_columnas[c] -= 1
                else:  # Vertical
                    for f in range(fila, fila + barco):
                        tablero[f][col] = 1
                        demanda_filas[f] -= 1
                        demanda_columnas[col] -= 1
                
                if ubicar_barcos(barcos, tablero, demanda_filas, demanda_columnas, paso + 1):
                    return True
                
                hay_espacio_en_columnas = True

                print("Backtracking...")
                time.sleep(TIEMPO_ENTRE_MSG)
                    
                if orientacion == "H":
                    for c in range(col, col + barco):
                        tablero[fila][c] = 0
                        demanda_filas[fila] += 1
                        demanda_columnas[c] += 1
                else:  # Vertical
                    for f in range(fila, fila + barco):
                        tablero[f][col] = 0
                        demanda_filas[f] += 1
                        demanda_columnas[col] += 1

    
    barcos.append(barco)
    return False

# -------------------------- Lectura del archivo para testear --------------------------------------------------------------


def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = [linea.strip() for linea in archivo.readlines()]
    
    # Ignorar las dos primeras líneas de explicación
    lineas = lineas[2:]
    
    bloques = []
    bloque_actual = []
    for linea in lineas:
        if linea == "":
            bloques.append(bloque_actual)
            bloque_actual = []
        else:
            bloque_actual.append(int(linea))
    if bloque_actual:
        bloques.append(bloque_actual)

    # Separar los bloques en filas, columnas y barcos
    demandas_filas = bloques[0] if len(bloques) > 0 else []
    demandas_columnas = bloques[1] if len(bloques) > 1 else []
    barcos = bloques[2] if len(bloques) > 2 else []

    barcos.sort(reverse= True)

    return demandas_filas, demandas_columnas, barcos

# Nombre del archivo
archivo = "10_10_10.txt"
demandas_filas, demandas_columnas, barcos = leer_archivo(archivo)

# Imprimir los datos para verificar
print("Demandas de las filas:", demandas_filas)
print("Demandas de las columnas:", demandas_columnas)
print("Barcos:", barcos)


n = len(demandas_filas)
m = len(demandas_columnas)
tablero = [[0] * m for _ in range(n)]  # Crear un tablero vacío de n x m

# Llamar a la función de backtracking con los datos procesados
resultado = ubicar_barcos(barcos, tablero, demandas_filas, demandas_columnas)