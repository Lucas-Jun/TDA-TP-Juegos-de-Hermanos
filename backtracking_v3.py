import os
import sys
import time

# ----------------------------------- imprimir por pantalla --------------
def mostrar_tablero(tablero, demanda_filas, demanda_columnas, paso=None, motivo_rechazo=None):
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
            elif casilla == -1:
                print(" . ", end="")
        
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


## ----------------------------------------- SOLUCION --------------------------------------------------------
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

# Verificar si se salio del tablero
def salio_limite_fila(tablero, fila, largo):
    return fila + largo > len(tablero)

def salio_limite_columna(tablero,col, largo):
    return col + largo > len(tablero[0])

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

def es_valido(tablero, fila, col, largo, orientacion, demanda_columnas):
    if not verifica_columa_demanda(col, largo, orientacion, demanda_columnas):
        return False

    if not verifica_superposicion(tablero, fila, col, largo, orientacion):
        return False
    
    if not verifica_adyacencia(tablero, fila, col, largo, orientacion):
        return False

    
    return True

def ubicar_barcos_backtracking(lista_barcos, tablero, demanda_filas, demanda_columnas,
                                solucion_p, solucion_opt, barcos_intentados):
    

    mejor_solucion = solucion_p if comprarar_demandas(solucion_p, solucion_opt) else solucion_opt

    if sum(demanda_columnas) == 0 and sum(demanda_filas) == 0:
        # Si se cumplio con toda la demanda de filas y de columnas es la mejor solucion
        return mejor_solucion.copy(), True
    
    # Se obtiene el barco siguiente
    barco_actual = get_sig_barco(lista_barcos, barcos_intentados)

    # Maximo valor de demanda de fila y columa anterior
    # Espacio en el tablero anterior
    max_fila_ant = 0
    max_col_ant = 0
    espacio_ant = 0

    if barco_actual is None:
        return mejor_solucion.copy(), False

    solo_una_orientacion = True

    for orientacion in ["H", "V"]:
        if solo_una_orientacion and barco_actual == 1:
            solo_una_orientacion = False
            continue
        for fila in range(len(tablero)):

            if orientacion == "V" and salio_limite_fila(tablero, fila, barco_actual):
                break
            if not verifica_fila_demanda(fila, barco_actual, demanda_filas, orientacion):
                continue

            for col in range(len(tablero[0])):
                if (orientacion == "H" and salio_limite_columna(tablero, col, barco_actual)):
                    break

                if es_valido(tablero, fila, col, barco_actual, orientacion, demanda_columnas):

                    colocar_barco(tablero, fila, col, barco_actual, orientacion, demanda_filas, demanda_columnas)

                    solucion_p.add((orientacion, fila, col, barco_actual))

                    # Maximo valor demanda de fila y columa actuales
                    # Espacio en el tablero anterior
                    max_fila_act = max(demanda_filas)
                    max_col_act = max(demanda_columnas)
                    espacio_act = contar_espacios_libres(tablero)

                    # Si se obtiene un mejor estado se llama a explorar las soluciones de ese estado
                    if comparar_estados_tableros(max_fila_ant, max_col_ant, espacio_ant,
                                         max_fila_act, max_col_act, espacio_act):
                        barcos_intentados.clear()

                        solucion_opt, hay_mejor_solucion = ubicar_barcos_backtracking(lista_barcos, tablero, demanda_filas, 
                                                                        demanda_columnas, 
                                                                        solucion_p, solucion_opt, barcos_intentados)
                        if hay_mejor_solucion :
                            return solucion_p.copy() if comprarar_demandas(solucion_p, solucion_opt) else solucion_opt.copy(), True
                        
                        # Si no hay mejor solucion actualizamos los valores anteriores a los valores actuales
                        # Asi en la prox iteracion obtenemos un mejor resultado
                        espacio_ant = espacio_act
                        max_col_ant = max_col_act
                        max_fila_ant = max_fila_act

                    solucion_p.remove((orientacion, fila, col, barco_actual))
                    
                    retirar_barco(tablero, fila, col, barco_actual, orientacion, demanda_filas, demanda_columnas)
    
    barcos_intentados.add(barco_actual)
    lista_barcos.append(barco_actual)
    return ubicar_barcos_backtracking(lista_barcos, tablero, demanda_filas, demanda_columnas, solucion_p, solucion_opt, barcos_intentados)


def comparar_estados_tableros(max_fila_ant, max_col_ant, espacio_ant, 
                      max_fila_act, max_col_act, espacio_act):
    
    if (max_fila_ant == max_fila_act or max_col_ant == max_col_act):
        # Condición 1: Si los máximos son iguales, evaluamos los espacios libres
        return espacio_act >= espacio_ant
    elif (max_fila_ant > max_fila_act or max_col_ant > max_col_act):
        # Condición 2: Si los valores anteriores son mayores no hay mejora
        return False
    elif (max_fila_act > max_fila_ant or max_col_act > max_col_ant):
        # Condición 3: Si los valores actuales son mayores hay mejora
        return True


def contar_espacios_libres(tablero):
    espacios_libres = 0
    for fila in tablero:
        espacios_libres += fila.count(0)
    return espacios_libres

# Devuelve true si el primer set es mejor que el segundo
def comprarar_demandas(set_barcos1, set_barcos2):
    demanda_cumplida_1 = 0
    demanda_cumplida_2 = 0
    for _, _, _, barco_actual_1 in set_barcos1:
        demanda_cumplida_1+= barco_actual_1 *2

    for _, _, _, barco_actual_2 in set_barcos2:
        demanda_cumplida_2+= barco_actual_2 *2
    return demanda_cumplida_1 > demanda_cumplida_2

