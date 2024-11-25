import os
import sys
import time

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


def ubicar_barcos(barcos, tablero, demanda_filas, demanda_columnas):
    if not barcos:
        # Verifica si todas las demandas están cumplidas
        return True

    barco = barcos.pop()  # Intentar colocar el barco más grande restante

    hay_espacio_en_columnas = True

    for fila in range(len(tablero)):
        primera_vez = True

        for orientacion in ["H", "V"]:
            if primera_vez and barco == 1:
                primera_vez = False
                continue
            
            if orientacion == "V" and salio_limite_fila(tablero, fila, barco):
                continue

            if not verifica_fila_demanda(fila, barco, demanda_filas, orientacion):
                continue

            if hay_espacio_en_columnas:
                hay_espacio_en_columnas = verificar_espacio_en_columnas(tablero, barco, demanda_columnas)

            if orientacion == "H" and not hay_espacio_en_columnas:
                continue
            
            for col in range(len(tablero[0])):
                if (orientacion == "H" and salio_limite_columna(tablero, col, barco)):
                    break

                if es_valido(tablero, fila, col, barco, orientacion, demanda_columnas):
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

                    if ubicar_barcos(barcos, tablero, demanda_filas, demanda_columnas):
                        return True
                    
                    hay_espacio_en_columnas = True

                    # Backtrack
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


def es_valido(tablero, fila, col, largo, orientacion, demanda_columnas):
    if not verifica_columa_demanda(col, largo, orientacion, demanda_columnas):
        return False

    if not verifica_superposicion(tablero, fila, col, largo, orientacion):
        return False
    
    if not verifica_adyacencia(tablero, fila, col, largo, orientacion):
        return False

    
    return True



def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_tablero(tablero, demanda_filas, demanda_columnas):
    limpiar_pantalla()

    print("   ", end="")
    for dem in demanda_columnas:
        print(f"[{dem}]", end="")
    print("\n")
    
    for i, fila in enumerate(tablero):
        print(f"{i:2} ", end="") 
        for casilla in fila:
            if casilla == 0:
                print(" · ", end="")
            elif casilla == 1:
                print(" █ ", end="")
        
        print(f"  [{demanda_filas[i]}]")

    print("    ", end="")
    for j in range(len(tablero[0])):
        print(f"{j:2} ", end="")
    print("\n")
    
    print("Leyenda:")
    print("· : Casilla vacía")
    print("█ : Barco")
    print()


def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = [linea.strip() for linea in archivo.readlines()]
    
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

    demandas_filas = bloques[0] if len(bloques) > 0 else []
    demandas_columnas = bloques[1] if len(bloques) > 1 else []
    barcos = bloques[2] if len(bloques) > 2 else []

    return demandas_filas, demandas_columnas, barcos

archivo = "10_10_10.txt"
demandas_filas, demandas_columnas, barcos = leer_archivo(archivo)

print("Demandas de las filas:", demandas_filas)
print("Demandas de las columnas:", demandas_columnas)
print("Barcos:", barcos)


n = len(demandas_filas)
m = len(demandas_columnas)
tablero = [[0] * m for _ in range(n)] 


resultado = ubicar_barcos(barcos, tablero, demandas_filas, demandas_columnas)

mostrar_tablero(tablero, demandas_filas, demandas_columnas)

