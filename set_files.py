import sys

def set_coins(archivo_txt):
    with open(archivo_txt, "r") as archivo:
        lineas = archivo.readlines()

    header = True
    for linea in lineas:
        if header:
            header = False
            continue
        monedas = linea.strip().split(';')
    
    archivo.close()

    for i in range(len(monedas)):
        monedas[i] = int(monedas[i])

    return monedas

def set_results(cont_s, cont_m, orden, archivo_txt):
    with open(archivo_txt, "w") as archivo:
            archivo.writelines(orden)
            archivo.write("\n")
            ganancia_s = "Ganancia de Sophia: " + str(cont_s) + "\n"
            ganancia_m = "Ganancia de Mateo: " + str(cont_m) + "\n"
            archivo.write(ganancia_s)
            archivo.write(ganancia_m)
    archivo.close()