# Devuelve el siguiente barco que no se haya usado
def get_sig_barco(lista_barcos, barcos_intentados):
    for barco in lista_barcos:
        if barco not in barcos_intentados:
            lista_barcos.remove(barco)
            return barco
    return None

def colocar_barco(tablero, fila, col, barco, orientacion, demanda_filas, demanda_columnas):
    filas = len(tablero)
    columnas = len(tablero[0])
    
    # Poner el barco
    if orientacion == "H":
        for c in range(col, col + barco):
            tablero[fila][c] = 1
            demanda_filas[fila] -= 1
            demanda_columnas[c] -= 1
        
        # Marcar -1 alrededor del barco
        for f in range(fila - 1, fila + 2):
            for c in range(col - 1, col + barco + 1):
                if 0 <= f < filas and 0 <= c < columnas and tablero[f][c] != 1:
                    tablero[f][c] = -1
    else:
        for f in range(fila, fila + barco):
            tablero[f][col] = 1
            demanda_filas[f] -= 1
            demanda_columnas[col] -= 1
        
        # Marcar -1 alrededor del barco
        for f in range(fila - 1, fila + barco + 1):
            for c in range(col - 1, col + 2):
                if 0 <= f < filas and 0 <= c < columnas and tablero[f][c] != 1:
                    tablero[f][c] = -1


def retirar_barco(tablero, fila, col, barco, orientacion, demanda_filas, demanda_columnas):
    filas = len(tablero)
    columnas = len(tablero[0])
    
    # Retirar el barco
    if orientacion == "H":
        for c in range(col, col + barco):
            tablero[fila][c] = 0
            demanda_filas[fila] += 1
            demanda_columnas[c] += 1
        
        # Limpiar los -1 alrededor del barco
        for f in range(fila - 1, fila + 2):
            for c in range(col - 1, col + barco + 1):
                if 0 <= f < filas and 0 <= c < columnas and tablero[f][c] == -1:
                    if not hay_barco_cercano(tablero, f, c):
                        tablero[f][c] = 0
    else:
        for f in range(fila, fila + barco):
            tablero[f][col] = 0
            demanda_filas[f] += 1
            demanda_columnas[col] += 1
        
        # Limpiar los -1 alrededor del barco
        for f in range(fila - 1, fila + barco + 1):
            for c in range(col - 1, col + 2):
                if 0 <= f < filas and 0 <= c < columnas and tablero[f][c] == -1:
                    # Verificamos que no haya un barco cercano
                    if not hay_barco_cercano(tablero, f, c):
                        tablero[f][c] = 0      

# Devuelve True si hay un barco cercano
def hay_barco_cercano(tablero, fila, col):
    filas = len(tablero)
    columnas = len(tablero[0])
    
    # Recorrer las celdas vecinas
    for f in range(fila - 1, fila + 2):
        for c in range(col - 1, col + 2):
            if 0 <= f < filas and 0 <= c < columnas and tablero[f][c] == 1:
                return True
    return False



###------------------------------------------- LECTURA DE ARCHIVO ---------------------

def reconstruir_tablero(tablero, solucion):
    for orientacion, fila, col, barco_actual in solucion:
        if orientacion == "H":  # Horizontal
            for c in range(col, col + barco_actual):
                tablero[fila][c] = 1  # Marca las celdas ocupadas por el barco
        elif orientacion == "V":  # Vertical
            for f in range(fila, fila + barco_actual):
                tablero[f][col] = 1  # Marca las celdas ocupadas por el barco
    return tablero

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

    # oden de mayor a menor
    barcos.sort(reverse=True)

    return demandas_filas, demandas_columnas, barcos

archivo = "./tests/10_10_10.txt"
demandas_filas, demandas_columnas, barcos = leer_archivo(archivo)

print("Demandas de las filas:", demandas_filas)
print("Demandas de las columnas:", demandas_columnas)
print("Barcos:", barcos)



n = len(demandas_filas)
m = len(demandas_columnas)
tablero_bc = [[0] * m for _ in range(n)]

# Nos quedamos con las copias originales
demandas_columnas_original = demandas_columnas.copy()
demandas_filas_original = demandas_filas.copy()
tablero_original = tablero_bc.copy()

import time

inicio = time.time()

solucion_opt = set()
solucion_p = set()
intentados = set()

resultado, _ = ubicar_barcos_backtracking(barcos, tablero_bc, demandas_filas, demandas_columnas,solucion_p, solucion_opt, intentados)

reconstruir_tablero(tablero_original, resultado)

fin = time.time()

tiempo_transcurrido = fin - inicio
mostrar_tablero(tablero_original, demandas_filas_original, demandas_columnas_original)

print( "Finalizo el algoritmo ")
print("-----------------------------------")

print(f"El algoritmo tardó {tiempo_transcurrido:.6f} segundos en ejecutarse.")

print(f"barcos tomados: {resultado}")


def calcular_demanda_total_y_cumplida(set_posiciones, demanda_filas, demanda_columnas):
    # Demanda total inicial
    demanda_total = sum(demanda_filas) + sum(demanda_columnas)
    demanda_cumplida = 0

    # Calcular las demandas cumplidas según el set de posiciones ocupadas
    for _, _, _, barco_actual in set_posiciones:
        demanda_cumplida+= barco_actual *2

    return demanda_total, demanda_cumplida

demanda_tota, demanda_cumplida = calcular_demanda_total_y_cumplida(resultado, demandas_filas_original, demandas_columnas_original)

print(f"Demanda total : {demanda_tota}")
print(f"Demanda cumplida {demanda_cumplida}")
